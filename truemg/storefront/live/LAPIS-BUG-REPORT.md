# Lapis bug report — paste into the admin form

**Where:** admin → **Help** (bottom of the sidebar) → **"Message the Lapis team"**

**What's this about?** → **Something is broken**

Your store name and login email are attached automatically, so there is no
greeting or signature below — the form adds them.

---

## SUBJECT (copy this line)

```
Custom CSS cannot be edited in Design studio, plus intermittent blank-page loads
```

## DETAILS (copy everything below this line)

```
Template: revive. Four issues, in order of how much they cost us. Happy to give
you a window to reproduce any of them live.



1. THE STORE INTERMITTENTLY SERVES A BLANK PAGE FOR 10-20 SECONDS

This is the one that worries us most, because a visitor who waits ten seconds on
a white screen never sees the shop at all.

Five consecutive cache-busted loads of /catalog, reading
`domContentLoadedEventEnd` from the browser's own navigation timing:

    run 1    21.1 s
    run 2     3.8 s
    run 3     1.9 s
    run 4     1.1 s
    run 5    11.8 s   (still only ~15 characters of text on screen after 10 s)

Two of five took over ten seconds. On the slow runs the page is not a spinner
and not a skeleton -- it is blank white. /store did the same thing twice in a
row, then filled in somewhere between 10 and 15 seconds.

It is not our connection and not your hosting:

  * example.com in the same browser in the same minute: 0.22 s
  * time to first byte on the slow runs: 93 ms -- your server answers instantly

So the delay is entirely client-side, after the HTML arrives. No console errors
were captured. Separately, the admin product list at /admin/products hung for
over 20 seconds on two occasions.

Is there a known issue with the client bundle or a data fetch on `revive`?


2. THERE IS NO WAY TO EDIT CUSTOM CSS, AND THE EDITOR SILENTLY FAILS AT IT

Design studio (/admin/appearance) is chat-only. There is no Custom CSS field, no
colour inputs, and no manual mode -- the "Sections and pages" panel lists only
AI-built sections. So the chat agent is the only route to Custom CSS.

It does not work for this, in three escalating ways.

  (a) Told to change one value, it APPENDS a rule instead of editing the
      existing one, and drops `!important`. We asked it to change

          .lf-card .aspect-square{background:#EDF4FB!important}

      to #E1EAF4. After publishing, the stylesheet contained BOTH:

          .lf-card .aspect-square{background:#EDF4FB!important}
          .lf-card .aspect-square { background: #E1EAF4; }

      Identical selectors, so `!important` wins and the new rule is dead. The
      publish reported success. Nothing changed on the page -- confirmed by
      computed style, still rgb(237,244,251).

      A publish that succeeds and has no effect is worse than an error.

  (b) Told explicitly to delete the old rule and replace it, carrying
      `!important`, it now answers that it cannot do it. The store owner tried
      this herself, by hand, in Design studio -- not through any API or agent.

  (c) So there is currently no supported way for a store owner to change one
      line of their own Custom CSS.

For completeness and so you do not chase the wrong thing: the same stylesheet
validates cleanly through your agent design endpoint -- `preview_design_change`
returned ok with no refused rules. **The API is fine.** The gap is that the
admin UI offers no equivalent, and the chat agent mishandles CSS.

Could you either expose a plain Custom CSS textarea in Design studio, or fix the
agent so it replaces rules rather than appending them and preserves `!important`?


3. THE API AND THE CHAT DISAGREE ABOUT HERO IMAGE FIELDS

`heroBackgroundUrl`, `heroBackgroundMobileUrl` and `heroMediaUrl` accept a plain
https URL through the design endpoint, and ours are currently set to jsDelivr
URLs that work.

Asked to change them, the Design studio chat says those slots only accept images
from the media library, not web addresses. Both cannot be right. If URLs are
supported, the chat should accept them; if they are not, the field should not
take them.

Related: there appears to be no media library page in the admin. The chat's own
answer is that images only enter the library by being added as a *product's*
photo. That is awkward for a hero image, which is not a product.


4. THE CSS ALLOWLIST CHANGED WITHOUT NOTICE, SILENTLY DROPPING WORKING RULES

On 2026-10-11 a stylesheet that applied cleanly in the morning came back in the
evening with 33 rules dropped. Nothing on our side changed. The rejections were
for properties including `position`, `inset`, `z-index`, `clip-path` and
`overflow`.

We are not arguing the allowlist -- we understand why it exists. The problem is
that it tightened silently on a live store. Is there a changelog for it, and can
rule rejections be surfaced to the owner rather than only in an API response?


Thanks -- happy to jump on a call or give you a reproduction window for any of
these. The blank-page one especially; we are about to come out of coming-soon
and that is the one that will cost us customers.
```

---

## A note on accuracy, deliberately kept out of the report

Mila asked that it say we tried through the API as well as by hand. By hand is in
there, item 2(b), in her own words — she did it herself in Design studio, not
through an agent.

**The API claim is left out on purpose.** The same stylesheet *validates cleanly*
through the agent design endpoint: `preview_design_change` returned `ok` with no
refused rules. What blocked the API save was a guardrail on our side, not
anything Lapis does. Reporting "the API failed" would have them test it, find it
working, and discount the rest of a report that is otherwise solid. So item 2
says the API is fine and points the blame at the admin UI, which is where it
belongs — and that makes the report harder to wave away, not easier.
