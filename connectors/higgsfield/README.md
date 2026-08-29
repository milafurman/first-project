# Higgsfield — Connect the Official MCP Server (no code needed)

Higgsfield has an **official** remote MCP server: `https://mcp.higgsfield.ai`.
Once connected, Claude can generate the episode's cinematic insert shots
(Section G of the episode file) directly — no API key, no custom code. It
signs you in with OAuth using your Higgsfield account.

In the pipeline, Higgsfield is optional and interchangeable with Runway:
**1–2 insert shots per episode, never the whole episode**, generated last and
matched to the locked Atlabs cast. Higgsfield's specialty is dramatic camera
moves (crash zooms, crane shots, bullet-time), so pick it when Section G calls
for a flashy camera move.

## What you need

- A Higgsfield account (a paid plan for anything you'll publish).
- That's it. No API key.

## Option 1 — Connect it in claude.ai (recommended)

This makes Higgsfield available in your normal Claude chats.

1. Go to [claude.ai](https://claude.ai) and log in.
2. Click your initials (bottom-left) → **Settings**.
3. Click **Connectors**.
4. Click **Add custom connector**.
5. Fill in:
   - **Name:** `Higgsfield`
   - **URL:** `https://mcp.higgsfield.ai`
6. Click **Add**.
7. Click **Connect** next to the new Higgsfield connector. A Higgsfield login
   window opens — sign in with your normal account and approve.
8. Done. In any chat, you can now say things like *"Generate insert shot 2
   from episode 002, Section G, using Higgsfield"* and Claude will do it.

## Option 2 — Connect it in Claude Code (the terminal)

Only needed if you also want it in Claude Code sessions.

1. Open a terminal where Claude Code is installed.
2. Run this one command:

   ```
   claude mcp add --transport http higgsfield https://mcp.higgsfield.ai
   ```

3. Start Claude Code (`claude`), type `/mcp`, pick **higgsfield**, and follow
   the login prompt (it opens the same Higgsfield sign-in in your browser).
4. Done.

## Notes

- Generations use your Higgsfield account/plan the same as making them on the
  website.
- If you ever want to disconnect: Settings → Connectors → Higgsfield → remove
  (claude.ai), or `claude mcp remove higgsfield` (Claude Code).
- Higgsfield also has a full developer API (docs.higgsfield.ai), but we don't
  need it — the official MCP covers the insert-shot use case with zero code.
