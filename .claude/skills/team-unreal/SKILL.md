---
name: team-unreal
description: Unreal Engine 5.8 traps the Ember City team already hit, with checks - Blueprint default vs placed level instances, components on placed actors, meshes without collision, NavMesh for the Frost AI, input mode for menus and the end screen, line-trace weapons, dispatcher binding order, Unreal MCP not answering. Use for ANY Unreal editor task in this project before acting - changing a Blueprint variable or default ("değerini … yap"), placing meshes, AI paths, widgets and input, weapons, or when the editor/MCP connection fails ("MCP bağlanmadı", ECONNREFUSED).
---

# Team Unreal gotchas · Ember City

Each rule says who brought it.

### R1 · A Blueprint default change is not done until placed instances are checked `[Nebil]`
- **Rule:** after changing a default (or adding a variable), list every placed instance of that class in `L_Chapter1` and your test map, compare the value, fix and save the level.
- **Why:** placed actors keep values saved on them; it cost me ~1.5 h over 4 times in my midterm.
- **Check:** select each placed instance, Details: the value matches, or the difference is on purpose.

### R2 · Every blocking mesh has simple collision `[Nebil]`
- **Rule:** walls, floors and props the player or Frost touch need simple collision; kit meshes often have none.
- **Why:** customers and the NavMesh went through kit walls for two weeks in my midterm.
- **Check:** Static Mesh editor → Show → Simple Collision shows a shape; in PIE the player cannot walk through.

### R3 · The Frost need a NavMesh that reaches the Core `[Nebil]`
- **Rule:** `L_Chapter1` and every test map with enemies has a NavMeshBoundsVolume; after moving walls or doors rebuild paths and check the doorways.
- **Why:** a door frame with complex collision closed a doorway in the NavMesh in my midterm.
- **Check:** press `P` in the viewport: green reaches the Core from every spawn point.

### R4 · End screen and menus use "Game and UI" input `[Nebil]`
- **Rule:** when `WBP_EndScreen` opens: Set Input Mode **Game and UI** (or UI Only only if no game key is needed), Show Mouse Cursor = true; on Retry set Game Only and hide the cursor before reloading.
- **Why:** with UI Only my pause key stopped working; without the cursor the Retry button cannot be clicked.
- **Check:** in PIE lose on purpose → the cursor shows, Retry reloads, mouse look works after reload.

### R5 · Bind dispatchers on BeginPlay, and check the target exists `[Nebil]`
- **Rule:** listeners find the other actor by gameplay tag on `BeginPlay`, check it is valid, then bind. If the target spawns later (enemies), bind when it spawns.
- **Why:** a bind on a missing actor fails silently and the HUD never updates.
- **Check:** print a string on the first event received; it appears in PIE.

### R6 · Editor via Claude: one map operation per call, PIE with a start point `[Nebil]`
- **Rule:** never duplicate the open map and load the copy in one Python call; start PIE from a PlayerStart.
- **Why:** duplicate + load in one call killed my editor ("World Memory Leaks"); a bare StartPIE spawned no pawn.
- **Check:** after StartPIE the player pawn exists.

### R7 · MCP not answering: start the server, do not retry blindly `[Nebil]`
- **Rule:** on ECONNREFUSED run `ModelContextProtocol.StartServer` in the editor console; after two failed calls stop and tell the user.
- **Check:** one cheap call (list actors) works before real work starts.

### R8 · The gameplay tag variable is `GameplayTags`, never `Tags` `[Nebil]`
- **Rule:** the `GameplayTagContainer` variable on every gameplay actor is named `GameplayTags` (Instance Editable). Do not name variables or functions like an `AActor` member (`Tags`, `GetLevel`, `GetOwner`, `Layers`).
- **Why:** `AActor` already has `Tags` (`TArray<FName>`); a second `Tags` does not compile or silently shadows it. Hit on 20.11 while building `BP_EmberCore`; same trap as my midterm's `GetLevel` UHT error.
- **Check:** `BlueprintService.list_variables(<bp>)` shows `GameplayTags` of type `GameplayTagContainer`; no variable named like a parent-class member.

