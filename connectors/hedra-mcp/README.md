# Hedra MCP Server (fallback animator — optional)

Hedra is **not** part of the locked pipeline (Atlabs is the animator). This is
a backup: if Atlabs ever falls through, Hedra has an official self-serve API,
and this little server lets Claude drive it — take a character image + an
audio file (like the Suno song) and get back an animated character video.

It exposes two tools to Claude:

- `generate_character_video(image_url, audio_url, prompt, aspect_ratio, resolution)`
- `get_generation_status(generation_id)`

You only need to set this up if/when you actually want to use Hedra.

## What you need first

1. A **paid Hedra subscription** (API generations spend the same credit
   balance as Hedra Studio).
2. An **API key**: go to [hedra.com/api-profile](https://hedra.com/api-profile),
   accept the API terms, and copy your key. Treat the key like a password —
   never paste it into a file in this repo.
3. **Node.js** installed on your computer (version 18 or newer). Check with
   `node --version` in a terminal; install from [nodejs.org](https://nodejs.org)
   if that fails.

## Setup (one time)

1. Open a terminal.
2. Go to this folder:

   ```
   cd path/to/first-project/connectors/hedra-mcp
   ```

3. Install and build (two commands):

   ```
   npm install
   npm run build
   ```

4. Add it to Claude Code, with your API key attached (replace
   `YOUR-KEY-HERE` with the real key — this stores it in Claude's local
   config, not in the repo):

   ```
   claude mcp add hedra --env HEDRA_API_KEY=YOUR-KEY-HERE -- node path/to/first-project/connectors/hedra-mcp/dist/index.js
   ```

5. Start Claude Code (`claude`) and type `/mcp` — you should see **hedra**
   listed. Done.

If you skip the API key, the server still starts, and the tools reply with
these setup instructions instead of generating anything — nothing crashes.

## Using it

In Claude Code, say something like:

> Use Hedra to generate a 9:16 video of the Prince Charming cast portrait
> singing this audio: [MP3 URL], prompt: [scene description from Section G].

Claude will start the generation and poll `get_generation_status` until the
video URL comes back. Generations take a few minutes and spend Hedra credits.

## Notes

- The API key comes **only** from the `HEDRA_API_KEY` environment variable.
  There is no key anywhere in this repo, and `.gitignore` blocks `.env` files
  from being committed.
- Endpoint paths follow Hedra's public docs at
  [hedra.com/docs](https://www.hedra.com/docs). If Hedra changes their API,
  the paths at the top of `src/index.ts` are the thing to update. Hedra's own
  official SDKs (`hedra-node`, `hedra-python`) and the
  `hedra-labs/hedra-api-starter` repo on GitHub are the reference.
