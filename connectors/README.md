# App Connectors — "The Body Is a Fairy Tale" Pipeline

This folder explains how each app in the production pipeline connects to Claude —
or doesn't (yet). Research verified August 2026.

The pipeline, in order:

**Claude → Suno → Atlabs → (optional) Higgsfield or Runway**

## Status at a glance

| App | What it does in the pipeline | Official API? | Integration path | What Mila does |
|---|---|---|---|---|
| **Suno** | Turns the episode's lyrics + style tags into the song (the song is the spine of every episode) | ❌ No public API — partner program intake only | Manual, in the browser | Follow [suno/MANUAL.md](suno/MANUAL.md) |
| **Atlabs** | Turns the Suno song + locked character Cast into the finished animated music video (9:16 short + 16:9 YouTube cut) | ❌ No public developer docs anywhere | Manual, in the browser | Follow [atlabs/MANUAL.md](atlabs/MANUAL.md) |
| **Runway** | Optional: 1–2 cinematic insert shots, never the whole episode | ✅ Official API **and** official MCP server | Connect the official Runway MCP — no code needed | One-time OAuth setup: [runway/README.md](runway/README.md) |
| **Higgsfield** | Optional: 1–2 cinematic insert shots, never the whole episode | ✅ Official API **and** official MCP server | Connect the official Higgsfield MCP — no code needed | One-time OAuth setup: [higgsfield/README.md](higgsfield/README.md) |
| **Hedra** | Fallback animator (not in the locked pipeline; kept as backup) | ✅ Official self-serve API + SDKs | Optional custom MCP server scaffold in [hedra-mcp/](hedra-mcp/) | Only if Atlabs ever falls through |

## What "connect via OAuth" means (plain English)

For Runway and Higgsfield, both companies run an official "MCP server" — a plug
Claude can connect to directly. You don't need an API key, you don't need any
code. You add the server's web address in your Claude settings, a login window
for that app opens, you sign in, and you're done. It uses the credits on your
existing paid plan for that app.

## The two manual apps

- **Suno** has no official API at all. Every "Suno API" you can find online
  (gcui-art/suno-api, sunoapi.org, musicapi.ai, unofficial MCP packages) is an
  unofficial wrapper or reseller that violates Suno's Terms of Service. We build
  nothing for Suno. Claude prepares the Suno brief; you paste it into suno.com
  by hand. Watch Suno's official **partner program** (announced July 2026) —
  that's the only legit path to automation later.
- **Atlabs** lists "API access" in some third-party feature roundups, but there
  are no public developer docs, no developer portal, and no API reference
  anywhere. We build nothing for Atlabs yet. The unlock: email Atlabs and ask
  about official API access (details in [atlabs/MANUAL.md](atlabs/MANUAL.md)).

## Bottom line for each episode

1. Claude writes the episode package (sections A–I in `characters/NNN-*.md`).
2. You do the **Suno** step by hand (~10 minutes): [suno/MANUAL.md](suno/MANUAL.md).
3. You do the **Atlabs** step by hand: [atlabs/MANUAL.md](atlabs/MANUAL.md).
4. If the episode calls for insert shots, Claude can drive **Runway** or
   **Higgsfield** directly once you've done the one-time connection.
