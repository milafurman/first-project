# Do this in Lapis — the whole live change, by hand

Everything below is built, validated and sitting ready. The **save** is refused
by this session (it classes a live-store write as a production deploy), twice,
so these are the keystrokes.

Design studio → and remember: **saving colours wipes the custom CSS.** Do all
three parts in one save, or do 1 and 2 first and paste 3 last.

---

## 1. Point the hero at the new pictures

Three fields still point at commit `a2e36e7`, which is a snapshot from before
the cap was fixed. Change `a2e36e7` to `a7ae839` in each. Nothing else about the
URL changes.

| Field | New value |
|---|---|
| `heroBackgroundUrl` | `https://cdn.jsdelivr.net/gh/milafurman/first-project@a7ae839/truemg/assets/web/hero-hand.jpg` |
| `heroBackgroundMobileUrl` | `https://cdn.jsdelivr.net/gh/milafurman/first-project@a7ae839/truemg/assets/web/hero-spa-mobile.jpg` |
| `heroMediaUrl` | `https://cdn.jsdelivr.net/gh/milafurman/first-project@a7ae839/truemg/assets/web/pixel.png` |

**The branch is pushed and the CDN is serving these.** Verified: the new
`hero-hand.jpg` comes back from the CDN byte-identical to the local file,
138,865 bytes against the 138,825 the site serves today.

## 2. Colours

| Key | Value |
|---|---|
| `background` | `#EEF2EE` |
| `card` | `#FCFDFB` |
| `secondary` | `#E9EDE9` |
| `border` | `#DCE5DC` |
| `muted` | `#E4EBE4` |
| `mutedForeground` | `#6E7A6E` |

Leave `accent`, `themeAccent`, `themeAccentDeep` and `primary` alone — the
brand blue does not change.

## 3. Custom CSS

Paste the whole of `customCss-eucalyptus.css` from this folder.

---

## What this does NOT fix

**The seventeen product photos.** Those live in Lapis's own storage, not in this
repo, so they are uploads and no CDN trick reaches them. Still Mila's hands,
still seventeen uploads, and it is also what clears the three odd cards.

## If it goes wrong

`customCss-2026-10-12.css` in this folder is the stylesheet exactly as it was
before any of this. The colour values to go back to: `background` `#ffffff`,
`secondary` `#ecebee`, and the hero fields back to `a2e36e7`.
