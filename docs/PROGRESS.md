# Progress (newest on top)

Format per entry: date · name · Done / Next / Problems / Commit.

---

## 26.11.2026 · Nebil (21) · branch `nebil/audio` · team audio (Skill Dojo R3)
- **Done:**
  - **Skill:** `.claude/skills/team-audio` (10 rules with why + check, plus `reference.md`).
  - **Audio core:** `Audio/Core` holds `SC_Master` ← `SC_Music`, `SC_SFX`, the `SM_Volumes` mix, `ATT_SFX_Near` / `ATT_SFX_Far` attenuation and `SCON_Repeat` concurrency (max 4).
  - **My 3 event sounds (CC0):**
    - `SFX_Weapon_Shot` (0.35 s, pitch 0.92–1.08, near attenuation) on the player's `OnShotFired` and the Frost shot.
    - `SFX_Core_FuelDelivered` on `BP_EmberCore.ReceiveFuel`.
    - `SFX_Chapter_Win` / `SFX_Chapter_Lose` in `BP_ChapterDirector.EndChapter`.
  - **Music:** `BP_MusicDirector` in `L_Chapter1` crossfades `MUS_Explore` and `MUS_Danger` over 2 s. Danger = nearest Frost within `Audio_DangerRadius` (2500, new `DA_Tuning` field), checked on a 0.5 s timer.
  - **Settings:** `BP_AudioSave` (slot `AudioSettings`) is loaded and applied at start. Pause menu `WBP_ProtoPause` (key P) has Master / Music / SFX sliders that save on change.
  - `credits.md` added.
- **Tested (PIE):**
  - Explore music starts and switches to danger with both tracks heard during the fade; at 16 s only danger plays.
  - Music saved at 0.2 → PIE restarted → loaded 0.2 (then reset to 0.7).
  - P pauses the game; the sliders show the saved 1.0 / 0.7 / 0.8.
  - All Blueprints compile clean.
- **Not tested:** nobody has listened yet (the editor was unfocused); the pause menu layout was not seen in play (the preview render overlaps the rows).
- **Next:** Emrecan, Kartal and Karahan each add 3 sounds on their own systems in `Audio/SFX/<Name>/` with rows in `credits.md`.

## 21.11.2026 · Nebil (20) · branch `nebil/prototype` · L_Chapter1 rebuilt as a collapsed turbine hall
- **Done:**
  - **Removed:** all LevelPrototyping blockout (cubes, ramps, cylinders) and the old `Dressing/Facades` + `Dressing/Rubble`. The template `Floor` is hidden but kept as collision.
  - **New `Env/*` folders** from Abandoned Power Plant:
    - Concrete floor (14×14 tiles).
    - 2-storey perimeter walls with windows, inner reinforcement pillars and corner columns.
    - Doors (west by the Frost spawner, east behind the core) with small closed rooms behind.
    - A ceiling strip along the walls and rusty roof beams with a collapsed span in the middle (sky and sun come in).
    - North and south catwalks at 2 m: platforms, beam railing, posts and 4 stairways.
    - Fallen beams, rubble along the walls, and moss/leak decals on floor and walls.
  - **Kept:** the 12 cover walls with 24 cover points, the core, the spawner and the fuel pickups. PlayerStart moved to (600, 0, 100), facing the spawner.
  - **Light:**
    - Sun at pitch −58.
    - Height fog at 0.01, volumetric fog off.
    - `PPV_Hall`: vignette, bloom 0.5, white temp 5600.
    - Red door lamps, a warm core heat light and cold catwalk lamps.
  - **Materials:** floor, beam and wall MIs slightly darker and less saturated.
  - **Asset migration:** new used assets moved from the gitignored pack to `Art/PowerPlant` with their materials and textures; 0 references to `/Game/AbandonedPowerPlant` left. 11 large textures downsized (floor 2K, others 1K). `Art/PowerPlant` is 74 MB (291 MB before).
- **Tested:**
  - NavMesh: spawner→core 2548 cm; 24/24 cover points and all 8 fuel pickups reachable.
  - PIE screenshots from the player view: robots come through the west door and take the cover walls.
  - 0 Blueprint runtime errors.
- **Problems / gotchas:**
  - In UE, a higher post-process `White Temp` makes the image warmer (7000 turned it yellow).
  - Volumetric fog with strong lights washed the hall out to white.
  - The catwalk stairs are 45°, so Frost cannot path up (the player can climb them).