### R9 · Building Blueprints through VibeUE: the traps we hit `[Nebil]`
- **Rule:** (1) after `add_member_variable` call `BlueprintEditorLibrary.set_blueprint_variable_instance_editable` and set defaults with `set_variable_default_value`, then check the CDO value; (2) object defaults (e.g. `Tuning` = `DA_Tuning`) with `BlueprintService.set_property(bp, "Tuning", "/Game/EmberCity/Core/DA_Tuning.DA_Tuning")` (VibeUE blocks direct CDO edits); (3) interface events with `BlueprintEditorLibrary.add_event_override(bp, "ApplyDamage", unreal.IntPoint(x, y))`; (4) "Call <Dispatcher>" nodes with `add_call_delegate_node`, other `SPAWN …` keys with `create_node_by_key("NODE K2Node_CreateWidget")` - `build_graph` rejects both; (5) non-pure calls (`GetActorOfClass`, `GetCurrentLevelName`) need their exec pin wired or they are pruned.
- **Why:** each one cost a failed build or a silent wrong default on 20.11 (`BPC_Ember`, `BP_EmberCore`, `BP_ChapterDirector`).
- **Check:** `build_graph` result `success: True` with `nodes n/n`, `conns n/n`, `defaults n/n`, and no "pruned" warning.

### R10 · Spawn and target only in the connected floor area of `L_Chapter1` `[Nebil]`
- **Rule:** `L_Chapter1` is the First Person template map; parts of its floor are closed pockets. Spawn points and pickups go where a path to the Core exists.
- **Why:** NavMesh test on 20.11: the Core was reachable from 19 of 24 random floor points; the misses were pockets around (-1539,-1433), (1667,-1587), (126,-456).
- **Check:** `NavigationSystemV1.find_path_to_location_synchronously(world, spawn, core_side_point)` is valid and not partial for every spawn point; or `P` in the viewport shows green connected to the Core.

### R11 · Line-trace weapons need targets that block `Visibility` `[Nebil]`
- **Rule:** the template `Pawn` (capsule) and `CharacterMesh` profiles **ignore** the `Visibility` channel. Every actor the weapon must hit (Frost) sets its capsule's `Visibility` response to **Block**.
- **Why:** 21.11: `BPC_ProtoWeapon` fired, ammo went down, Frost took no damage - the trace went through it.
- **Check:** in PIE aim at a Frost, fire once: its health drops.

### R12 · Actors that AI walks to must not cut a hole in the NavMesh `[Nebil]`
- **Rule:** the Core's mesh has `Can Ever Affect Navigation = false`; AI targets are reached through an overlap zone around them, not by touching the mesh.
- **Why:** 21.11: `SimpleMoveToActor(Core)` did nothing - no path ends inside the hole the cylinder made.
- **Check:** `find_path_to_actor_synchronously(world, spawn, core)` has points and is not partial.

### R13 · VibeUE nodes that crash the editor's Python `[Nebil]`
- **Rule:** create Spawn Actor with the localized spawner key from `discover_nodes(bp, "Sınıf")` (`SPAWN K2Node_SpawnActorFromClass|…`), never `NODE K2Node_SpawnActorFromClass`; read a macro's pin names (`ForLoop`: `execute`, `LoopBody`, `FirstIndex`…) with `get_node_pins` before wiring. Interface calls on another actor: `Cast To BPI_x` (interface cast) → call on `AsBPI x`.
- **Why:** both crashed Python on 21.11 (editor restart each time); interface function nodes reject a plain Actor pin.
- **Check:** create risky nodes alone in one call and print their pins first.

### R14 · Python `unreal.Rotator(a, b, c)` is roll, pitch, yaw `[Nebil]`
- **Rule:** always use keywords: `unreal.Rotator(roll=0, pitch=0, yaw=-90)`. A Material on a skeletal mesh needs `used_with_skeletal_mesh = True`, or it renders as the grey default.
- **Why:** 21.11: `Rotator(0,-90,0)` laid every Frost flat on the floor ("yatay sürünüyorlar"); the icy Frost material showed grey until the flag was set.
- **Check:** after a mesh rotation/material change, one screenshot in PIE (`HighResShot 1` → `Saved/Screenshots` when `capture_image` fails).

