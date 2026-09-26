---
name: inventory-stock-reconciliation
description: "Inventory / Stock Reconciliation: context-first intake, then CSV, SQL, JSON Schema and Notion on request. One short question per message. Use for stock reconciliation."
category: business
risk: safe
source: self
source_type: self
date_added: "2026-09-26"
author: WHOISABHISHEKADHIKARI
tags: [sme, accounting, audit, finance, database, csv, notion, sql, reconciliation]
tools: [claude, cursor, gemini, antigravity]
---

# Inventory / Stock Reconciliation

**What it is:** Physical counts against book quantities, differences investigated and authorised adjustments passed.

## Overview

Works out the smallest useful **Inventory / Stock Reconciliation** setup for the business in front of it, then
builds it only when asked. The default output is a short recommendation, not a
spreadsheet. Artifacts - CSV, SQL DDL, JSON Schema, Notion mapping - are produced on
request, from one field list so they cannot drift apart.

The count is periodic by design. Book quantity is a number the system believes; it is
only ever as good as the last entry. Until someone walks the shelves and writes down what
is actually there, the books are an opinion, and the frequency of the count is a business
decision driven by volume, value and risk rather than a setting anyone can skip. Two
things follow from that. First, every adjustment needs a named approver before it is
booked - a correction passed without authorisation is just a quiet write-off. Second,
investigating a shrinkage is a human judgement, not a calculation: no formula tells you
whether 22 missing cartons were theft, a mis-pick, or two dispatches that never got a
stock entry.

Layer: Layer 7: Reconcile. Fits: Growth stage. Table code: n/a.

## When to Use This Skill

- physical stock count
- stock variance investigation
- stock adjustment register
- inventory shrinkage tracker
- cycle count sheet

Also use it when the user says "physical counts against book quantities, differences investigated and authorised adjustments passed", or describes the same process happening in a
spreadsheet, a document or someone inboxes.

Do not use it for: purchase or sales booking, valuation method design, or legal advice. This skill produces
empty templates only - it never holds or processes real employee or customer data.

## How It Works

### Step 1 - Identify intent

Read the request and pick the intent before asking anything.

- "set up" or "build" or "create" -> the user wants artifacts; go to Step 2.
- "our process is ..." or "it is in a sheet" -> the user wants to move an existing process; capture it, then Step 2.
- "is this right" or "review" or "audit" -> the user wants a check, not a build; answer from what they share.
- "how do I ..." -> advice question; answer directly and offer the build only if it helps.

One message, one question, no batching. Open with:

> **Q:** How many items do you hold, and when did you last count them physically?

### Step 2 - Ask only what is missing

Skip anything the user already answered, in any earlier message. Ask the rest one at a
time, and stop as soon as the remaining answers would not change the output.

- **Stock** - What do you hold? / Raw material, finished goods or both? / How many locations?
- **Count** - Full count or cycle count? / How often? / Who counts and who verifies?
- **Differences** - What gets investigated? / Who approves an adjustment? / Any threshold to escalate?
- **Current process** - Counted today at all? / Sheet or accounting package? / What gets missed?
- **Outcome** - What do you need? / A reconciliation record, a count sheet or both?

Never invent an answer. If the user does not know, record it as unknown and carry on.

### Step 3 - Build the internal context

Hold the answers in this shape. It stays internal - it is not shown to the user unless
they ask, and it never carries a value the user did not give.

```yaml
module: inventory-stock-reconciliation
intent: null            # set in Step 1, one of: set up, fix, review, report, import
scale: null             # Starter | Growth | Scale, only if the answer changes it
areas:
  "Stock": null
  "Count": null
  "Differences": null
  "Current process": null
  "Outcome": null
requested_outputs: []   # csv | sql | json | notion - only what was explicitly asked for
confirmed_facts: []     # only what the user actually said
open_questions: []      # the unanswered ones, in the order worth asking
```

### Step 4 - Recommend the smallest workflow

Give a short recommendation, then ask whether to build it. Do not build unprompted.

