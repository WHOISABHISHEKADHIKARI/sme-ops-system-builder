---
name: tax-register
description: "Tax Register: context-first intake, then CSV, SQL, JSON Schema and Notion on request. One short question per message. Use for tax register."
category: business
risk: safe
source: self
source_type: self
date_added: "2026-09-26"
author: WHOISABHISHEKADHIKARI
tags: [sme, business, operations, database, csv, notion, sql, protect]
tools: []
---

# Tax Register

**What it is:** Tax collected, tax paid, withholding and filing deadlines per period.

## Overview

Works out the smallest useful **Tax Register** setup for the business in front of it, then
builds it only when asked. The default output is a short recommendation, not a
spreadsheet. Artifacts - CSV, SQL DDL, JSON Schema, Notion mapping - are produced on
request, from one field list so they cannot drift apart.

Layer: Layer 7: Protect. Fits: Starter stage. Table code: n/a.

## When to Use This Skill

- tax register
- gst tracker
- vat records
- tax filing calendar

Also use it when the user says "tax collected, tax paid, withholding and filing deadlines per period", or describes the same process happening in a
spreadsheet, a document or someone inboxes.

Do not use it for: payroll calculation, tax filing, or legal advice. This skill produces
empty templates only - it never holds or processes real employee or customer data.

## How It Works

Follow the [shared execution contract](../../references/execution-contract.md). The module-specific rules below define only domain fields, decisions, calculations, and safety constraints.

### Step 1 - Identify intent

Read the request and pick the intent before asking anything.

- "set up" or "build" or "create" -> the user wants artifacts; go to Step 2.
- "our process is ..." or "it is in a sheet" -> the user wants to move an existing process; capture it, then Step 2.
- "is this right" or "review" or "audit" -> the user wants a check, not a build; answer from what they share.
- "how do I ..." -> advice question; answer directly and offer the build only if it helps.

One message, one question, no batching. Open with:

> **Q:** Which taxes are you registered for?

### Step 2 - Ask only what is missing

Skip anything the user already answered, in any earlier message. Ask the rest one at a
time, and stop as soon as the remaining answers would not change the output.

- **Taxes** - Which taxes? / How many periods? / Which entities?
- **Data** - Invoice data available? / Where is it? / Any missing receipts?
- **Filing** - Who files? / Internal or accountant? / Deadlines recurring?
- **Current process** - Is it tracked now? / Accountant or spreadsheet? / What gets missed?
- **Outcome** - What do you need? / A register, a data extract or both?

Never invent an answer. If the user does not know, record it as unknown and carry on.

### Step 3 - Hold the internal context

Hold the answers in this shape. It stays internal - it is not shown to the user unless
they ask, and it never carries a value the user did not give.

```yaml
module: tax-register
intent: null            # set in Step 1, one of: set up, fix, review, report, import
scale: null             # Starter | Growth | Scale, only if the answer changes it
areas:
  "Taxes": null
  "Data": null
  "Filing": null
  "Current process": null
  "Outcome": null
requested_outputs: []   # csv | sql | json | notion - only what was explicitly asked for
confirmed_facts: []     # only what the user actually said
open_questions: []      # the unanswered ones, in the order worth asking
```

### Step 4 - Recommend the smallest workflow

Give a short recommendation, then ask whether to build it. Do not build unprompted. Ask: "Want me to build the CSV, SQL DDL, JSON Schema, Notion mapping, or an Excel workbook from these confirmed rules?"

**Recommended approach:** Keep the tax register as a record of periods, amounts and filing status, and let the accountant or filing tool do the calculation.

**Why this one:** Tax mistakes are calculation errors, and calculations belong in software. This should hold the record and the status, not the arithmetic.

**Workflow:** Period opened → Source data recorded → Amount entered → Filed → Reconciled

### Step 5 - Build only on request

Once the user asks for it, derive the fields from the confirmed context and emit the
artifacts as data only. No preamble, no summary, no closing line.

