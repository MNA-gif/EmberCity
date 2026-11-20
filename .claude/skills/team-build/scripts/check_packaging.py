#!/usr/bin/env python3
"""check_packaging.py - pre-package check for the unreal-packaging skill.

Finds the problems that only show up in a packaged (cooked) build, BEFORE the 3+ minute package:

  [R3] assets loaded at runtime by a path string whose folder is not in DirectoriesToAlwaysCook
       (the cooker leaves them out -> "Failed to find object", silent game)
  [R4] maps opened by name / the default maps missing from MapsToCook
  [R2] raw `static UObject*` pointers that are not kept alive (freed by GC on a map change -> crash)
  [R5] Windows headers included without #undef of PlaySound/CreateWindow-style macros
  [R6] anti-aliasing off or automatic screen percentage (pixelated outside the editor)

Usage (no Unreal needed, plain Python 3.8+):
    python check_packaging.py "C:/path/to/MyProject"
    python check_packaging.py "C:/path/to/MyProject" --keepalive LoadUIAsset --keepalive MyKeepHelper

--keepalive: name of a project helper that roots / keeps the asset alive (lines using it are OK).
Exit code: 0 = no FAIL, 1 = at least one FAIL. WARN lines need a human look.
Read-only: it changes nothing.
"""
import argparse
import os
import re
import sys

results = {"PASS": 0, "WARN": 0, "FAIL": 0}


def report(level, rule, msg):
    results[level] += 1
    print(f"{level:4} [{rule}] {msg}")


def read(path):
    try:
        with open(path, encoding="utf-8", errors="replace") as f:
            return f.read()
    except OSError:
        return ""


def ini_values(text, key):
    """All values of `key=` / `+key=` lines (Unreal ini arrays)."""
    vals = []
    for line in text.splitlines():
        m = re.match(r"\s*[+]?" + re.escape(key) + r"\s*=\s*(.*)$", line)
        if m:
            vals.append(m.group(1).strip())
    return vals


def find_project(root):
    for name in os.listdir(root):
        if name.endswith(".uproject"):
            return os.path.join(root, name)
    return None


