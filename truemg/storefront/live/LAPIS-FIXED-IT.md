# Lapis fixed all four — 13 Oct 2026

Austin Siddiqi (AUS Consulting, austin@byaus.co) replied twice to the bug report
and shipped all four fixes the same day. **Verified independently, not taken on
his word.**

## 1. The blank page — fixed, and the numbers are not close

Five cache-busted loads of `/catalog`, measured again:

| Run | Before (12 Oct, DOM ready) | After (14 Oct, complete) |
|---|---|---|
| 1 | **21.1 s** | **0.41 s** |
| 2 | 3.8 s | 0.35 s |
| 3 | 1.9 s | 0.32 s |
| 4 | 1.1 s | 0.28 s |
| 5 | **11.8 s** | 0.29 s |

**The worst run now beats the best run before.** First byte 0.18–0.28 s.

More important than the timing: **the product names are in the first response.**
Grepped the raw HTML for `TESAMORELIN|IPAMORELIN` — present, all five runs. The
store is server-rendered now, so the blank white page is structurally impossible
rather than merely less likely.

His account of the cause: on 12 Oct their database was overloaded and the store
waited on it with no timeout, first server-side then again in the browser,
showing nothing until data arrived. Platform-wide fix: layout renders
immediately, slow reads give up after a couple of seconds and retry, and the
store never shows "store unavailable" for a slow read. This store was also
switched to server rendering. The admin Products page now stops after 15 s with
a **Try again** button instead of hanging.

## 2. Custom CSS — fixed, and there is now a manual editor

- The chat **edits the existing rule** instead of appending a second one, and
  **keeps `!important`** unless asked to drop it. It can delete a rule, or
  delete and replace.
- A change that would not show on the store now **says why and saves nothing**,
  instead of reporting success. That was the specific complaint.
- **New: a "Manual controls" button (sliders icon) in Design studio** — a plain
  Custom CSS editor, the colours and sizes, and a list of every rule that is not
  applying with the reason.

Austin, explicitly: *"When you're ready, try your card colour change again
(#EDF4FB to #E1EAF4). It should update that one rule and show on the store."*

## 3. Hero images — fixed, and there is a media library

An `https` image link can be pasted into the chat for the hero background, phone
hero background or hero image, and **Lapis copies the image into the store**, so
it keeps working even if the source changes. There is a **Media library page
under Online store**: upload, add from a link, copy an image's address, set any
image as the hero.

This retires the whole workaround — no more uploading a hero as a product photo,
and no more jsDelivr commit pin to re-point.

## 4. The allowlist — re-opened with stated limits

The tightening was **9 Oct**, not the 11th; our 11 Oct update was simply the
first to hit it. Re-allowed, with limits:

| Property | Limit |
|---|---|
| `position` | `relative`, `absolute`, `sticky` — not `fixed` |
| offsets | within 400px |
| `z-index` | up to 9 |
| `clip-path` | shapes allowed |
| `overflow` | allowed |
| backdrop blur | up to 40px |
| transitions | up to 3 s |

Refused rules now come back to the agent **with the reason** and also appear
under **Settings → Connected agents**. **Help guide 72** ("Custom CSS: What the
Store Accepts") keeps a dated changelog.

He did not touch the saved CSS, so **the 33 dropped rules need resending**;
anything still refused will say why. One specific tip from him: for a nav
underline that grows on hover, animate `width` 0→100% rather than `scaleX(0)`.

## And: cleared to launch

*"You're clear to come out of Coming Soon whenever you're ready."*

Note `comingSoonEnabled` is still `1`. **That is Mila's call and nobody else's.**

## Worth remembering

The report worked because it carried measurements, named what had been ruled out
(connection, hosting), and **told him his API was fine**. He opened his reply
with *"Thanks for writing this up so clearly. The detail made all four easy to
pin down."* A measured report to a named person beat four days of working around
the symptoms.
