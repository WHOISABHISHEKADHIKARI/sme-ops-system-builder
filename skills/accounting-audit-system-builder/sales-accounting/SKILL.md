---
name: sales-accounting
description: "Sales Accounting: context-first intake, then CSV, SQL, JSON Schema and Notion on request. One short question per message. Use for sales accounting."
category: business
risk: safe
source: self
source_type: self
date_added: "2026-09-26"
author: WHOISABHISHEKADHIKARI
tags: [sme, accounting, audit, finance, database, csv, notion, sql, sales]
tools: [claude, cursor, gemini, antigravity]
---

# Sales Accounting

**What it is:** Sales orders, delivery challans, invoices and the receivables they create.

## Overview

Works out the smallest useful **Sales Accounting** setup for the business in front of it, then
builds it only when asked. The default output is a short recommendation, not a
spreadsheet. Artifacts - CSV, SQL DDL, JSON Schema, Notion mapping - are produced on
request, from one field list so they cannot drift apart.

Layer: Layer 3: Record. Fits: Starter stage. Table code: n/a.

## When to Use This Skill

- sales accounting
- sales invoice register
- customer billing and receivable tracker
- sales vat register log

Also use it when the user says "sales orders, delivery challans, invoices and the receivables they create", or describes the same process happening in a
spreadsheet, a document or someone inboxes.

Do not use it for: customer collections, tax filing, or legal advice. This skill produces
empty templates only - it never holds or processes real employee or customer data.

## How It Works

### Step 1 - Identify intent

Read the request and pick the intent before asking anything.

- "set up" or "build" or "create" -> the user wants artifacts; go to Step 2.
- "our process is ..." or "it is in a sheet" -> the user wants to move an existing process; capture it, then Step 2.
- "is this right" or "review" or "audit" -> the user wants a check, not a build; answer from what they share.
- "how do I ..." -> advice question; answer directly and offer the build only if it helps.

One message, one question, no batching. Open with:

> **Q:** How are sales invoices raised today?

### Step 2 - Ask only what is missing

Skip anything the user already answered, in any earlier message. Ask the rest one at a
time, and stop as soon as the remaining answers would not change the output.

- **Volume** - How many invoices a month? / How many customers?
- **Documents** - Sales order and challan every time? / Or invoice only?
- **Taxes and credit** - VAT charged? / TDS deducted by customers? / Discounts given? / How many sales are on credit? / Standard credit period? / Who follows up?
- **Current process** - Tracked now? / Software or sheet? / What gets missed?
- **Outcome** - What do you need? / A sales register, an aging view or both?

Never invent an answer. If the user does not know, record it as unknown and carry on.

### Step 3 - Build the internal context

Hold the answers in this shape. It stays internal - it is not shown to the user unless
they ask, and it never carries a value the user did not give.

```yaml
module: sales-accounting
intent: null            # set in Step 1, one of: set up, fix, review, report, import
scale: null             # Starter | Growth | Scale, only if the answer changes it
areas:
  "Volume": null
  "Documents": null
  "Taxes and credit": null
  "Current process": null
  "Outcome": null
requested_outputs: []   # csv | sql | json | notion - only what was explicitly asked for
confirmed_facts: []     # only what the user actually said
open_questions: []      # the unanswered ones, in the order worth asking
```

### Step 4 - Recommend the smallest workflow

Give a short recommendation, then ask whether to build it. Do not build unprompted.

**Recommended approach:** One sales record per invoice, holding the order, challan and source document as relations, the full tax breakdown, and - where the sale is on credit - the due date, the debtor ledger and the outstanding balance - five steps: prepare documents, issue the invoice, update the Sales VAT Register, record in software, confirm the debtor ledger.

**Why this one:** A sales register that stops at the invoice total loses the receivable. Keeping credit terms, due date and balance on the same row is what turns billing into a collections list.

**Workflow:** Order and challan prepared → Invoice issued → VAT register updated → Recorded → Debtor ledger confirmed

### Step 5 - Build only on request

Once the user asks for it, derive the fields from the confirmed context and emit the
artifacts as data only. No preamble, no summary, no closing line.

