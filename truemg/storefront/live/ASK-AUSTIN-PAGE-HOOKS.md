# Second ask for Austin — page and section hooks

Mila chose **Direction A** (the dark About page) on 14 Oct. It cannot be built on
Lapis as things stand, for two reasons, both verified rather than assumed.

## What was measured

Fetched the raw HTML of all five pages and counted the hooks:

| Page | `lf-section-*` hooks | page identifier |
|---|---|---|
| `/store` | 35 | **none** |
| `/catalog` | 27 | **none** |
| `/about` | **0** | **none** |
| `/contact` | 0 | **none** |
| `/lab-results` | 0 | **none** |

And on `/about`, nothing on `<html>`, `<body>`, `<main id="lapis-main">`,
`.lf-store` or `.theme-revive` identifies the route. Every page carries
byte-identical wrappers.

## Why that blocks it

1. **No page identifier → customCss cannot scope to one page.** Any rule that
   darkens the About page darkens the whole store. The only workaround is making
   the entire site dark, which is a far bigger decision than one page.
2. **No section hooks on About → its bands cannot be targeted either.** Its three
   sections carry only Tailwind utilities (`max-w-3xl`, `max-w-5xl`), which are
   not stable to theme updates, and which do not appear in the server-rendered
   HTML at all — they arrive on client render.

The catalog and home page do have `lf-section-*` hooks, so the pattern already
exists in the codebase; About, Contact and Lab results simply never got it.

## The ask — small, and in their existing idiom

```
Two small hooks, in the pattern you already use:

1. A route class on the store root, so custom CSS can target one page.
   Something like `lf-page-about`, `lf-page-catalog`, `lf-page-contact`
   alongside the existing `lf-store`. Right now every page carries identical
   wrappers, so any rule we write hits all of them.

2. `lf-section-*` classes on the About, Contact and Lab results pages, the
   same way /store and /catalog already have them. Those two pages have 35
   and 27 hooks respectively; About has none, so its sections can only be
   reached through Tailwind utilities, which are not stable and are not in
   the server-rendered HTML.

With those two, a store owner can style an individual page without touching
the rest of the store.
```

Austin's own form is at admin → **Help** → *Message the Lapis team* →
**Feature request**. Or reply in the existing thread with him; he asked to be
kept posted.

## What is NOT blocked

The About **copy** can ship today — `aboutHeading`, `aboutBody`,
`aboutCtaHeading`, `aboutCtaSub`, `aboutCtaButton` and `aboutImageUrl` all
exist. Direction A's words and its image can go in now; only the dark treatment
waits.

⚠️ There is also content on the live About page that the rewrite did not account
for: a numbered four-card grid (*01 Documented to the lot*, *Independently
analysed*, *Out in 48 hours*, *Research use only*). Check whether those are
editable copy keys before replacing `aboutBody`, or they will sit oddly against
the new story.
