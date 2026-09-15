# Suno — Manual Workflow (no API exists)

Suno has **no official public API** as of August 2026 — only a partner-program
intake form (announced July 2026), with no self-serve keys or docs. Every
third-party "Suno API" is an unofficial wrapper that violates Suno's Terms of
Service, so we don't use any of them. This step is done by hand, in the
browser. It takes about 10 minutes per episode.

## What you need before you start

- The episode file, e.g. `characters/001-testosterone.md`
- Inside it, **Section C — SUNO PRODUCTION BRIEF**. It contains everything
  Suno needs: song title, style tags, the 50-second lyrics, the optional
  YouTube extra verse, and negative style notes.
- A **paid Suno plan (Pro or Premier)** — see "Commercial rights" below.

## Steps

1. Open [suno.com](https://suno.com) and log in.
2. Click **Create**, and switch to **Custom** mode (so you can paste your own
   lyrics instead of letting Suno write them).
3. Open the episode file and find **Section C**.
4. Copy the **Lyrics — 50-second cut** block (everything inside the code
   fence, including the `[Verse 1]` / `[Chorus]` labels — Suno reads those)
   and paste it into Suno's **Lyrics** box.
5. Copy the **Style tags** line and paste it into Suno's **Style of Music**
   box.
6. Copy the **Song title** into the **Title** box.
7. Look at the brief's **Negative style notes**. If your Suno plan shows an
   "Exclude styles" box, paste them there; otherwise just keep them in mind
   when judging the takes.
8. Click **Create**. Suno generates two takes per click.
9. Listen to the takes. Generate a few more batches if nothing lands (this is
   normal — expect to pick from 6–10 takes). Judge against the negative style
   notes: if it drifted into anything the brief says "no" to, skip that take.
10. **Pick ONE take.** That take is now the locked song for the episode.
11. On the winning take, click **Share** and **copy the share URL**. Also
    download the MP3 (menu on the song → Download → Audio) — Atlabs can take
    either.
12. Paste the share URL into the episode's Section I checklist (or just tell
    Claude the URL) so it's on record.

### For the YouTube long cut

The brief includes an **optional extra verse block** (Verse 3 + bridge). Two
ways to get the long version:

- **Easiest:** Use Suno's **Extend** on your winning take, and paste the extra
  verse block as the lyrics for the extension. Then use **Get Whole Song** to
  merge it.
- **Alternative:** Re-run Custom mode with the full lyrics (50s lyrics + extra
  verse inserted before the final chorus, as the brief instructs) — but the
  song may come out sounding different from the short cut, so Extend is
  preferred.

## Commercial rights — read this part

- Commercial use of Suno songs requires a **paid plan (Pro or Premier)**.
  Songs made on the free tier are non-commercial. Make the episode songs while
  subscribed.
- Suno's licensing terms changed in 2026 following its deal with Warner
  Music. **Recheck Suno's current terms before each commercial release** —
  don't assume last month's terms still apply.
- The thing to watch for automation: Suno's **official partner program**
  (intake form announced July 2026). If Suno grants partner API access, this
  whole step can be automated. Until then, nothing gets built.
