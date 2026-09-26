---
name: credit-cycle-analysis
description: "Debtor & Creditor Credit-Cycle Analysis: context-first intake, then CSV, SQL, JSON Schema and Notion on request. One short question per message. Use for credit cycle analysis."
category: business
risk: safe
source: self
source_type: self
date_added: "2026-09-26"
author: WHOISABHISHEKADHIKARI
tags: [sme, accounting, audit, finance, database, csv, notion, sql, working-capital]
tools: [claude, cursor, gemini, antigravity]
---

# Debtor & Creditor Credit-Cycle Analysis

**What it is:** How long the business waits to be paid and how long it takes to pay, measured per party.

## Overview

Works out the smallest useful **Debtor & Creditor Credit-Cycle Analysis** setup for the business in front of it, then
builds it only when asked. The default output is a short recommendation, not a
spreadsheet. Artifacts - CSV, SQL DDL, JSON Schema, Notion mapping - are produced on
request, from one field list so they cannot drift apart.

The SOP rule this skill is built around: analyse debtors on the average collection
period, outstanding invoices, overdue receivables and the aging of receivables; analyse
creditors on the average payment period, outstanding supplier balances, overdue payables
and supplier aging; then compare the debtor collection cycle with the creditor payment
cycle to assess the working-capital position. The comparison is the point. Two cycles
measured the same way can be read against each other, and where the debtor cycle is
longer than the creditor cycle, the difference between them is what the business funds
itself with. That gap is the working-capital drag, and it does not appear anywhere on the
balance sheet.

Layer: Layer 8: Close & Analyse. Fits: Growth stage. Table code: n/a.

## When to Use This Skill

- debtor collection analysis
- creditor payment analysis
- average collection period tracker
- supplier aging analysis
- working capital cycle review

Also use it when the user says "how long the business waits to be paid and how long it takes to pay, measured per party", or describes the same process happening in a
spreadsheet, a document or someone inboxes.

Do not use it for: credit control action, collections chasing, or legal advice. This skill produces
empty templates only - it never holds or processes real employee or customer data.

## How It Works

### Step 1 - Identify intent

Read the request and pick the intent before asking anything.

- "set up" or "build" or "create" -> the user wants artifacts; go to Step 2.
- "our process is ..." or "it is in a sheet" -> the user wants to move an existing process; capture it, then Step 2.
- "is this right" or "review" or "audit" -> the user wants a check, not a build; answer from what they share.
- "how do I ..." -> advice question; answer directly and offer the build only if it helps.

One message, one question, no batching. Open with:

> **Q:** How long do your customers take to pay you today, and how long do you take to pay suppliers?

### Step 2 - Ask only what is missing

Skip anything the user already answered, in any earlier message. Ask the rest one at a
time, and stop as soon as the remaining answers would not change the output.

- **Parties** - Debtors and creditors both? / How many of each? / Any credit limits set?
- **Cycles** - Payment terms in days? / Cycle measured today? / Who measures it?
- **Aging** - Aging buckets in use? / How is overdue chased? / Who chases?
- **Current process** - Any report today? / Spreadsheet or accounting package? / What gets missed?
- **Outcome** - What do you need? / A cycle analysis, a working-capital view or both?

Never invent an answer. If the user does not know, record it as unknown and carry on.

### Step 3 - Build the internal context

Hold the answers in this shape. It stays internal - it is not shown to the user unless
they ask, and it never carries a value the user did not give.

```yaml
module: credit-cycle-analysis
intent: null            # set in Step 1, one of: set up, fix, review, report, import
scale: null             # Starter | Growth | Scale, only if the answer changes it
areas:
  "Parties": null
  "Cycles": null
  "Aging": null
  "Current process": null
  "Outcome": null
requested_outputs: []   # csv | sql | json | notion - only what was explicitly asked for
confirmed_facts: []     # only what the user actually said
open_questions: []      # the unanswered ones, in the order worth asking
```

### Step 4 - Recommend the smallest workflow

Give a short recommendation, then ask whether to build it. Do not build unprompted.

**Recommended approach:** One analysis record per party per period, in the same shape for debtors and for creditors, so the collection cycle and the payment cycle can be read side by side and the difference between them priced as working capital.

**Why this one:** The two cycles are only worth comparing if they are measured identically, and a single record shape is the only way to guarantee that. Once both sides sit in the same fields, the question the business actually has - am I waiting longer than I wait - becomes a subtraction instead of an argument, and the gap can be quantified in money rather than adjectives.

