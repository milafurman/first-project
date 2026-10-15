# Where everything goes — the whole outstanding list

Everything left to do on the store, and exactly where. Nothing here needs Austin.

---

## DESIGN STUDIO — three things, then one Publish

**app.uselapis.io/admin** → Home → **"Open Design studio"**
(or straight to **app.uselapis.io/admin/appearance**)

> ⚠️ It is **not** in the sidebar. It is a button on the admin home page, in the
> *Lapis AI store editor* card.

### In the chat box (the one saying "What should change?")

> ⛔ **NEVER give Mila a file path to paste.** She pasted
> `../copy/APPLY-REFUNDS-AND-FAQ.md` into the chat because this file told her
> to, and the editor answered *"I can't open files from your computer."* The
> text itself has to be in the message she is reading. This is the single
> most repeated mistake of the whole session.

| | What | Note |
|---|---|---|
| **1** | The refund policy | Paste the **wording itself**. The editor said *"I can't write a refund policy myself, because policies have to come from you, but if you paste your own wording I can help place it."* |
| **2** | The FAQ answer | Same — the words, not a reference to them. |

Paste one, send. Paste the other, send. **Both, or neither** — doing one
re-creates the contradiction they were fixing.

### In Manual controls (the sliders icon, top of the Store editor panel)

| | What |
|---|---|
| **3** | Paste the **whole stylesheet** from `customCss-with-card-fix.css` and say "replace the entire Custom CSS with exactly this". |

⚠️ **Do not ask it to edit one line.** It replied: *"I can't see the existing
Custom CSS from here, so I can't delete one rule by itself. My only options are
adding new rules at the end or replacing the whole Custom CSS."* Replacing
wholesale is the only route that works, which is why
`customCss-with-card-fix.css` is the live stylesheet with the single value
already changed — **dry-run and accepted**, and only one line differs from what
is live.

### Then press **Publish**. Once. It ships all three.

---

## PRODUCTS — three photos, not in Design studio

**Products → Catalog → click the product row → Pictures → + Add**

Files are on the **Desktop**, in **TRUEMG UPLOAD**, named *"DO THIS ONE FIRST"*:

| File | Product |
|---|---|
| `11 SS-31 - DO THIS ONE FIRST.png` | SS-31 |
| `14 TMG-2TZ - DO THIS ONE FIRST.png` | TMG-2TZ |
| `15 TMG-3RT - DO THIS ONE FIRST.png` | TMG-3RT |

For each: **+ Add** → pick the file → **drag it to FIRST position** → delete the
grey room photos → **Save**.

⚠️ The drag matters. *"The first image is the main photo shown on the
storefront."* These three have **no** clean cut-out at all — verified by opening
them — which is why their tiles look wrong while the other fourteen look fine.

The other fourteen (files 01–10, 12, 13, 16, 17) already show a clean bottle;
replacing them fixes the cap defect, which is real but subtle. Not urgent.

---

## Afterwards

Check at **truemglabs.com/?peek=1** — and press **Cmd+0** first. A zoomed-out
browser makes the fixed 1280px content column look like a broken ribbon; that
already caused one false alarm.

---

## Not on this list, and why

| | |
|---|---|
| The dark About page | needs route hooks from Lapis — in Austin's inbox |
| Anything Nurish-caliber | needs the six asks — same |
| Stock | the inventory owner's job, not Mila's |
| The Terms of Service read | a human with the qualification; Sam has the list |
