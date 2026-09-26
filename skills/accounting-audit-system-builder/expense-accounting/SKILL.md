---
name: expense-accounting
description: "Expense Accounting: context-first intake, then CSV, SQL, JSON Schema and Notion on request. One short question per message. Use for expense bookkeeping."
category: business
risk: safe
source: self
source_type: self
date_added: "2026-09-26"
author: WHOISABHISHEKADHIKARI
tags: [sme, accounting, audit, finance, database, csv, notion, sql, expenses]
tools: [claude, cursor, gemini, antigravity]
---

# Expense Accounting

**What it is:** Expenses booked to the right account, with the tax treatment and the document type recorded for each.

## Overview

Works out the smallest useful **Expense Accounting** setup for the business in front of it, then
builds it only when asked. The default output is a short recommendation, not a
spreadsheet. Artifacts - CSV, SQL DDL, JSON Schema, Notion mapping - are produced on
request, from one field list so they cannot drift apart.

One guardrail shapes the whole table. Where a formal bill is not available, an internal
supporting document is acceptable only where it is legally and operationally acceptable -
purchases from farmers and individual suppliers, salary and wage sheets, rent agreements
and rent records, and other transactions where formal invoices are not normally issued.
The absence of an invoice does **not** automatically justify raising a purchase
"Kharche/Kharpai". A Kharche/Kharpai is a payment voucher standing in for a bill; using it
because a bill was never asked for hides the real transaction behind a made-up document
type. The document must reflect the actual nature of the transaction and meet the
applicable tax requirements. `Document Type`, `Internal Support Justified` and
`Justification` exist to hold that decision.

Layer: Layer 5: Expense & Payroll. Fits: Starter stage. Table code: n/a.

## When to Use This Skill

- expense register
- petty expense sheet
- expense book with tax
- bill and voucher log

Also use it when the user says "expenses booked to the right account, with the tax treatment and the document type recorded for each", or describes the same process happening in a
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

> **Q:** What is your biggest expense category this month?

### Step 2 - Ask only what is missing

Skip anything the user already answered, in any earlier message. Ask the rest one at a
time, and stop as soon as the remaining answers would not change the output.

- **Categories** - What do you spend on? / How many categories do you actually use? / Any fixed monthly bills?
- **Documents** - Do you get a bill for everything? / Which expenses never have one? / What is accepted instead?
- **Tax** - Is VAT/GST charged? / Is TDS deducted? / Who decides the rates?
- **Approvals** - Who approves an expense? / Who reviews the entry? / Any spending limits?
- **Outcome** - What do you need? / An expense register, a payment file or both?

Never invent an answer. If the user does not know, record it as unknown and carry on.

### Step 3 - Build the internal context

Hold the answers in this shape. It stays internal - it is not shown to the user unless
they ask, and it never carries a value the user did not give.

```yaml
module: expense-accounting
intent: null            # set in Step 1, one of: set up, fix, review, report, import
scale: null             # Starter | Growth | Scale, only if the answer changes it
areas:
  "Categories": null
  "Documents": null
  "Tax": null
  "Approvals": null
  "Outcome": null
requested_outputs: []   # csv | sql | json | notion - only what was explicitly asked for
confirmed_facts: []     # only what the user actually said
open_questions: []      # the unanswered ones, in the order worth asking
```

### Step 4 - Recommend the smallest workflow

Give a short recommendation, then ask whether to build it. Do not build unprompted.

**Recommended approach:** One expense row per bill or supporting document, carrying the nature of the expense, the document type, the account and the tax treatment on the same row.

**Why this one:** An expense is only auditable if the document behind it and the tax treatment on it travel together. Splitting them into two registers is what causes the mismatch at year end.

**Workflow:** Nature identified → Document obtained → Payee verified → Tax treatment decided → Posted to account → Attached and reviewed

### Step 5 - Build only on request

Once the user asks for it, derive the fields from the confirmed context and emit the
artifacts as data only. No preamble, no summary, no closing line.

```csv
Expense Number,Expense Date,Category,Payee,Payee PAN/VAT,Bill/Invoice Number,Bill Date,Document Type,Internal Support Justified,Justification,Amount,VAT Rate %,VAT Amount,TDS Rate %,TDS Amount,Net Payable,Payment Mode,Department,Ledger Account,Approved By,Source Document,Payment Reference,Entry Verified,Prepared By,Notes,Expense ID
EXP-2026-0338,2026-08-18,Professional Fees,Pixelworks Studio,29ABCDE1234F1Z5,BILL-2211,2026-08-12,Tax Invoice,Not Applicable,"A proper tax invoice is available, so no internal support is relied on.",32500.00,18,5850.00,10,3250.00,35100.00,Bank Transfer,Admin,Professional Fees,Vikram Singh,DOC-2026-0451,PAY-2026-0291,Done,Ananya Rao,"Design retainer for August; TDS deducted and carried to the TDS register.",
```

