---
name: accounting-software-selection
description: "Accounting Software Selection: context-first intake, then CSV, SQL, JSON Schema and Notion on request. One short question per message. Use for accounting software selection."
category: business
risk: safe
source: self
source_type: self
date_added: "2026-09-26"
author: WHOISABHISHEKADHIKARI
tags: [sme, accounting, audit, finance, database, csv, notion, sql, evaluation]
tools: [claude, cursor, gemini, antigravity]
---

# Accounting Software Selection

**What it is:** Scored evaluation of shortlisted accounting packages before one is chosen.

## Overview

Works out the smallest useful **Accounting Software Selection** setup for the business in front of it, then
builds it only when asked. The default output is a short recommendation, not a
spreadsheet. Artifacts - CSV, SQL DDL, JSON Schema, Notion mapping - are produced on
request, from one field list so they cannot drift apart.

Layer: Layer 1: Foundation. Fits: Growth stage. Table code: n/a.

## When to Use This Skill

- accounting software selection
- software comparison sheet
- vendor evaluation record
- accounting package quotation tracker

Also use it when the user says "scored evaluation of shortlisted accounting packages before one is chosen", or describes the same process happening in a
spreadsheet, a document or someone inboxes.

Do not use it for: day-to-day bookkeeping once the package is live, tax filing, or legal advice. This skill produces
empty templates only - it never holds or processes real employee or customer data.

## How It Works

### Step 1 - Identify intent

Read the request and pick the intent before asking anything.

- "set up" or "build" or "create" -> the user wants artifacts; go to Step 2.
- "our process is ..." or "it is in a sheet" -> the user wants to move an existing process; capture it, then Step 2.
- "is this right" or "review" or "audit" -> the user wants a check, not a build; answer from what they share.
- "how do I ..." -> advice question; answer directly and offer the build only if it helps.

One message, one question, no batching. Open with:

> **Q:** Which accounting packages are on your shortlist?

### Step 2 - Ask only what is missing

Skip anything the user already answered, in any earlier message. Ask the rest one at a
time, and stop as soon as the remaining answers would not change the output.

- **Business** - What does the business do? / How many people? / How many transactions a month?
- **Requirements** - Inventory needed? / VAT, TDS, payroll? / Which reports must come out?
- **Shortlist** - How many packages? / Demos seen or not yet? / Who evaluates?
- **Costs** - Quotations in hand? / Licence plus implementation? / Annual renewal known?
- **Outcome** - What do you need? / A comparison register, a go-live checklist or both?

Never invent an answer. If the user does not know, record it as unknown and carry on.

### Step 3 - Build the internal context

Hold the answers in this shape. It stays internal - it is not shown to the user unless
they ask, and it never carries a value the user did not give.

```yaml
module: accounting-software-selection
intent: null            # set in Step 1, one of: set up, fix, review, report, import
scale: null             # Starter | Growth | Scale, only if the answer changes it
areas:
  "Business": null
  "Requirements": null
  "Shortlist": null
  "Costs": null
  "Outcome": null
requested_outputs: []   # csv | sql | json | notion - only what was explicitly asked for
confirmed_facts: []     # only what the user actually said
open_questions: []      # the unanswered ones, in the order worth asking
```

### Step 4 - Recommend the smallest workflow

Give a short recommendation, then ask whether to build it. Do not build unprompted.

**Recommended approach:** One evaluation record per shortlisted package, scored on the same coverage, cost and support fields so the comparison is repeatable, plus a go-live configuration checklist built from the same record.

**Why this one:** Software decisions get argued on memory. Scoring every package on identical fields turns the argument into a table, and the same record then carries the go-live settings.

**Workflow:** Requirements listed → Package shortlisted → Demo tested → Scored → Recommended → Configured → Go-live

### Step 5 - Build only on request

Once the user asks for it, derive the fields from the confirmed context and emit the
artifacts as data only. No preamble, no summary, no closing line.

```csv
Software,Vendor,Modules Needed,Deployment Type,Accounting Coverage,Inventory Support,VAT Support,TDS Support,Payroll Support,Reporting Capability,Data Backup & Security,User Access Control,After-Sales Support,Reliability Rating,Ease of Use Rating,Support Quality Rating,Demo Date,Test Transactions Run,Quotation Amount,Implementation Fee,Annual Cost,Total Cost,Recommendation,Evaluated By,Notes,Selection ID
TallyPrime,Business Standard,"Accounting, Inventory, VAT, TDS, Payroll, Reporting",Cloud,Full,Full,Full,Partial,Missing,Full,Full,Full,Partial,4,5,4,2026-07-18,25,48000.00,15000.00,36000.00,99000.00,Shortlisted,Ananya Rao,"Payroll is a dealbreaker for us; asked the vendor for a module quote.",
```

