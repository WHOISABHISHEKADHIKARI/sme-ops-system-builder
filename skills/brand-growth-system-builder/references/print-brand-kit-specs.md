# Print Brand Kit Specifications

Production specifications for the physical brand kit. Read this before quoting a print
supplier, not after artwork is approved.

Reference file for `skills/brand-growth-system-builder/skills/brand-design/brand-kit-print-collateral/SKILL.md`. Load on demand; do not
load at runtime unless the user is asking about print, a supplier quote, or an export.

**Status of every number here:** supplier specifications change, paper stocks change
availability, and postal standards change. Treat each figure below as a *starting point
that must be confirmed with the printer for the specific job*. Nothing here is a supplier
quote.

---

## The three questions that decide everything else

Before any specification is meaningful, three answers decide the whole kit:

1. **Digital only, or print too?** A brand kit for a website needs none of this file.
2. **Process black or full colour?** Process black (black on white) is cheaper, sharper,
   more consistent between runs, and completely fine for a letterhead, a visiting card
   and an employee card. Full colour is only needed where the brand's colour carries
   meaning, not decoration.
3. **Who prints it?** A local print shop, an online printer, or an in-house laser printer
   produce different files. Digital press, offset and laser are not interchangeable, and
   an online print shop will usually supply its own template.

The `Colour Mode` and `Export Format` fields in the collateral register exist to record
the answers, because "it looked right on screen" is the most common reason a print job
comes back wrong.

---

## Standard sizes

Trimming sizes in millimetres, as stocked. Confirm with the printer; some regions and
printers differ by 1-2mm and some suppliers only offer a subset.

### Letterhead - A4

| Property | Value |
|---|---|
| Trim size | 210 x 297 mm (A4 portrait) |
| US Letter equivalent | 216 x 279 mm - do not mix in one set |
| Bleed | 3 mm all sides, only if artwork runs to the edge |
| Safe margin | 15 mm minimum from trim; 20 mm is safer for hole-punching and binding |
| Safe area | Everything that must survive trimming lives inside the safe margin |
| Orientation | Portrait. Landscape letterhead is a different design, not a rotation |
| Sides | One side used. Two-sided letterhead is wasteful for most businesses |

### Letterhead - US Letter

| Property | Value |
|---|---|
| Trim size | 216 x 279 mm (8.5 x 11 in) |
| Bleed | 3 mm all sides where artwork runs to the edge |
| Safe margin | 15 mm minimum, 19 mm (0.75 in) typical |

### Visiting / Business card - the default

| Property | Value |
|---|---|
| Trim size, EU | 85 x 55 mm |
| Trim size, UK | 85 x 55 mm |
| Trim size, US | 89 x 51 mm (3.5 x 2 in) |
| Bleed | 3 mm all sides, required - a full-bleed card is common |
| Safe margin | 4 mm minimum; 5 mm for text |
| Corner radius | 3 mm is the usual choice. Rounded corners are a separate die, and cost more |
| Sides | Two-sided is the norm: identity one side, the practical details the other |
| Stock | 350-400 gsm card is the usual "premium" band; 300 gsm is fine and cheaper |
| Finish | Matte laminate hides fingerprints; soft-touch is dearer; spot UV on the mark only |

**Do not put a full address, phone, email and social handle on the front.** The front is
the mark and the name. A visiting card with everything on it is a leaflet that costs
money per card.

### Employee / ID card

| Property | Value |
|---|---|
| Trim size, CR80 | 54 x 86 mm, 0.76 mm thick - the standard for a badge sleeve or a card printer |
| Trim size, credit-card | 85.6 x 54 mm, 0.76 mm - what a card printer expects if it is not CR80 |
| Bleed | 3 mm all sides |
| Safe margin | 4 mm; keep clear of any punch slot |
| Sides | Two-sided. Photo and name one side, role and contact the other |
| Personalisation | Name, role, photo and number are per-person variables, so the artwork is a template with defined fields - not 40 separate files |
| Data protection | If it carries a photo, a role and a number, treat it as personal data. Do not put anything sensitive on it, and do not issue a card that has not been issued |
| Stock | 350 gsm PVC or coated card, or CR80 for a sleeve |

