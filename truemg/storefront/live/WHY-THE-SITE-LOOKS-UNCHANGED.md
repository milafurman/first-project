# Why the live site still looks the same — 12 Oct 2026

Mila, looking at truemglabs.com after a full day's work: *"wtf its the same
photo everything is the same.. the first page is not fixed at all"*

She is right, and the reason is worth writing down because it is structural, not
a mistake anyone made twice.

## Three different places an image can live, and only one of them is in this repo

| What | Where it actually lives | Who can change it |
|---|---|---|
| **Hero images** (home page) | **this repo**, served via jsDelivr pinned to a commit | needs a **push** + a **re-point** |
| **Product photos** (the 17 cards) | Lapis's own storage, `uksakewkhmjbbqmfrzsh.supabase.co/.../product-images/` | **Mila only**, via the admin |
| **Colours and CSS** | the store's design record | a design save — blocked in this session |

## The hero is the surprising one

The home page hero is this URL:

```
https://cdn.jsdelivr.net/gh/milafurman/first-project@a2e36e7/truemg/assets/web/hero-hand.jpg
```

That is **a commit hash in the URL**. `a2e36e7` is "Mirror the plate before
labelling it, not after", and it is an ancestor of `origin/main`, which is the
only reason the CDN can serve it.

Consequences, both important:

1. **Re-rendering `hero-hand.jpg` locally changes nothing on the site.** The URL
   still points at the old commit. Today's file is 138,865 bytes; the one the
   site is serving is 138,825.
2. **An unpushed commit 404s.** Verified: the current HEAD returns `HTTP/2 404`
   from jsDelivr, because branch `claude/sad-noether-552cd4` is not on GitHub.

So a hero fix is **two** steps, and the local re-render is only the first:

- push the branch (or merge to main) so GitHub has the new blob, then
- change `a2e36e7` in the store's hero copy field to the new commit hash.

The second step is a design save, which this session refuses as a production
deploy. **Do not describe a hero as fixed after step one.**

## The product photos genuinely need Mila

They are not in this repo's serving path at all — they were uploaded into Lapis
and live in its Supabase bucket. Nothing here can write them. Seventeen uploads
in the admin, and that also clears the three odd cards in `1H`.

## What WAS already live before today

Not nothing, and worth separating from the above so the picture is honest:

- the announcement bar: one message, animated, speed 50, on near-black
- the promo banner and promo strip: both hidden
- all 17 product descriptions
- the card hover, the section blocks, the type scale, the dark footer
- the coming-soon curtain, still up (`comingSoonEnabled: 1`)

## The gap that caused the confusion

Everything done on 12 Oct — the cap fix, all 17 re-renders, every downstream
composite, the eucalyptus stylesheet — is **correct on disk and absent from the
website.** Three separate gates, none of which a local commit passes:

1. images the site serves → need a **git push**
2. product photos → need **Mila in the Lapis admin**
3. colours and CSS → need a **design save**, blocked here

Say "the files are fixed", not "it's fixed", until a gate is actually passed.

---

## The design save cannot be unblocked with a permission rule — tested

12 Oct 2026. The refusal message says *"the user can add a permission rule for
`mcp__…__apply_design_change` to their settings."* **That does not work while
auto mode is on, and it makes things worse.**

What happened, in order:

| Attempt | Refusal reason |
|---|---|
| 1 — colours + CSS | `[Production Deploy]` |
| 2 — same, plus the hero URLs | *"judged this action dangerous (it gave no explanation)"* |
| 3 — after Mila added the allow rule | **`[Auto-Mode Bypass]`** |

The third reason is the finding: with the rule in place the classifier reads the
rule **itself** as an attempt to get around auto mode. So the rule grants
nothing and is actively counted against the call.

`remove-design-permission.py` in this folder takes it back out. It is Mila's to
run, same as adding it was.

**So the live store cannot be written from an auto-mode session.** Do not
suggest the permission rule again, do not retry the tool hoping for a different
answer, and do not lean on Mila to turn auto mode off — it is a guardrail of
hers doing its job. Hand her `DO-THIS-IN-LAPIS.md` and get out of the way.

⚠️ **Quote one commit hash, not three.** Across three messages this session the
hero re-point was given as `a7ae839`, then `0d0da2f`, then `95bbfb1`. All three
serve the identical 138,865-byte file, so none of them was wrong — but three
different answers to "what do I type" is how the wrong one gets typed.
`DO-THIS-IN-LAPIS.md` is the single source; it now says `95bbfb1` everywhere.
