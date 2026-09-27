---
name: clients-accounts
description: "Clients & Accounts: context-first intake, then CSV, SQL, JSON Schema and Notion on request. One short question per message. Use for client database."
category: business
risk: safe
source: self
source_type: self
date_added: "2026-09-26"
author: WHOISABHISHEKADHIKARI
tags: [sme, business, operations, database, csv, notion, sql, operate]
tools: [claude, cursor, gemini, antigravity]
---

# Clients & Accounts

**What it is:** Every client with contacts, terms and what they owe.

## Overview

Works out the smallest useful **Clients & Accounts** setup for the business in front of it, then
builds it only when asked. The default output is a short recommendation, not a
spreadsheet. Artifacts - CSV, SQL DDL, JSON Schema, Notion mapping - are produced on
request, from one field list so they cannot drift apart.

Layer: Layer 8: Operate. Fits: Starter stage. Table code: n/a.

## When to Use This Skill

- client database
- customer records
- client account tracker
- accounts receivable list

Also use it when the user says "every client with contacts, terms and what they owe", or describes the same process happening in a
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

> **Q:** How many active clients do you have?

### Step 2 - Ask only what is missing

Skip anything the user already answered, in any earlier message. Ask the rest one at a
time, and stop as soon as the remaining answers would not change the output.

- **Clients** - How many active? / Who owns each relationship? / Any churn risk?
- **Details** - Billing details needed? / Contacts per client? / Contract linked?
- **Activity** - How often do you speak? / Meetings logged? / Any health score?
- **Current process** - Where are clients recorded? / CRM or spreadsheet? / What is missing?
- **Outcome** - What do you need? / A client register, a pipeline or reporting?

Never invent an answer. If the user does not know, record it as unknown and carry on.

### Step 3 - Hold the internal context

Hold the answers in this shape. It stays internal - it is not shown to the user unless
they ask, and it never carries a value the user did not give.

```yaml
module: clients-accounts
intent: null            # set in Step 1, one of: set up, fix, review, report, import
scale: null             # Starter | Growth | Scale, only if the answer changes it
areas:
  "Clients": null
  "Details": null
  "Activity": null
  "Current process": null
  "Outcome": null
requested_outputs: []   # csv | sql | json | notion - only what was explicitly asked for
confirmed_facts: []     # only what the user actually said
open_questions: []      # the unanswered ones, in the order worth asking
```

### Step 4 - Recommend the smallest workflow

Give a short recommendation, then ask whether to build it. Do not build unprompted. Ask: "Want me to build the CSV, SQL DDL, JSON Schema, Notion mapping, or an Excel workbook from these confirmed rules?"

**Recommended approach:** One record per client with a named owner and next action, and keep activity notes on that record rather than in a separate log.

**Why this one:** Client records go stale when contact details change. A named owner and a next-action date keep the register usable.

**Workflow:** Client recorded → Owner assigned → Activity logged → Next action → Review

### Step 5 - Build only on request

Once the user asks for it, derive the fields from the confirmed context and emit the
artifacts as data only. No preamble, no summary, no closing line.

An Excel workbook is the CSV emitted with a UTF-8 byte order mark, so Excel opens it with
correct text and no import dialog. A CSV carries no types, so after it, name the columns
that need a number, date or currency format applied.

```csv
Client Name,Client Type,Industry,Contact Person,Email,Phone,Billing Address,Tax ID,Currency,Payment Terms (Days),Account Manager,Projects,Invoices,Total Invoiced,Total Paid,Outstanding,Client Portal Access,Status,Notes,Client ID
Northwind Traders,Retainer,Professional services,Rahul Mehta,aarav.sharma@example.com,+91 98xxxxxx21,"14 MG Road, Bengaluru 560001",29ABCDE1234F1Z5,INR,30,Rahul Mehta,"Website Redesign, Data Migration","INV-1041, INV-1042",1392400.00,1253160.00,13800.00,"Read-only portal, expires 31 Mar",Active,Account review set for March once the quarterly numbers are signed off.,
```

