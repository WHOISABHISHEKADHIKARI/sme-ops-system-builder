---
name: day-book
description: "Day Book: context-first intake, then CSV, SQL, JSON Schema and Notion on request. One short question per message. Use for daily cash and bank book."
category: business
risk: safe
source: self
source_type: self
date_added: "2026-09-26"
author: WHOISABHISHEKADHIKARI
tags: [sme, accounting, audit, finance, database, csv, notion, sql, day-book, cash-book]
tools: [claude, cursor, gemini, antigravity]
---

# Day Book

**What it is:** The daily cash, bank and digital receipt-and-payment record, reviewed and reconciled at day end.

## Overview

Works out the smallest useful **Day Book** setup for the business in front of it, then
builds it only when asked. The default output is a short recommendation, not a
spreadsheet. Artifacts - CSV, SQL DDL, JSON Schema, Notion mapping - are produced on
request, from one field list so they cannot drift apart.

Layer: Layer 4: Cash. Fits: Starter stage. Table code: n/a.

**The rule this table exists to enforce:** the debit/credit presentation of a day book
**depends on the software's day-book format**. It is not a universal rule that all receipts
are debit and all payments are credit - some books present receipts on the payment side,
some carry both columns, some carry neither. So this table does not hardcode a Debit/Credit
pair. `Debit/Credit Presentation` is a text field that records the presentation **as
configured in the business's own software**, and the six amount columns plus the two
running balances are the part that is universal.

## When to Use This Skill

- day book
- daily cash and bank book
- cash book and bank book
- daily receipts and payments register
- end of day balance check

Also use it when the user says "the daily cash, bank and digital receipt-and-payment record, reviewed and reconciled at day end", or describes the same process happening in a
spreadsheet, a document or someone inboxes.

Do not use it for: making payments, recording receipts in detail, tax filing, or legal advice. This skill produces
empty templates only - it never holds or processes real employee or customer data.

## How It Works

### Step 1 - Identify intent

Read the request and pick the intent before asking anything.

- "set up" or "build" or "create" -> the user wants artifacts; go to Step 2.
- "our process is ..." or "it is in a sheet" -> the user wants to move an existing process; capture it, then Step 2.
- "is this right" or "review" or "audit" -> the user wants a check, not a build; answer from what they share.
- "how do I ..." -> advice question; answer directly and offer the build only if it helps.

One message, one question, no batching. Open with:

> **Q:** What does your cash and bank record look like at the end of a day today?

### Step 2 - Ask only what is missing

Skip anything the user already answered, in any earlier message. Ask the rest one at a
time, and stop as soon as the remaining answers would not change the output.

- **Books** - Cash, bank and digital all separate? / Which software or format? / Daily or
  weekly entries?
- **Entries** - Who writes them? / From vouchers or from the bank feed? / Same day or next?
- **Balances** - Opening and closing balance carried daily? / Verified against statement?
  / Who signs off?
- **Controls** - Duplicate check done? / Missing entries spotted how? / Digital wallets counted?
- **Outcome** - What do you need? / A daily book, a reconciliation record or both?

Never invent an answer. If the user does not know, record it as unknown and carry on.

### Step 3 - Build the internal context

Hold the answers in this shape. It stays internal - it is not shown to the user unless
they ask, and it never carries a value the user did not give.

```yaml
module: day-book
intent: null            # set in Step 1, one of: set up, fix, review, report, import
scale: null             # Starter | Growth | Scale, only if the answer changes it
areas:
  "Books": null
  "Entries": null
  "Balances": null
  "Controls": null
  "Outcome": null
requested_outputs: []   # csv | sql | json | notion - only what was explicitly asked for
confirmed_facts: []     # only what the user actually said
open_questions: []      # the unanswered ones, in the order worth asking
```

### Step 4 - Recommend the smallest workflow

Give a short recommendation, then ask whether to build it. Do not build unprompted.

**Recommended approach:** One day book with a row per receipt and payment, a book section for cash, bank or digital, a running balance per book, and a day-end row that totals the day across all three books and verifies the balances and checks for duplicates before the day is closed.

**Why this one:** The day book is where a missing or duplicated entry becomes visible. Everything else in the cash cycle is downstream of the balance agreeing at day end.

