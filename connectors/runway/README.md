# Runway — Connect the Official MCP Server (no code needed)

Runway has an **official** remote MCP server: `https://mcp.runwayml.com/mcp`.
Once connected, Claude can generate the episode's cinematic insert shots
(Section G of the episode file) directly — no API key, no custom code. It
signs you in with OAuth and **bills your existing Runway plan's credits**.

In the pipeline, Runway is optional: **1–2 insert shots per episode, never the
whole episode**, generated last and matched to the locked Atlabs cast.

## What you need

- A Runway account on a paid plan (the MCP uses your plan's credits).
- That's it. No API key.

## Option 1 — Connect it in claude.ai (recommended)

This makes Runway available in your normal Claude chats.

1. Go to [claude.ai](https://claude.ai) and log in.
2. Click your initials (bottom-left) → **Settings**.
3. Click **Connectors**.
4. Click **Add custom connector**.
5. Fill in:
   - **Name:** `Runway`
   - **URL:** `https://mcp.runwayml.com/mcp`
6. Click **Add**.
7. Click **Connect** next to the new Runway connector. A Runway login window
   opens — sign in with your normal Runway account and approve.
8. Done. In any chat, you can now say things like *"Generate insert shot 1
   from episode 001, Section G, using Runway"* and Claude will do it.

## Option 2 — Connect it in Claude Code (the terminal)

Only needed if you also want it in Claude Code sessions.

1. Open a terminal where Claude Code is installed.
2. Run this one command:

   ```
   claude mcp add --transport http runway https://mcp.runwayml.com/mcp
   ```

3. Start Claude Code (`claude`), type `/mcp`, pick **runway**, and follow the
   login prompt (it opens the same Runway sign-in in your browser).
4. Done.

## Notes

- Generations spend your Runway credits exactly as if you'd made them on
  runwayml.com — check your plan's balance if something won't generate.
- If you ever want to disconnect: Settings → Connectors → Runway → remove
  (claude.ai), or `claude mcp remove runway` (Claude Code).
- Runway also has a full developer API (docs.dev.runwayml.com), but we don't
  need it — the official MCP covers the insert-shot use case with zero code.
