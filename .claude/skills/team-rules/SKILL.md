---
name: team-rules
description: How the Ember City team works with Claude in this repo - who owns which folder and Blueprint, the Contracts (interfaces, dispatchers, gameplay tags) systems must use to talk, DA_Tuning for every number, branches, "[Name] area: what" commits, PROGRESS.md hand-off, asking before downloads. Use at the start of every session and before any new system, Blueprint change, commit, merge or "devam et / kaldığımız yerden / ne yapalım" in this project.
---

# Team rules · Ember City

Merged by the integration owner (Nebil). Each rule says who brought it. Details: `docs/technical_design.md`.

### R1 · Work only in your own folder `[Nebil]`
- **Rule:** a member's Claude creates and edits assets only in `Content/EmberCity/Systems/<Name>/` and `Maps/Test/L_Test_<Name>`. Shared files (`Core/`, `Config/`, `L_Chapter1`, `BP_Player`) change only through their owner.
- **Why:** `.uasset` / `.umap` files cannot be merged; two people editing one file = one person's work is lost.
- **Check:** `git status` before a commit lists only files under your own folder (plus `docs/PROGRESS.md`).

### R2 · Systems talk only through the Contracts `[Nebil]`
- **Rule:** use the interfaces, dispatchers and gameplay tags in technical_design.md §4. Find other actors by gameplay tag, never by name or "Get All Actors Of Class" on another member's class. A missing contract = change the doc first, the owner approves, then code.
- **Why:** lets four people build in parallel and merge system by system (B4).
- **Check:** your Blueprints reference no asset from another member's folder except through an interface call or a dispatcher bind.

### R3 · No number inside a Blueprint `[Nebil]`
- **Rule:** speeds, damage, timers, counts, costs come from `DA_Tuning` through the `Tuning` variable. A new number = a new field in `PDA_Tuning` (ask Nebil) + a row in technical_design.md §4.4.
- **Why:** balancing is one asset; B5 requires it. In my midterm this made every balance pass a one-file change.
- **Check:** change one value in `DA_Tuning`, play: the game changes without opening a Blueprint.

### R4 · Give options first, build what is picked `[Nebil]`
- **Rule:** for "ne ekleyelim / what next", answer with numbered options (size S/M/L) and build nothing until the user picks. A question gets an answer, not an edit.
- **Why:** it kept me in charge of my midterm design; unasked edits cost time to undo.
- **Check:** no file changed before the user's pick.

### R5 · Done = tested in PIE, with evidence `[Nebil]`
- **Rule:** a system is done after a PIE test in your test map, reported with what was seen (log line, number, screenshot) and a "Not tested:" line.
- **Why:** every bug that reached me in the midterm sat in an untested path.
- **Check:** the report has "Tested:" and "Not tested:".

### R6 · Commit with your name, hand off in PROGRESS.md `[Nebil]`
- **Rule:** branch `<name>/<system>`; commit message `[Name] area: what changed`; at the end of a session 3 lines on top of `docs/PROGRESS.md`. Only Nebil merges into `main`.
- **Why:** B3–B4 are graded per member from commits with `[Name]`; PROGRESS.md is how the next person (or the next Claude) continues.
- **Check:** `git log --oneline -5` shows `[Name]` in every message.

### R7 · Ask before downloads, never delete for good `[Nebil]`
- **Rule:** before a download say name, source, licence, size and wait; write the licence into `ThirdPartyLicenses/`. Deleted files go to the Recycle Bin.
- **Check:** each new pack has a licence line.

### R8 · Never let git rewrite `.uasset` files under an open editor `[Nebil]`
- **Rule:** `git pull`, `checkout`, `merge` that change Content files only with the editor closed. With the editor open, only moves that keep the files the same: e.g. fast-forward a branch with `git branch -f <branch> <commit>` and then check it out (same tree, no file changes).
- **Why:** the editor keeps loaded packages in memory and saves them back over the new files; on 20.11 `nebil/ember` → `main` was done this way with the editor open and nothing was lost.
- **Check:** before such a command, `git diff --stat HEAD <target> -- Content` is empty or the editor is closed.

### R9 · Use the system's functions listed in §4.2b, nothing else `[Nebil]`
- **Rule:** besides interfaces and dispatchers, another system may only call the functions in technical_design.md §4.2b (e.g. `RetryChapter()` from the end screen, `AddFuel` / `LoseHeat` on `BPC_Ember` through the Core's interfaces).
- **Why:** keeps "no system edits another system's Blueprint" (B4) true while the end screen still needs a Retry.
- **Check:** every cross-system node in your Blueprint is an interface message, a dispatcher bind or a §4.2b function.

## From the team (to be merged)
<!-- Emrecan, Kartal, Karahan: send 1–2 rules each from your Part A skills; Nebil adds them here as R8+ with your name. -->