**Notion needs a connected workspace first.** When the user selects Notion as the
output, emit the connection prerequisite from the
[shared execution contract](../../references/execution-contract.md) verbatim before
the Notion mapping, then stop and wait for the reply "Notion connected." If the user
would rather not connect, emit the mapping as text, add one line saying it is
unverified until the workspace is connected, and offer
[notion-manual-import](../notion-manual-import/SKILL.md) for the full manual path.
Never claim a connection exists, and never ask for a Notion password or token.

For an Excel-compatible CSV, use UTF-8 with a byte order mark so Excel opens the
text correctly. A CSV is not an `.xlsx` workbook; create `.xlsx` only when the user
requests a workbook.
A CSV carries no types, so after it, name the columns
that need a number, date or currency format applied.

```csv
Tax Record,Tax Type,Tax Period,Period Start,Period End,Tax Collected on Sales,Tax Paid on Purchases,Withholding Tax Deducted,Withholding Tax Paid to Us,Net Tax Payable,Currency,Filing Due Date,Filed Date,Payment Date,Filing Reference,Prepared By,Reviewed By,Days to Due,Status,Notes,Tax ID
TAX-2026-03,GST,2026-03,2026-03-01,2026-03-31,354000.00,82000.00,2700.00,2700.00,272000.00,INR,2026-01-15,2026-01-15,2026-01-15,TAX-2026-03-Q1,Ananya Rao,Sneha Iyer,21,Filed,Filed with the accountant; working papers saved.,
```

