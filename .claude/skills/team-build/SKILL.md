---
name: team-build
description: How the Ember City team makes and checks the packaged Windows build (B7) - pre-package check script, GameDefaultMap and MapsToCook, assets loaded by path, testing the exe from the start map to the end screen, reading the packaged log, what to zip and hand in. Use whenever someone asks for a build, package, exe, hand-in zip, or says "build al", "paketle", "teslim", "build açılmıyor".
---

# Team build · Ember City

Each rule says who brought it. Script: `scripts/check_packaging.py` (from my Part A skill unreal-packaging).

### R1 · Run the pre-package check first `[Nebil]`
- **Rule:** before packaging run `"<Engine>\Engine\Binaries\ThirdParty\Python3\Win64\python.exe" .claude/skills/team-build/scripts/check_packaging.py "<project folder>"`. Fix every FAIL.
- **Why:** in my proof test it caught a GameDefaultMap pointing to an engine template; in my midterm three packaged-only bugs each cost a 3-minute package loop.
- **Check:** `Summary: … 0 FAIL`.

### R2 · The game starts in `L_Chapter1` (or the menu) `[Nebil]`
- **Rule:** Project Settings → Maps & Modes: Game Default Map = `L_Chapter1` (or a menu map once it exists), Default GameMode = ours. Every map opened by name is in the cook list.
- **Check:** the script's R4 lines are PASS.

### R3 · Test the exe from start to end screen `[Nebil]`
- **Rule:** start the packaged exe with no arguments, play to a win AND a loss, press Retry once. The build is done only when both end screens appeared.
- **Why:** the editor hides packaged-only crashes; my midterm build crashed only on a menu → game transition.
- **Check:** both end screens seen; the log has no `EXCEPTION_ACCESS_VIOLATION`.

### R4 · Read the packaged log `[Nebil]`
- **Rule:** after each test open `Packaged\Windows\EmberCity\Saved\Logs\EmberCity.log`, search `Error`, `Failed to find object`, `Fatal`.
- **Check:** 0 `Failed to find object`; every `Error:` explained.

### R5 · Package with one command, hand in the whole folder `[Nebil]`
- **Rule:** `"<Engine>\Engine\Build\BatchFiles\RunUAT.bat" BuildCookRun -project="<path>\EmberCity.uproject" -platform=Win64 -clientconfig=Development -build -cook -stage -pak -archive -archivedirectory="<path>\Packaged"`; zip the whole `Packaged\Windows` folder (not only the exe) for the hand-in link.
- **Check:** UAT ends with `BUILD SUCCESSFUL`; the zip opens and runs on another PC.

## From the team (to be merged)
<!-- Add build traps you hit as R6+ with your name. -->