```sql
CREATE TABLE accounting_software_selection (
  software VARCHAR(255),
  vendor VARCHAR(255),
  modules_needed TEXT,
  deployment_type VARCHAR(100) NOT NULL,
  accounting_coverage VARCHAR(100) NOT NULL,
  inventory_support VARCHAR(100) NOT NULL,
  vat_support VARCHAR(100) NOT NULL,
  tds_support VARCHAR(100) NOT NULL,
  payroll_support VARCHAR(100) NOT NULL,
  reporting_capability VARCHAR(100) NOT NULL,
  data_backup_security VARCHAR(100) NOT NULL,
  user_access_control VARCHAR(100) NOT NULL,
  after_sales_support VARCHAR(100) NOT NULL,
  reliability_rating NUMERIC,
  ease_of_use_rating NUMERIC,
  support_quality_rating NUMERIC,
  demo_date DATE NOT NULL,
  test_transactions_run NUMERIC,
  quotation_amount NUMERIC(14,2) NOT NULL,
  implementation_fee NUMERIC(14,2) NOT NULL,
  annual_cost NUMERIC(14,2) NOT NULL,
  total_cost NUMERIC(14,2) NOT NULL,
  recommendation VARCHAR(100) NOT NULL,
  evaluated_by VARCHAR(255),
  notes TEXT,
  selection_id SERIAL PRIMARY KEY,
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);
```

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "Accounting Software Selection",
  "type": "object",
  "additionalProperties": false,
  "properties": {
      "Software": { "type": "string" },
      "Vendor": { "type": "string" },
      "Modules Needed": { "type": "string" },
      "Deployment Type": { "type": "string" },
      "Accounting Coverage": { "type": "string" },
      "Inventory Support": { "type": "string" },
      "VAT Support": { "type": "string" },
      "TDS Support": { "type": "string" },
      "Payroll Support": { "type": "string" },
      "Reporting Capability": { "type": "string" },
      "Data Backup & Security": { "type": "string" },
      "User Access Control": { "type": "string" },
      "After-Sales Support": { "type": "string" },
      "Reliability Rating": { "type": "number" },
      "Ease of Use Rating": { "type": "number" },
      "Support Quality Rating": { "type": "number" },
      "Demo Date": { "type": "string", "format": "date" },
      "Test Transactions Run": { "type": "number" },
      "Quotation Amount": { "type": "number" },
      "Implementation Fee": { "type": "number" },
      "Annual Cost": { "type": "number" },
      "Total Cost": { "type": "number" },
      "Recommendation": { "type": "string" },
      "Evaluated By": { "type": "string" },
      "Notes": { "type": "string" },
      "Selection ID": { "type": "integer" }
  },
  "required": [
      "Deployment Type",
      "Accounting Coverage",
      "Inventory Support",
      "VAT Support",
      "TDS Support",
      "Payroll Support",
      "Reporting Capability",
      "Data Backup & Security",
      "User Access Control",
      "After-Sales Support",
      "Demo Date",
      "Quotation Amount",
      "Implementation Fee",
      "Annual Cost",
      "Total Cost",
      "Recommendation"
  ]
}
```

```markdown
| CSV column | Notion property | Set after import |
|---|---|---|
| Software | Text | Leave as Text |
| Vendor | Text | Leave as Text |
| Modules Needed | Text | Leave as Text |
| Deployment Type | Select (add options after import) | Convert to Select, add options: "Cloud", "On-premise", "Hybrid" |
| Accounting Coverage | Select (add options after import) | Convert to Select, add options: "Full", "Partial", "Missing" |
| Inventory Support | Select (add options after import) | Convert to Select, add options: "Full", "Partial", "Missing" |
| VAT Support | Select (add options after import) | Convert to Select, add options: "Full", "Partial", "Missing" |
| TDS Support | Select (add options after import) | Convert to Select, add options: "Full", "Partial", "Missing" |
| Payroll Support | Select (add options after import) | Convert to Select, add options: "Full", "Partial", "Missing" |
| Reporting Capability | Select (add options after import) | Convert to Select, add options: "Full", "Partial", "Missing" |
| Data Backup & Security | Select (add options after import) | Convert to Select, add options: "Full", "Partial", "Missing" |
| User Access Control | Select (add options after import) | Convert to Select, add options: "Full", "Partial", "Missing" |
| After-Sales Support | Select (add options after import) | Convert to Select, add options: "Full", "Partial", "Missing" |
| Reliability Rating | Number | Convert to Number |
| Ease of Use Rating | Number | Convert to Number |
| Support Quality Rating | Number | Convert to Number |
| Demo Date | Date | Convert to Date |
| Test Transactions Run | Number | Convert to Number |
| Quotation Amount | Number (format: currency) | Convert to Number, set format to Currency |
| Implementation Fee | Number (format: currency) | Convert to Number, set format to Currency |
| Annual Cost | Number (format: currency) | Convert to Number, set format to Currency |
| Total Cost | Number (format: currency) | Convert to Number, set format to Currency |
| Recommendation | Select (add options after import) | Convert to Select, add options: "Selected", "Shortlisted", "Rejected", "Rejected - Cost", "Rejected - Capability" |
| Evaluated By | Text | Leave as Text |
| Notes | Text | Leave as Text |
| Selection ID | Text (or Notion auto-ID) | Delete the column and switch the primary column to auto-ID, or keep as Text |
```

One example row per artifact, visibly fake. Money stays `currency`, dates stay `date`,
and anything pointing at another table stays `relation`.

## Field Reference

| # | Field | Type | SQL | JSON Schema | Notion | CSV example |
|---:|---|---|---|---|---|---|
| 1 | Software | `text` | `VARCHAR(255)` | `string` | Text | `TallyPrime` |
| 2 | Vendor | `text` | `VARCHAR(255)` | `string` | Text | `Business Standard` |
| 3 | Modules Needed | `long_text` | `TEXT` | `string` | Text | `Accounting, Inventory, VAT, TDS, Payroll, Reporting` |
| 4 | Deployment Type | `select` | `VARCHAR(100)` | `string` | Select (add options after import) | `Cloud` |
| 5 | Accounting Coverage | `select` | `VARCHAR(100)` | `string` | Select (add options after import) | `Full` |
| 6 | Inventory Support | `select` | `VARCHAR(100)` | `string` | Select (add options after import) | `Full` |
| 7 | VAT Support | `select` | `VARCHAR(100)` | `string` | Select (add options after import) | `Full` |
| 8 | TDS Support | `select` | `VARCHAR(100)` | `string` | Select (add options after import) | `Partial` |
| 9 | Payroll Support | `select` | `VARCHAR(100)` | `string` | Select (add options after import) | `Missing` |
| 10 | Reporting Capability | `select` | `VARCHAR(100)` | `string` | Select (add options after import) | `Full` |
| 11 | Data Backup & Security | `select` | `VARCHAR(100)` | `string` | Select (add options after import) | `Full` |
| 12 | User Access Control | `select` | `VARCHAR(100)` | `string` | Select (add options after import) | `Full` |
| 13 | After-Sales Support | `select` | `VARCHAR(100)` | `string` | Select (add options after import) | `Partial` |
| 14 | Reliability Rating | `number` | `NUMERIC` | `number` | Number | `4` |
| 15 | Ease of Use Rating | `number` | `NUMERIC` | `number` | Number | `5` |
| 16 | Support Quality Rating | `number` | `NUMERIC` | `number` | Number | `4` |
| 17 | Demo Date | `date` | `DATE` | `string, format: date` | Date | `2026-07-18` |
| 18 | Test Transactions Run | `number` | `NUMERIC` | `number` | Number | `25` |
| 19 | Quotation Amount | `currency` | `NUMERIC(14,2)` | `number` | Number (format: currency) | `48000.00` |
| 20 | Implementation Fee | `currency` | `NUMERIC(14,2)` | `number` | Number (format: currency) | `15000.00` |
| 21 | Annual Cost | `currency` | `NUMERIC(14,2)` | `number` | Number (format: currency) | `36000.00` |
| 22 | Total Cost | `currency` | `NUMERIC(14,2)` | `number` | Number (format: currency) | `99000.00` |
| 23 | Recommendation | `select` | `VARCHAR(100)` | `string` | Select (add options after import) | `Shortlisted` |
| 24 | Evaluated By | `text` | `VARCHAR(255)` | `string` | Text | `Ananya Rao` |
| 25 | Notes | `long_text` | `TEXT` | `string` | Text | `Payroll is a dealbreaker for us; asked the vendor for a module quote.` |
| 26 | Selection ID | `id` | `SERIAL PRIMARY KEY` | `integer` | Text (or Notion auto-ID) | `(blank)` |

## Select Options

**Deployment Type**

```
Cloud | On-premise | Hybrid
```
**Accounting Coverage**

```
Full | Partial | Missing
```
**Inventory Support**

```
Full | Partial | Missing
```
**VAT Support**

```
Full | Partial | Missing
```
**TDS Support**

```
Full | Partial | Missing
```
**Payroll Support**

```
Full | Partial | Missing
```
**Reporting Capability**

```
Full | Partial | Missing
```
**Data Backup & Security**

```
Full | Partial | Missing
```
**User Access Control**

```
Full | Partial | Missing
```
**After-Sales Support**

```
Full | Partial | Missing
```
**Recommendation**

```
Selected | Shortlisted | Rejected | Rejected - Cost | Rejected - Capability
```

## Relations

Link fields: none

## Examples

**Prompt**

```
We are replacing Tally and cannot tell which package actually covers payroll.
```

**Context first** - one question per message, nothing already answered:

> **Q:** Which packages are on the shortlist?
> **A:** TallyPrime and one cloud package.
>
> **Q:** Is payroll a must-have?
> **A:** Yes, it is the sticking point.
>
> **Q:** Quotations in hand?
> **A:** One so far.

**Recommended next step** - offered, not built:

> One evaluation record per shortlisted package, scored on the same coverage, cost and support fields so the comparison is repeatable, plus a go-live configuration checklist built from the same record.
>
> Workflow: Requirements listed → Package shortlisted → Demo tested → Scored → Recommended → Configured → Go-live
>
> Want the CSV, SQL, JSON Schema and Notion mapping for this?

## Best Practices

- Recommend before building. The recommendation is the product; the files are the follow-up.
- One question per message. A batched intake reads as a form and gets guessed at.
- Keep every field name identical across CSV, SQL and JSON Schema.
- Use `relation` for anything that points at another table, `text` only for free text.
- Money fields are `currency`, never `text`. Dates are `date`, never free text.
- Keep the example row obviously fake so nobody imports it as real data.

## Limitations

- Empty template only. It does not score for you, test the software or compute TCO.
- Does not choose the software and does not configure a live system. Go-live settings - chart of
  accounts, tax configuration, users, inventory, opening balances, test entry - are a checklist
  the business carries out with the vendor, not something this skill does.
- Notion relations need both databases imported before the link column resolves.
- Select options are a starting set. Rename them to match how the business talks.
- No automation, reminders or sync. Those need the integration layer.
- Does not procure licences or give vendor or legal advice.
- Legal, tax and HR review is still required before this drives real decisions.

## Security & Safety Notes

- Never fill in real names, salaries, medical or banking data. Placeholders only.
- Never mark an example row `Confidential`, and keep bank details masked.
- This skill writes nothing outside the chat. It runs no commands and calls no APIs.
- If the user pastes real employee data, generate the template and tell them to delete
  the pasted data from the conversation.
- Privacy, legal and disciplinary cases need a qualified human reviewer before anything
  is acted on.

## Common Pitfalls

- **Problem:** asked all six questions in one message.
  **Solution:** ask one, wait, and drop any the first answer already covered.
- **Problem:** built a full system when one table was asked for.
  **Solution:** build what was requested; mention the parent skill separately.
- **Problem:** all four artifacts drift apart.
  **Solution:** derive all four from the field list in this file, never by hand.
- **Problem:** Notion import shows every column as Text.
  **Solution:** that is expected. Apply the property mapping table once, after import.

## Related Skills

- `accounting-audit-system-builder` - routes to this skill and the other accounting modules.
- `purchase-accounting` - the entry flow the chosen package has to support.
- `sales-accounting` - the entry flow the chosen package has to support.
- `salary-wage-accounting` - the payroll module being evaluated here.
- `tds-booking-payment` - the withholding module being evaluated here.
- `monthly-closing-statements` - the reporting output being evaluated here.

## Reusable Prompt

```
I want to set up scored evaluation of shortlisted accounting packages before one is chosen for my company.
Ask me one short question at a time, and only about what I have not already told you.
Then recommend the smallest setup that fits, and wait for me to ask before you build it.
When I ask, output CSV, SQL DDL, JSON Schema and a Notion property mapping. Data only.
```
