---
name: payroll-finance
description: "Payroll & Finance: context-first intake, then CSV, SQL, JSON Schema and Notion on request. One short question per message. Use for payroll tracker."
category: business
risk: safe
source: self
source_type: self
date_added: "2026-09-26"
author: WHOISABHISHEKADHIKARI
tags: [sme, business, operations, database, csv, notion, sql, manage]
tools: [claude, cursor, gemini, antigravity]
---

# Payroll & Finance

**What it is:** Compensation.

## Overview

Works out the smallest useful **Payroll & Finance** setup for the business in front of it, then
builds it only when asked. The default output is a short recommendation, not a
spreadsheet. Artifacts - CSV, SQL DDL, JSON Schema, Notion mapping - are produced on
request, from one field list so they cannot drift apart.

Layer: Layer 4: Manage. Fits: Starter stage. Table code: n/a.

## When to Use This Skill

- payroll tracker
- salary register
- payroll sheet template
- monthly payroll log

Also use it when the user says "compensation", or describes the same process happening in a
spreadsheet, a document or someone inboxes.

Do not use it for: payroll calculation, tax filing, or legal advice. This skill produces
empty templates only - it never holds or processes real employee or customer data.

## How It Works

### Step 1 - Identify intent

Read the request and pick the intent before asking anything.

- "set up" or "build" or "create" -> the user wants artifacts; go to Step 2.
- "our process is ..." or "it is in a sheet" -> the user wants to move an existing process; capture it, then Step 2.
- "is this right" or "review" or "audit" -> the user wants a check, not a build; answer from what they share.
- "how do I ..." -> advice question; answer directly and offer the build only if it helps.

One message, one question, no batching. Open with:

> **Q:** How many people are on payroll?

### Step 2 - Ask only what is missing

Skip anything the user already answered, in any earlier message. Ask the rest one at a
time, and stop as soon as the remaining answers would not change the output.

- **Payroll** - How many people? / Monthly payslip? / Variable pay?
- **Components** - Which allowances? / Deductions? / Bonus included?
- **Process** - Who runs it? / Accountant or in-house? / When is cut-off?
- **Current process** - How is payroll done now? / Software or manual? / What gets missed?
- **Outcome** - What do you need? / A register, a calculation or an input feed?

Never invent an answer. If the user does not know, record it as unknown and carry on.

### Step 3 - Hold the internal context

Hold the answers in this shape. It stays internal - it is not shown to the user unless
they ask, and it never carries a value the user did not give.

```yaml
module: payroll-finance
intent: null            # set in Step 1, one of: set up, fix, review, report, import
scale: null             # Starter | Growth | Scale, only if the answer changes it
areas:
  "Payroll": null
  "Components": null
  "Process": null
  "Current process": null
  "Outcome": null
requested_outputs: []   # csv | sql | json | notion - only what was explicitly asked for
confirmed_facts: []     # only what the user actually said
open_questions: []      # the unanswered ones, in the order worth asking
```

### Step 4 - Recommend the smallest workflow

Give a short recommendation, then ask whether to build it. Do not build unprompted. Ask: "Want me to build the CSV, SQL DDL, JSON Schema, Notion mapping, or an Excel workbook from these confirmed rules?"

**Recommended approach:** Treat payroll as an input record for finance, not a calculator. If you need calculation, use payroll software and record the result.

**Why this one:** Payroll is high-risk to compute by hand and cheap to record. Keep this as the register, and let software do the arithmetic.

**Workflow:** Payroll input → Validation → Payroll run → Register update → Finance and tax

### Step 5 - Build only on request

Once the user asks for it, derive the fields from the confirmed context and emit the
artifacts as data only. No preamble, no summary, no closing line.

An Excel workbook is the CSV emitted with a UTF-8 byte order mark, so Excel opens it with
correct text and no import dialog. A CSV carries no types, so after it, name the columns
that need a number, date or currency format applied.

