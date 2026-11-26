---
name: team-audio
description: How the Ember City team adds sound and music in Unreal 5.8 - SFX_/MUS_/AMB_ names under Content/EmberCity/Audio, sounds started from gameplay events (never Tick), attenuation radius numbers for 3D sounds, concurrency limits, small random pitch, Sound Classes Master/Music/SFX with saved volume sliders, explore/danger music crossfade, CC0 or Starter Content only with credits.md. Use whenever anyone on the team adds, replaces, balances or debugs a sound, music, ambience or volume setting, or says "ses ekle", "müzik", "ses gelmiyor", "ses çok yüksek", "ses ayarı", "danger müziği".
---

# Team audio · Ember City

Merged by the integration owner (Nebil). Each rule says who brought it. Numbers live in `reference.md` next to this file.

### R1 · Names and folders `[Nebil]`
- **Rule:** sound effects `SFX_<System>_<What>`, music `MUS_<State>`, ambience `AMB_<Place>`; source WAVs and assets in `Content/EmberCity/Audio/{SFX,MUS,AMB}/<YourName>/`; Sound Classes, Sound Mix and attenuation in `Content/EmberCity/Audio/Core/` (owner Nebil).
- **Why:** four people add sounds in parallel; one naming scheme makes it obvious who owns a file and stops two members from editing the same asset.
- **Check:** `find Content/EmberCity/Audio -name "*.uasset"` lists only `SFX_`, `MUS_`, `AMB_`, `SC_`, `SM_`, `ATT_`, `SCON_` names.

### R2 · Sounds start from events, never Tick `[Nebil]`
- **Rule:** play a sound on the gameplay event that causes it (fire, hit, pickup, wave start, `OnChapterEnded`), or on a timer of at least 0.25 s for a state check (music). No Play Sound node is reachable from Event Tick.
- **Why:** a sound from Tick restarts every frame (a buzzing loop) and wastes voices; the event already exists in our Contracts.
- **Check:** in each Blueprint you touched, follow Event Tick: no `PlaySound*`, `SpawnSound*` or `SetSoundMix*` node on that path.

### R3 · Every 3D sound uses a shared attenuation `[Nebil]`
- **Rule:** world sounds use `ATT_SFX_Near` (inner 300 cm, falloff 1500 cm) or `ATT_SFX_Far` (inner 600 cm, falloff 3500 cm). UI, stingers and music are 2D. Never leave Attenuation empty on a 3D sound.
- **Why:** without attenuation an enemy shot across the map is as loud as your own gun; with one asset the team can retune all distances at once.
- **Check:** play the sound 3000 cm away in PIE: `ATT_SFX_Near` sounds are not heard; `au.DumpActiveSounds` shows the attenuation name.

### R4 · Concurrency limit on repeated sounds `[Nebil]`
- **Rule:** any sound that can fire more than twice a second (shots, hits, steps) uses `SCON_Repeat` (max 4 voices, stop oldest) and is shorter than 0.4 s.
- **Why:** 8 Frost shooting at once stacked 30+ voices into noise and pushed out the music.
- **Check:** during a full wave, `au.DumpActiveSounds` shows at most 4 instances of any one `SFX_` sound.

### R5 · Small random pitch on repeated SFX `[Nebil]`
- **Rule:** repeated one-shots play with pitch 0.92–1.08 (Random Float in Range into Pitch Multiplier) and volume ≤ 0.5; one-off stingers keep pitch 1.0.
- **Why:** the same sample at the same pitch sounds like a machine gun even when it is one pistol; ±8 % is enough to hide it.
- **Check:** fire 5 shots in a row: each shot sounds slightly different, none clips.

### R6 · Every sound has a Sound Class: Master / Music / SFX `[Nebil]`
- **Rule:** `SC_Music` and `SC_SFX` are children of `SC_Master`. Every `MUS_`/`AMB_` asset uses `SC_Music`, every `SFX_` uses `SC_SFX`. Volumes are changed only through `SM_Volumes` (Set Sound Mix Class Override), never by editing an asset's volume at runtime.
- **Why:** the three settings sliders only work if every sound is in one of the classes; a sound without a class ignores the sliders.
- **Check:** set the SFX slider to 0 in the pause menu: every gunshot is silent and the music still plays.

### R7 · Two music states with a 2 s crossfade `[Nebil]`
- **Rule:** `BP_MusicDirector` (one per level) plays `MUS_Explore` and `MUS_Danger` on two Audio Components and crossfades with Fade In / Fade Out of 2.0 s. Danger = at least one Frost alive and within `Audio_DangerRadius` of the player, checked on a 0.5 s timer. Both loops start at volume 0 and fade in (no hard start).
- **Why:** a hard cut between tracks is the first thing a player notices; a timer keeps it out of Tick (R2).
- **Check:** in PIE, a Frost walks into range: within ~0.5 s both tracks are heard for 2 s, then only danger; kill it: back to explore the same way.

### R8 · Volume settings are saved and loaded `[Nebil]`
- **Rule:** the pause menu has Master, Music, SFX sliders (0–1). On change: apply to `SM_Volumes` and save `BP_AudioSave` (slot `AudioSettings`, user 0). On level start: load the slot (create it with 1.0 / 0.7 / 0.8 if missing) and apply before the music starts.
- **Why:** the brief requires that values survive a restart; applying before the music starts avoids one loud second at full volume.
- **Check:** set Music to 0.2, quit PIE, start again: the slider shows 0.2 and the music is quiet from the first frame.

### R9 · Only CC0 or Starter Content, listed the same day `[Nebil]`
- **Rule:** use real recordings from CC0 sources (Kenney, OpenGameArt CC0, freesound CC0) or Unreal Starter Content. Ask the team owner before each download (name, source, licence, size). Add file, source URL and licence to `credits.md` in the same commit as the sound.
- **Why:** course rule; and in Nebil's midterm synthesized beeps were rejected as "çok yapay" (too artificial).
- **Check:** every `SFX_`/`MUS_`/`AMB_` asset name appears in `credits.md`; `git show --stat` of the commit lists `credits.md`.

### R10 · Prove it with a dump, then a human listens `[Nebil]`
- **Rule:** after wiring a sound, trigger its event in PIE and run `au.DumpActiveSounds` within a few frames; then a team member listens once. Before automated tests start the editor with `-ini:Engine:[Audio]:UnfocusedVolumeMultiplier=1.0` (only on the command line, not in ini files).
- **Why:** an unfocused editor plays every sound at volume 0, so working sounds look broken; only an ear can judge the mix.
- **Check:** the dump shows the `SFX_` name; the PROGRESS.md entry says who listened.

## From the team (to be merged)
<!-- Add audio rules you learned as R11+ with your name. -->