```csv
Sales Number,Customer,Customer PAN/VAT,Sales Order,Delivery Challan,Invoice Number,Invoice Date,Item Description,Quantity,UOM,Rate,Gross Amount,Discount,Taxable Value,VAT Rate %,VAT Amount,TDS Rate %,TDS Amount,Invoice Total,Net Receivable,Credit Terms (Days),Due Date,Receivable Status,Amount Received,Balance,Ledger Account,Source Document,VAT Register Updated,Entry Verified,Prepared By,Notes,Sales ID
SAL-2026-0033,Greyson Foods,33CDEFG9012H1Z9,SO-2026-0094,DC-2026-0911,INV-2026-0733,2026-08-16,Corrugated carton packs printed,800,Nos,142.50,114000.00,2280.00,111720.00,18,20109.60,1,1117.20,131829.60,130712.40,30,2026-09-15,Part Paid,50000.00,80712.40,Sales - Cartons,DOC-2026-0455,Done,In progress,Ananya Rao,Invoice issued with the challan; credit sale net 30.,
```

```sql
CREATE TABLE sales_accounting (
  sales_number VARCHAR(255),
  customer VARCHAR(255),
  customer_pan_vat VARCHAR(255),
  sales_order VARCHAR(255),  -- relation -> target record
  delivery_challan VARCHAR(255),  -- relation -> target record
  invoice_number VARCHAR(255),
  invoice_date DATE NOT NULL,
  item_description VARCHAR(255),
  quantity NUMERIC NOT NULL,
  uom VARCHAR(100) NOT NULL,
  rate NUMERIC(14,2) NOT NULL,
  gross_amount NUMERIC(14,2) NOT NULL,
  discount NUMERIC(14,2) NOT NULL,
  taxable_value NUMERIC(14,2) NOT NULL,
  vat_rate NUMERIC NOT NULL,
  vat_amount NUMERIC(14,2) NOT NULL,
  tds_rate NUMERIC NOT NULL,
  tds_amount NUMERIC(14,2) NOT NULL,
  invoice_total NUMERIC(14,2) NOT NULL,
  net_receivable NUMERIC(14,2) NOT NULL,
  credit_terms_days NUMERIC NOT NULL,
  due_date DATE NOT NULL,
  receivable_status VARCHAR(100) NOT NULL,
  amount_received NUMERIC(14,2) NOT NULL,
  balance NUMERIC(14,2) NOT NULL,
  ledger_account VARCHAR(255),
  source_document VARCHAR(255),  -- relation -> target record
  vat_register_updated VARCHAR(100) NOT NULL,
  entry_verified VARCHAR(100) NOT NULL,
  prepared_by VARCHAR(255),
  notes TEXT,
  sales_id SERIAL PRIMARY KEY,
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);
```

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "Sales Accounting",
  "type": "object",
  "additionalProperties": false,
  "properties": {
      "Sales Number": { "type": "string" },
      "Customer": { "type": "string" },
      "Customer PAN/VAT": { "type": "string" },
      "Sales Order": { "type": "string" },
      "Delivery Challan": { "type": "string" },
      "Invoice Number": { "type": "string" },
      "Invoice Date": { "type": "string", "format": "date" },
      "Item Description": { "type": "string" },
      "Quantity": { "type": "number" },
      "UOM": { "type": "string" },
      "Rate": { "type": "number" },
      "Gross Amount": { "type": "number" },
      "Discount": { "type": "number" },
      "Taxable Value": { "type": "number" },
      "VAT Rate %": { "type": "number" },
      "VAT Amount": { "type": "number" },
      "TDS Rate %": { "type": "number" },
      "TDS Amount": { "type": "number" },
      "Invoice Total": { "type": "number" },
      "Net Receivable": { "type": "number" },
      "Credit Terms (Days)": { "type": "number" },
      "Due Date": { "type": "string", "format": "date" },
      "Receivable Status": { "type": "string" },
      "Amount Received": { "type": "number" },
      "Balance": { "type": "number" },
      "Ledger Account": { "type": "string" },
      "Source Document": { "type": "string" },
      "VAT Register Updated": { "type": "string" },
      "Entry Verified": { "type": "string" },
      "Prepared By": { "type": "string" },
      "Notes": { "type": "string" },
      "Sales ID": { "type": "integer" }
  },
  "required": [
      "Invoice Date",
      "Quantity",
      "UOM",
      "Rate",
      "Gross Amount",
      "Discount",
      "Taxable Value",
      "VAT Rate %",
      "VAT Amount",
      "TDS Rate %",
      "TDS Amount",
      "Invoice Total",
      "Net Receivable",
      "Credit Terms (Days)",
      "Due Date",
      "Receivable Status",
      "Amount Received",
      "Balance",
      "VAT Register Updated",
      "Entry Verified"
  ]
}
```

```markdown
| CSV column | Notion property | Set after import |
|---|---|---|
| Sales Number | Text | Leave as Text |
| Customer | Text | Leave as Text |
| Customer PAN/VAT | Text | Leave as Text |
| Sales Order | Relation (link to the target database) | Convert to Relation, link to the target database |
| Delivery Challan | Relation (link to the target database) | Convert to Relation, link to the target database |
| Invoice Number | Text | Leave as Text |
| Invoice Date | Date | Convert to Date |
| Item Description | Text | Leave as Text |
| Quantity | Number | Convert to Number |
| UOM | Select (add options after import) | Convert to Select, add options: "Nos", "Kg", "Litre", "Metre", "Set", "Hour", "Box", "Packet" |
| Rate | Number (format: currency) | Convert to Number, set format to Currency |
| Gross Amount | Number (format: currency) | Convert to Number, set format to Currency |
| Discount | Number (format: currency) | Convert to Number, set format to Currency |
| Taxable Value | Number (format: currency) | Convert to Number, set format to Currency |
| VAT Rate % | Number | Convert to Number |
| VAT Amount | Number (format: currency) | Convert to Number, set format to Currency |
| TDS Rate % | Number | Convert to Number |
| TDS Amount | Number (format: currency) | Convert to Number, set format to Currency |
| Invoice Total | Number (format: currency) | Convert to Number, set format to Currency |
| Net Receivable | Number (format: currency) | Convert to Number, set format to Currency |
| Credit Terms (Days) | Number | Convert to Number |
| Due Date | Date | Convert to Date |
| Receivable Status | Select (add options after import) | Convert to Select, add options: "Outstanding", "Part Paid", "Settled", "Written Off", "Overdue" |
| Amount Received | Number (format: currency) | Convert to Number, set format to Currency |
| Balance | Number (format: currency) | Convert to Number, set format to Currency |
| Ledger Account | Text | Leave as Text |
| Source Document | Relation (link to the target database) | Convert to Relation, link to the target database |
| VAT Register Updated | Select (add options after import) | Convert to Select, add options: "Not started", "In progress", "Blocked", "Done", "Cancelled" |
| Entry Verified | Select (add options after import) | Convert to Select, add options: "Not started", "In progress", "Blocked", "Done", "Cancelled" |
| Prepared By | Text | Leave as Text |
| Notes | Text | Leave as Text |
| Sales ID | Text (or Notion auto-ID) | Delete the column and switch the primary column to auto-ID, or keep as Text |
```

One example row per artifact, visibly fake. Money stays `currency`, dates stay `date`,
and anything pointing at another table stays `relation`.

## Field Reference

| # | Field | Type | SQL | JSON Schema | Notion | CSV example |
|---:|---|---|---|---|---|---|
| 1 | Sales Number | `text` | `VARCHAR(255)` | `string` | Text | `SAL-2026-0033` |
| 2 | Customer | `text` | `VARCHAR(255)` | `string` | Text | `Greyson Foods` |
| 3 | Customer PAN/VAT | `text` | `VARCHAR(255)` | `string` | Text | `33CDEFG9012H1Z9` |
| 4 | Sales Order | `relation` | `VARCHAR(255)` | `string` | Relation (link to the target database) | `SO-2026-0094` |
| 5 | Delivery Challan | `relation` | `VARCHAR(255)` | `string` | Relation (link to the target database) | `DC-2026-0911` |
| 6 | Invoice Number | `text` | `VARCHAR(255)` | `string` | Text | `INV-2026-0733` |
| 7 | Invoice Date | `date` | `DATE` | `string, format: date` | Date | `2026-08-16` |
| 8 | Item Description | `text` | `VARCHAR(255)` | `string` | Text | `Corrugated carton packs printed` |
| 9 | Quantity | `number` | `NUMERIC` | `number` | Number | `800` |
| 10 | UOM | `select` | `VARCHAR(100)` | `string` | Select (add options after import) | `Nos` |
| 11 | Rate | `currency` | `NUMERIC(14,2)` | `number` | Number (format: currency) | `142.50` |
| 12 | Gross Amount | `currency` | `NUMERIC(14,2)` | `number` | Number (format: currency) | `114000.00` |
| 13 | Discount | `currency` | `NUMERIC(14,2)` | `number` | Number (format: currency) | `2280.00` |
| 14 | Taxable Value | `currency` | `NUMERIC(14,2)` | `number` | Number (format: currency) | `111720.00` |
| 15 | VAT Rate % | `number` | `NUMERIC` | `number` | Number | `18` |
| 16 | VAT Amount | `currency` | `NUMERIC(14,2)` | `number` | Number (format: currency) | `20109.60` |
| 17 | TDS Rate % | `number` | `NUMERIC` | `number` | Number | `1` |
| 18 | TDS Amount | `currency` | `NUMERIC(14,2)` | `number` | Number (format: currency) | `1117.20` |
| 19 | Invoice Total | `currency` | `NUMERIC(14,2)` | `number` | Number (format: currency) | `131829.60` |
| 20 | Net Receivable | `currency` | `NUMERIC(14,2)` | `number` | Number (format: currency) | `130712.40` |
| 21 | Credit Terms (Days) | `number` | `NUMERIC` | `number` | Number | `30` |
| 22 | Due Date | `date` | `DATE` | `string, format: date` | Date | `2026-09-15` |
| 23 | Receivable Status | `select` | `VARCHAR(100)` | `string` | Select (add options after import) | `Part Paid` |
| 24 | Amount Received | `currency` | `NUMERIC(14,2)` | `number` | Number (format: currency) | `50000.00` |
| 25 | Balance | `currency` | `NUMERIC(14,2)` | `number` | Number (format: currency) | `80712.40` |
| 26 | Ledger Account | `text` | `VARCHAR(255)` | `string` | Text | `Sales - Cartons` |
| 27 | Source Document | `relation` | `VARCHAR(255)` | `string` | Relation (link to the target database) | `DOC-2026-0455` |
| 28 | VAT Register Updated | `select` | `VARCHAR(100)` | `string` | Select (add options after import) | `Done` |
| 29 | Entry Verified | `select` | `VARCHAR(100)` | `string` | Select (add options after import) | `In progress` |
| 30 | Prepared By | `text` | `VARCHAR(255)` | `string` | Text | `Ananya Rao` |
| 31 | Notes | `long_text` | `TEXT` | `string` | Text | `Invoice issued with the challan; credit sale net 30.` |
| 32 | Sales ID | `id` | `SERIAL PRIMARY KEY` | `integer` | Text (or Notion auto-ID) | `(blank)` |

## Select Options

**UOM**

```
Nos | Kg | Litre | Metre | Set | Hour | Box | Packet
```
**Receivable Status**

```
Outstanding | Part Paid | Settled | Written Off | Overdue
```
**VAT Register Updated**

```
Not started | In progress | Blocked | Done | Cancelled
```
**Entry Verified**

```
Not started | In progress | Blocked | Done | Cancelled
```

## Relations

Link fields: `Sales Order`, `Delivery Challan`, `Source Document`

- `Sales Order` -> the sales order the invoice was raised against.
- `Delivery Challan` -> the delivery challan that evidences despatch.
- `Source Document` -> the filed document register row for the invoice and its support.

## Examples

**Prompt**

```
We issue credit invoices and nobody can tell which customers have actually paid.
```

**Context first** - one question per message, nothing already answered:

> **Q:** How many invoices a month?
> **A:** About thirty.
>
> **Q:** Do you always raise an order and a challan?
> **A:** Order only for bigger customers.
>
> **Q:** Standard credit period?
> **A:** Net 30.

**Recommended next step** - offered, not built:

> One sales record per invoice, holding the order, challan and source document as relations, the full tax breakdown, and - where the sale is on credit - the due date, the debtor ledger and the outstanding balance - five steps: prepare documents, issue the invoice, update the Sales VAT Register, record in software, confirm the debtor ledger.
>
> Workflow: Order and challan prepared → Invoice issued → VAT register updated → Recorded → Debtor ledger confirmed
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
- Does not raise or send invoices, collect money, or file the VAT return.
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
- `source-document-filing` - files the invoice with its order, challan and other support.
- `receipt-accounting` - clears the receivable carried in Net Receivable and Balance.
- `credit-cycle-analysis` - ages the outstanding balances this module produces.
- `party-ledger-reconciliation` - reconciles the debtor ledger against this register.
- `tds-booking-payment` - handles the TDS customers deduct at 1 per cent.
- `day-book` - the daily entry log this register feeds.

## Reusable Prompt

```
I want to set up sales orders, delivery challans, invoices and the receivables they create for my company.
Ask me one short question at a time, and only about what I have not already told you.
Then recommend the smallest setup that fits, and wait for me to ask before you build it.
When I ask, output CSV, SQL DDL, JSON Schema and a Notion property mapping. Data only.
```