A lanyard-and-sleeve version is 54 x 86 mm with a slot; the slot position must be given to
the printer because it is a die cut, not a crop.

### Compliment slip / A5 leaflet

| Property | Value |
|---|---|
| Trim size | 148 x 210 mm (A5) |
| Bleed | 3 mm all sides if full-bleed; otherwise no bleed needed |
| Safe margin | 12 mm |
| Sides | Two-sided is normal for an A5 leaflet |
| Stock | 170-250 gsm for a leaflet that is handed out; heavier if it is a price list that must look permanent |

### Folder

| Property | Value |
|---|---|
| Trim | A4 or US Letter, with a pocket and a spine; die lines vary by supplier |
| Stock | 350 gsm board, wrapped or self-folded |
| Finish | Matte laminate outside; inside left uncoated so a pen writes on it |
| Note | A folder die is supplier-specific. Do not design to a generic A4 folder template - request the supplier's die line first |

### Invoice / statement

| Property | Value |
|---|---|
| Trim size | A4, or 210 x 99 mm for a continuous-feed dot-matrix form if that is still what the accounting software emits |
| Purpose | The layout must match what the accounting software outputs. Match the software, not the design |
| Personalisation | The register's `Personalisation` field records what varies per customer - usually only name, address and invoice number |
| Practical | Leave the fold and punch positions clear; check whether the business files these |

### Email signature

Not printed, but part of the same kit, and it is the piece most often shipped broken.

| Property | Value |
|---|---|
| Format | HTML that survives Outlook and Gmail, plus a plain-text alternative |
| Images | Hosted, not embedded. An embedded image is blocked by default in most clients |
| Size | Under 200 KB is the working target; many clients truncate beyond that |
| Text | Must be readable with images off, and must not be an image of text |
| Mobile | Roughly half of opens are mobile, so it must reflow. Fixed-width tables break |
| Accessibility | Meaningful link text, no text in images, contrast on any background |
| Consent | Analytics and tracking pixels need a lawful basis and, in some places, consent. The `Consent` question in the email module is the right place to record that |
| Legal | Depending on jurisdiction, a physical postal address and, in some cases, an unsubscribe line are required in commercial email |
| Version | Record the version in the register. An HTML signature lives in ten people's inboxes and cannot be recalled |

---

## Colour

| Property | Value |
|---|---|
| Default recommendation | Process black on white for letterhead, visiting card and employee card |
| Full colour when | The brand colour carries meaning, or the piece is customer-facing marketing |
| RGB to CMYK | Convert in the layout tool, not in an image viewer. Screens are RGB, press is CMYK |
| Rich black | A large area of 100% K only is standard. 60/40/40/100 "rich black" is for large solid areas and can show a mottled edge on uncoated stock |
| Total ink coverage | Keep below about 300% on coated stock and below 240% on uncoated, or you get set-off and drying problems |
| Proofing | A screen proof is not a press proof. Get a physical proof from the printer for anything with a brand colour |
| Uncoated stock | Ink looks darker and slightly different on uncoated than on coated. A coated-only design will not match |
| Paper white | "White" is not a standard. Bright white, natural white and recycled white are visibly different |
| Spot colour | If a brand colour must be an exact match, ask the printer for a spot colour match against a physical sample |

Record the measured value, not the intended one. `design-theme-guide` holds the hex for
screens; the printed result is whatever the press and stock produce, and only a proof
tells you.

---

## Export settings by process

