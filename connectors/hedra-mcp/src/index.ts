#!/usr/bin/env node
/**
 * hedra-mcp — MCP server for Hedra's official public API.
 *
 * Hedra is the FALLBACK animator for "The Body Is a Fairy Tale" (the locked
 * pipeline uses Atlabs). This server exposes just the pieces the pipeline
 * needs: turn a character image + a song/voice audio file into an animated
 * character video, and poll until it's done.
 *
 * Auth: HEDRA_API_KEY environment variable only. Never hardcode a key here.
 * Requires accepting Hedra's API terms at hedra.com/api-profile and a paid
 * Hedra subscription (API usage shares the Studio credit balance).
 *
 * Endpoint paths follow Hedra's public API docs (hedra.com/docs). If Hedra
 * revs their API, update BASE_URL / paths below to match the current docs.
 */

import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";

const BASE_URL = process.env.HEDRA_BASE_URL ?? "https://api.hedra.com/web-app/public";

const MISSING_KEY_MESSAGE =
  "HEDRA_API_KEY is not set, so I can't call Hedra. To fix: get an API key at " +
  "hedra.com/api-profile (you must accept the API terms and have a paid Hedra " +
  "subscription), then add HEDRA_API_KEY to this MCP server's environment — see " +
  "connectors/hedra-mcp/README.md, Setup step 4. No video was generated.";

function apiKey(): string | undefined {
  const key = process.env.HEDRA_API_KEY?.trim();
  return key ? key : undefined;
}

type ToolResult = {
  content: { type: "text"; text: string }[];
  isError?: boolean;
};

function text(message: string, isError = false): ToolResult {
  return { content: [{ type: "text", text: message }], isError: isError || undefined };
}

async function hedraFetch(path: string, init: RequestInit = {}): Promise<unknown> {
  const key = apiKey();
  if (!key) throw new Error(MISSING_KEY_MESSAGE);
  const headers = new Headers(init.headers);
  headers.set("X-API-Key", key);
  if (init.body && typeof init.body === "string") {
    headers.set("Content-Type", "application/json");
  }
  const response = await fetch(`${BASE_URL}${path}`, { ...init, headers });
  const raw = await response.text();
  if (!response.ok) {
    throw new Error(`Hedra API ${response.status} on ${path}: ${raw.slice(0, 500)}`);
  }
  try {
    return raw ? JSON.parse(raw) : {};
  } catch {
    return { raw };
  }
}

/** Download a file from a URL and upload it to Hedra as an asset; returns the asset id. */
async function uploadAssetFromUrl(
  url: string,
  type: "image" | "audio",
  name: string
): Promise<string> {
  const download = await fetch(url);
  if (!download.ok) {
    throw new Error(`Could not download ${type} from ${url} (HTTP ${download.status})`);
  }
  const bytes = await download.arrayBuffer();

  const created = (await hedraFetch("/assets", {
    method: "POST",
    body: JSON.stringify({ name, type }),
  })) as { id?: string };
  if (!created.id) {
    throw new Error(`Hedra asset creation returned no id: ${JSON.stringify(created)}`);
  }

  const form = new FormData();
  const filename = name + (type === "image" ? ".png" : ".mp3");
  form.append("file", new Blob([bytes]), filename);
  const key = apiKey()!;
  const upload = await fetch(`${BASE_URL}/assets/${created.id}/upload`, {
    method: "POST",
    headers: { "X-API-Key": key },
    body: form,
  });
  if (!upload.ok) {
    throw new Error(`Hedra asset upload failed (HTTP ${upload.status}): ${(await upload.text()).slice(0, 500)}`);
  }
  return created.id;
}

const server = new McpServer({ name: "hedra-mcp", version: "0.1.0" });

server.tool(
  "generate_character_video",
  "Generate an animated character video with Hedra: a character image (URL) speaks/sings the " +
    "given audio (URL), guided by a text prompt. Returns a generation id — poll it with " +
    "get_generation_status. Uses the paid Hedra credit balance.",
  {
    image_url: z.string().url().describe("URL of the character image (the locked cast portrait)"),
    audio_url: z.string().url().describe("URL of the audio the character performs (e.g. the Suno MP3 or a voice line)"),
    prompt: z.string().describe("Text prompt describing the performance/scene, matched to the locked cast"),
    aspect_ratio: z.enum(["9:16", "16:9", "1:1"]).default("9:16")
      .describe("9:16 for TikTok/Reels/Shorts, 16:9 for YouTube"),
    resolution: z.enum(["540p", "720p"]).default("720p"),
  },
  async ({ image_url, audio_url, prompt, aspect_ratio, resolution }) => {
    if (!apiKey()) return text(MISSING_KEY_MESSAGE, true);
    try {
      const stamp = Date.now().toString(36);
      const imageId = await uploadAssetFromUrl(image_url, "image", `character-${stamp}`);
      const audioId = await uploadAssetFromUrl(audio_url, "audio", `audio-${stamp}`);
      const generation = (await hedraFetch("/generations", {
        method: "POST",
        body: JSON.stringify({
          type: "video",
          start_keyframe_id: imageId,
          audio_id: audioId,
          generated_video_inputs: {
            text_prompt: prompt,
            aspect_ratio,
            resolution,
          },
        }),
      })) as { id?: string; asset_id?: string };
      return text(
        `Generation started.\n` +
          `generation_id: ${generation.id ?? "(missing — raw: " + JSON.stringify(generation) + ")"}\n` +
          `Poll it with get_generation_status. Video generation typically takes a few minutes.`
      );
    } catch (error) {
      return text(error instanceof Error ? error.message : String(error), true);
    }
  }
);

server.tool(
  "get_generation_status",
  "Check the status of a Hedra generation started with generate_character_video. " +
    "When complete, the response includes the video download URL.",
  {
    generation_id: z.string().describe("The generation id returned by generate_character_video"),
  },
  async ({ generation_id }) => {
    if (!apiKey()) return text(MISSING_KEY_MESSAGE, true);
    try {
      const status = await hedraFetch(`/generations/${encodeURIComponent(generation_id)}/status`);
      return text(JSON.stringify(status, null, 2));
    } catch (error) {
      return text(error instanceof Error ? error.message : String(error), true);
    }
  }
);

async function main() {
  if (!apiKey()) {
    // Start anyway so the client sees the tools; each tool answers with setup
    // guidance instead of crashing the whole server on a missing key.
    console.error("hedra-mcp: HEDRA_API_KEY is not set — tools will return setup instructions.");
  }
  const transport = new StdioServerTransport();
  await server.connect(transport);
  console.error("hedra-mcp: ready on stdio");
}

main().catch((error) => {
  console.error("hedra-mcp failed to start:", error);
  process.exit(1);
});
