# Codex agent files — the three fixes applied 15 Oct 2026, and how to undo them

The files in `.codex/agents/` are untracked, so this records the change in version
control even though the files themselves are not in it. Mila authorised the fix and asked
to be told exactly what changed.

Three facts were wrong. Four of the seven files were not touched at all:
brand, compliance, cro, ops-qa.

## What changed

1. **truemg-pm.toml** — said the template was `arcane`; it is `revive`.
2. **truemg-storefront.toml** — same wrong template, plus a guard sentence added, because
   this is the only agent that can change the template and a template apply wipes the copy
   keys and the whole `customCss` block.
3. **truemg-seo.toml** — had the contact address as `research@truemg.com` and listed it as
   a defect to fix. It is `support@truemglabs.com` and already correct on the site.

All seven files were confirmed to still parse as valid TOML afterwards.

## To undo: apply this patch in reverse from the repo root

```diff
--- a/b/.codex/agents/truemg-pm.toml	2026-10-15 10:47:45
+++ b/.codex/agents/truemg-pm.toml	2026-10-15 10:47:45
@@ -1,7 +1,7 @@
 name = "truemg-pm"
 description = "Project manager for the TrueMG Labs storefront. Use when asked for project status, what's blocking the Friday launch, what to work on next, who owns what, or to re-plan the schedule. Owns the critical path and is the only agent that decides sequencing."
 developer_instructions = """
-You run delivery for the TrueMG Labs storefront (https://truemglabs.com, Lapis platform, `arcane` template).
+You run delivery for the TrueMG Labs storefront (https://truemglabs.com, Lapis platform, `revive` template).
 
 **The goal that defines done:** a real order can be placed and completed end-to-end — by Mila internally and by a stranger as a customer — on a site that looks and behaves 90% finished.
 
--- a/b/.codex/agents/truemg-seo.toml	2026-10-15 10:47:45
+++ b/.codex/agents/truemg-seo.toml	2026-10-15 10:47:45
@@ -10,7 +10,7 @@
 This is a research-use-only catalog. The high-volume queries in this space are human-use queries, and you may not chase them — not with copy, not with metadata, not with an FAQ answer written to rank. Chasing them is both a compliance breach and, since the server screens copy for research-use framing, a rejected change. Target what you can honestly own: compound identity and purity, certificate of analysis availability, handling and storage for laboratory material, sourcing and documentation, lot traceability, and brand-name queries.
 
 ## Working order
-1. **Fix the obvious defects first.** The contact email (`research@truemg.com`) does not match the domain (`truemglabs.com`) — that is a trust and deliverability problem before it is an SEO one. Audit for more of these.
+1. **Fix the obvious defects first.** The contact email is `support@truemglabs.com` and matches the domain — that one is already resolved, do not re-flag it. Audit for others of the same kind.
 2. **Title and description per page**, written for a click rather than for a crawler, inside the key limits.
 3. **One H1 per page**, headings that describe real sections, `heroHeadlineAccent` used for emphasis rather than decoration.
 4. **The FAQ key is a JSON array** of `{"question","answer"}` — up to 4000 chars. This is the single highest-leverage SEO surface available, because it is long-form, question-shaped, and eligible for rich results. Write it properly. Keep every answer research-use framed.
--- a/b/.codex/agents/truemg-storefront.toml	2026-10-15 10:47:45
+++ b/.codex/agents/truemg-storefront.toml	2026-10-15 10:47:45
@@ -4,7 +4,7 @@
 You are the hands on the TrueMG storefront. You turn decisions into live pages.
 
 ## Know your surface
-The Lapis design endpoint exposes **~281 editable copy keys** plus the palette, a template choice, and a custom CSS block. Most of the site is reachable. Always start with `get_store_design` — it returns the exact key list for the `arcane` template, and the key list is the spec. Never guess a key name; an invalid field rejects the entire change.
+The Lapis design endpoint exposes **~281 editable copy keys** plus the palette, a template choice, and a custom CSS block. Most of the site is reachable. Always start with `get_store_design` — it returns the exact key list for the `revive` template, and the key list is the spec. **Never change the template.** `revive` is what is live; applying another template wipes copy keys and the entire `customCss` block. Never guess a key name; an invalid field rejects the entire change.
 
 Key clusters you will use constantly:
 - Hero: `heroEyebrow`, `heroHeadline`, `heroHeadlineAccent`, `heroSub`, `heroCta`, `heroCtaAlt`, `heroAlign`, `heroBackgroundUrl`, `hide:heroContent`
```

`git apply -R` that block, or just reverse the three substitutions by hand — each is a
single line.
