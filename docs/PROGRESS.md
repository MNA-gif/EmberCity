# Progress (newest on top)

Format per entry: date · name · Done / Next / Problems / Commit.

---

## 20.11.2026 · Nebil (7) · main
- **Done:** checked the team plan (Kül Şehri doc) against the repo: Nebil's rule mapping for B1 is complete (team-unreal ← unreal-gotchas R1/R3/R4/R7/R13/R14, team-rules ← my-workflow R2/R3/R8/R10/R11/R13, team-build ← unreal-packaging + script). Added today's lessons: team-unreal R8 `GameplayTags` name, R9 VibeUE traps, R10 connected floor in `L_Chapter1`; team-rules R8 git under an open editor, R9 §4.2b functions.
- **Next:** team sends 3–5 rules each (B1 needs every name); Kül Şehri doc: `Tags` → `GameplayTags`, add §4.2b; invite collaborators and share the repo link.
- **Commit:** `[Nebil] skills: lessons from building ember + chapter`

## 20.11.2026 · Nebil (6) · main
- **Done:** `nebil/ember` fast-forwarded into `main` (Core, BPC_Ember, BP_EmberCore, BP_ChapterDirector). On main: `L_Chapter1` has `EmberCore` at (1200, 0, floor), `ChapterDirector`, `NavMeshBounds` (40 × 40 m, ±300 z) → `RecastNavMesh-Default`; `Config/DefaultEngine.ini` GameDefaultMap + EditorStartupMap = `L_Chapter1`.
- **Tested (PIE, L_Chapter1):** `[Chapter] Started`, pawn spawns; 5 fuel → `Ended, won = true`; Retry reloads; 500 damage → `Ended, won = false`; 0 Blueprint runtime errors. NavMesh: core reachable from 19/24 random floor points; the 5 misses are closed pockets of the template map (e.g. around (-1539,-1433), (1667,-1587), (126,-456)).
- **Not tested:** end screen in L_Chapter1 (`EndScreenClass` empty until Karahan's `WBP_EndScreen` is on main → cursor stays off on end); packaged build.
- **Next:** team: `git merge main` into your branch, use `GameplayTags` and §4.2b. Kartal: spawn Frost only in the connected floor area (test with `P` in the viewport). Nebil: merge member branches one by one and play after each.
- **Problems:** template map has disconnected floor areas (start-to-start full paths 344/552).
- **Commit:** `[Nebil] chapter1: core, director, navmesh, default map`

## 20.11.2026 · Nebil (5) · branch `nebil/ember`
- **Done:** `Systems/Nebil/BP_ChapterDirector` (Actor, one per level): BeginPlay prints `[Chapter] Started`, finds `BP_EmberCore`, stores its `Ember` and binds `OnEmberDepleted` → `EndChapter(false)`, `OnEmberIgnited` → `EndChapter(true)`. `EndChapter(bWonIn)` runs once (`bEnded`), stops the Ember, calls `OnChapterEnded(bWon)`, prints the result, and if `EndScreenClass` is set creates it, adds to viewport, input Game and UI + cursor (team-unreal R4). `RetryChapter()` = Game Only, hide cursor, reopen current level. Contracts §4.2b added (callable functions, `EndScreenClass`, player death pending `BPC_Health`). Dev widget `WBP_EndScreenTest` (empty) set only on the director placed in `L_Test_Nebil`.
- **Tested (PIE, L_Test_Nebil):** win: 5 fuel → log `[Chapter] Ended, won = true`, bEnded/bWon true, cursor on; 500 damage after the win → no second end. Retry → level reloads (t=0.67, Heat 99.3, Fuel 0, bEnded false, cursor off). Fail: ApplyDamage(500) → `[Chapter] Ended, won = false`, cursor on. No Blueprint runtime errors in the log.
- **Not tested:** player death (needs Emrecan's `BPC_Health`); a real end screen (Karahan's `WBP_EndScreen`); Retry clicked from a button.
- **Next:** merge `nebil/ember` → main; NavMesh + Game Default Map + director/core in `L_Chapter1` on main; tell the team about `GameplayTags` and §4.2b.
- **Commit:** `[Nebil] chapter: BP_ChapterDirector win/fail/retry`

## 20.11.2026 · Nebil (4) · branch `nebil/ember`
- **Done:** `Systems/Nebil/BPC_Ember` (Actor Component): `Tuning`=DA_Tuning, `Heat/MaxHeat/FuelDelivered/bActive`; BeginPlay sets heat from `Ember_StartHeat`; Tick drains `Ember_DrainPerSecond`; function `ChangeHeat(Delta)` clamps 0..MaxHeat and calls `OnHeatChanged(Heat, MaxHeat)`, at 0 calls `OnEmberDepleted`; events `AddFuel(Amount int)` (+`Ember_HeatPerFuel` each, `Chapter_FuelToWin` reached → `OnEmberIgnited`), `LoseHeat(Amount float)`, `StopEmber`. `BP_EmberCore` (Actor): cylinder placeholder + `Ember` component, `GameplayTags`=`Target.EmberCore`, implements `BPI_Damageable` (Amount × `Ember_DamageToHeat` → LoseHeat) and `BPI_FuelReceiver` (→ AddFuel). Dev helper `BP_EmberDebug` prints the 3 dispatchers. Contract change: tag variable is `GameplayTags` (not `Tags`, clashes with AActor::Tags) in technical_design §4.3.
- **Tested (PIE, L_Test_Nebil):** drain 100→95.20 at t=4.80 s (1/s); ReceiveFuel(1) +15 (clamped at 100), Fuel=1; ApplyDamage(20) −10; 5 fuel → bActive=false + log `[EmberDebug] OnEmberIgnited`; ApplyDamage(500) → Heat 0 + `OnEmberDepleted`. B5: DA_Tuning `Ember_DrainPerSecond` 1→5 without opening a BP → Heat 56.67 at t=8.67 s (5/s); set back to 1.0.
- **Not tested:** core mesh height on the floor (placed at z=212), real fuel/damage from other systems (not built yet).
- **Next:** `BP_ChapterDirector` (win/fail, `OnChapterEnded`, end screen, Retry); merge `nebil/ember` → main; NavMesh + Game Default Map on main.
- **Commit:** `[Nebil] ember: BPC_Ember heat/fuel component + BP_EmberCore`

## 20.11.2026 · Nebil (3)
- **Done:** `Core/PDA_Tuning` (PrimaryDataAsset BP, 19 fields from technical_design §4.4, Instance Editable, category = prefix) + `Core/DA_Tuning` (instance, defaults checked 19/19); interfaces `BPI_Damageable.ApplyDamage(Amount float, Instigator Actor)`, `BPI_Interactable.Interact(Interactor Actor)`, `BPI_FuelReceiver.ReceiveFuel(Amount int)`; `Maps/L_Chapter1` + `Maps/Test/L_Test_{Nebil,Emrecan,Kartal,Karahan}` duplicated from `Lvl_FirstPerson` (63 actors, PlayerStart). All made through the editor MCP (VibeUE `execute_python_code`).
- **Next:** Nebil: `BPC_Ember` + `BP_EmberCore` on `nebil/ember`; set Game Default Map = `L_Chapter1`; NavMeshBoundsVolume in `L_Chapter1` (needed by Kartal). Members: merge `main` into your branch to get Core.
- **Problems:** no NavMesh in the maps yet; Game Default Map still `Lvl_FirstPerson`.
- **Commit:** `[Nebil] core: PDA_Tuning, DA_Tuning, 3 interfaces, chapter + test maps`

## 20.11.2026 · Nebil (2)
- **Done:** team skills moved from `_setup/skills/` to `.claude/skills/` (team-rules, team-unreal, team-build), `.mcp.json` at the root, `Content/Developers/` + `Content/Collections/` ignored; `git init` on `main` with Git LFS, first commit; branches `nebil/ember`, `emrecan/health-weapon`, `kartal/frost`, `karahan/fuel-hud` created from it.
- **Done (later):** published as private repo `MNA-gif/EmberCity` (GitHub Desktop); `main` + 4 member branches pushed, all LFS objects uploaded.
- **Next:** Nebil: invite Emrecan, Kartal, Karahan as collaborators on GitHub; then `Core/` assets (`PDA_Tuning`, `DA_Tuning`, 3 interfaces), `L_Chapter1` + 4 test maps through the editor MCP. Everyone: clone, check out your branch, send 3–5 rules for B1.
- **Problems:** repo is private, members cannot clone until invited; all team-skill rules are still `[Nebil]` only.
- **Commit:** `[Nebil] setup: git, LFS, team skills in .claude/skills`

## 20.11.2026 · Nebil
- **Done:** project from the First Person template (UE 5.8, Blueprint); repo setup: `.gitignore`, Git LFS (`.gitattributes`), `.mcp.json`, `CLAUDE.md`, `docs/technical_design.md` with the Contracts, gameplay tags in `Config/DefaultGameplayTags.ini`, team skills (first version, Nebil's rules).
- **Next:** Nebil: create `Core/` assets (`PDA_Tuning`, `DA_Tuning`, 3 interfaces) and `L_Chapter1`. Everyone: clone, create your branch, send 3–5 rules from your Part A skills to Nebil for the team skills.
- **Problems:** none yet.
- **Commit:** `[Nebil] setup: repo, contracts, team skills`
