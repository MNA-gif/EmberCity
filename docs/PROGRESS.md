# Progress (newest on top)

Format per entry: date · name · Done / Next / Problems / Commit.

---

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