**Recommended approach:** One reconciliation record per item counted, carrying the book quantity, the physical quantity, the variance, the reason and the authorised adjustment, with the count sheet filed against the same record so the count can be repeated next time.

**Why this one:** A count that is not reconciled back to the books proves nothing, and an adjustment passed without a named approver is just a correction dressed up as control. Keeping the count, the difference, the reason and the authorisation on one row is the minimum that makes the number defensible later.

**Workflow:** Count planned → Items counted → Compared with books → Variance investigated → Adjustment authorised → Adjustment booked → Reconciliation filed

### Step 5 - Build only on request

Once the user asks for it, derive the fields from the confirmed context and emit the
artifacts as data only. No preamble, no summary, no closing line.

```csv
Reconciliation Number,Count Date,Item Code,Item Name,Category,UOM,Location/Warehouse,Book Quantity,Physical Quantity,Variance Quantity,Unit Rate,Variance Value,Variance Reason,Damaged Quantity,Expired Quantity,Slow Moving Flag,Unrecorded Purchases,Unrecorded Issues,Investigation Notes,Adjustment Entry,Adjustment Date,Approved By,Counted By,Verified By,Count Frequency,Status,Notes,Inventory Reconciliation ID
STK-2026-0031,2026-08-29,ITM-0455,"Corrugated carton, 3 ply, 24x18x12",Packaging,Nos,Main Store,1240,1218,-22,169.00,-3718.00,Unrecorded Issue,12,2,No,1,8,"Shortfall of 22 units: 12 damaged and 2 expired units written off at the count, 8 units issued on two dispatches with no stock entry; raised with the warehouse and booked.",ADJ-STK-2026-0031,2026-08-30,Vikram Singh,Rohit Menon,Sneha Iyer,Monthly,In progress,Count sheet filed with the reconciliation record.,
```