```sql
CREATE TABLE clients_accounts (
  client_name VARCHAR(255),
  client_type VARCHAR(100) NOT NULL,
  industry VARCHAR(255),
  contact_person VARCHAR(255),
  email VARCHAR(255),
  phone VARCHAR(255),
  billing_address VARCHAR(255),
  tax_id VARCHAR(255),
  currency VARCHAR(255),
  payment_terms_days NUMERIC NOT NULL,
  account_manager VARCHAR(255),
  projects VARCHAR(255),
  invoices VARCHAR(255),
  total_invoiced NUMERIC(14,2) NOT NULL,
  total_paid NUMERIC(14,2) NOT NULL,
  outstanding NUMERIC(14,2) NOT NULL,
  client_portal_access VARCHAR(255),
  status VARCHAR(100) NOT NULL,
  notes TEXT,
  client_id SERIAL PRIMARY KEY,
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_clients_accounts_status ON clients_accounts (status);
```

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "Clients & Accounts",
  "type": "object",
  "additionalProperties": false,
  "properties": {
      "Client Name": { "type": "string" },
      "Client Type": { "type": "string" },
      "Industry": { "type": "string" },
      "Contact Person": { "type": "string" },
      "Email": { "type": "string", "format": "email" },
      "Phone": { "type": "string" },
      "Billing Address": { "type": "string" },
      "Tax ID": { "type": "string" },
      "Currency": { "type": "string" },
      "Payment Terms (Days)": { "type": "number" },
      "Account Manager": { "type": "string" },
      "Projects": { "type": "string" },
      "Invoices": { "type": "string" },
      "Total Invoiced": { "type": "number" },
      "Total Paid": { "type": "number" },
      "Outstanding": { "type": "number" },
      "Client Portal Access": { "type": "string" },
      "Status": { "type": "string" },
      "Notes": { "type": "string" },
      "Client ID": { "type": "integer" }
  },
  "required": [
      "Client Type",
      "Payment Terms (Days)",
      "Total Invoiced",
      "Total Paid",
      "Outstanding",
      "Status"
  ]
}
```

```markdown
| CSV column | Notion property | Set after import |
|---|---|---|
| Client Name | Text | Leave as Text |
| Client Type | Select (add options after import) | Convert to Select, add options: "Retainer", "Project", "One Off", "Enterprise", "SME" |
| Industry | Text | Leave as Text |
| Contact Person | Text | Leave as Text |
| Email | Email | Convert to Email |
| Phone | Text | Leave as Text |
| Billing Address | Text | Leave as Text |
| Tax ID | Text | Leave as Text |
| Currency | Text | Leave as Text |
| Payment Terms (Days) | Number | Convert to Number |
| Account Manager | Text | Leave as Text |
| Projects | Text | Leave as Text |
| Invoices | Text | Leave as Text |
| Total Invoiced | Number (format: currency) | Convert to Number, set format to Currency |
| Total Paid | Number (format: currency) | Convert to Number, set format to Currency |
| Outstanding | Number (format: currency) | Convert to Number, set format to Currency |
| Client Portal Access | Text | Leave as Text |
| Status | Select (add options after import) | Convert to Select, add options: "Prospect", "Active", "Onboarding", "At Risk", "Closed", "Lost" |
| Notes | Text | Leave as Text |
| Client ID | Text (or Notion auto-ID) | Delete the column and switch the primary column to auto-ID, or keep as Text |
```

One example row per artifact, visibly fake. Money stays `currency`, dates stay `date`,
and anything pointing at another table stays `relation`.

## Field Reference

| # | Field | Type | SQL | JSON Schema | Notion | CSV example |
|---:|---|---|---|---|---|---|
| 1 | Client Name | `text` | `VARCHAR(255)` | `string` | Text | `Northwind Traders` |
| 2 | Client Type | `select` | `VARCHAR(100)` | `string` | Select (add options after import) | `Retainer` |
| 3 | Industry | `text` | `VARCHAR(255)` | `string` | Text | `Professional services` |
| 4 | Contact Person | `text` | `VARCHAR(255)` | `string` | Text | `Rahul Mehta` |
| 5 | Email | `email` | `VARCHAR(255)` | `string, format: email` | Email | `aarav.sharma@example.com` |
| 6 | Phone | `text` | `VARCHAR(255)` | `string` | Text | `+91 98xxxxxx21` |
| 7 | Billing Address | `text` | `VARCHAR(255)` | `string` | Text | `14 MG Road, Bengaluru 560001` |
| 8 | Tax ID | `text` | `VARCHAR(255)` | `string` | Text | `29ABCDE1234F1Z5` |
| 9 | Currency | `text` | `VARCHAR(255)` | `string` | Text | `INR` |
| 10 | Payment Terms (Days) | `number` | `NUMERIC` | `number` | Number | `30` |
| 11 | Account Manager | `text` | `VARCHAR(255)` | `string` | Text | `Rahul Mehta` |
| 12 | Projects | `text` | `VARCHAR(255)` | `string` | Text | `Website Redesign, Data Migration` |
| 13 | Invoices | `text` | `VARCHAR(255)` | `string` | Text | `INV-1041, INV-1042` |
| 14 | Total Invoiced | `currency` | `NUMERIC(14,2)` | `number` | Number (format: currency) | `1392400.00` |
| 15 | Total Paid | `currency` | `NUMERIC(14,2)` | `number` | Number (format: currency) | `1253160.00` |
| 16 | Outstanding | `currency` | `NUMERIC(14,2)` | `number` | Number (format: currency) | `13800.00` |
| 17 | Client Portal Access | `text` | `VARCHAR(255)` | `string` | Text | `Read-only portal, expires 31 Mar` |
| 18 | Status | `select` | `VARCHAR(100)` | `string` | Select (add options after import) | `Active` |
| 19 | Notes | `long_text` | `TEXT` | `string` | Text | `Account review set for March once the quarterly numbers are signed off.` |
| 20 | Client ID | `id` | `SERIAL PRIMARY KEY` | `integer` | Text (or Notion auto-ID) | `(blank)` |

## Select Options

**Client Type**

```
Retainer | Project | One Off | Enterprise | SME
```
**Status**

```
Prospect | Active | Onboarding | At Risk | Closed | Lost
```

## Relations

Link fields: none

## Examples

**Prompt**

```
Client details live in three people inboxes.
```

**Context first** - one question per message, nothing already answered:

> **Q:** How many active?
> **A:** About fifteen.
>
> **Q:** Where recorded?
> **A:** One shared spreadsheet.
>
> **Q:** Billing details?
> **A:** In an accounting package.

**Recommended next step** - offered, not built:

> One record per client with a named owner and next action, and keep activity notes on that record rather than in a separate log.
>
> Workflow: Client recorded → Owner assigned → Activity logged → Next action → Review
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
- Does not contact clients, send invoices or manage the relationship for you.
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
I want to set up every client with contacts, terms and what they owe for my company.
Ask me one short question at a time, and only about what I have not already told you.
Then recommend the smallest setup that fits, and wait for me to ask before you build it.
When I ask, output CSV, SQL DDL, JSON Schema, a Notion property mapping or an Excel workbook. Data only.
```

