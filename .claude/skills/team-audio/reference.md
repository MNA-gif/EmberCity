# team-audio · reference numbers

| What | Value | Where |
|---|---|---|
| Near attenuation | inner 300 cm, falloff 1500 cm | `Audio/Core/ATT_SFX_Near` |
| Far attenuation | inner 600 cm, falloff 3500 cm | `Audio/Core/ATT_SFX_Far` |
| Repeat concurrency | max 4 voices, stop oldest | `Audio/Core/SCON_Repeat` |
| Repeated SFX pitch | 0.92 – 1.08 | Random Float in Range |
| Repeated SFX max length / volume | 0.4 s / 0.5 | asset |
| Music crossfade | 2.0 s fade in + 2.0 s fade out | `BP_MusicDirector` |
| Danger check | every 0.5 s, Frost alive within `Audio_DangerRadius` (2500 cm) | `DA_Tuning` |
| Default volumes | Master 1.0 · Music 0.7 · SFX 0.8 | `BP_AudioSave` slot `AudioSettings` |
| Sound classes | `SC_Master` ← `SC_Music`, `SC_SFX` | `Audio/Core/` |