```sql
CREATE TABLE inventory_stock_reconciliation (
  reconciliation_number VARCHAR(255),
  count_date DATE NOT NULL,
  item_code VARCHAR(255),
  item_name VARCHAR(255),
  category VARCHAR(100) NOT NULL,
  uom VARCHAR(100) NOT NULL,
  location_warehouse VARCHAR(255),
  book_quantity NUMERIC,
  physical_quantity NUMERIC,
  variance_quantity NUMERIC,
  unit_rate NUMERIC(14,2) NOT NULL,
  variance_value NUMERIC(14,2) NOT NULL,
  variance_reason VARCHAR(100) NOT NULL,
  damaged_quantity NUMERIC,
  expired_quantity NUMERIC,
  slow_moving_flag VARCHAR(100),
  unrecorded_purchases NUMERIC,
  unrecorded_issues NUMERIC,
  investigation_notes TEXT,
  adjustment_entry VARCHAR(255),
  adjustment_date DATE,
  approved_by VARCHAR(255),
  counted_by VARCHAR(255),
  verified_by VARCHAR(255),
  count_frequency VARCHAR(100) NOT NULL,
  status VARCHAR(100) NOT NULL,
  notes TEXT,
  inventory_reconciliation_id SERIAL PRIMARY KEY,
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_inventory_stock_reconciliation_status ON inventory_stock_reconciliation (status);
```

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "Inventory / Stock Reconciliation",
  "type": "object",
  "additionalProperties": false,
  "properties": {
      "Reconciliation Number": { "type": "string" },
      "Count Date": { "type": "string", "format": "date" },
      "Item Code": { "type": "string" },
      "Item Name": { "type": "string" },
      "Category": { "type": "string" },
      "UOM": { "type": "string" },
      "Location/Warehouse": { "type": "string" },
      "Book Quantity": { "type": "number" },
      "Physical Quantity": { "type": "number" },
      "Variance Quantity": { "type": "number" },
      "Unit Rate": { "type": "number" },
      "Variance Value": { "type": "number" },
      "Variance Reason": { "type": "string" },
      "Damaged Quantity": { "type": "number" },
      "Expired Quantity": { "type": "number" },
      "Slow Moving Flag": { "type": "string" },
      "Unrecorded Purchases": { "type": "number" },
      "Unrecorded Issues": { "type": "number" },
      "Investigation Notes": { "type": "string" },
      "Adjustment Entry": { "type": "string" },
      "Adjustment Date": { "type": "string", "format": "date" },
      "Approved By": { "type": "string" },
      "Counted By": { "type": "string" },
      "Verified By": { "type": "string" },
      "Count Frequency": { "type": "string" },
      "Status": { "type": "string" },
      "Notes": { "type": "string" },
      "Inventory Reconciliation ID": { "type": "integer" }
  },
  "required": [
      "Count Date",
      "Category",
      "UOM",
      "Unit Rate",
      "Variance Value",
      "Variance Reason",
      "Count Frequency",
      "Status"
  ]
}
```

```markdown
| CSV column | Notion property | Set after import |
|---|---|---|
| Reconciliation Number | Text | Leave as Text |
| Count Date | Date | Convert to Date |
| Item Code | Text | Leave as Text |
| Item Name | Text | Leave as Text |
| Category | Select (add options after import) | Convert to Select, add options: "Raw Material", "Work In Progress", "Finished Goods", "Consumable", "Packaging", "Spare", "Other" |
| UOM | Select (add options after import) | Convert to Select, add options: "Nos", "Kg", "Litre", "Metre", "Set", "Hour", "Box", "Packet" |
| Location/Warehouse | Text | Leave as Text |
| Book Quantity | Number | Convert to Number |
| Physical Quantity | Number | Convert to Number |
| Variance Quantity | Number | Convert to Number |
| Unit Rate | Number (format: currency) | Convert to Number, set format to Currency |
| Variance Value | Number (format: currency) | Convert to Number, set format to Currency |
| Variance Reason | Select (add options after import) | Convert to Select, add options: "Shortage", "Excess", "Damage", "Expiry", "Slow Moving", "Unrecorded Purchase", "Unrecorded Issue", "Data Entry Error", "Under Investigation" |
| Damaged Quantity | Number | Convert to Number |
| Expired Quantity | Number | Convert to Number |
| Slow Moving Flag | Select (add options after import) | Convert to Select, add options: "Yes", "No" |
| Unrecorded Purchases | Number | Convert to Number |
| Unrecorded Issues | Number | Convert to Number |
| Investigation Notes | Text | Leave as Text |
| Adjustment Entry | Text | Leave as Text |
| Adjustment Date | Date | Convert to Date |
| Approved By | Text | Leave as Text |
| Counted By | Text | Leave as Text |
| Verified By | Text | Leave as Text |
| Count Frequency | Select (add options after import) | Convert to Select, add options: "Monthly", "Quarterly", "Half-Yearly", "Annual" |
| Status | Select (add options after import) | Convert to Select, add options: "Not started", "In progress", "Blocked", "Done", "Cancelled" |
| Notes | Text | Leave as Text |
| Inventory Reconciliation ID | Text (or Notion auto-ID) | Delete the column and switch the primary column to auto-ID, or keep as Text |
```

One example row per artifact, visibly fake. Money stays `currency`, dates stay `date`,
and anything pointing at another table stays `relation`.

## Field Reference

| # | Field | Type | SQL | JSON Schema | Notion | CSV example |
|---:|---|---|---|---|---|---|
| 1 | Reconciliation Number | `text` | `VARCHAR(255)` | `string` | Text | `STK-2026-0031` |
| 2 | Count Date | `date` | `DATE` | `string, format: date` | Date | `2026-08-29` |
| 3 | Item Code | `text` | `VARCHAR(255)` | `string` | Text | `ITM-0455` |
| 4 | Item Name | `text` | `VARCHAR(255)` | `string` | Text | `Corrugated carton, 3 ply, 24x18x12` |
| 5 | Category | `select` | `VARCHAR(100)` | `string` | Select (add options after import) | `Packaging` |
| 6 | UOM | `select` | `VARCHAR(100)` | `string` | Select (add options after import) | `Nos` |
| 7 | Location/Warehouse | `text` | `VARCHAR(255)` | `string` | Text | `Main Store` |
| 8 | Book Quantity | `number` | `NUMERIC` | `number` | Number | `1240` |
| 9 | Physical Quantity | `number` | `NUMERIC` | `number` | Number | `1218` |
| 10 | Variance Quantity | `number` | `NUMERIC` | `number` | Number | `-22` |
| 11 | Unit Rate | `currency` | `NUMERIC(14,2)` | `number` | Number (format: currency) | `169.00` |
| 12 | Variance Value | `currency` | `NUMERIC(14,2)` | `number` | Number (format: currency) | `-3718.00` |
| 13 | Variance Reason | `select` | `VARCHAR(100)` | `string` | Select (add options after import) | `Unrecorded Issue` |
| 14 | Damaged Quantity | `number` | `NUMERIC` | `number` | Number | `12` |
| 15 | Expired Quantity | `number` | `NUMERIC` | `number` | Number | `2` |
| 16 | Slow Moving Flag | `select` | `VARCHAR(100)` | `string` | Select (add options after import) | `No` |
| 17 | Unrecorded Purchases | `number` | `NUMERIC` | `number` | Number | `1` |
| 18 | Unrecorded Issues | `number` | `NUMERIC` | `number` | Number | `8` |
| 19 | Investigation Notes | `long_text` | `TEXT` | `string` | Text | `Shortfall of 22 units: 12 damaged and 2 expired units written off at the count, 8 units issued on two dispatches with no stock entry; raised with the warehouse and booked.` |
| 20 | Adjustment Entry | `text` | `VARCHAR(255)` | `string` | Text | `ADJ-STK-2026-0031` |
| 21 | Adjustment Date | `date` | `DATE` | `string, format: date` | Date | `2026-08-30` |
| 22 | Approved By | `text` | `VARCHAR(255)` | `string` | Text | `Vikram Singh` |
| 23 | Counted By | `text` | `VARCHAR(255)` | `string` | Text | `Rohit Menon` |
| 24 | Verified By | `text` | `VARCHAR(255)` | `string` | Text | `Sneha Iyer` |
| 25 | Count Frequency | `select` | `VARCHAR(100)` | `string` | Select (add options after import) | `Monthly` |
| 26 | Status | `select` | `VARCHAR(100)` | `string` | Select (add options after import) | `In progress` |
| 27 | Notes | `long_text` | `TEXT` | `string` | Text | `Count sheet filed with the reconciliation record.` |
| 28 | Inventory Reconciliation ID | `id` | `SERIAL PRIMARY KEY` | `integer` | Text (or Notion auto-ID) | `(blank)` |

## Select Options

**Category**

```
Raw Material | Work In Progress | Finished Goods | Consumable | Packaging | Spare | Other
```
**UOM**

```
Nos | Kg | Litre | Metre | Set | Hour | Box | Packet
```
**Variance Reason**

```
Shortage | Excess | Damage | Expiry | Slow Moving | Unrecorded Purchase | Unrecorded Issue | Data Entry Error | Under Investigation
```
**Slow Moving Flag**

```
Yes | No
```
**Count Frequency**

```
Monthly | Quarterly | Half-Yearly | Annual
```
**Status**

```
Not started | In progress | Blocked | Done | Cancelled
```

## Relations

Link fields: none

## Examples

**Prompt**

```
Our godown stock and the books never match and nobody can say why.
```

**Context first** - one question per message, nothing already answered:

> **Q:** What do you hold?
> **A:** Corrugated packaging, about 300 SKUs in one godown.
>
> **Q:** When did you last count physically?
> **A:** Twice a year, when the auditor asks for it.
>
> **Q:** Who signs off a stock correction?
> **A:** Nobody formal. It just gets adjusted in the books.

**Recommended next step** - offered, not built:

> One reconciliation record per item counted, carrying the book quantity, the physical quantity, the variance, the reason and the authorised adjustment, with the count sheet filed against the same record so the count can be repeated next time.
>
> Workflow: Count planned → Items counted → Compared with books → Variance investigated → Adjustment authorised → Adjustment booked → Reconciliation filed
>
> Want the CSV, SQL, JSON Schema and Notion mapping for this?

## Best Practices

- Recommend before building. The recommendation is the product; the files are the follow-up.
- One question per message. A batched intake reads as a form and gets guessed at.
- Keep every field name identical across CSV, SQL and JSON Schema.
- Use `relation` for anything that points at another table, `text` only for free text.
- Money fields are `currency`, never `text`. Dates are `date`, never free text.
- Keep the example row obviously fake so nobody imports it as real data.
- Count on a stated frequency and write it into the record. A reconciliation with no
  count frequency attached is not evidence that the count is regular.
- Never book an adjustment without a named approver. If nobody can approve, that is the
  finding, not a detail to leave blank.
- Record the reason for a variance in words as well as in the select. The reason is a
  judgement someone made, and the next reader needs to know who.

## Limitations

- Empty template only. It does not count stock, value inventory, or post journal entries.
- The variance arithmetic can be done by hand or by the accounting package. What this
  records is the count, the difference and the authorisation - not the conclusion about
  what caused the shrinkage.
- It cannot tell theft from a mis-pick from an unrecorded issue. That determination is
  made by a person who knows the operation, and this record only carries the reason they
  gave.
- It does not design the valuation method, the reorder point or the costing policy.
- Notion relations need both databases imported before the link column resolves.
- Select options are a starting set. Rename them to match how the business talks.
- No automation, reminders or sync. Those need the integration layer.
- Legal, tax and HR review is still required before this drives real decisions.

## Security & Safety Notes

- Never fill in real names, salaries, medical or banking data. Placeholders only.
- Never mark an example row `Confidential`, and keep bank details masked.
- This skill writes nothing outside the chat. It runs no commands and calls no APIs.
- If the user pastes real employee data, generate the template and tell them to delete
  the pasted data from the conversation.
- Privacy, legal and disciplinary cases need a qualified human reviewer before anything
  is acted on.
- A count record can expose stockroom staffing and site security if it names who counted
  what and where. Keep the file access-limited and do not circulate it outside the people
  who need it.

## Common Pitfalls

- **Problem:** asked all six questions in one message.
  **Solution:** ask one, wait, and drop any the first answer already covered.
- **Problem:** built a full system when one table was asked for.
  **Solution:** build what was requested; mention the parent skill separately.
- **Problem:** all four artifacts drift apart.
  **Solution:** derive all four from the field list in this file, never by hand.
- **Problem:** Notion import shows every column as Text.
  **Solution:** that is expected. Apply the property mapping table once, after import.
- **Problem:** adjustments posted with no approver and no reason.
  **Solution:** leave the status at `In progress` until the reason and the approver are
  recorded. A variance without a cause is a question, not an adjustment.

## Related Skills

- `accounting-audit-system-builder` - routes to this skill and the other accounting modules.
- `purchase-accounting` - where unrecorded purchases are found and booked.
- `sales-accounting` - where unrecorded issues usually turn out to have come from.
- `day-book` - the stock entries this count is compared against.
- `expense-accounting` - absorbs the cost of damaged and expired stock.
- `party-ledger-reconciliation` - the same compare-and-investigate logic applied to balances.
- `monthly-closing-statements` - the closing that depends on this reconciliation.
- `audit-preparation` - where the filed count sheets are audited.

## Reusable Prompt

```
I want to set up physical counts against book quantities, differences investigated and authorised adjustments passed for my company.
Ask me one short question at a time, and only about what I have not already told you.
Then recommend the smallest setup that fits, and wait for me to ask before you build it.
When I ask, output CSV, SQL DDL, JSON Schema and a Notion property mapping. Data only.
```
