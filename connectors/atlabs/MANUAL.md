# Atlabs — Manual Workflow (no public API yet)

Atlabs is where the episode becomes a finished animated music video. As of
August 2026 there are **no public developer docs, no developer portal, and no
API reference** for Atlabs — "API access" shows up only in third-party feature
listings. So we build nothing yet; this step is done by hand in the Atlabs app.

## What you need before you start

- The locked Suno song: the **share URL or the downloaded MP3** from the Suno
  step ([../suno/MANUAL.md](../suno/MANUAL.md)).
- The episode file, e.g. `characters/001-testosterone.md`, open to:
  - **Section A — Character bible** (the Cast)
  - **Section B — Visual style lock**
  - **Section D — Atlabs music-video brief** (scene list, cast mapping,
    caption/karaoke notes, reframe notes)

## Steps

1. Log in to Atlabs and start a new **Music Video** project.
2. **Paste the Suno share URL** (or upload the MP3) as the project's audio.
   The song is the spine — everything is timed to it.
3. **Build the Cast before generating anything.** For each character in the
   episode's **Section A**, create a Cast character card and paste in that
   character's full description: name, personality, age look, body type,
   wardrobe, signature color, face notes, and the "what never changes" line.
   The "what never changes" line is the most important — it's what keeps the
   character consistent shot to shot.
4. Apply the **Section B visual style lock** as the project's style setting,
   word for word. Don't improvise style — it's locked for the whole series.
5. **Lock the Cast.** Do not let Atlabs invent new characters or redesign
   yours. Every scene uses the cards you just made (Section D's "Cast
   mapping" table says exactly which characters appear in which scene).
6. **Generate the 9:16 SHORT CUT first** (TikTok / Reels / Shorts):
   - Set the aspect ratio to **9:16** and follow Section D's reframe notes
     (which scenes center-punch, which re-stage vertically, keep captions out
     of the bottom 15%).
   - Build the scenes from Section D's timed scene list — each row gives the
     seconds, who's on screen, the action, the camera move, and the caption
     line.
   - Captions: follow Section D's caption/karaoke notes (storybook serif,
     bottom third, chorus lines karaoke-style in the compound's signature
     color).
   - The short cut must land **under 50 seconds**.
7. Review the short cut. Redo any scene where a character drifted off-model
   (check against the "what never changes" line) before moving on.
8. **Then generate the 16:9 YouTube cut from the SAME Cast** — same project,
   same character cards, do not rebuild them. Use the long version of the song
   (with the extra verse) and add Section F's extra scenes and the compound
   character's monologue. Master in 16:9 per Section D.
9. If the episode has insert shots (Section G), those come from Runway or
   Higgsfield **after** the Atlabs cuts exist, matched to the locked Cast —
   see [../runway/README.md](../runway/README.md) and
   [../higgsfield/README.md](../higgsfield/README.md).
10. Export both cuts and check off Section I.

## The future-automation unlock

The single thing that would let Claude automate this step: **official API
access from Atlabs**. Email Atlabs support/sales, say you produce a recurring
animated music-video series with a locked recurring cast, and ask whether API
or programmatic access exists or is planned. If they ever say yes and provide
docs, we build a proper connector then — not before.
