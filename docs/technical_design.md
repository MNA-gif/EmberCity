# Ember City · Technical Design

Team: Nebil (integration owner), Emrecan, Kartal, Karahan · DGD727 final project · UE 5.8, Blueprint
Planning doc (Turkish, with the loop diagram): https://claude.ai/artifact/QVHtfQDHT3uuC66DA5ryf7

## 1. Game in one paragraph

**Ember City** is a story-driven single-player FPS of about one hour (5 chapters). The world is freezing; the last warm place is the Ember Core inside the citadel. The player is its keeper: they bring fuel from the frozen city to keep the Core burning and shoot the Frost, creatures that drain heat and attack the Core. This lab task builds **Chapter 1 only** as a complete loop; chapters 2–5, new enemies, weapons and cutscenes come before the final.

## 2. Chapter 1 loop (B6)

1. **Start:** `L_Chapter1` loads, `BP_ChapterDirector` starts the chapter, the Core's heat starts to drain.
2. **Main action:** the player picks up fuel in the city (`BP_FuelPickup`), carries it to the Core (slower while carrying) and shoots the Frost.
3. **Fail:** the Core's heat reaches 0 (`OnEmberDepleted`) or the player dies (`OnDied` on the player).
4. **Win:** `Chapter_FuelToWin` fuel delivered (default 5) → the Core ignites (`OnEmberIgnited`).
5. **End screen:** `WBP_EndScreen` shows "The fire lives" / "The fire went out" + a Retry button that reloads the level.

## 3. Systems and owners (B3)

| Owner | System | Type | Responsibility | Folder |
|---|---|---|---|---|
| Nebil | `BPC_Ember` | Actor Component | Heat drains over time, fuel raises it, 0 = depleted, target fuel = ignited. Lives on `BP_EmberCore` | `Content/EmberCity/Systems/Nebil` |
| Nebil | `BP_ChapterDirector` | Actor (one per level) | Starts the chapter, decides win / fail, shows the end screen, Retry reloads the level | `Content/EmberCity/Systems/Nebil` |
| Emrecan | `BPC_Health` | Actor Component | Health, taking damage, death. The same component on the player and on enemies | `Content/EmberCity/Systems/Emrecan` |
| Emrecan | `BPC_Weapon` | Actor Component | Fire (line trace), magazine, reload; damages what it hits through `BPI_Damageable` | `Content/EmberCity/Systems/Emrecan` |
| Kartal | `BPC_FrostBrain` | Actor Component | Enemy AI: picks the nearest target (player or Core), walks, attacks. Lives on `BP_Frostling` | `Content/EmberCity/Systems/Kartal` |
| Kartal | `BP_FrostSpawner` | Actor | Spawns enemies in waves | `Content/EmberCity/Systems/Kartal` |
| Karahan | `BPC_FuelCarrier` + `BP_FuelPickup` | Actor Component + Actor | Pick up fuel (`BPI_Interactable`), slower while carrying, deliver to the Core (`BPI_FuelReceiver`) | `Content/EmberCity/Systems/Karahan` |
| Karahan | `WBP_HUD` + `WBP_EndScreen` | Widgets | Health, ammo, Core heat, fuel count, wave; end screen. **Listens only**, never changes another system | `Content/EmberCity/Systems/Karahan` |

Shared, owned by Nebil: `Content/EmberCity/Core/` (`PDA_Tuning`, `DA_Tuning`, `Interfaces/`), `Config/DefaultGameplayTags.ini`, `Content/EmberCity/Maps/L_Chapter1`, `Config/`.
`BP_Player` (from the First Person template) is owned by Emrecan; others add their components to it only through Emrecan.

## 4. Contracts (B2, B4)

Rules:
- Systems talk **only** through the interfaces, dispatchers and tags below. No system edits another system's Blueprint.
- Listeners bind to dispatchers on `BeginPlay`; they find other actors by gameplay tag, never by name.
- The HUD only listens: it binds to dispatchers and never calls a function that changes game state.
- A new or changed contract: first a change in this file, approved by the owner, then code.

### 4.1 Interfaces (`Content/EmberCity/Core/Interfaces`)