**Workflow:** Receipt or payment recorded from voucher → Booked to cash, bank or digital → Running balance updated → Duplicate and missing entries checked → Day-end balance verified and reviewed

### Step 5 - Build only on request

Once the user asks for it, derive the fields from the confirmed context and emit the
artifacts as data only. No preamble, no summary, no closing line.

```csv
Entry Number,Entry Date,Book Section,Transaction Reference,Voucher Number,Party,Narration,Mode,Cash In,Cash Out,Cash Balance,Bank In,Bank Out,Bank Balance,Digital In,Digital Out,Debit/Credit Presentation,Source Documents,Duplicate Check,Balance Verified,Prepared By,Reviewed By,Entry Verified,Notes,Day Book ID
DB-2026-08-0141,2026-08-21,Day Summary,RCP-2026-0312,VCH-2026-1027,Several parties,Day total across the three books; each detail line carries its own reference,Mixed,15000.00,11800.00,38200.00,140000.00,95485.00,1284500.00,24600.00,4300.00,As per software day-book format,DOC-2026-0461,Checked - Clear,Yes,Rohit Menon,Sneha Iyer,Done,"Cash counted at day end; bank balance agreed to the statement.",
```

```sql
CREATE TABLE day_book (
  entry_number VARCHAR(255),
  entry_date DATE NOT NULL,
  book_section VARCHAR(100) NOT NULL,
  transaction_reference VARCHAR(255),
  voucher_number VARCHAR(255),
  party VARCHAR(255),
  narration VARCHAR(255),
  mode VARCHAR(100) NOT NULL,
  cash_in NUMERIC(14,2) NOT NULL,
  cash_out NUMERIC(14,2) NOT NULL,
  cash_balance NUMERIC(14,2) NOT NULL,
  bank_in NUMERIC(14,2) NOT NULL,
  bank_out NUMERIC(14,2) NOT NULL,
  bank_balance NUMERIC(14,2) NOT NULL,
  digital_in NUMERIC(14,2) NOT NULL,
  digital_out NUMERIC(14,2) NOT NULL,
  debit_credit_presentation VARCHAR(255),
  source_documents VARCHAR(255),  -- relation -> target record
  duplicate_check VARCHAR(100) NOT NULL,
  balance_verified VARCHAR(100) NOT NULL,
  prepared_by VARCHAR(255),
  reviewed_by VARCHAR(255),
  entry_verified VARCHAR(100) NOT NULL,
  notes TEXT,
  day_book_id SERIAL PRIMARY KEY,
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);
```

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "Day Book",
  "type": "object",
  "additionalProperties": false,
  "properties": {
      "Entry Number": { "type": "string" },
      "Entry Date": { "type": "string", "format": "date" },
      "Book Section": { "type": "string" },
      "Transaction Reference": { "type": "string" },
      "Voucher Number": { "type": "string" },
      "Party": { "type": "string" },
      "Narration": { "type": "string" },
      "Mode": { "type": "string" },
      "Cash In": { "type": "number" },
      "Cash Out": { "type": "number" },
      "Cash Balance": { "type": "number" },
      "Bank In": { "type": "number" },
      "Bank Out": { "type": "number" },
      "Bank Balance": { "type": "number" },
      "Digital In": { "type": "number" },
      "Digital Out": { "type": "number" },
      "Debit/Credit Presentation": { "type": "string" },
      "Source Documents": { "type": "string" },
      "Duplicate Check": { "type": "string" },
      "Balance Verified": { "type": "string" },
      "Prepared By": { "type": "string" },
      "Reviewed By": { "type": "string" },
      "Entry Verified": { "type": "string" },
      "Notes": { "type": "string" },
      "Day Book ID": { "type": "integer" }
  },
  "required": [
      "Entry Date",
      "Book Section",
      "Mode",
      "Cash In",
      "Cash Out",
      "Cash Balance",
      "Bank In",
      "Bank Out",
      "Bank Balance",
      "Digital In",
      "Digital Out",
      "Duplicate Check",
      "Balance Verified",
      "Entry Verified"
  ]
}
```

```markdown
| CSV column | Notion property | Set after import |
|---|---|---|
| Entry Number | Text | Leave as Text |
| Entry Date | Date | Convert to Date |
| Book Section | Select (add options after import) | Convert to Select, add options: "Cash Book", "Bank Book", "Digital Payments Book", "Day Summary" |
| Transaction Reference | Text | Leave as Text |
| Voucher Number | Text | Leave as Text |
| Party | Text | Leave as Text |
| Narration | Text | Leave as Text |
| Mode | Select (add options after import) | Convert to Select, add options: "Cash", "Bank", "Cheque", "Fonepay/QR", "Other Digital Payment", "Mixed" |
| Cash In | Number (format: currency) | Convert to Number, set format to Currency |
| Cash Out | Number (format: currency) | Convert to Number, set format to Currency |
| Cash Balance | Number (format: currency) | Convert to Number, set format to Currency |
| Bank In | Number (format: currency) | Convert to Number, set format to Currency |
| Bank Out | Number (format: currency) | Convert to Number, set format to Currency |
| Bank Balance | Number (format: currency) | Convert to Number, set format to Currency |
| Digital In | Number (format: currency) | Convert to Number, set format to Currency |
| Digital Out | Number (format: currency) | Convert to Number, set format to Currency |
| Debit/Credit Presentation | Text | Leave as Text |
| Source Documents | Relation (link to the target database) | Convert to Relation, link to the target database |
| Duplicate Check | Select (add options after import) | Convert to Select, add options: "Checked - Clear", "Checked - Duplicate Found", "Not Checked" |
| Balance Verified | Select (add options after import) | Convert to Select, add options: "Yes", "No", "Pending" |
| Prepared By | Text | Leave as Text |
| Reviewed By | Text | Leave as Text |
| Entry Verified | Select (add options after import) | Convert to Select, add options: "Not started", "In progress", "Blocked", "Done", "Cancelled" |
| Notes | Text | Leave as Text |
| Day Book ID | Text (or Notion auto-ID) | Delete the column and switch the primary column to auto-ID, or keep as Text |
```

One example row per artifact, visibly fake. Money stays `currency`, dates stay `date`, and anything pointing at another table stays `relation`.

## Field Reference

| # | Field | Type | SQL | JSON Schema | Notion | CSV example |
|---:|---|---|---|---|---|---|
| 1 | Entry Number | `text` | `VARCHAR(255)` | `string` | Text | `DB-2026-08-0141` |
| 2 | Entry Date | `date` | `DATE` | `string, format: date` | Date | `2026-08-21` |
| 3 | Book Section | `select` | `VARCHAR(100)` | `string` | Select (add options after import) | `Day Summary` |
| 4 | Transaction Reference | `text` | `VARCHAR(255)` | `string` | Text | `RCP-2026-0312` |
| 5 | Voucher Number | `text` | `VARCHAR(255)` | `string` | Text | `VCH-2026-1027` |
| 6 | Party | `text` | `VARCHAR(255)` | `string` | Text | `Several parties` |
| 7 | Narration | `text` | `VARCHAR(255)` | `string` | Text | `Day total across the three books; each detail line carries its own reference` |
| 8 | Mode | `select` | `VARCHAR(100)` | `string` | Select (add options after import) | `Mixed` |
| 9 | Cash In | `currency` | `NUMERIC(14,2)` | `number` | Number (format: currency) | `15000.00` |
| 10 | Cash Out | `currency` | `NUMERIC(14,2)` | `number` | Number (format: currency) | `11800.00` |
| 11 | Cash Balance | `currency` | `NUMERIC(14,2)` | `number` | Number (format: currency) | `38200.00` |
| 12 | Bank In | `currency` | `NUMERIC(14,2)` | `number` | Number (format: currency) | `140000.00` |
| 13 | Bank Out | `currency` | `NUMERIC(14,2)` | `number` | Number (format: currency) | `95485.00` |
| 14 | Bank Balance | `currency` | `NUMERIC(14,2)` | `number` | Number (format: currency) | `1284500.00` |
| 15 | Digital In | `currency` | `NUMERIC(14,2)` | `number` | Number (format: currency) | `24600.00` |
| 16 | Digital Out | `currency` | `NUMERIC(14,2)` | `number` | Number (format: currency) | `4300.00` |
| 17 | Debit/Credit Presentation | `text` | `VARCHAR(255)` | `string` | Text | `As per software day-book format` |
| 18 | Source Documents | `relation` | `VARCHAR(255)` | `string` | Relation (link to the target database) | `DOC-2026-0461` |
| 19 | Duplicate Check | `select` | `VARCHAR(100)` | `string` | Select (add options after import) | `Checked - Clear` |
| 20 | Balance Verified | `select` | `VARCHAR(100)` | `string` | Select (add options after import) | `Yes` |
| 21 | Prepared By | `text` | `VARCHAR(255)` | `string` | Text | `Rohit Menon` |
| 22 | Reviewed By | `text` | `VARCHAR(255)` | `string` | Text | `Sneha Iyer` |
| 23 | Entry Verified | `select` | `VARCHAR(100)` | `string` | Select (add options after import) | `Done` |
| 24 | Notes | `long_text` | `TEXT` | `string` | Text | `Cash counted at day end; bank balance agreed to the statement.` |
| 25 | Day Book ID | `id` | `SERIAL PRIMARY KEY` | `integer` | Text (or Notion auto-ID) | `(blank)` |

## Select Options

**Book Section**

```
Cash Book | Bank Book | Digital Payments Book | Day Summary
```
**Mode**

```
Cash | Bank | Cheque | Fonepay/QR | Other Digital Payment | Mixed
```
**Duplicate Check**

```
Checked - Clear | Checked - Duplicate Found | Not Checked
```
**Balance Verified**

```
Yes | No | Pending
```
**Entry Verified**

```
Not started | In progress | Blocked | Done | Cancelled
```

## Relations

Link fields: `Source Documents`

`Source Documents` points at the filing register, so a day-book line can be traced back to
the voucher or advice behind it. `Transaction Reference` is deliberately free text - it
holds the receipt, payment or petty cash number the line came from, and the same number
also appears in that table. Confirm with the business whether they want it as a live
relation before adding one.

## Examples

**Prompt**

```
We cannot tell at the end of the day whether the bank balance is right, and twice we
found the same payment entered twice.
```

**Context first** - one question per message, nothing already answered:

> **Q:** Cash, bank and digital - kept separately?
> **A:** Bank and one Fonepay number. Cash is in the drawer.
>
> **Q:** Who writes the entries?
> **A:** My accounts person, from the vouchers, in the evening.
>
> **Q:** How is the balance checked?
> **A:** Against the bank statement once a month.

**Recommended next step** - offered, not built:

> One day book with a row per receipt and payment, a book section for cash, bank or digital, a running balance per book, and a day-end row that totals the day across all three books and verifies the balances and checks for duplicates before the day is closed.
>
> Workflow: Receipt or payment recorded from voucher → Booked to cash, bank or digital → Running balance updated → Duplicate and missing entries checked → Day-end balance verified and reviewed
>
> Want the CSV, SQL, JSON Schema and Notion mapping for this?

## Best Practices

- Recommend before building. The recommendation is the product; the files are the follow-up.
- One question per message. A batched intake reads as a form and gets guessed at.
- Never hardcode a Debit/Credit rule. The presentation follows the software's day-book
  format, and `Debit/Credit Presentation` records what that format actually is.
- Close the day, not the week. Count the cash, agree the bank balance to the statement and
  confirm the digital wallet balance before the day is marked verified.
- Use `Duplicate Check` honestly. `Not Checked` is a valid answer; a false `Checked -
  Clear` is not.
- One row per movement, from the voucher. A day book that is written from memory is where
  duplicates and omissions come from.
- Close the books on the identity: opening balance + money in - money out = closing balance,
  for cash and for bank separately. A `Day Summary` row carries that day's totals for all
  three books so the day can be agreed in one place; the detail lines under it still carry
  one movement each, and that row's `Transaction Reference` is the day's largest single
  reference.
- Keep the narration specific enough to be understood six months later - invoice number,
  party and what it was for.
- Keep every field name identical across CSV, SQL and JSON Schema.
- Use `relation` for anything that points at another table, `text` only for free text.
- Money fields are `currency`, never `text`. Dates are `date`, never free text.
- Keep the example row obviously fake so nobody imports it as real data.

## Limitations

- Empty template only. It does not post entries, move money or connect to a bank feed.
- The debit/credit presentation cannot be settled by this skill. It follows whatever the
  business's software produces, so read the format out of the software and write it into
  `Debit/Credit Presentation` rather than assuming one.
- A day book is a record of what was entered, not proof that it was correct. The proof
  comes from the supporting document, which is why the source link and the voucher number
  are on every row.
- Digital wallet balances settle late against some aggregators, so a same-day agreement is
  not always possible. `Balance Verified` = `Pending` exists for that.
- Reconciliation against the bank statement is a separate routine; this table records that
  it was done, not what it found.
- Notion relations need both databases imported before the link column resolves.
- Select options are a starting set. Rename them to match how the business talks.
- No automation, reminders or sync. Those need the integration layer.
- Legal, tax and HR review is still required before this drives real decisions.

## Security & Safety Notes

- Never fill in real names, bank details or transaction references. Placeholders only.
- Never mark an example row `Confidential`, and keep bank details masked.
- A day book is a map of every movement of the business's money. Do not paste real
  statements, balances or UTR references into a chat.
- A duplicate or a balance break is a control finding, not a clerical fix. Report it, do
  not edit the balance to make it go away.
- This skill writes nothing outside the chat. It runs no commands and calls no APIs.
- If the user pastes real transaction data, generate the template and tell them to delete
  the pasted data from the conversation.
- Privacy, legal and disciplinary cases need a qualified human reviewer before anything
  is acted on.

## Common Pitfalls

- **Problem:** asked all six questions in one message.
  **Solution:** ask one, wait, and drop any the first answer already covered.
- **Problem:** the day book was built with hardcoded Debit and Credit columns.
  **Solution:** the presentation depends on the software's format. Capture it in
  `Debit/Credit Presentation` instead of assuming a universal rule.
- **Problem:** the same cheque or UTR is entered twice and both stay.
  **Solution:** run the duplicate check on the transaction reference, set `Checked -
  Duplicate Found`, and resolve it with a human.
- **Problem:** the balance is verified only at month end.
  **Solution:** day end is the control. `Balance Verified` = `Pending` is what an open day
  looks like.
- **Problem:** a day-book line is written with no source document.
  **Solution:** the line is a claim. Link the source or mark the entry blocked.
- **Problem:** the day's movements are spread over three books and nobody can see the day.
  **Solution:** a `Day Summary` row totals cash, bank and digital together, with `Mode` =
  `Mixed`, and the running balances on it are the ones that get verified.
- **Problem:** all four artifacts drift apart.
  **Solution:** derive all four from the field list in this file, never by hand.
- **Problem:** Notion import shows every column as Text.
  **Solution:** that is expected. Apply the property mapping table once, after import.

## Related Skills

- `accounting-audit-system-builder` - routes to this skill and the other 15 modules.
- `receipt-accounting` - the detail behind the receipt lines in this book.
- `payment-accounting` - the detail behind the payment lines in this book.
- `petty-cash-management` - the float that the cash book section is counting.
- `source-document-filing` - holds the `Source Documents` target.
- `party-ledger-reconciliation` - takes the balances this book produces and proves them.
- `expense-accounting` - the expense detail behind the payments booked here.
- `inventory-stock-reconciliation` - the same count discipline applied to stock.
- `monthly-closing-statements` - takes the closed day book into the trial balance.
- `audit-preparation` - a daily book with verified balances is an audit-trail item.
- `accounting-software-selection` - decides the day-book format this table must capture.
- `credit-cycle-analysis` - reads the debtor movement out of the receipts booked here.
- `salary-wage-accounting` - the salary run lands in the bank book here.

## Reusable Prompt

```
I want to set up a day book for my company - daily cash, bank and digital receipts and
payments, with running balances, a duplicate check and a day-end balance verification.
Ask me one short question at a time, and only about what I have not already told you.
Then recommend the smallest setup that fits, and wait for me to ask before you build it.
When I ask, output CSV, SQL DDL, JSON Schema and a Notion property mapping. Data only.
```
