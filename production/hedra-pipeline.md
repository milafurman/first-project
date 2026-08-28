# PRODUCTION PIPELINE — HEDRA

The series animates in **Hedra** (Character-3, omnimodal: image + audio + text). This doc is
the standing workflow every episode follows from locked script to posted video. Episode files
carry their own HEDRA SHOT PACK section conforming to these rules.

## Why Hedra fits this series

- Character-3 animates **any illustrated portrait** — including storybook/painted character
  art — with audio-driven lip-sync, blinks, micro-expressions, and body motion. Our characters
  are storybook illustrations by design, so the input is exactly what the model wants.
- **Character consistency comes from the input image, not the model.** One canonical portrait
  per character, reused every episode, is the entire consistency strategy. Sir Osterone in
  Episode 40 is the same PNG as Episode 1.
- Long-form Character-3 supports videos up to ~10 minutes — the YouTube versions (6–7 min)
  fit inside a single performance generation when needed, though we cut per-shot anyway.

## THE PIPELINE (per episode)

1. **Script locks** in `characters/NNN-*.md` (already the repo convention).
2. **Voice records** — one audio file per shot, named `NNN-S##-character.wav`. Narrator + each
   character get distinct, locked voices (same voice every episode — voice consistency is as
   canon as the portrait). Record in Descript or any VO tool; Descript AI voices are the
   fallback for drafts.
3. **Hedra generates PERFORMANCE shots** — canonical portrait + that shot's audio + a one-line
   motion/emotion prompt. Output per shot, 9:16 for the short, 16:9 for the long version.
4. **SCENE shots** (no speaking character: mist rolling, dragons circling, castle establishing)
   are generated as short video/b-roll — Hedra's video generation where it serves, otherwise
   AI/stock b-roll assembled in Descript. Scene shots obey the series bible: metaphor only,
   never anatomy.
5. **Assembly in Descript** — cut performance + scene shots to the script's timing beats, add
   captions (burned-in for TikTok/Reels), music, sound design, and the logo beat (wax-seal
   stamp + series title card).
6. **Publish** — Blotato/Metricool push to TikTok, Instagram, Meta, YouTube on schedule.

Claude's role per episode: everything in steps 1 is authored here; for steps 3–4 the episode's
HEDRA SHOT PACK provides copy-paste-ready prompts and the audio-file manifest. Hedra itself is
operated in Hedra Studio (no direct connector in this workspace); Descript and Blotato can be
driven from here.

## CHARACTER SHEETS (canonical portraits)

One portrait per character, generated once, stored in `production/character-sheets/` when
approved, and NEVER regenerated casually — a new portrait is a canon change.

**Series style token (prepend to every character-image prompt):**
> "storybook fairy-tale illustration, painterly oil texture, rich warm palette, expressive
> exaggerated character design in the spirit of classic animated fairy-tale films, portrait
> orientation, character centered, chest-up, looking near camera, no text, no watermark"

**Portraits needed now (Episodes 001–002):**

| Character | Portrait prompt (after style token) |
|---|---|
| Sir Osterone | weathered blacksmith knight, soot-streaked armor over a leather forge apron, warm forge-glow rim light, heavy hammer over shoulder, gruff kind eyes, short iron-grey beard |
| Queen Meridia | regal queen in her prime, commanding posture on a throne edge, deep crimson and gold, crown worn like she earned it, amused unimpressed expression |
| The Fade | translucent grey mist coalescing into a faceless tax-collector silhouette with a ledger, cold desaturated palette (SCENE character — rarely speaks) |
| Sir Reta | slick young knight, three wax seals across his chest plate, insufferable smirk, immaculate hair, lounging confidence |
| Princess Bella | princess with tired but defiant eyes, beautiful, hand resting on a laden banquet table she is not looking at |
| Marrow the Kitchen Witch | magnificent older kitchen witch, sleeves rolled, ladle like a scepter, surrounded by potion-steam, zero patience, total warmth |
| The Three Dragons | three-dragon group scene: sleek whisper-dragon coiled on a tower (Craving), fat smug dragon on a grain hoard (the Hoard), grey ember-cold dragon in a basement boiler room (the Cold Furnace) — SCENE characters |

Villain rule on screen: The Fade and the dragons are *processes* — they read as weather,
appetite, and cold, not as monsters with relatable faces. Keep them beautiful and unsettling;
never cute enough to root for.

## SHOT TYPES (used by every episode's shot pack)

- **PERFORMANCE** — a character speaks or reacts on camera. Hedra Character-3: portrait +
  audio + motion prompt. This is the backbone of every episode.
- **SCENE** — metaphor visuals, no lip-sync (mist over shoulders, dragons circling the
  waistline silhouette, forge relighting). Series-bible enforcement lives here: no anatomy,
  no diagrams, ever.
- **CARD** — title card, thesis line, logo beat. Static or minimal motion; built in
  Descript/Canva, not Hedra.

## FORMATS

- Short (TikTok/Reels/Shorts): 9:16, under 50s, burned-in captions, hook in frame one.
- Long (YouTube): 16:9, cut per the five-act outline; performance shots may run long takes
  (monologues are single Hedra generations for continuity of performance).
- Audio: 48kHz WAV masters; music ducked under VO; the whisper-dragon's "Cake. Cake. Cake."
  is a sound-design motif, keep it identical across episodes (audio branding).
