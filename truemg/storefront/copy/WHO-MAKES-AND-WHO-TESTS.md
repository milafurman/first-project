# Who makes it and who tests it — settled 15 Oct 2026

Mila: *"It says that we are a lab right here in the United States, and everything is made on
site and tested on site."*

I stopped before writing, because "tested on site" is the **opposite** of what the whole site
claimed. Eleven places said the testing is done by somebody else:

`productTrust2` "Tested by a lab that isn't us" · `quality4Title` "A lab that isn't us" ·
`quality4Body` · `qualitySub` · `labIntro` · `aboutBody` · `aboutValue2Title/Body` ·
`how1Body` · `faq` · `comparisonTable` · `promoSub` · `seoDescription` · `comingSoonSub`

That claim is the spine of the pitch, and the reason it appears everywhere is that a seller
grading its own homework is exactly what a careful buyer worries about. Writing "tested on
site" would have meant tearing all of it out.

## What she confirmed

**Made on site, tested by an outside lab.** Compounds are synthesised, filled and labelled in
TrueMG's own United States facility; a sample from every finished lot goes out to an
independent laboratory for identity and purity.

That is the strongest available version and **nothing had to be removed.** The independent-lab
claim stays everywhere it already was, and the made-in-the-USA fact — which appeared **nowhere
on the site** before today — was added.

## What changed

| Key | Change |
|---|---|
| `heroSub` | now opens with "Synthesised, filled and labelled in our own United States facility, then sent out to an independent laboratory lot by lot" |
| `heroTrust2` | "Lot number on the vial and the COA" → **"Made in our own US facility"** (the lot-match point is still carried by `heroSub`) |
| `labIntro` | rewritten to tell the process: made here → sampled → sent out → what the lab reports → filed to the lot |
| `aboutBody` | "WHAT TRUEMG LABS DOES" now opens on the facility before the testing |
| `comingSoonSub` | the made-in-the-USA fact added to the one page the public can currently reach |
| `how1Body` | **defect fix** — see below |

## The defect I introduced and then found

`how1Body` has a **200-character cap** and my earlier text was exactly 200. It shipped
truncated, so step one of "How this works" on the home page ended mid-sentence with a dangling
semicolon: *"…as they are issued;"* Live, on the front page, for hours. Rewritten to 194
characters and verified to end with a full stop.

Same trap as `pdCoaOnRequest` earlier today. **Count the characters against the cap before
sending, every time** — the API returns `ok: true` and truncates silently.

## Deliberately left alone

- **Lab Results' four-step "How documentation is posted" block** is theme-generated with no
  copy keys behind it. Re-checked, not assumed. `labIntro` (600 characters) is the only
  writable surface on that page, so it covers **making and testing** and lets the theme block
  keep covering **publishing**. That division is why 600 characters is enough.
- **The curtain.** `comingSoonEnabled` untouched.

## Still worth asking Sam

Two factual gaps that would strengthen this further and that I will not invent: whether the
outside laboratory is **named** on the certificate (the copy says it is), and whether the
facility holds any **accreditation** worth stating.