| Interface | Function | Implemented by | Called by | Owner |
|---|---|---|---|---|
| `BPI_Damageable` | `ApplyDamage(Amount: float, Instigator: Actor)` | `BP_Player`, `BP_Frostling` (forward to `BPC_Health`), `BP_EmberCore` (turns damage into heat loss) | `BPC_Weapon`, `BPC_FrostBrain` | Emrecan |
| `BPI_Interactable` | `Interact(Interactor: Actor)` | `BP_FuelPickup` | Player interact key (E) | Karahan |
| `BPI_FuelReceiver` | `ReceiveFuel(Amount: int)` | `BP_EmberCore` (forwards to `BPC_Ember`) | `BPC_FuelCarrier` | Nebil |

### 4.2 Event dispatchers

| Dispatcher | On | Parameters | Listeners | Owner |
|---|---|---|---|---|
| `OnHealthChanged` | `BPC_Health` | `Current: float, Max: float` | `WBP_HUD` | Emrecan |
| `OnDied` | `BPC_Health` | `DeadActor: Actor` | `BP_ChapterDirector` (player died = fail), `BP_FrostSpawner` (alive count) | Emrecan |
| `OnAmmoChanged` | `BPC_Weapon` | `InMag: int, Reserve: int` | `WBP_HUD` | Emrecan |
| `OnHeatChanged` | `BPC_Ember` | `Heat: float, MaxHeat: float` | `WBP_HUD` | Nebil |
| `OnEmberDepleted` | `BPC_Ember` | — | `BP_ChapterDirector` (fail) | Nebil |
| `OnEmberIgnited` | `BPC_Ember` | — | `BP_ChapterDirector` (win) | Nebil |
| `OnFuelChanged` | `BPC_FuelCarrier` | `Carried: int, Delivered: int, Needed: int` | `WBP_HUD` | Karahan |
| `OnWaveStarted` | `BP_FrostSpawner` | `WaveIndex: int, WaveCount: int` | `WBP_HUD` | Kartal |
| `OnChapterEnded` | `BP_ChapterDirector` | `bWon: bool` | `WBP_EndScreen`, `BP_FrostSpawner` (stops), `BPC_FrostBrain` (stops) | Nebil |

### 4.2b Functions other systems may call (added 20.11.2026, Nebil)

| Function | On | Called by | Owner |
|---|---|---|---|
| `AddFuel(Amount: int)`, `LoseHeat(Amount: float)`, `StopEmber()` | `BPC_Ember` | `BP_EmberCore` (through the interfaces), `BP_ChapterDirector` | Nebil |
| `RetryChapter()` | `BP_ChapterDirector` | `WBP_EndScreen` Retry button (finds the director with Get Actor Of Class) | Nebil |
| `EndChapter(bWon: bool)` | `BP_ChapterDirector` | only the director itself (Ember events, player `OnDied`) | Nebil |

`BP_ChapterDirector.EndScreenClass` (UserWidget class, Instance Editable): set to `WBP_EndScreen` in `L_Chapter1` after Karahan's widget is on main. The director creates it on chapter end, sets input Game and UI + mouse cursor; `RetryChapter` sets Game Only, hides the cursor and reloads the level. The widget reads `bWon` from `OnChapterEnded`.
Player death: the director binds to the player's `BPC_Health.OnDied` once Emrecan's component is on main; until then `EndChapter(false)` is reached only by `OnEmberDepleted`.

### 4.3 Gameplay tags (`Config/DefaultGameplayTags.ini`, owner Nebil)

