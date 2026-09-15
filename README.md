# The Body Is a Fairy Tale

A science-education video series where the body is a fairy-tale kingdom and
each episode makes one compound (a peptide, steroid, or supplement) the
storybook hero. Every episode is a music video: Shrek-style humor, PG-13
ceiling, facts accurate and cited.

## Where everything lives

| File / folder | What it is |
|---|---|
| `system-prompt.md` | The series bible — golden rule, tone, format, character rules |
| `production/pipeline.md` | The locked production pipeline (Claude → Suno → Atlabs → optional insert shots) |
| `characters/` | Episode packages (`NNN-<compound>.md`, sections A–I) and the story slate |
| `connectors/` | How each app connects to Claude — status table, manual workflows, OAuth setup |

## Making an episode (short version)

1. Claude writes the episode package into `characters/`.
2. Make the song at suno.com — `connectors/suno/MANUAL.md`.
3. Animate it in Atlabs — `connectors/atlabs/MANUAL.md`.
4. Optional insert shots via Runway or Higgsfield — Claude handles these
   directly once connected (`connectors/runway/`, `connectors/higgsfield/`).
