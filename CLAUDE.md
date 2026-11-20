# Ember City · Agent front door (CLAUDE.md)

> Claude reads this file automatically. For Codex, copy it as `AGENTS.md`. Keep it SHORT; details live in the files below.

## Read first (every session)
- `docs/PROGRESS.md` (newest on top: what was done, what is next)
- `docs/technical_design.md` (systems, owners, **Contracts**, `DA_Tuning` fields)
- Team skills in `.claude/skills/` (team-rules, team-unreal, team-build) open by themselves when they match

Start every session by saying in 2 lines what was done last and what is next for the person you are working with, then wait for their go.

## Who is who
Team: Nebil (integration owner), Emrecan, Kartal, Karahan. Ask the user's name at the start of a session if it is not clear; work only in **their** folder `Content/EmberCity/Systems/<Name>/` and their test map `Content/EmberCity/Maps/Test/L_Test_<Name>`.

## Rules
- Answer the user in Turkish; code, asset names, commit messages and docs stay in English.
- Never edit another member's Blueprint or folder. Shared files (`Core/`, `Config/`, `L_Chapter1`, `BP_Player`) only by their owner (see technical_design.md).
- Systems talk only through the Contracts (interfaces, dispatchers, gameplay tags). A new contract = change technical_design.md first, then code.
- No gameplay number inside a Blueprint: read it from `DA_Tuning` through the `Tuning` variable.
- The HUD only listens.
- One step at a time. After a step works in PIE: say what was tested, then tell the user to commit with `[Name] area: what changed`.
- At the end of a session: add 3 lines on top of `docs/PROGRESS.md` (Done / Next / Problems).
- Ask before every download (name, source, licence, size) and before closing the editor; never delete permanently.
- Never put passwords, API keys, tokens or Claude session logs into the repo.

## Editor tools
Unreal MCP (`.mcp.json`, `http://127.0.0.1:8000/mcp`). If calls fail with ECONNREFUSED: in the editor console run `ModelContextProtocol.StartServer`. The project enables the plugins ModelContextProtocol, EditorToolset, MCPClientToolset and VibeUE; a member without VibeUE can disable it in Edit → Plugins.
