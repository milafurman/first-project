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

⚠️ **The four cards are editable — found them.** The numbered grid on the live
About page is `aboutValue1Title`/`Body` through `aboutValue4Title`/`Body`:
*Documented to the lot*, *Independently analysed*, *Out in 48 hours*,
*Research use only*. They are separate from `aboutBody`, so they survive a body
rewrite and must be edited deliberately.

They matter to Direction A: the new story already **says** three of these four
things in prose, so left as they are the page argues with itself. Either cut
them to one or two, or let them carry the detail the story deliberately keeps
short (the 48-hour turnaround is the one fact the new copy drops).

## Third batch for Austin — found 14–15 Oct 2026, all verified on the live store

1. **The catalog card truncates every product description at the first period.**
   The product detail page renders the full text; the card drops everything after
   the first `.`. Verified against all 17 products — card text equalled stored text
   up to the first period, 17/17. EPITHALON's card showed only `Ala-Glu-Asp-Gly.`
   Nine products were losing copy; three of them silently, because what survived
   still read as a sentence. There is no separate card-blurb field.

2. **`pdCoaOnRequest` is ignored by the theme.** The field is documented as
   "Product page — text shown when no certificate is published", and a write to it
   is accepted, but the product page still renders the theme default
   "COA available on request". So the owner cannot tell a buyer *how* to request it.

3. **`pdCoaOnRequest` also has an undocumented 60-character cap that truncates
   silently, mid-word.** A longer value was accepted with `ok: true`, no warning
   and no entry in `cssRejected`, and stored cut at 60 characters ending
   "...with your l". Fields with a `max` should refuse or report, not silently cut.

4. **The catalog filter heading builds an ungrammatical string.** Unfiltered it reads
   "Research Compound Catalog"; with the Research Peptide filter it becomes
   "Research Peptide peptides", and with Lab Supplies, "Lab Supplies peptides" — on a
   page whose only item is a 10 mL solution, which is not a peptide.

5. **The four `/legal/*` pages have no site header and no site footer.** A buyer
   reading the Terms cannot reach the catalog, FAQ or Contact without going back.
   `/legal/research-use-only` is not linked from the footer at all, and none of the
   four legal pages appear in the sitemap.

6. **Category tiles carry generated placeholder copy.** The home page "Pick a lane"
   tiles read "Research-grade research peptide compounds for laboratory research."
   — the word research three times, and not grammatical. It is generated from the
   category name, so the owner cannot edit it. Both tiles also link to the same
   unfiltered catalog. Hidden via `hide:categories` for now.

7. **Footer colour rule is undocumented.** `footer a{color:...}` is refused with
   "footer colors must set color and background-color together". Worth documenting,
   because the obvious consequence is that an owner who darkens the footer gets
   black-on-navy text until they discover the pairing requirement.