```csv
Payroll Record,Basic Salary,Bonus,Currency,DA (Dearness Allowance),Deductions,Department,Employee Name,HRA,Month,Net Pay,Notes,Pay Period,Payment Date,Payment Method,Payroll ID,Status,TA (Travel Allowance),Year
PAY-2026-03,650000.00,97500.00,INR,14500.00,82500.00,Delivery,Aarav Sharma,260000.00,2026-03,958700.00,February run reconciled with the accountant; one deduction code was mapped to the wrong head.,2026-03,2026-04-07,Bank Transfer,,Paid,19200.00,2026
```

```sql
CREATE TABLE payroll_finance (
  payroll_record VARCHAR(255),
  basic_salary NUMERIC(14,2) NOT NULL,
  bonus NUMERIC(14,2) NOT NULL,
  currency VARCHAR(255),
  da_dearness_allowance VARCHAR(255),
  deductions NUMERIC(14,2) NOT NULL,
  department VARCHAR(255),
  employee_name VARCHAR(255),
  hra NUMERIC(14,2) NOT NULL,
  month VARCHAR(255),
  net_pay NUMERIC(14,2) NOT NULL,
  notes TEXT,
  pay_period VARCHAR(255),
  payment_date DATE NOT NULL,
  payment_method VARCHAR(100) NOT NULL,
  payroll_id SERIAL PRIMARY KEY,
  status VARCHAR(100) NOT NULL,
  ta_travel_allowance NUMERIC(14,2) NOT NULL,
  year VARCHAR(255),
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_payroll_finance_status ON payroll_finance (status);
```

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "Payroll & Finance",
  "type": "object",
  "additionalProperties": false,
  "properties": {
      "Payroll Record": { "type": "string" },
      "Basic Salary": { "type": "number" },
      "Bonus": { "type": "number" },
      "Currency": { "type": "string" },
      "DA (Dearness Allowance)": { "type": "string" },
      "Deductions": { "type": "number" },
      "Department": { "type": "string" },
      "Employee Name": { "type": "string" },
      "HRA": { "type": "number" },
      "Month": { "type": "string" },
      "Net Pay": { "type": "number" },
      "Notes": { "type": "string" },
      "Pay Period": { "type": "string" },
      "Payment Date": { "type": "string", "format": "date" },
      "Payment Method": { "type": "string" },
      "Payroll ID": { "type": "integer" },
      "Status": { "type": "string" },
      "TA (Travel Allowance)": { "type": "number" },
      "Year": { "type": "string" }
  },
  "required": [
      "Basic Salary",
      "Bonus",
      "Deductions",
      "HRA",
      "Net Pay",
      "Payment Date",
      "Payment Method",
      "Status",
      "TA (Travel Allowance)"
  ]
}
```

```markdown
| CSV column | Notion property | Set after import |
|---|---|---|
| Payroll Record | Text | Leave as Text |
| Basic Salary | Number (format: currency) | Convert to Number, set format to Currency |
| Bonus | Number (format: currency) | Convert to Number, set format to Currency |
| Currency | Text | Leave as Text |
| DA (Dearness Allowance) | Text | Leave as Text |
| Deductions | Number (format: currency) | Convert to Number, set format to Currency |
| Department | Text | Leave as Text |
| Employee Name | Text | Leave as Text |
| HRA | Number (format: currency) | Convert to Number, set format to Currency |
| Month | Text | Leave as Text |
| Net Pay | Number (format: currency) | Convert to Number, set format to Currency |
| Notes | Text | Leave as Text |
| Pay Period | Text | Leave as Text |
| Payment Date | Date | Convert to Date |
| Payment Method | Select (add options after import) | Convert to Select, add options: "Bank Transfer", "UPI", "Card", "Cash", "Cheque", "NEFT/RTGS" |
| Payroll ID | Text (or Notion auto-ID) | Delete the column and switch the primary column to auto-ID, or keep as Text |
| Status | Select (add options after import) | Convert to Select, add options: "Draft", "Submitted", "Approved", "Paid", "Reconciled" |
| TA (Travel Allowance) | Number (format: currency) | Convert to Number, set format to Currency |
| Year | Text | Leave as Text |
```

One example row per artifact, visibly fake. Money stays `currency`, dates stay `date`,
and anything pointing at another table stays `relation`.

## Field Reference

| # | Field | Type | SQL | JSON Schema | Notion | CSV example |
|---:|---|---|---|---|---|---|
| 1 | Payroll Record | `text` | `VARCHAR(255)` | `string` | Text | `PAY-2026-03` |
| 2 | Basic Salary | `currency` | `NUMERIC(14,2)` | `number` | Number (format: currency) | `650000.00` |
| 3 | Bonus | `currency` | `NUMERIC(14,2)` | `number` | Number (format: currency) | `97500.00` |
| 4 | Currency | `text` | `VARCHAR(255)` | `string` | Text | `INR` |
| 5 | DA (Dearness Allowance) | `text` | `VARCHAR(255)` | `string` | Text | `14500.00` |
| 6 | Deductions | `currency` | `NUMERIC(14,2)` | `number` | Number (format: currency) | `82500.00` |
| 7 | Department | `text` | `VARCHAR(255)` | `string` | Text | `Delivery` |
| 8 | Employee Name | `text` | `VARCHAR(255)` | `string` | Text | `Aarav Sharma` |
| 9 | HRA | `currency` | `NUMERIC(14,2)` | `number` | Number (format: currency) | `260000.00` |
| 10 | Month | `text` | `VARCHAR(255)` | `string` | Text | `2026-03` |
| 11 | Net Pay | `currency` | `NUMERIC(14,2)` | `number` | Number (format: currency) | `958700.00` |
| 12 | Notes | `long_text` | `TEXT` | `string` | Text | `February run reconciled with the accountant; one deduction code was mapped to the wrong head.` |
| 13 | Pay Period | `text` | `VARCHAR(255)` | `string` | Text | `2026-03` |
| 14 | Payment Date | `date` | `DATE` | `string, format: date` | Date | `2026-04-07` |
| 15 | Payment Method | `select` | `VARCHAR(100)` | `string` | Select (add options after import) | `Bank Transfer` |
| 16 | Payroll ID | `id` | `SERIAL PRIMARY KEY` | `integer` | Text (or Notion auto-ID) | `(blank)` |
| 17 | Status | `select` | `VARCHAR(100)` | `string` | Select (add options after import) | `Paid` |
| 18 | TA (Travel Allowance) | `currency` | `NUMERIC(14,2)` | `number` | Number (format: currency) | `19200.00` |
| 19 | Year | `text` | `VARCHAR(255)` | `string` | Text | `2026` |

## Select Options

**Payment Method**

```
Bank Transfer | UPI | Card | Cash | Cheque | NEFT/RTGS
```
**Status**

```
Draft | Submitted | Approved | Paid | Reconciled
```

## Relations

Link fields: none

## Examples

**Prompt**

```
Payroll runs in a spreadsheet and finance re-keys everything.
```

**Context first** - one question per message, nothing already answered:

> **Q:** Who runs it?
> **A:** Our accountant.
>
> **Q:** Variable pay?
> **A:** Yes, bonuses.
>
> **Q:** How many people?
> **A:** Twelve.

**Recommended next step** - offered, not built:

> Treat payroll as an input record for finance, not a calculator. If you need calculation, use payroll software and record the result.
>
> Workflow: Payroll input → Validation → Payroll run → Register update → Finance and tax
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

- Empty template only. It does not compute payroll, tax, leave balances or KPIs.
- Notion relations need both databases imported before the link column resolves.
- Select options are a starting set. Rename them to match how the business talks.
- No automation, reminders or sync. Those need the integration layer.
- Does not calculate pay, deduct tax or transfer money.
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

- `sme-ops-system-builder` - routes to this skill and the other 70 modules.
- `people-directory` - the employee master record most modules link to.
- `notification-reminder-hub` - turns due dates in this module into reminders.

## Reusable Prompt

```
I want to set up compensation for my company.
Ask me one short question at a time, and only about what I have not already told you.
Then recommend the smallest setup that fits, and wait for me to ask before you build it.
When I ask, output CSV, SQL DDL, JSON Schema, a Notion property mapping or an Excel workbook. Data only.
```