**Workflow:** Party selected → Period movement recorded → Cycle days measured → Overdue and aging reviewed → Compared against the other side → Gap priced as working capital → Trend recorded → Reviewed

### Step 5 - Build only on request

Once the user asks for it, derive the fields from the confirmed context and emit the
artifacts as data only. No preamble, no summary, no closing line.

```csv
Analysis Number,Period Start,Period End,Party Type,Party Name,Opening Balance,Total Billed,Total Collected/Paid,Closing Balance,Average Balance,Average Collection/Payment Days,Weighted Days,Overdue Amount,Aging Bucket,Credit Limit,Credit Utilisation %,Benchmark Days,Gap vs Benchmark,Working Capital Impact,Cycle Trend,Reviewed By,Status,Notes,Cycle Analysis ID
CC-2026-08,2026-08-01,2026-08-31,Customer/Debtor,Greyson Foods,420000.00,114000.00,47800.00,486200.00,453100.00,42,38,131829.60,31-60 days,500000.00,97,30,8,51000.00,Deteriorating,Sneha Iyer,Done,Collection is slower than the creditor payment cycle; working capital is absorbing the gap.,
```

```sql
CREATE TABLE credit_cycle_analysis (
  analysis_number VARCHAR(255),
  period_start DATE NOT NULL,
  period_end DATE NOT NULL,
  party_type VARCHAR(100) NOT NULL,
  party_name VARCHAR(255),
  opening_balance NUMERIC(14,2) NOT NULL,
  total_billed NUMERIC(14,2) NOT NULL,
  total_collected_paid NUMERIC(14,2) NOT NULL,
  closing_balance NUMERIC(14,2) NOT NULL,
  average_balance NUMERIC(14,2),
  average_collection_payment_days NUMERIC,
  weighted_days NUMERIC,
  overdue_amount NUMERIC(14,2),
  aging_bucket VARCHAR(100) NOT NULL,
  credit_limit NUMERIC(14,2),
  credit_utilisation NUMERIC,
  benchmark_days NUMERIC,
  gap_vs_benchmark NUMERIC,
  working_capital_impact NUMERIC(14,2),
  cycle_trend VARCHAR(100) NOT NULL,
  reviewed_by VARCHAR(255),
  status VARCHAR(100) NOT NULL,
  notes TEXT,
  cycle_analysis_id SERIAL PRIMARY KEY,
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_credit_cycle_analysis_status ON credit_cycle_analysis (status);
```

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "Debtor & Creditor Credit-Cycle Analysis",
  "type": "object",
  "additionalProperties": false,
  "properties": {
      "Analysis Number": { "type": "string" },
      "Period Start": { "type": "string", "format": "date" },
      "Period End": { "type": "string", "format": "date" },
      "Party Type": { "type": "string" },
      "Party Name": { "type": "string" },
      "Opening Balance": { "type": "number" },
      "Total Billed": { "type": "number" },
      "Total Collected/Paid": { "type": "number" },
      "Closing Balance": { "type": "number" },
      "Average Balance": { "type": "number" },
      "Average Collection/Payment Days": { "type": "number" },
      "Weighted Days": { "type": "number" },
      "Overdue Amount": { "type": "number" },
      "Aging Bucket": { "type": "string" },
      "Credit Limit": { "type": "number" },
      "Credit Utilisation %": { "type": "number" },
      "Benchmark Days": { "type": "number" },
      "Gap vs Benchmark": { "type": "number" },
      "Working Capital Impact": { "type": "number" },
      "Cycle Trend": { "type": "string" },
      "Reviewed By": { "type": "string" },
      "Status": { "type": "string" },
      "Notes": { "type": "string" },
      "Cycle Analysis ID": { "type": "integer" }
  },
  "required": [
      "Period Start",
      "Period End",
      "Party Type",
      "Opening Balance",
      "Total Billed",
      "Total Collected/Paid",
      "Closing Balance",
      "Aging Bucket",
      "Cycle Trend",
      "Status"
  ]
}
```

```markdown
| CSV column | Notion property | Set after import |
|---|---|---|
| Analysis Number | Text | Leave as Text |
| Period Start | Date | Convert to Date |
| Period End | Date | Convert to Date |
| Party Type | Select (add options after import) | Convert to Select, add options: "Customer/Debtor", "Supplier/Creditor" |
| Party Name | Text | Leave as Text |
| Opening Balance | Number (format: currency) | Convert to Number, set format to Currency |
| Total Billed | Number (format: currency) | Convert to Number, set format to Currency |
| Total Collected/Paid | Number (format: currency) | Convert to Number, set format to Currency |
| Closing Balance | Number (format: currency) | Convert to Number, set format to Currency |
| Average Balance | Number (format: currency) | Convert to Number, set format to Currency |
| Average Collection/Payment Days | Number | Convert to Number |
| Weighted Days | Number | Convert to Number |
| Overdue Amount | Number (format: currency) | Convert to Number, set format to Currency |
| Aging Bucket | Select (add options after import) | Convert to Select, add options: "Current", "0-30 days", "31-60 days", "61-90 days", "91-180 days", "180+ days" |
| Credit Limit | Number (format: currency) | Convert to Number, set format to Currency |
| Credit Utilisation % | Number | Convert to Number |
| Benchmark Days | Number | Convert to Number |
| Gap vs Benchmark | Number | Convert to Number |
| Working Capital Impact | Number (format: currency) | Convert to Number, set format to Currency |
| Cycle Trend | Select (add options after import) | Convert to Select, add options: "Improving", "Stable", "Deteriorating" |
| Reviewed By | Text | Leave as Text |
| Status | Select (add options after import) | Convert to Select, add options: "Not started", "In progress", "Blocked", "Done", "Cancelled" |
| Notes | Text | Leave as Text |
| Cycle Analysis ID | Text (or Notion auto-ID) | Delete the column and switch the primary column to auto-ID, or keep as Text |
```

One example row per artifact, visibly fake. Money stays `currency`, dates stay `date`,
and anything pointing at another table stays `relation`.

## Field Reference

| # | Field | Type | SQL | JSON Schema | Notion | CSV example |
|---:|---|---|---|---|---|---|
| 1 | Analysis Number | `text` | `VARCHAR(255)` | `string` | Text | `CC-2026-08` |
| 2 | Period Start | `date` | `DATE` | `string, format: date` | Date | `2026-08-01` |
| 3 | Period End | `date` | `DATE` | `string, format: date` | Date | `2026-08-31` |
| 4 | Party Type | `select` | `VARCHAR(100)` | `string` | Select (add options after import) | `Customer/Debtor` |
| 5 | Party Name | `text` | `VARCHAR(255)` | `string` | Text | `Greyson Foods` |
| 6 | Opening Balance | `currency` | `NUMERIC(14,2)` | `number` | Number (format: currency) | `420000.00` |
| 7 | Total Billed | `currency` | `NUMERIC(14,2)` | `number` | Number (format: currency) | `114000.00` |
| 8 | Total Collected/Paid | `currency` | `NUMERIC(14,2)` | `number` | Number (format: currency) | `47800.00` |
| 9 | Closing Balance | `currency` | `NUMERIC(14,2)` | `number` | Number (format: currency) | `486200.00` |
| 10 | Average Balance | `currency` | `NUMERIC(14,2)` | `number` | Number (format: currency) | `453100.00` |
| 11 | Average Collection/Payment Days | `number` | `NUMERIC` | `number` | Number | `42` |
| 12 | Weighted Days | `number` | `NUMERIC` | `number` | Number | `38` |
| 13 | Overdue Amount | `currency` | `NUMERIC(14,2)` | `number` | Number (format: currency) | `131829.60` |
| 14 | Aging Bucket | `select` | `VARCHAR(100)` | `string` | Select (add options after import) | `31-60 days` |
| 15 | Credit Limit | `currency` | `NUMERIC(14,2)` | `number` | Number (format: currency) | `500000.00` |
| 16 | Credit Utilisation % | `number` | `NUMERIC` | `number` | Number | `97` |
| 17 | Benchmark Days | `number` | `NUMERIC` | `number` | Number | `30` |
| 18 | Gap vs Benchmark | `number` | `NUMERIC` | `number` | Number | `8` |
| 19 | Working Capital Impact | `currency` | `NUMERIC(14,2)` | `number` | Number (format: currency) | `51000.00` |
| 20 | Cycle Trend | `select` | `VARCHAR(100)` | `string` | Select (add options after import) | `Deteriorating` |
| 21 | Reviewed By | `text` | `VARCHAR(255)` | `string` | Text | `Sneha Iyer` |
| 22 | Status | `select` | `VARCHAR(100)` | `string` | Select (add options after import) | `Done` |
| 23 | Notes | `long_text` | `TEXT` | `string` | Text | `Collection is slower than the creditor payment cycle; working capital is absorbing the gap.` |
| 24 | Cycle Analysis ID | `id` | `SERIAL PRIMARY KEY` | `integer` | Text (or Notion auto-ID) | `(blank)` |

## Select Options

**Party Type**

```
Customer/Debtor | Supplier/Creditor
```
**Aging Bucket**

```
Current | 0-30 days | 31-60 days | 61-90 days | 91-180 days | 180+ days
```
**Cycle Trend**

```
Improving | Stable | Deteriorating
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
We are profitable on paper but cash is always tight and we cannot say why.
```

**Context first** - one question per message, nothing already answered:

> **Q:** How long do customers take to pay?
> **A:** Terms are 30 days, but the big ones take about six weeks.
>
> **Q:** And suppliers?
> **A:** Most of them are 45 days and they are strict about it.
>
> **Q:** Do you track it anywhere today?
> **A:** No. We just look at the bank balance and hope.

**Recommended next step** - offered, not built:

> One analysis record per party per period, in the same shape for debtors and for creditors, so the collection cycle and the payment cycle can be read side by side and the difference between them priced as working capital.
>
> Workflow: Party selected → Period movement recorded → Cycle days measured → Overdue and aging reviewed → Compared against the other side → Gap priced as working capital → Trend recorded → Reviewed
>
> Want the CSV, SQL, JSON Schema and Notion mapping for this?

## Best Practices

- Recommend before building. The recommendation is the product; the files are the follow-up.
- One question per message. A batched intake reads as a form and gets guessed at.
- Keep every field name identical across CSV, SQL and JSON Schema.
- Use `relation` for anything that points at another table, `text` only for free text.
- Money fields are `currency`, never `text`. Dates are `date`, never free text.
- Keep the example row obviously fake so nobody imports it as real data.
- Measure debtors and creditors in the same record shape, always. Two different shapes
  produce two numbers that cannot be subtracted, and the comparison is the whole point.
- Set a benchmark in days and hold it. Without one, a 42 day cycle looks acceptable in
  isolation and alarming next to a 34 day payment cycle.
- Record the trend against the same period last time. A cycle that is lengthening is a
  different problem from one that is simply long.

## Limitations

- Empty template only. It does not calculate collection periods, chase anyone, or set a
  credit limit. The days and the money on each row are the ones the business entered.
- It measures the gap; it does not close it. Deciding whether to tighten terms, call
  earlier or use a credit note is a commercial decision, not a record.
- A cycle measured from a ledger is only as good as the ledger. Reconciled party
  balances first, or the days will be precise and wrong.
- Overdue amounts depend on due dates being recorded against every invoice. Where they
  are not, aging buckets are guesses.
- It does not cover retention, factoring, bill discounting or foreign currency
  settlement timing. Those need their own treatment.
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
- A cycle analysis names customers and suppliers alongside how badly each is paying.
  Treat it as commercially sensitive and do not share it outside the finance function.

## Common Pitfalls

- **Problem:** asked all six questions in one message.
  **Solution:** ask one, wait, and drop any the first answer already covered.
- **Problem:** built a full system when one table was asked for.
  **Solution:** build what was requested; mention the parent skill separately.
- **Problem:** all four artifacts drift apart.
  **Solution:** derive all four from the field list in this file, never by hand.
- **Problem:** Notion import shows every column as Text.
  **Solution:** that is expected. Apply the property mapping table once, after import.
- **Problem:** debtors measured one way and creditors another, then compared.
  **Solution:** same period, same record, same calculation. If the basis differs, the
  difference between the two cycles is meaningless.
- **Problem:** closing balance does not equal opening plus billed less collected.
  **Solution:** the movement fields must agree before any days figure is read from them.

## Related Skills

- `accounting-audit-system-builder` - routes to this skill and the other accounting modules.
- `party-ledger-reconciliation` - agree the balances before measuring the cycle.
- `sales-accounting` - where the billed side of the debtor cycle is recorded.
- `purchase-accounting` - where the payable side of the creditor cycle is recorded.
- `receipt-accounting` - the collections that shorten the debtor cycle.
- `payment-accounting` - the payments that set the creditor cycle.
- `day-book` - cash movement behind both cycles.
- `monthly-closing-statements` - the receivables and payables review this measures.
- `petty-cash-management` - the small working-capital swings this sits alongside.

## Reusable Prompt

```
I want to set up how long the business waits to be paid and how long it takes to pay, measured per party for my company.
Ask me one short question at a time, and only about what I have not already told you.
Then recommend the smallest setup that fits, and wait for me to ask before you build it.
When I ask, output CSV, SQL DDL, JSON Schema and a Notion property mapping. Data only.
```
