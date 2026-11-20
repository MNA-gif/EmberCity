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

## From the team (to be merged)
<!-- Emrecan (weapon/health), Kartal (AI), Karahan (UI): add the traps you hit as R8+ with your name. -->