Every gameplay actor has a variable `GameplayTags` of type `GameplayTagContainer` (Instance Editable); systems find each other by tag. (Not `Tags`: that name is already AActor's built-in `TArray<FName>` and cannot be reused. Changed 20.11.2026 by Nebil.)

| Tag | On | Used for | Owner |
|---|---|---|---|
| `Team.Player` | `BP_Player` | Enemy target choice, HUD finds the player | Nebil |
| `Team.Frost` | `BP_Frostling` | Weapon knows what it hit, alive enemy count | Kartal |
| `Target.EmberCore` | `BP_EmberCore` | Enemies and the fuel carrier find the Core | Nebil |
| `Item.Fuel` | `BP_FuelPickup` | Interaction and HUD hint | Karahan |
| `State.CarryingFuel` | Player while carrying fuel | Slow-down, enemy priority target | Karahan |
| `State.Dead` | Any actor whose health reached 0 | No more damage or targeting | Emrecan |

### 4.4 `Content/EmberCity/Core/DA_Tuning` (B5)

`PDA_Tuning` is a Primary Data Asset Blueprint; `DA_Tuning` is its one instance. Every system has a variable `Tuning` (type `PDA_Tuning`, default `DA_Tuning`). **No gameplay number is typed inside a Blueprint.** Defaults are first guesses, balanced by play.

| Field | Default | Unit | Used by | Owner |
|---|---|---|---|---|
| `Ember_StartHeat` | 100 | heat | `BPC_Ember` | Nebil |
| `Ember_DrainPerSecond` | 1.0 | heat/s | `BPC_Ember` | Nebil |
| `Ember_HeatPerFuel` | 15 | heat | `BPC_Ember` | Nebil |
| `Ember_DamageToHeat` | 0.5 | multiplier | `BP_EmberCore` | Nebil |
| `Chapter_FuelToWin` | 5 | count | `BPC_Ember`, `WBP_HUD` | Nebil |
| `Player_MaxHealth` | 100 | health | `BPC_Health` | Emrecan |
| `Frost_MaxHealth` | 40 | health | `BPC_Health` | Emrecan |
| `Weapon_Damage` | 20 | health | `BPC_Weapon` | Emrecan |
| `Weapon_FireInterval` | 0.15 | s | `BPC_Weapon` | Emrecan |
| `Weapon_MagSize` | 12 | rounds | `BPC_Weapon` | Emrecan |
| `Weapon_ReloadTime` | 1.5 | s | `BPC_Weapon` | Emrecan |
| `Frost_WalkSpeed` | 300 | cm/s | `BPC_FrostBrain` | Kartal |
| `Frost_AttackDamage` | 10 | health | `BPC_FrostBrain` | Kartal |
| `Frost_AttackInterval` | 1.2 | s | `BPC_FrostBrain` | Kartal |
| `Spawner_WaveCount` | 3 | waves | `BP_FrostSpawner` | Kartal |
| `Spawner_EnemiesPerWave` | 4 | enemies | `BP_FrostSpawner` | Kartal |
| `Spawner_TimeBetweenWaves` | 25 | s | `BP_FrostSpawner` | Kartal |
| `Fuel_CarrySpeedMultiplier` | 0.7 | multiplier | `BPC_FuelCarrier` | Karahan |
| `Fuel_PickupCount` | 8 | count | `BP_FuelPickup` placement in `L_Chapter1` | Karahan |

## 5. Folders

```
Content/EmberCity/
  Core/              PDA_Tuning, DA_Tuning, Interfaces/          (Nebil)
  Maps/L_Chapter1    the chapter map                             (Nebil)
  Maps/Test/         L_Test_Nebil, L_Test_Emrecan, L_Test_Kartal, L_Test_Karahan
  Player/            BP_Player                                   (Emrecan)
  Systems/Nebil/     BPC_Ember, BP_EmberCore, BP_ChapterDirector
  Systems/Emrecan/   BPC_Health, BPC_Weapon
  Systems/Kartal/    BPC_FrostBrain, BP_Frostling, BP_FrostSpawner
  Systems/Karahan/   BPC_FuelCarrier, BP_FuelPickup, WBP_HUD, WBP_EndScreen
```

## 6. Git

- Branches: `nebil/ember`, `emrecan/health-weapon`, `kartal/frost`, `karahan/fuel-hud`. Only Nebil merges into `main`, one system at a time, and plays after every merge.
- Commit message: `[Name] area: what changed`, e.g. `[Kartal] frost: enemies pick the nearest target`.
- Git LFS for `.uasset`, `.umap`, art and audio (`.gitattributes`). Never commit passwords, API keys, tokens or Claude session logs.