```sql
CREATE TABLE expense_accounting (
  expense_number VARCHAR(255),
  expense_date DATE NOT NULL,
  category VARCHAR(100) NOT NULL,
  payee VARCHAR(255),
  payee_pan_vat VARCHAR(255),
  bill_invoice_number VARCHAR(255),
  bill_date DATE,
  document_type VARCHAR(100) NOT NULL,
  internal_support_justified VARCHAR(100) NOT NULL,
  justification TEXT,
  amount NUMERIC(14,2) NOT NULL,
  vat_rate NUMERIC NOT NULL,
  vat_amount NUMERIC(14,2) NOT NULL,
  tds_rate NUMERIC NOT NULL,
  tds_amount NUMERIC(14,2) NOT NULL,
  net_payable NUMERIC(14,2) NOT NULL,
  payment_mode VARCHAR(100) NOT NULL,
  department VARCHAR(100) NOT NULL,
  ledger_account VARCHAR(255),
  approved_by VARCHAR(255),
  source_document VARCHAR(255),  -- relation -> target record
  payment_reference VARCHAR(255),  -- relation -> target record
  entry_verified VARCHAR(100) NOT NULL,
  prepared_by VARCHAR(255),
  notes TEXT,
  expense_id SERIAL PRIMARY KEY,
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);
```

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "Expense Accounting",
  "type": "object",
  "additionalProperties": false,
  "properties": {
      "Expense Number": { "type": "string" },
      "Expense Date": { "type": "string", "format": "date" },
      "Category": { "type": "string" },
      "Payee": { "type": "string" },
      "Payee PAN/VAT": { "type": "string" },
      "Bill/Invoice Number": { "type": "string" },
      "Bill Date": { "type": "string", "format": "date" },
      "Document Type": { "type": "string" },
      "Internal Support Justified": { "type": "string" },
      "Justification": { "type": "string" },
      "Amount": { "type": "number" },
      "VAT Rate %": { "type": "number" },
      "VAT Amount": { "type": "number" },
      "TDS Rate %": { "type": "number" },
      "TDS Amount": { "type": "number" },
      "Net Payable": { "type": "number" },
      "Payment Mode": { "type": "string" },
      "Department": { "type": "string" },
      "Ledger Account": { "type": "string" },
      "Approved By": { "type": "string" },
      "Source Document": { "type": "string" },
      "Payment Reference": { "type": "string" },
      "Entry Verified": { "type": "string" },
      "Prepared By": { "type": "string" },
      "Notes": { "type": "string" },
      "Expense ID": { "type": "integer" }
  },
  "required": [
      "Expense Date",
      "Category",
      "Document Type",
      "Internal Support Justified",
      "Amount",
      "VAT Rate %",
      "VAT Amount",
      "TDS Rate %",
      "TDS Amount",
      "Net Payable",
      "Payment Mode",
      "Department",
      "Entry Verified"
  ]
}
```

```markdown
| CSV column | Notion property | Set after import |
|---|---|---|
| Expense Number | Text | Leave as Text |
| Expense Date | Date | Convert to Date |
| Category | Select (add options after import) | Convert to Select, add options: "Rent", "Utilities", "Travel", "Professional Fees", "Marketing", "Repairs", "Insurance", "Subscriptions", "Bank Charges", "Office Supplies", "Salaries & Wages", "Other" |
| Payee | Text | Leave as Text |
| Payee PAN/VAT | Text | Leave as Text |
| Bill/Invoice Number | Text | Leave as Text |
| Bill Date | Date | Convert to Date |
| Document Type | Select (add options after import) | Convert to Select, add options: "Tax Invoice", "Bill", "Internal Supporting Document", "Wage Sheet", "Rent Agreement/Record", "Bank Statement", "Other" |
| Internal Support Justified | Select (add options after import) | Convert to Select, add options: "Yes", "No", "Not Applicable" |
| Justification | Text | Leave as Text |
| Amount | Number (format: currency) | Convert to Number, set format to Currency |
| VAT Rate % | Number | Convert to Number |
| VAT Amount | Number (format: currency) | Convert to Number, set format to Currency |
| TDS Rate % | Number | Convert to Number |
| TDS Amount | Number (format: currency) | Convert to Number, set format to Currency |
| Net Payable | Number (format: currency) | Convert to Number, set format to Currency |
| Payment Mode | Select (add options after import) | Convert to Select, add options: "Cash", "Bank Transfer", "Cheque", "Digital Payment" |
| Department | Select (add options after import) | Convert to Select, add options: "Sales", "Purchase", "Accounts", "Payroll", "Admin", "Finance", "Operations" |
| Ledger Account | Text | Leave as Text |
| Approved By | Text | Leave as Text |
| Source Document | Relation (link to the target database) | Convert to Relation, link to the target database |
| Payment Reference | Relation (link to the target database) | Convert to Relation, link to the target database |
| Entry Verified | Select (add options after import) | Convert to Select, add options: "Not started", "In progress", "Blocked", "Done", "Cancelled" |
| Prepared By | Text | Leave as Text |
| Notes | Text | Leave as Text |
| Expense ID | Text (or Notion auto-ID) | Delete the column and switch the primary column to auto-ID, or keep as Text |
```

One example row per artifact, visibly fake. Money stays `currency`, dates stay `date`,
and anything pointing at another table stays `relation`.

## Field Reference

| # | Field | Type | SQL | JSON Schema | Notion | CSV example |
|---:|---|---|---|---|---|---|
| 1 | Expense Number | `text` | `VARCHAR(255)` | `string` | Text | `EXP-2026-0338` |
| 2 | Expense Date | `date` | `DATE` | `string, format: date` | Date | `2026-08-18` |
| 3 | Category | `select` | `VARCHAR(100)` | `string` | Select (add options after import) | `Professional Fees` |
| 4 | Payee | `text` | `VARCHAR(255)` | `string` | Text | `Pixelworks Studio` |
| 5 | Payee PAN/VAT | `text` | `VARCHAR(255)` | `string` | Text | `29ABCDE1234F1Z5` |
| 6 | Bill/Invoice Number | `text` | `VARCHAR(255)` | `string` | Text | `BILL-2211` |
| 7 | Bill Date | `date` | `DATE` | `string, format: date` | Date | `2026-08-12` |
| 8 | Document Type | `select` | `VARCHAR(100)` | `string` | Select (add options after import) | `Tax Invoice` |
| 9 | Internal Support Justified | `select` | `VARCHAR(100)` | `string` | Select (add options after import) | `Not Applicable` |
| 10 | Justification | `long_text` | `TEXT` | `string` | Text | `A proper tax invoice is available, so no internal support is relied on.` |
| 11 | Amount | `currency` | `NUMERIC(14,2)` | `number` | Number (format: currency) | `32500.00` |
| 12 | VAT Rate % | `number` | `NUMERIC` | `number` | Number | `18` |
| 13 | VAT Amount | `currency` | `NUMERIC(14,2)` | `number` | Number (format: currency) | `5850.00` |
| 14 | TDS Rate % | `number` | `NUMERIC` | `number` | Number | `10` |
| 15 | TDS Amount | `currency` | `NUMERIC(14,2)` | `number` | Number (format: currency) | `3250.00` |
| 16 | Net Payable | `currency` | `NUMERIC(14,2)` | `number` | Number (format: currency) | `35100.00` |
| 17 | Payment Mode | `select` | `VARCHAR(100)` | `string` | Select (add options after import) | `Bank Transfer` |
| 18 | Department | `select` | `VARCHAR(100)` | `string` | Select (add options after import) | `Admin` |
| 19 | Ledger Account | `text` | `VARCHAR(255)` | `string` | Text | `Professional Fees` |
| 20 | Approved By | `text` | `VARCHAR(255)` | `string` | Text | `Vikram Singh` |
| 21 | Source Document | `relation` | `VARCHAR(255)` | `string` | Relation (link to the target database) | `DOC-2026-0451` |
| 22 | Payment Reference | `relation` | `VARCHAR(255)` | `string` | Relation (link to the target database) | `PAY-2026-0291` |
| 23 | Entry Verified | `select` | `VARCHAR(100)` | `string` | Select (add options after import) | `Done` |
| 24 | Prepared By | `text` | `VARCHAR(255)` | `string` | Text | `Ananya Rao` |
| 25 | Notes | `long_text` | `TEXT` | `string` | Text | `Design retainer for August; TDS deducted and carried to the TDS register.` |
| 26 | Expense ID | `id` | `SERIAL PRIMARY KEY` | `integer` | Text (or Notion auto-ID) | `(blank)` |

## Select Options

**Category**

```
Rent | Utilities | Travel | Professional Fees | Marketing | Repairs | Insurance | Subscriptions | Bank Charges | Office Supplies | Salaries & Wages | Other
```
**Document Type**

```
Tax Invoice | Bill | Internal Supporting Document | Wage Sheet | Rent Agreement/Record | Bank Statement | Other
```
**Internal Support Justified**

```
Yes | No | Not Applicable
```
**Payment Mode**

```
Cash | Bank Transfer | Cheque | Digital Payment
```
**Department**

```
Sales | Purchase | Accounts | Payroll | Admin | Finance | Operations
```
**Entry Verified**

```
Not started | In progress | Blocked | Done | Cancelled
```

## Relations

Link fields: `Source Document`, `Payment Reference`

## Examples

**Prompt**

```
We keep expenses in a notebook and at year end nobody can say which bill is missing.
```

**Context first** - one question per message, nothing already answered:

> **Q:** Do you get a bill for everything you spend on?
> **A:** Not for the farm suppliers and not for the rent.
>
> **Q:** What do you record instead?
> **A:** A payment voucher.
>
> **Q:** Is TDS deducted on anything?
> **A:** On professional fees, yes.

**Recommended next step** - offered, not built:

> One expense row per bill or supporting document, carrying the nature of the expense, the document type, the account and the tax treatment on the same row.
>
> Workflow: Nature identified → Document obtained → Payee verified → Tax treatment decided → Posted to account → Attached and reviewed
>
> Want the CSV, SQL, JSON Schema and Notion mapping for this?

## Best Practices

- Recommend before building. The recommendation is the product; the files are the follow-up.
- One question per message. A batched intake reads as a form and gets guessed at.
- Keep every field name identical across CSV, SQL and JSON Schema.
- Use `relation` for anything that points at another table, `text` only for free text.
- Money fields are `currency`, never `text`. Dates are `date`, never free text.
- Record the real document type every time. A purchase voucher standing in for a bill is only
  correct where a bill would not exist anyway.
- Set `Internal Support Justified` to `No` and write the reason in `Justification` when you
  cannot explain why internal evidence is acceptable for that expense.
- Keep the example row obviously fake so nobody imports it as real data.

## Limitations

- Empty template only. It does not compute tax, post entries or approve anything.
- It does not decide whether a Kharche/Kharpai is acceptable in your case. Internal support
  is only defensible where the transaction does not normally produce a formal invoice, and
  the tax authority's position is what settles it.
- It does not file returns, pay taxes or give tax advice.
- Notion relations need both databases imported before the link column resolves.
- Select options are a starting set. Rename them to match how the business talks.
- No automation, reminders or sync. Those need the integration layer.
- Legal, tax and HR review is still required before this drives real decisions.

## Security & Safety Notes

- Never fill in real names, payee details, PAN numbers or banking data. Placeholders only.
- Never mark an example row `Confidential`, and keep tax identifiers masked.
- This skill writes nothing outside the chat. It runs no commands and calls no APIs.
- If the user pastes real employee or supplier data, generate the template and tell them to
  delete the pasted data from the conversation.
- Expense approvals and any tax treatment decision need a qualified human reviewer before
  anything is acted on.

## Common Pitfalls

- **Problem:** asked all six questions in one message.
  **Solution:** ask one, wait, and drop any the first answer already covered.
- **Problem:** no bill, so a Kharche/Kharpai was raised to close the entry.
  **Solution:** check the transaction type first. Only buy from farmers and individuals, wage
  sheets and rent records genuinely lack a formal invoice. Everywhere else, chase the bill.
- **Problem:** the document type is right but nothing is attached.
  **Solution:** link `Source Document` so the entry carries its own evidence.
- **Problem:** TDS was deducted here but never reached the TDS register.
  **Solution:** link `Payment Reference` and hand the deduction to `tds-booking-payment`.
- **Problem:** built a full system when one table was asked for.
  **Solution:** build what was requested; mention the parent skill separately.
- **Problem:** all four artifacts drift apart.
  **Solution:** derive all four from the field list in this file, never by hand.
- **Problem:** Notion import shows every column as Text.
  **Solution:** that is expected. Apply the property mapping table once, after import.

## Related Skills

- `accounting-audit-system-builder` - routes to this skill and the other accounting modules.
- `payment-accounting` - pays the net figure this row produces.
- `source-document-filing` - stores the bill or supporting document that must be attached.
- `tds-booking-payment` - carries the deduction from this row into the statutory register.
- `salary-wage-accounting` - handles the wage sheet and salary expense lines.
- `day-book` - the dated journal trail the entries land in.

## Reusable Prompt

```
I want to set up expenses booked to the right account, with the tax treatment and the document type recorded for each, for my company.
Ask me one short question at a time, and only about what I have not already told you.
Then recommend the smallest setup that fits, and wait for me to ask before you build it.
When I ask, output CSV, SQL DDL, JSON Schema and a Notion property mapping. Data only.
```