```sql
CREATE TABLE tax_register (
  tax_record VARCHAR(255),
  tax_type VARCHAR(100) NOT NULL,
  tax_period VARCHAR(255),
  period_start DATE NOT NULL,
  period_end DATE NOT NULL,
  tax_collected_on_sales NUMERIC(14,2) NOT NULL,
  tax_paid_on_purchases NUMERIC(14,2) NOT NULL,
  withholding_tax_deducted NUMERIC(14,2) NOT NULL,
  withholding_tax_paid_to_us NUMERIC(14,2) NOT NULL,
  net_tax_payable NUMERIC(14,2) NOT NULL,
  currency VARCHAR(255),
  filing_due_date DATE NOT NULL,
  filed_date DATE NOT NULL,
  payment_date DATE NOT NULL,
  filing_reference VARCHAR(255),
  prepared_by VARCHAR(255),
  reviewed_by VARCHAR(255),
  days_to_due NUMERIC NOT NULL,
  status VARCHAR(100) NOT NULL,
  notes TEXT,
  tax_id SERIAL PRIMARY KEY,
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_tax_register_status ON tax_register (status);
```

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "Tax Register",
  "type": "object",
  "additionalProperties": false,
  "properties": {
      "Tax Record": { "type": "string" },
      "Tax Type": { "type": "string" },
      "Tax Period": { "type": "string" },
      "Period Start": { "type": "string", "format": "date" },
      "Period End": { "type": "string", "format": "date" },
      "Tax Collected on Sales": { "type": "number" },
      "Tax Paid on Purchases": { "type": "number" },
      "Withholding Tax Deducted": { "type": "number" },
      "Withholding Tax Paid to Us": { "type": "number" },
      "Net Tax Payable": { "type": "number" },
      "Currency": { "type": "string" },
      "Filing Due Date": { "type": "string", "format": "date" },
      "Filed Date": { "type": "string", "format": "date" },
      "Payment Date": { "type": "string", "format": "date" },
      "Filing Reference": { "type": "string" },
      "Prepared By": { "type": "string" },
      "Reviewed By": { "type": "string" },
      "Days to Due": { "type": "number" },
      "Status": { "type": "string" },
      "Notes": { "type": "string" },
      "Tax ID": { "type": "integer" }
  },
  "required": [
      "Tax Type",
      "Period Start",
      "Period End",
      "Tax Collected on Sales",
      "Tax Paid on Purchases",
      "Withholding Tax Deducted",
      "Withholding Tax Paid to Us",
      "Net Tax Payable",
      "Filing Due Date",
      "Filed Date",
      "Payment Date",
      "Days to Due",
      "Status"
  ]
}
```

```markdown
| CSV column | Notion property | Set after import |
|---|---|---|
| Tax Record | Text | Leave as Text |
| Tax Type | Select (add options after import) | Convert to Select, add options: "GST", "VAT", "TDS", "TCS", "Service Tax", "Income Tax", "Withholding" |
| Tax Period | Text | Leave as Text |
| Period Start | Date | Convert to Date |
| Period End | Date | Convert to Date |
| Tax Collected on Sales | Number (format: currency) | Convert to Number, set format to Currency |
| Tax Paid on Purchases | Number (format: currency) | Convert to Number, set format to Currency |
| Withholding Tax Deducted | Number (format: currency) | Convert to Number, set format to Currency |
| Withholding Tax Paid to Us | Number (format: currency) | Convert to Number, set format to Currency |
| Net Tax Payable | Number (format: currency) | Convert to Number, set format to Currency |
| Currency | Text | Leave as Text |
| Filing Due Date | Date | Convert to Date |
| Filed Date | Date | Convert to Date |
| Payment Date | Date | Convert to Date |
| Filing Reference | Text | Leave as Text |
| Prepared By | Text | Leave as Text |
| Reviewed By | Text | Leave as Text |
| Days to Due | Number | Convert to Number |
| Status | Select (add options after import) | Convert to Select, add options: "Draft", "Filed", "Paid", "Overdue", "Amended" |
| Notes | Text | Leave as Text |
| Tax ID | Text (or Notion auto-ID) | Delete the column and switch the primary column to auto-ID, or keep as Text |
```

The rows above are documentation examples only. Emit empty templates unless the user explicitly requests examples. Money stays `currency`, dates stay `date`,
and anything pointing at another table stays `relation`.

## Field Reference

| # | Field | Type | SQL | JSON Schema | Notion | CSV example |
|---:|---|---|---|---|---|---|
| 1 | Tax Record | `text` | `VARCHAR(255)` | `string` | Text | `TAX-2026-03` |
| 2 | Tax Type | `select` | `VARCHAR(100)` | `string` | Select (add options after import) | `GST` |
| 3 | Tax Period | `text` | `VARCHAR(255)` | `string` | Text | `2026-03` |
| 4 | Period Start | `date` | `DATE` | `string, format: date` | Date | `2026-03-01` |
| 5 | Period End | `date` | `DATE` | `string, format: date` | Date | `2026-03-31` |
| 6 | Tax Collected on Sales | `currency` | `NUMERIC(14,2)` | `number` | Number (format: currency) | `354000.00` |
| 7 | Tax Paid on Purchases | `currency` | `NUMERIC(14,2)` | `number` | Number (format: currency) | `82000.00` |
| 8 | Withholding Tax Deducted | `currency` | `NUMERIC(14,2)` | `number` | Number (format: currency) | `2700.00` |
| 9 | Withholding Tax Paid to Us | `currency` | `NUMERIC(14,2)` | `number` | Number (format: currency) | `2700.00` |
| 10 | Net Tax Payable | `currency` | `NUMERIC(14,2)` | `number` | Number (format: currency) | `272000.00` |
| 11 | Currency | `text` | `VARCHAR(255)` | `string` | Text | `INR` |
| 12 | Filing Due Date | `date` | `DATE` | `string, format: date` | Date | `2026-01-15` |
| 13 | Filed Date | `date` | `DATE` | `string, format: date` | Date | `2026-01-15` |
| 14 | Payment Date | `date` | `DATE` | `string, format: date` | Date | `2026-01-15` |
| 15 | Filing Reference | `text` | `VARCHAR(255)` | `string` | Text | `TAX-2026-03-Q1` |
| 16 | Prepared By | `text` | `VARCHAR(255)` | `string` | Text | `Ananya Rao` |
| 17 | Reviewed By | `text` | `VARCHAR(255)` | `string` | Text | `Sneha Iyer` |
| 18 | Days to Due | `number` | `NUMERIC` | `number` | Number | `21` |
| 19 | Status | `select` | `VARCHAR(100)` | `string` | Select (add options after import) | `Filed` |
| 20 | Notes | `long_text` | `TEXT` | `string` | Text | `Filed with the accountant; working papers saved.` |
| 21 | Tax ID | `id` | `SERIAL PRIMARY KEY` | `integer` | Text (or Notion auto-ID) | `(blank)` |

## Select Options

**Tax Type**

```
GST | VAT | TDS | TCS | Service Tax | Income Tax | Withholding
```
**Status**

```
Draft | Filed | Paid | Overdue | Amended
```

## Relations

Link fields: none

## Examples

**Prompt**

```
Our accountant asks for figures every quarter and we assemble them manually.
```

**Context first** - one question per message, nothing already answered:

> **Q:** Which taxes?
> **A:** VAT and corporation tax.
>
> **Q:** Who files?
> **A:** Our accountant.
>
> **Q:** Source data?
> **A:** Invoices, but not consistently.

**Recommended next step** - offered, not built:

> Keep the tax register as a record of periods, amounts and filing status, and let the accountant or filing tool do the calculation.
>
> Workflow: Period opened → Source data recorded → Amount entered → Filed → Reconciled
>
> Want the CSV, SQL, JSON Schema and Notion mapping for this?

## Best Practices

- Recommend before building. The recommendation is the product; the files are the follow-up.
- One question per message. A batched intake reads as a form and gets guessed at.
- Keep every field name identical across CSV, SQL and JSON Schema.
- Use `relation` for anything that points at another table, `text` only for free text.
- Money fields are `currency`, never `text`. Dates are `date`, never free text.
- If the user requests an example row, keep it obviously fake so nobody imports it as real data.

## Limitations

- Empty template only. It does not compute payroll, tax, leave balances or KPIs.
- Notion relations need both databases imported before the link column resolves.
- Select options are a starting set. Rename them to match how the business talks.
- No automation, reminders or sync. Those need the integration layer.
- Does not calculate tax, file returns or give tax advice.
- Legal, tax and HR review is still required before this drives real decisions.

## Security & Safety Notes

- Never fill in real names, salaries, medical or banking data. Placeholders only.
- Never mark an example row `Confidential`, and keep bank details masked.
- Creating a requested artifact may write that artifact locally. Do not run commands,
  call APIs, provision infrastructure, or make other external changes unless the user
  explicitly requests and authorizes them.
- If the user pastes real employee data, generate the template and tell them to delete
  the pasted data from the conversation.
- Privacy, legal and disciplinary cases need a qualified human reviewer before anything
  is acted on.

## Common Pitfalls

- **Problem:** the Notion mapping is handed over with no workspace connected.
  **Solution:** the connection prerequisite goes first, and a mapping handed over as
  text is labelled unverified until the workspace is connected.
- **Problem:** asked all six questions in one message.
  **Solution:** ask one, wait, and drop any the first answer already covered.
- **Problem:** built a full system when one table was asked for.
  **Solution:** build what was requested; mention the parent skill separately.
- **Problem:** all four artifacts drift apart.
  **Solution:** derive all four from the field list in this file, never by hand.
- **Problem:** Notion import shows every column as Text.
  **Solution:** that is expected. Apply the property mapping table once, after import.

## Related Skills

- [SME Ops System Builder](../../SKILL.md) - routes to this skill and the other 70 modules.
- [People Directory](../people-directory/SKILL.md) - the employee master record most modules link to.
- [Notification & Reminder Hub](../notification-reminder-hub/SKILL.md) - turns due dates in this module into reminders.

## Reusable Prompt

```
I want to set up tax collected, tax paid, withholding and filing deadlines per period for my company.
Ask me one short question at a time, and only about what I have not already told you.
Then recommend the smallest setup that fits, and wait for me to ask before you build it.
When I ask, output CSV, SQL DDL, JSON Schema, a Notion property mapping or an Excel workbook. Data only.
```