| Process | Colour | Format | Resolution | Fonts | Notes |
|---|---|---|---|---|---|
| Digital press | CMYK | PDF/X-1a or PDF/X-4 | 300 dpi images, vector preferred | Outline or embed | Ask the supplier which PDF/X they want |
| Offset | CMYK | PDF/X-1a or PDF/X-4 | 300 dpi, 1200 dpi for fine text | Outline or embed | PDF/X-4 for transparency and large spot areas |
| Laser / office | Greyscale or colour | PDF | 300 dpi | Embed | Test on the actual machine; it is the cheapest check available |
| Large format | CMYK | PDF | 150 dpi at final size | Outline | Only relevant to a banner, not this kit |
| Full bleed | Add 3 mm on every side | | | | The bleed area must have content; a bleed with nothing in it shows a white sliver |
| Spot UV / foil | Add a separate spot layer | | | | Never as a flattened image. A separate spot channel is the whole point |

**Always supply PDF.** PDF is the only format every print supplier accepts, and PDF/X is
the version that will not re-interpret colours, fonts or transparency. Never send a
designer application file to a printer, and never send a screenshot of a design.

**Outline the fonts** for anything going to a press, or the printer's RIP will substitute.
Keep the original live file with outlined *and* live versions; the outlined one prints and
the live one stays editable.

---

## Files a supplier should receive

| File | Why |
|---|---|
| Print PDF, outlined fonts | What gets printed |
| Print PDF, live fonts | What gets edited, if the supplier asks to change text |
| Trim and bleed marked | So the supplier knows the intended size without asking |
| A physical proof | Only for full-colour pieces with a brand colour |
| The logo as a separate file | In case it is set into a supplier's own die line |
| The brand colour values | Hex, RGB, CMYK and Pantone if one exists |

A supplier who has to ask "what size is this?" will either guess or charge you for a
proof. Both are avoidable.

---

## Accessibility and legal notes for print

- **Contrast** - the WCAG 2.2 AA thresholds in `design-theme-guide` are written for
  screens. Light grey on white that passes on a monitor can disappear on uncoated paper.
  Check a physical proof, not the file.
- **Type size** - a 9pt body text in a document will be illegible in print. 10-11pt is
  the practical minimum for body copy on A4 letterhead; footnotes can go smaller.
- **Braille and large print** - a business that serves customers with a visual
  impairment may be required to provide accessible documents. That is a fact about the
  jurisdiction and the sector, not something this file decides.
- **Language** - where a document may be read by people whose first language is not the
  document's language, plain wording is an accessibility issue as well as a courtesy one.
- **QR codes** - a printed QR code needs a minimum size, adequate contrast and a printed
  short URL as a fallback for people who cannot or will not scan. A QR code that is the
  only route to information excludes people.
- **Trademark and registered marks** - a mark that is not registered can still be
  protected, and a ™ or ® must be used correctly. `logo-image-design` holds the
  trademark status; the print artwork must match it.
- **Personal data on print** - an employee card, an invoice and a mailing label all carry
  personal data. Print is not a privacy control: a bin is a breach. Decide what is
  collected, and shred what is not needed.

---

## Common print failures

| Symptom | Cause | Fix |
|---|---|---|
| White sliver at the edge | No bleed, or the bleed has no content in it | 3 mm bleed, filled to the edge |
| Trimmed text | Content in the safe margin | Move content inside 15 mm |
| Colours do not match the screen | RGB file, or a screen proof compared to print | Convert to CMYK, compare a physical proof |
| Washed-out pale colour | Uncoated stock | Accept the difference or change stock |
| Font substituted | Font not outlined, or not licensed for the use | Outline, and check the licence |
| Card corners square when they should be rounded | Corner radius is a die, not a crop | Ask the supplier for a rounded-corner die |
| Two-sided misaligned | Flipped on the long edge when the design assumed short-edge | State the flip explicitly on the artwork |
| Holes through the content | Punch position unknown to the designer | Get the punch or slot position from the supplier first |
| Everything on the visiting card front | No hierarchy | Front is mark and name; details go on the back |
| Signature renders as raw HTML or a broken image | Hosted image blocked, or an embedded image | Host the image, keep it under 200 KB, add a plain-text alternative |
| Signature unreadable on a phone | Fixed-width layout | Reflow, test on a real phone before rollout |