- **Commit:** `[Nebil] chapter1: rebuild the arena as a collapsed power-plant hall`

## 21.11.2026 · Nebil (19) · branch `nebil/prototype` · crouch + RobotBody error fix
- **Done:**
  - **Error fix:** "RobotBody accessed none" happened because the hit-flash `SetOverlayMaterial` ran on a Frost already destroyed by the killing shot (and again after the Delay). Both calls are now behind `IsValid(RobotBody)`.
  - **Player crouch:** hold Left Ctrl, or press C to toggle. `bCanCrouch` is on; crouched speed is `Player_CrouchSpeed`.
  - **Frost crouch:** crouches at its cover point (speed `Frost_CrouchSpeed`), stands up to shoot, and crouches again after `Frost_PeekTime` (`PeekDone` event). It stands while moving, strafing or going back to the core.
  - **Line of sight:** the check now starts at `Frost_EyeHeight` above the feet, so a crouched Frost still "peeks".
  - 4 new `DA_Tuning` fields documented first.
  - **Crouch animations:** 6 Manny crouch assets (idle, 4 walks, `BS_MM_CrouchStrafe`) come from the engine's own MoverExamples plugin (no download, 3 MB). They were loaded once through a temporary `[CoreRedirects]` onto our `SK_Mannequin`, resaved and moved to `Content/EmberCity/Art/Crouch`; the redirect is removed again.
  - **Crouch pose:** `ABP_ProtoTPPistol` (copy of `ABP_TP_Pistol`) uses the crouch blendspace for the lower body when `IsCrouched` (Blend Poses by bool, 0.2 s); the upper body keeps the pistol aim. Used by the Frost `Mesh` (the robot follows it) and the player body.
  - **Player camera:** the FP arms do not copy the body pose, so `OnStartCrouch`/`OnEndCrouch` move `FirstPersonMesh` (with the camera) down and up by the capsule change.
- **Tested (PIE):**
  - Key C toggles crouch: camera z 377.6 → 321.6 → 377.6, crouched speed 200.
  - A Frost at its cover point crouched by itself: head 104 cm above the feet (156 standing). Screenshot: a robot crouched behind a low wall, aiming.
  - 2 Frost killed → no RobotBody error.
  - 0 Blueprint runtime errors in 4 PIE runs.
- **Not tested:** Left Ctrl hold, only C was injected. Crouch walk while moving (the robots crouch only when standing at cover).

## 21.11.2026 · Nebil (18) · branch `nebil/prototype` · cover AI, fire feel, hit feedback
- **Done:**
  - **Map:** 12 low walls (`SM_Wall_Plain_300`, 130 cm high) in `Dressing/Cover` of `L_Chapter1`, with 24 `BP_ProtoCoverPoint` actors, one on each side of every wall. NavMesh rebuilt.
  - **Frost cover AI:** `BP_ProtoFrost` `FindCover` keeps a cover point while the player→point trace is blocked. Otherwise it claims the nearest free point (Owner = Frost) that is hidden and inside `Frost_ShootRange`. While engaged it runs to cover, or side-steps up to `Frost_StrafeRadius` when no cover is free. It stops orienting to movement so it keeps aiming at the player. Out of sight it releases the cover and goes back to the core.
  - **Fire feel:** `MM_Pistol_Fire_Montage` plays on the FP arms. Camera recoil is `Weapon_RecoilPitch`; the `CS_ProtoFire` shake is scaled by `Weapon_FireShakeScale`.
  - **Feedback:**
    - New dispatcher `OnHitConfirmed` on `BPC_ProtoWeapon`; `WBP_ProtoHUD` binds it and shows a red X hit marker for `Feedback_HitMarkerTime`.
    - Frost flash red (`M_ProtoHitFlash` overlay) for `Feedback_HitFlashTime`.
    - When the player is hurt: `CS_ProtoHurt` shake and a red screen-edge vignette (`M_ProtoHurtVignette`) over `Feedback_HurtVignetteTime`.
  - 6 new `DA_Tuning` fields and 1 dispatcher added to `technical_design.md` first.
- **Tested (PIE):**
  - Frost claimed different cover points (03_A, 04_B, 09_A/B) and others strafed; screenshot shows a robot shooting from behind a low wall.
  - One shot: fire montage active, control pitch +0.35°, Frost HP 40→20, red overlay on and off after the flash time, HUD `HitMarkerUntil` = now + 0.15.
  - Player hurt → `HurtUntil` set.
  - All Blueprints compile clean.