def norm_pkg(path):
    """'/Game/A/B.B' or '/Game/A/B' -> '/Game/A/B' (package path)."""
    path = path.strip().strip('"').strip("'")
    path = path.split(":")[0]
    if "." in path.rsplit("/", 1)[-1]:
        path = path.rsplit(".", 1)[0]
    return path.rstrip("/")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("project_dir")
    ap.add_argument("--keepalive", action="append", default=[],
                    help="project helper that keeps an asset alive (e.g. LoadUIAsset)")
    args = ap.parse_args()

    root = os.path.abspath(args.project_dir)
    uproject = find_project(root)
    if not uproject:
        print(f"No .uproject in {root}")
        return 2
    print(f"Project: {os.path.basename(uproject)}\n")

    game_ini = read(os.path.join(root, "Config", "DefaultGame.ini"))
    engine_ini = read(os.path.join(root, "Config", "DefaultEngine.ini"))

    always_cook = []
    for v in ini_values(game_ini, "DirectoriesToAlwaysCook"):
        m = re.search(r'Path="([^"]+)"', v)
        if m:
            always_cook.append(m.group(1).rstrip("/"))
    maps_to_cook = []
    for v in ini_values(game_ini, "MapsToCook"):
        m = re.search(r'FilePath="([^"]+)"', v)
        if m:
            maps_to_cook.append(norm_pkg(m.group(1)))
    cook_all_maps = not maps_to_cook  # empty list = the cooker takes every map in the project

    def is_always_cooked(pkg):
        return any(pkg == d or pkg.startswith(d + "/") for d in always_cook)

    print("DirectoriesToAlwaysCook: " + (", ".join(always_cook) or "(none)"))
    print("MapsToCook: " + (", ".join(maps_to_cook) or "(none = all maps are cooked)") + "\n")

    # ---------------- R4: default maps must be cooked ----------------
    for key in ("GameDefaultMap", "ServerDefaultMap", "TransitionMap"):
        for v in ini_values(engine_ini, key):
            if not v or v.lower() == "none":
                continue
            pkg = norm_pkg(v)
            if pkg.startswith("/Engine/"):
                report("FAIL", "R4", f"{key} {pkg} is an ENGINE template map, not a map of this game "
                                     f"-> set it to your own start map (Project Settings > Maps & Modes)")
                continue
            if pkg.startswith("/Game/") and not os.path.exists(
                    os.path.join(root, "Content", *pkg[len("/Game/"):].split("/")) + ".umap"):
                report("FAIL", "R4", f"{key} {pkg} does not exist in Content/ -> the packaged game opens nothing")
                continue
            if cook_all_maps or pkg in maps_to_cook:
                report("PASS", "R4", f"{key} {pkg} is cooked")
            else:
                report("FAIL", "R4", f"{key} {pkg} is NOT in MapsToCook -> packaged game cannot start there")

    # ---------------- scan C++ source ----------------
    src_dir = os.path.join(root, "Source")
    files = []
    for dp, _, fns in os.walk(src_dir):
        for fn in fns:
            if fn.endswith((".cpp", ".h", ".inl")):
                files.append(os.path.join(dp, fn))
    if not files:
        report("PASS", "src", "no C++ source (Blueprint project) - source checks skipped")

    path_re = re.compile(r'TEXT\(\s*"(/Game/[^"]*)"\s*\)|"(/Game/[^"]*)"')
    hard_ref_markers = ("ConstructorHelpers::FObjectFinder", "ConstructorHelpers::FClassFinder")
    runtime_markers = ("LoadObject", "StaticLoadObject", "LoadClass", "StaticLoadClass", "FSoftObjectPath",
                       "TSoftObjectPtr", "TSoftClassPtr", "LoadSynchronous", "LoadPackage", "FStringAssetReference",
                       "Printf", "OpenLevel", "ServerTravel", "ClientTravel") + tuple(args.keepalive)
    level_markers = ("OpenLevel", "ServerTravel", "ClientTravel")
    static_ptr_re = re.compile(r'^\s*static\s+(?:const\s+)?(?:class\s+)?([UA]\w+)\s*\*\s*(\w+)\s*=\s*(.+)$')
    keepalive_words = ("AddToRoot", "TStrongObjectPtr", "FGCObject", "UPROPERTY") + tuple(args.keepalive)
    win_header_re = re.compile(r'#\s*include\s*[<"](windows\.h|mmsystem\.h|Windows\.h|winuser\.h)[>"]')

    # helpers that root what they load (body contains AddToRoot) count as keep-alive automatically
    for fp in files:
        text = read(fp)
        for m in re.finditer(r"(\w+)\s*\([^;{}()]*\)\s*(?:const\s*)?\{", text):
            if "AddToRoot" in text[m.end():m.end() + 400] and m.group(1) not in ("if", "for", "while", "switch"):
                if m.group(1) not in args.keepalive:
                    args.keepalive.append(m.group(1))
                    print(f"(auto keep-alive helper found: {m.group(1)} in {os.path.relpath(fp, root)})")
    runtime_markers = runtime_markers + tuple(args.keepalive)
    keepalive_words = keepalive_words + tuple(args.keepalive)

    runtime_paths = {}   # folder -> [(file, line)]
    level_paths = {}
    static_issues = []
    win_issues = []

    for fp in files:
        text = read(fp)
        rel = os.path.relpath(fp, root)
        lines = text.splitlines()
        for i, line in enumerate(lines, 1):
            stripped = line.strip()
            if stripped.startswith("//"):
                continue
            for m in path_re.finditer(line):
                raw = m.group(1) or m.group(2)
                ctx = " ".join(lines[max(0, i - 3):i])  # this line + 2 before
                if any(h in ctx for h in hard_ref_markers):
                    continue  # hard reference from the CDO: cooked with the class
                if not any(r in ctx for r in runtime_markers):
                    continue
                pkg = norm_pkg(raw.split("%")[0])
                if any(l in ctx for l in level_markers) or "/Maps/" in pkg:
                    level_paths.setdefault(pkg, []).append(f"{rel}:{i}")
                    continue
                if raw.rstrip().endswith("/"):
                    folder = pkg
                elif "%" in raw:
                    prefix = raw.split("%")[0]
                    folder = prefix.rstrip("/") if prefix.endswith("/") else prefix.rsplit("/", 1)[0]
                else:
                    folder = pkg.rsplit("/", 1)[0]
                runtime_paths.setdefault(folder, []).append(f"{rel}:{i}")
            m = static_ptr_re.match(line)
            if m and not any(k in line for k in keepalive_words):
                static_issues.append(f"{rel}:{i}  static {m.group(1)}* {m.group(2)}")
        if win_header_re.search(text):
            undef_playsound = re.search(r"#\s*undef\s+PlaySound\b", text)
            wrapped = "AllowWindowsPlatformTypes" in text and "HideWindowsPlatformTypes" in text
            # mmsystem.h defines PlaySound -> PlaySoundW: require the explicit #undef that fixed midterm Bug 25
            ok = undef_playsound if re.search(r"mmsystem\.h", text, re.I) else (wrapped or undef_playsound)
            if ok:
                report("PASS", "R5", f"{rel}: Windows header is wrapped / macros undefined")
            else:
                win_issues.append(rel)

    # ---------------- R3: runtime-loaded folders must be always cooked ----------------
    for folder, where in sorted(runtime_paths.items()):
        if is_always_cooked(folder):
            report("PASS", "R3", f"{folder} loaded at runtime, folder is always cooked")
        else:
            report("WARN", "R3", f"{folder} loaded at runtime ({len(where)}x, e.g. {where[0]}) but NOT in "
                                  f"DirectoriesToAlwaysCook -> only safe if a cooked asset also references it. "
                                  f"Add +DirectoriesToAlwaysCook=(Path=\"{folder}\") or check it in the packaged game")

    # ---------------- R4: maps opened by name ----------------
    for pkg, where in sorted(level_paths.items()):
        if cook_all_maps or pkg in maps_to_cook:
            report("PASS", "R4", f"map {pkg} (opened in {where[0]}) is cooked")
        else:
            report("FAIL", "R4", f"map {pkg} is opened in {where[0]} but NOT in MapsToCook")

    # ---------------- R2: static raw UObject pointers ----------------
    for s in static_issues:
        report("WARN", "R2", f"{s} -> raw static UObject pointer; GC can free it on a map change "
                             f"(packaged crash). Use a UPROPERTY, TStrongObjectPtr or AddToRoot")
    if files and not static_issues:
        report("PASS", "R2", "no raw static UObject pointers without a keep-alive")

    # ---------------- R5: Windows macros ----------------
    for rel in win_issues:
        report("FAIL", "R5", f"{rel} includes a Windows header without the needed guard (mmsystem.h: #undef PlaySound; windows.h: Allow/HideWindowsPlatformTypes) "
                             f"-> unity build can break engine headers (C2838 'PlaySoundW')")

    # ---------------- R6: AA and screen percentage ----------------
    aa = ini_values(engine_ini, "r.AntiAliasingMethod")
    if aa and aa[-1].strip() == "0":
        report("FAIL", "R6", "r.AntiAliasingMethod=0 -> no AA, pixelated in standalone/packaged (use 4 = TSR or 2 = TAA)")
    else:
        report("PASS", "R6", f"r.AntiAliasingMethod={aa[-1] if aa else 'engine default'}")
    sp = ini_values(engine_ini, "r.ScreenPercentage.Default.Desktop.Mode")
    if sp and sp[-1].strip() == "1":
        report("WARN", "R6", "r.ScreenPercentage.Default.Desktop.Mode=1 (automatic) -> may render below 100% outside the editor")

    print(f"\nSummary: {results['PASS']} PASS, {results['WARN']} WARN, {results['FAIL']} FAIL")
    return 1 if results["FAIL"] else 0


if __name__ == "__main__":
    sys.exit(main())
