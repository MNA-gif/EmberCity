# Karahan · fuel + HUD systems

Branch: `karahan/fuel-hud`. Contracts: `docs/technical_design.md`. All four Blueprints are built and tested in PIE (see `docs/PROGRESS.md`); this file describes them.

**Differences from the first plan (what was actually built):**
- `BPC_FuelCarrier` delivers by itself: on Tick, if it carries fuel and the Core (first actor implementing `BPI_FuelReceiver`, found on BeginPlay) is within `DeliverRange`, it calls `ReceiveFuel(1)`. No extra interact key for the Core.
- `DeliverRange` (250 cm) is a variable on the component for now; it should become `Fuel_DeliverRange` in `DA_Tuning` (needs Nebil, team-rules R3).
- `State.CarryingFuel` is NOT added to the player yet: only `BP_Player` can edit its own `GameplayTags` (Emrecan). Open contract point.
- `WBP_HUD` binds fuel (`OnFuelChanged`) and Core heat (`OnHeatChanged`) now; health, ammo and wave texts are placeholders until `BPC_Health`, `BPC_Weapon`, `BP_FrostSpawner` are on main.
- `WBP_EndScreen` reads `bWon` from `BP_ChapterDirector` on Construct (works even if `OnChapterEnded` fired before the widget existed).

## BPC_FuelCarrier (Actor Component, on BP_Player)
- Variables: `Tuning` (DA_Tuning), `Carried: int`, `Delivered: int`, `BaseWalkSpeed: float`.
- Dispatcher: `OnFuelChanged(Carried, Delivered, Needed)`; `Needed` = `Chapter_FuelToWin`.
- `PickUpFuel()`: Carried += 1, MaxWalkSpeed = BaseWalkSpeed x `Fuel_CarrySpeedMultiplier`, add `State.CarryingFuel` to the owner's `GameplayTags`, call `OnFuelChanged`.
- `DeliverToCore()`: find the actor tagged `Target.EmberCore` through `BPI_Tagged` (no cast, no name), call `BPI_FuelReceiver.ReceiveFuel(1)`, Carried -= 1, Delivered += 1, restore speed, remove `State.CarryingFuel`, call `OnFuelChanged`.

## BP_FuelPickup (Actor)
- StaticMesh placeholder + sphere collision. `GameplayTags` = `Item.Fuel`.
- Implements `BPI_Tagged` (returns `GameplayTags`) and `BPI_Interactable.Interact(Interactor)`: finds `BPC_FuelCarrier` on the Interactor, calls `PickUpFuel()`, destroys itself. Ignored if the player already carries fuel.
- `Fuel_PickupCount` (8) pickups are placed in the connected floor area of `L_Chapter1` (team-unreal R10).

## WBP_HUD (Widget, listens only)
| Element | Source |
|---|---|
| Health bar | `OnHealthChanged` (BPC_Health) |
| Ammo `InMag / Reserve` | `OnAmmoChanged` (BPC_Weapon) |
| Core heat bar | `OnHeatChanged` (BPC_Ember) |
| Fuel `Delivered / Needed` | `OnFuelChanged` (BPC_FuelCarrier) |
| Wave `WaveIndex / WaveCount` | `OnWaveStarted` (BP_FrostSpawner) |
- Bind on Construct after finding each owner by gameplay tag and checking it is valid (team-unreal R5). A missing target leaves that element empty, no error.

## WBP_EndScreen (Widget)
- Text from `OnChapterEnded(bWon)`: "The fire lives" / "The fire went out".
- Retry button: `Get Actor Of Class(BP_ChapterDirector)` -> `RetryChapter()` (technical_design 4.2b).
- Nebil sets `BP_ChapterDirector.EndScreenClass` to this widget; input mode and cursor are handled by the director (team-unreal R4).

## Tuning fields used
`Fuel_CarrySpeedMultiplier` (0.7), `Fuel_PickupCount` (8), `Chapter_FuelToWin` (5).