- **Problems:**
  - PIE started with "spawn at 0,0,0" fails (player hits the core); start PIE from PlayerStart.
  - 8 robots at `Frost_HitChance` 0.35 kill the player in ~20 s: balance not decided.
  - HUD (hit marker, vignette) cannot be seen in `HighResShot`; check it by eye.
- **Commit:** `[Nebil] prototype: frost cover AI, fire feel, hit feedback`

## 21.11.2026 · Nebil (17) · branch `nebil/prototype` · Frost aim fix
- **Done:** in the `ABP_TP_Pistol` aim pose the barrel points ~28–30° to the side of the actor's forward, so Frost faced the player but shot past him. `BP_ProtoFrost` AttackTick now measures the barrel yaw (hand_r → `TPWeapon` Muzzle) each shot and sets actor yaw = look-at yaw − (barrel yaw − actor yaw); no hard-coded angle.
- **Tested (PIE):** shooting Frost barrel-vs-player error 1.5° and 2.8° (before ~30°); screenshot: all 4 robots point their pistols at the camera; player took hits; 0 Blueprint runtime errors.
- **Commit:** `[Nebil] prototype: frost aim the barrel at the player`

## 21.11.2026 · Nebil (16) · branch `nebil/prototype` · sci-fi robot enemies
- **Done:** Fab *Retro Futuristic Soldier* (Red Mallet Studio, free Personal licence, Standard License, UE5 Manny skeleton, 30.9 MB) added via the launcher; used assets (mesh, its skeleton copy, physics, 2 materials, 5 textures) moved to `Content/EmberCity/Art/RetroSoldier` (28 MB), pack folder in `.gitignore`. `BP_ProtoFrost`: new `RobotBody` skeletal mesh follows the existing `Mesh` with `SetLeaderPoseComponent`; `Mesh` keeps `ABP_TP_Pistol`, AI, weapon socket, but is not rendered (`SetRenderInMainPass false`, tick pose always). Animations untouched.
- **Tested (PIE):** robots walk (speed 300, ShouldMove true), aim and hold the pistol; `RobotBody` hand_r = `Mesh` hand_r (0.0 cm); 0 Blueprint runtime errors.
- **Not tested:** hit reaction/death look (Frost is destroyed on death); icy tint of the robot lights (still the pack's blue).
- **Commit:** `[Nebil] prototype: retro sci-fi robot look for frost`

## 21.11.2026 · Nebil (15) · branch `nebil/prototype` · official first-person pistol rig
- **Done:** the hand-made grip looked wrong (third-person pose forced onto the FP arms). Copied UE 5.8's own template content (engine `Templates/TemplateResources/Standard`, same as "Add Feature Pack": `Content/Variant_Shooter`, `Content/Weapons`, 20 MB, no download). Player: `FPWeapon` = `SKM_Pistol` snapped to `FirstPersonMesh` socket `HandGrip_R`, arms anim = `ABP_ProtoFPPistol` (copy of `ABP_FP_Pistol` with its BeginPlay cast changed from `BP_ShooterCharacter` to `BP_FirstPersonCharacter`, otherwise `Aim Target` stayed at 0,0,0), body anim = `ABP_TP_Pistol`; `Gun`/`Muzzle` (tracer + flash) snapped to the pistol's `Muzzle` socket; Pistol 9mm hidden. Frost: `ABP_TP_Pistol` + `TPWeapon` (`SKM_Pistol`) on `HandGrip_R`, muzzle the same way.
- **Tested (PIE):** right hand grips the pistol like the Arena Shooter template; Frost hold it two-handed in aim pose and shoot (tracer seen); 0 Blueprint runtime errors.
- **Not tested:** fire recoil montage (not wired yet), looking up/down.
- **Commit:** `[Nebil] prototype: template FP pistol rig for player and frost`

## 21.11.2026 · Nebil (14) · branch `nebil/prototype` · firm grip
- **Done:** gun grip solved from the right-hand bones (fist centre = mean of `*_01_r` and `*_03_r`, grip axis = `index_01_r` → `pinky_01_r`, barrel = camera forward) → `Gun` relative to `hand_r`: (-10.48, 1.77, -3.73), (P-18.75, Y-157.87, R5.11), same on `BP_ProtoPlayer` and `BP_ProtoFrost`; left-hand IK effector (-1.41, 4.79, -4.14) in `hand_r` space so it supports under the right hand.
- **Tested (PIE):** fingers wrap the grip, slide above the fist; left hand under/behind the right hand; Frost hold the pistol in the fist two-handed; 0 Blueprint runtime errors.
- **Commit:** `[Nebil] prototype: firm two-handed pistol grip`

## 21.11.2026 · Nebil (13) · branch `nebil/prototype` · CS-style grip, Frost shoot back
- **Done:** two-handed pistol grip: `ABP_ProtoFPArms` (copy of `ABP_FP_Copy`) + Two Bone IK after the FP warp puts `hand_l` under `hand_r` (effector in `hand_r` space (-3.6, 12.1, -4.7) = the offset in the body pistol pose, `bMaintainEffectorRelRot`); set at BeginPlay with `SetAnimInstanceClass`. Contract: `Frost_ShootRange` 2500 cm and `Frost_HitChance` 0.35 in technical_design §4.4 + `PDA_Tuning`/`DA_Tuning` (23 fields). `BP_ProtoFrost`: `ABP_ProtoPlayerArmed` on its mesh, Pistol 9mm on `hand_r` (same grip offset as the player), `AttackTick` → if the player is valid, within `Frost_ShootRange` and visible (trace from the eyes, all Frost ignored): stop, turn to the player, tracer from the muzzle, `Frost_HitChance` → `BPI_Damageable.ApplyDamage(Frost_AttackDamage)`; else the old Core behaviour.
- **Tested (PIE):** FP hands gap 0 → left hand cups the grip; Frost hold the pistol two-handed; Frost shot the player 100 → 40 HP in a few seconds at the start; Frost turn to the player; 0 Blueprint runtime errors. `ABP_ProtoPlayerArmed` IK alpha = 0 (kept for later).
- **Problems:** a body-ABP compile error opened a modal dialog at PIE start and froze the editor (fixed: Local↔Component conversion nodes). Balance: 4 Frost with 35 % hit chance kill an exposed player in ~10 s; candidate `Frost_HitChance` 0.2.
- **Commit:** `[Nebil] prototype: two-handed grip, frost pistols and shooting`

## 21.11.2026 · Nebil (12) · branch `nebil/prototype` · gun held in the hand
- **Done:** `Gun` now attaches at BeginPlay to `FirstPersonMesh` socket `hand_r` with a measured grip offset (loc -8.26, 4.90, -1.33; rot P-18.30 Y-158.42 R0.64), fingers wrap the grip; gun kick offset set to 0 (it pushed along the bone axis). Cause of the earlier "floating" gun: the Tick interpolated `Gun` to `GunRest` measured in camera space.
- **Not tested:** running + shooting with the new attach, looking up/down, muzzle/tracer position after the change.
- **Commit:** `[Nebil] prototype: gun held in the right hand`

## 21.11.2026 · Nebil (11) · branch `nebil/prototype` · Fab assets, gun in hand, Frost walk
- **Done:** Fab (free Personal licence, Standard License): *Modular Old Power Plant* (Nimikko) added to the project via the Epic launcher, 22 used meshes + deps moved to `Content/EmberCity/Art/PowerPlant` (textures downsized to 1K), the rest of the 890 MB pack stays local (`Content/AbandonedPowerPlant/` in `.gitignore`); *Pistol 9mm Custom* (DTry) FBX → `Art/Pistol9mm/SM_Pistol9mm` (main pistol + magazine merged, 1K textures, other parts moved to `Content/Developers/`). `L_Chapter1`: 3-storey ruined power-plant facades outside the arena walls + flat rubble inside (no nav/collision). Player: `ABP_ProtoPlayerArmed` (copy of ABP_Unarmed + Layered Blend from `spine_01` with `MF_Pistol_Idle_ADS`) on the body mesh, so the first-person arms (they copy the body pose) hold the pistol pose while running; real pistol at the right hand, muzzle moved. Frost: `NavMovementProperties.bUseAccelerationForPaths = true` → walk animation plays.
- **Tested (PIE):** running (W) + holding LMB → arms stay in pistol pose, tracer from the new muzzle, impact burst; Frost velocity 300 with acceleration 2048, `ShouldMove = true`; no Blueprint runtime errors; `Art/` = 33.6 MB.
- **Not tested / problems:** City Street Props (Dekogon, shop signs) is in the Fab library but not added (launcher UI froze); no gun sound/reload animation; looking up/down does not pitch the arms (pose is fixed to the camera).
- **Commit:** `[Nebil] prototype: fab power plant + pistol, armed arms, frost walk fix`

## 21.11.2026 · Nebil (10) · branch `nebil/prototype` · enemies upright, visible gun, map look
- **Done:** `BP_ProtoFrost` mesh rotation fixed (was pitch -90: `unreal.Rotator(a,b,c)` is roll, pitch, yaw) + icy material `M_ProtoFrostIce`. Gun: placeholder pistol from engine shapes on `BP_ProtoPlayer` (`Gun` attached to `FirstPersonCamera` at BeginPlay, `Muzzle`, `MuzzleFlash`), hold LMB = auto fire at `Weapon_FireInterval`, `BPC_ProtoWeapon.OnFired(HitLocation, bHit)` → tracer `BP_ProtoTracer`, muzzle light, gun kick + small pitch recoil, Niagara `RadialBurst` at impact; debug trace line off. `L_Chapter1` look: snow floor, stone walls, rust blocks, cold low sun, blue fog, glowing Core (`M_ProtoEmber` + `EmberLight`), glowing fuel (`M_ProtoFuel` + light).
- **Tested (PIE):** Frost stand and walk upright to the Core; LMB held (InputService.inject_key) → ammo 12→5, tracers spawn and expire, Frost hit 40→20→dead; screenshots via `HighResShot 1` (Saved/Screenshots); 0 Blueprint runtime errors.
- **Not tested / problems:** first-person arms do not hold the gun (pistol anims on `SKM_Manny_Simple` did not play), no gun sound (no CC0 sound in the project). Free asset downloads approved (Quaternius Ultimate Guns Pack, Downtown City MegaKit 223 MB, CC0) but blocked: Google Drive "quota exceeded", itch.io HTTP 429 - retry later, then swap the gun mesh and dress the map.
- **Commit:** `[Nebil] prototype: upright frost, visible gun and firing feedback, chapter1 look`

## 21.11.2026 · Nebil (9) · branch `nebil/prototype` · playable loop (placeholder)
- **Done:** placeholder versions of the members' systems, only in `Systems/Nebil/Prototype/` (to be replaced by Emrecan's, Kartal's and Karahan's real ones on merge): `BPC_ProtoHealth` (InitHealth, TakeDamage, OnHealthChanged, OnDied), `BPC_ProtoWeapon` (line trace from the camera, mag/reserve/reload, damages only `Team.Frost` and not `State.Dead` via `BPI_Tagged` + `BPI_Damageable`), `BP_ProtoPlayer` (child of `BP_FirstPersonCharacter`, LMB fire, R reload, picks up `Item.Fuel` on overlap at `Fuel_CarrySpeedMultiplier`, delivers to the Core's `BPI_FuelReceiver`, `State.Dead` on death), `BP_ProtoFrost` (walks to the Core, attacks Core/player in its `AttackZone` every `Frost_AttackInterval`), `BP_ProtoFrostSpawner` (`Spawner_*` waves), `BP_ProtoFuel`, `WBP_ProtoHUD`, `WBP_ProtoEndScreen` (result + Retry → `RetryChapter`), `BP_ProtoGameMode`. Nebil's own: `BP_EmberCore` + `DeliveryZone` sphere, `CoreMesh` no longer affects navigation (Core was unreachable); `BP_ChapterDirector` + `HUDClass`, binds the player's `OnDied` → `EndChapter(false)`. `L_Chapter1`: GameMode override = `BP_ProtoGameMode`, 8 fuel + 1 spawner on the connected floor, director HUD/EndScreen set.
- **Tested (PIE, L_Chapter1):** pawn = `BP_ProtoPlayer`, HUD shows heat/fuel/HP/ammo; wave 1 = 4 Frost walk to the Core and drain it; heat 0 → end screen "The ember went out", cursor on; Retry button (OnClicked) reloads; fuel pickup → carrying, speed 600→420, tag `State.CarryingFuel`; delivery → +15 heat, Fuel 1; weapon hits Frost 40→20→dead (`[Frost] Died`); 5 fuel → won, end screen win text; 125 damage to player → `State.Dead`, `Ended, won = false`; 0 Blueprint runtime errors.
- **Not tested:** real mouse/keyboard play by a human; reload by R key (Reload called on empty mag only); packaged build. **Balance:** 4 Frost drain ~14 heat/s at the Core → the chapter is lost ~15 s after they arrive if the player does not defend; candidate fix `Ember_DamageToHeat` 0.5 → 0.25.
- **Problems:** template `Pawn`/`CharacterMesh` profiles ignore `Visibility` → line traces pass through characters (Frost capsule now blocks Visibility); VibeUE `create_node_by_key("NODE K2Node_SpawnActorFromClass")` and a wrong macro pin name crash the editor's Python (editor restart needed).
- **Next:** team: replace the prototypes with your systems (same contracts); Nebil: on each merge remove the matching `Proto` asset and play.
- **Commit:** `[Nebil] prototype: playable loop with placeholder player, frost, fuel, HUD`
## 21.11.2026 · Emrecan · branch `emrecan/health-weapon`
- **Done:** `Systems/Emrecan/BPC_Health` (Player/Frost max health from DA_Tuning by owner tag via `BPI_Tagged`, `ApplyDamage(Amount, DamageInstigator)`, `OnHealthChanged`, `OnDied`), `BPC_Weapon` (line trace `Weapon_Range`, mag/reserve/interval/reload from DA_Tuning, damages only `Team.Frost` and not `State.Dead` through `BPI_Damageable`, `OnAmmoChanged`), `Player/BP_Player` (template copy + both components, `GameplayTags`=`Team.Player`, `BPI_Tagged`, `BPI_Damageable`→Health, `OnDied` adds `State.Dead`, `IA_Fire` LMB / `IA_Reload` R in `IMC_Player`); `L_Test_Emrecan` GameMode Override = `BP_GM_TestEmrecan` (pawn BP_Player). Tested in PIE: Frost dummy 40→20→0 + `State.Dead`, no-tag and Frost+Dead targets take no damage, auto reload 12/36, player 100→70→0 + `State.Dead`, real LMB/R input.
- **Next:** Nebil: add `BPC_Health.ApplyDamage(Amount, DamageInstigator)` to technical_design §4.2b (Kartal's BP_Frostling forwards to it), merge this branch, set BP_Player as pawn on main; Karahan: bind HUD to `OnHealthChanged`/`OnAmmoChanged`.
- **Problems:** no crosshair yet (trace uses eye view point, not the camera socket); reload with reserve smaller than a magazine not tested; dev helpers `BP_TestDummy`, `BP_TestShooter` stay in Systems/Emrecan.
## 21.11.2026 · Kartal · branch `kartal/frost`
- **Done:** `Systems/Kartal/BP_Frostling` (Character, `GameplayTags`=`Team.Frost`, `BPI_Tagged`, `BPI_Damageable` stub that only logs), `BPC_FrostBrain` (every `Frost_AttackInterval` picks the nearest `Team.Player`/`Target.EmberCore` via `BPI_Tagged`, skips `State.Dead`, walks at `Frost_WalkSpeed`, `ApplyDamage(Frost_AttackDamage)`, stops on `OnChapterEnded` or own `State.Dead`), `BP_FrostSpawner` (`Spawner_WaveCount` × `Spawner_EnemiesPerWave` every `Spawner_TimeBetweenWaves`, `OnWaveStarted(WaveIndex, WaveCount)`, `SpawnPoints` = TargetPoints, stops on `OnChapterEnded`); `L_Test_Kartal`: NavMesh, EmberCore, ChapterDirector, 3 spawn points with a valid full path to the Core. Tested in PIE: alive target 900 cm chosen over a `State.Dead` one at 400 cm, 10 damage per interval, retarget to Core when the target is gone (heat 60 → 19), waves 1/2/3 → 12 Frostlings, `EndChapter(false)` stops the spawner and all 13 brains, 0 Blueprint runtime errors.
- **Next:** Kartal, once Emrecan's `BPC_Health` is on main: add it to `BP_Frostling`, forward `ApplyDamage`, `OnDied` adds `State.Dead`, spawner decrements `AliveCount` on `OnDied`. Nebil: add `Frost_AttackRange` (float, cm, default 150, used by `BPC_FrostBrain`) to technical_design §4.4 + DA_Tuning; place `BP_FrostSpawner` + TargetPoints in `L_Chapter1` on the connected floor (R10).
- **Problems:** `MoveToActor` fails on the Core (it carves a NavMesh hole), so the brain walks to a point just outside the target's bounds and attacks on arrival (no typed range until `Frost_AttackRange`). VibeUE `create_node_by_key("NODE K2Node_SpawnActorFromClass")` crashes UE 5.8: use `BeginDeferredActorSpawnFromClass` + `FinishSpawningActor`. Dev helper `BP_TestPlayerTarget` stays in Systems/Kartal.
- **Commit:** `[Kartal] frost: ...` (9589401, dcba50b, ac5e942)
## 21.11.2026 · Karahan · branch `karahan/fuel-hud`
- **Done:** `Systems/Karahan/BPC_FuelCarrier` (Actor Component: `Carried/Delivered`, `OnFuelChanged(Carried, Delivered, Needed)`, speed x `Fuel_CarrySpeedMultiplier` while carrying, delivers to the Core through `BPI_FuelReceiver.ReceiveFuel`), `BP_FuelPickup` (implements `BPI_Interactable` + `BPI_Tagged`, `GameplayTags` = `Item.Fuel`, refuses a second fuel while carrying), `WBP_HUD` (fuel + Core heat bound to dispatchers, health/ammo/wave placeholders), `WBP_EndScreen` (win/lose text from the director's `bWon`, Retry calls `RetryChapter()`). `L_Test_Karahan` has the Core and 2 pickups; `BP_FuelTestPlayer` (child of the template character + the component) is a test harness only. 5 rules `[Karahan]` for the team skills in `team_skill_rules.md`.
- **Tested (PIE, L_Test_Karahan):** pickup -> Carried 1, walk speed 600 -> 420, pickup destroyed; second pickup while carrying -> ignored; walking near the Core -> Carried 0, Delivered 1, speed 600, `BPC_Ember.FuelDelivered` 1 (heat +15); HUD showed `FUEL 2 / 5` and the heat bar moved; end screen showed "THE FIRE WENT OUT" (`bWon` false) and "THE FIRE LIVES" after `EndChapter(true)`; Retry button (`on_clicked.broadcast()`) reloaded the level. All 4 Blueprints compile with no errors.
- **Not tested:** `BP_Player` with the component (Emrecan adds it), E key from the real player, health/ammo/wave on the HUD, `EndScreenClass` set on the director in `L_Chapter1` (Nebil), real mouse click on Retry, packaged build.
- **Next:** Emrecan: add `BPC_FuelCarrier` to `BP_Player`, forward E to `BPI_Interactable.Interact`, and add `State.CarryingFuel` to the player while carrying (or tell me a function to call). Nebil: `Fuel_DeliverRange` field in `DA_Tuning`, set `EndScreenClass` and place 8 `BP_FuelPickup` in the connected floor of `L_Chapter1`, add the HUD to the viewport.
- **Problems:** `State.CarryingFuel` cannot be set from my side without a cast to another member's class; `DeliverRange` is still a component variable (breaks R3 until Nebil adds the field).
- **Commit:** `[Karahan] fuel: BPC_FuelCarrier, BP_FuelPickup, WBP_HUD, WBP_EndScreen`

## 20.11.2026 · Nebil (8) · main · contract change requested by Emrecan
- **Done:** technical_design.md first, then code: `PDA_Tuning` / `DA_Tuning` + `Weapon_Range` 5000 cm, `Weapon_StartReserve` 48 (21 fields); `State.Dead` is added by the dying actor in its own `OnDied` (BP_Player: Emrecan, BP_Frostling: Kartal); `BPC_Weapon` damages only `Team.Frost` and not `State.Dead`; new interface `Core/Interfaces/BPI_Tagged.GetGameplayTags() → Tags` so systems read another actor's tags without a cast; `BP_EmberCore` implements it (returns `GameplayTags`).
- **Tested:** DA_Tuning shows the 2 new values; PIE in L_Chapter1: `core.GetGameplayTags()` → `Target.EmberCore`, Ember still drains (89.67 at t=10.33); BP_EmberCore class implements `BPI_Tagged_C`.
- **Next:** Emrecan, Kartal, Karahan: implement `BPI_Tagged` on your tagged actors (BP_Player, BP_Frostling, BP_FuelPickup); Kül Şehri doc: same changes.
- **Commit:** `[Nebil] contracts: weapon tuning fields, State.Dead rule, BPI_Tagged`

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