### R15 · First-person arms, AI walk, Fab packs `[Nebil]`
- **Rule:** (1) the template `FirstPersonMesh` copies the BODY mesh pose (`ABP_FP_Copy`): change the arms by giving the body mesh an AnimBP (upper body layered from `spine_01`), never by playing anims on the arms; attach the gun to the camera, not to an arm bone. (2) AI characters using `ABP_Unarmed` need `NavMovementProperties.bUseAccelerationForPaths = true`, else they slide in idle. (3) A Fab pack goes in through the launcher "Add to Project"; move only the used assets + dependencies into `Content/EmberCity/Art/<Pack>/`, resave them, downsize textures to 1K, and keep the full pack folder in `.gitignore`.
- **Why:** 21.11: arms showed the running pose with a floating gun; Frost slid without walking; one free pack was 890 MB and one pistol 499 MB.
- **Check:** in PIE run + shoot: hands keep the pistol pose; Frost `ShouldMove` is true while walking; `git status` shows no files from the pack folder.

### R16 · Guns in hands: use the template's shooter rig, do not hand-tune offsets `[Nebil]`
- **Rule:** weapon meshes snap to the mannequin socket `HandGrip_R` (no offset); first-person arms use `ABP_FP_Pistol` (our copy `ABP_ProtoFPPistol`), bodies/NPCs use `ABP_TP_Pistol`. Content comes from the engine's `Templates/TemplateResources/Standard/Variant_Shooter` + `Weapons` (copied into `Content/`). If a copied AnimBP casts to `BP_ShooterCharacter`, cast to our character class instead.
- **Why:** 21.11: three rounds of hand-measured offsets + IK still looked broken ("eller tam kavramıyor"); the template rig was right on the first try.
- **Check:** in PIE the right hand closes on the grip, and `Aim Target` on the FP anim instance is not (0,0,0).

## From the team (to be merged)
<!-- Emrecan (weapon/health), Kartal (AI), Karahan (UI): add the traps you hit as R8+ with your name. -->

### R11 · The Frost cannot `MoveToActor` onto the Core: walk to a point beside it `[Kartal]`
- **Rule:** for targets that carve the NavMesh (the Core, big props), move to a reachable point just outside the target's bounds (project it with `ProjectPointToNavigation`), then attack on arrival. Attack distance comes from `DA_Tuning` (`Frost_AttackRange`, requested), never a typed number.
- **Why:** `BP_EmberCore` cuts a hole in the NavMesh, so `MoveToActor(Core)` failed with no error and the Frost stood still (21.11, `BPC_FrostBrain`).
- **Check:** in PIE a Frost with only the Core as target reaches it and the Core's heat drops.

### R12 · VibeUE: never spawn `K2Node_SpawnActorFromClass` by key `[Kartal]`
- **Rule:** to spawn actors in a graph built through VibeUE, use `BeginDeferredActorSpawnFromClass` + `FinishSpawningActor` (call-function nodes), not `create_node_by_key("NODE K2Node_SpawnActorFromClass")`.
- **Why:** that key crashed UE 5.8 while building `BP_FrostSpawner` (21.11).
- **Check:** the spawner graph compiles with 0 errors and PIE spawns the wave.

### R13 · After an editor crash, the Crash Reporter can hold the MCP port `[Kartal]`
- **Rule:** if MCP stays dead after a crash and `StartServer`, check who listens on port 8000 (`lsof -nP -iTCP:8000 -sTCP:LISTEN`). If it is `CrashReportClient`, close it, then run `ModelContextProtocol.StartServer` again.
- **Why:** on 21.11 a leftover Crash Reporter held port 8000 and every MCP call failed with HTTP 000.
- **Check:** `lsof` shows `UnrealEditor` on 8000 and one cheap MCP call works.

### R14 · Sizing a NavMeshBoundsVolume from mesh bounds: skip the sky sphere `[Kartal]`
- **Rule:** ignore `SM_SkySphere` and any mesh with an extent over 200 m. If a volume was ever oversized, delete `RecastNavMesh-Default` and Build Paths again; `RebuildNavigation` alone does not fix it.
- **Why:** the sky sphere made my volume 32 km wide, the RecastNavMesh kept a tiny tile pool ("3 tile limit reached") and the navmesh stayed empty (Part A, F53).
- **Check:** `NavigationSystemV1.project_point_to_navigation` returns a point at 3 floor spots, and `P` shows green.

### R15 · Python rotators use named values `[Kartal]`
- **Rule:** always `unreal.Rotator(pitch=0, yaw=90, roll=0)`, never positional.
- **Why:** the positional order is (roll, pitch, yaw); my meshes ended up lying on the floor (Part A, F03).
- **Check:** read the actor's rotation back after placing it and print it.
