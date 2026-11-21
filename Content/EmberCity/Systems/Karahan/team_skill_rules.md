# Rules from Karahan for the team skills (B1)

For Nebil to merge into `.claude/skills/` (shared files are Nebil's). Source: Karahan's midterm "Power Failure" (`scan_report.md`, finding ids in brackets).
Suggested target: `team-unreal` R11-R13 and a new `team-ui` skill (R1-R2).

### team-unreal · R11 · Stop PIE before any asset edit or build script `[Karahan]`
- **Rule:** never create, delete or overwrite assets while Play-In-Editor runs. Stop PIE, run the script, then start PIE again.
- **Why:** an "Overwrite existing object" window froze every MCP call, and a PC crash happened when PIE started during a long script (F05, F06).
- **Check:** the script log shows the asset saved; no modal window is open in the editor.

### team-unreal · R12 · After a visual change, take a screenshot and zoom before saying done `[Karahan]`
- **Rule:** after every look change (HUD, mesh, material, pose) capture the game view and zoom into the changed part. "Done" needs the picture.
- **Why:** the AI tuned hand angles for hours and said "done" while the template hand had no fingers, so no pose could work (F01).
- **Check:** the report names the screenshot file and what was seen in the zoom.

### team-unreal · R13 · Reset player state on respawn and retry `[Karahan]`
- **Rule:** when the player respawns or the level retries, reset every flag the earlier state changed (hiding, carrying, input mode, collision, movement mode, camera roll).
- **Why:** a respawn while hiding left `bHiding = true`, collision off and movement None, so the player walked around "inside" the object (F15).
- **Check:** in PIE die or retry while the state is on (e.g. while carrying fuel); movement and collision work after the respawn and `State.CarryingFuel` is gone.

### team-ui · R1 · Colors, fonts and texts come from one source `[Karahan]`
- **Rule:** every HUD and end-screen color, font and string comes from one file (`docs/` design note or a Data Asset); prompts say "from that file only".
- **Why:** the AI invented colors and fonts when no source of truth existed (F10).
- **Check:** change one color in the source; HUD and end screen both change without opening a widget.

### team-ui · R2 · A widget is only done when it is visible and its buttons fire `[Karahan]`
- **Rule:** create the widget, add it to the viewport, and capture the game view to prove it shows. Bind button events with `create_component_bound_event` and test them by calling `on_clicked.broadcast()` from a script, then by one real click.
- **Why:** widgets were created but not visible, and delegate-bound buttons did nothing (F11).
- **Check:** screenshot shows the widget; the broadcast test logs the expected result (e.g. Retry reloads the level).
