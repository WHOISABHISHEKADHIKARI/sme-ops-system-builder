---
name: contract-document-renewal
description: "Contract & Document Renewal: context-first intake, then CSV, SQL, JSON Schema and Notion on request. One short question per message. Use for contract tracker."
category: business
risk: safe
source: self
source_type: self
date_added: "2026-09-26"
author: WHOISABHISHEKADHIKARI
tags: [sme, business, operations, database, csv, notion, sql, protect]
tools: [claude, cursor, gemini, antigravity]
---

# Contract & Document Renewal

**What it is:** Renewal management.

## Overview

Works out the smallest useful **Contract & Document Renewal** setup for the business in front of it, then
builds it only when asked. The default output is a short recommendation, not a
spreadsheet. Artifacts - CSV, SQL DDL, JSON Schema, Notion mapping - are produced on
request, from one field list so they cannot drift apart.

Layer: Layer 7: Protect. Fits: Growth stage. Table code: n/a.

## When to Use This Skill

- contract tracker
- renewal calendar
- contract expiry alerts
- vendor agreement register

Also use it when the user says "renewal management", or describes the same process happening in a
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

> **Q:** When is your next renewal?

### Step 2 - Ask only what is missing

Skip anything the user already answered, in any earlier message. Ask the rest one at a
time, and stop as soon as the remaining answers would not change the output.

- **Documents** - How many contracts? / Which types? / Customers or vendors?
- **Dates** - Renewal date known? / Notice period? / Auto-renew or manual?
- **Ownership** - Who owns each? / Who signs? / Where stored?
- **Current process** - Is it tracked now? / Calendar or reminders? / What gets missed?
- **Outcome** - What do you need? / A renewal calendar, an owner list or both?

Never invent an answer. If the user does not know, record it as unknown and carry on.

### Step 3 - Build the internal context

Hold the answers in this shape. It stays internal - it is not shown to the user unless
they ask, and it never carries a value the user did not give.

```yaml
module: contract-document-renewal
intent: null            # set in Step 1, one of: set up, fix, review, report, import
scale: null             # Starter | Growth | Scale, only if the answer changes it
areas:
  "Documents": null
  "Dates": null
  "Ownership": null
  "Current process": null
  "Outcome": null
requested_outputs: []   # csv | sql | json | notion - only what was explicitly asked for
confirmed_facts: []     # only what the user actually said
open_questions: []      # the unanswered ones, in the order worth asking
```

### Step 4 - Recommend the smallest workflow

Give a short recommendation, then ask whether to build it. Do not build unprompted.

**Recommended approach:** Track the renewal date, the notice deadline and the owner as one record. Set the notice date as the trigger, not the renewal date.

**Why this one:** Renewals are missed because the notice deadline is earlier than the renewal date. Record both and act on the earlier one.

**Workflow:** Contract recorded → Notice window → Reminder → Review → Renewed, amended or ended

### Step 5 - Build only on request

Once the user asks for it, derive the fields from the confirmed context and emit the
artifacts as data only. No preamble, no summary, no closing line.

```csv
Contract Title,Counterparty,Contract Type,Owner,Department,Start Date,End Date,Renewal Notice (Days),Auto-Renew,Contract Value,Currency,Linked Legal Record,Status,Contract ID
Northwind MSA,Acme Corp,Customer,Sneha Iyer,Delivery,2025-10-01,2026-09-30,60,FALSE,450000.00,INR,LEG-2026-007,In Renewal,
```

```sql
CREATE TABLE contract_document_renewal (
  contract_title VARCHAR(255),
  counterparty VARCHAR(255),
  contract_type VARCHAR(100) NOT NULL,
  owner VARCHAR(255),
  department VARCHAR(255),
  start_date DATE NOT NULL,
  end_date DATE NOT NULL,
  renewal_notice_days NUMERIC NOT NULL,
  auto_renew BOOLEAN NOT NULL,
  contract_value NUMERIC(14,2) NOT NULL,
  currency VARCHAR(255),
  linked_legal_record VARCHAR(255),  -- relation -> target record
  status VARCHAR(100) NOT NULL,
  contract_id SERIAL PRIMARY KEY,
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_contract_document_renewal_status ON contract_document_renewal (status);
```

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "Contract & Document Renewal",
  "type": "object",
  "additionalProperties": false,
  "properties": {
      "Contract Title": { "type": "string" },
      "Counterparty": { "type": "string" },
      "Contract Type": { "type": "string" },
      "Owner": { "type": "string" },
      "Department": { "type": "string" },
      "Start Date": { "type": "string", "format": "date" },
      "End Date": { "type": "string", "format": "date" },
      "Renewal Notice (Days)": { "type": "number" },
      "Auto-Renew": { "type": "boolean" },
      "Contract Value": { "type": "number" },
      "Currency": { "type": "string" },
      "Linked Legal Record": { "type": "string" },
      "Status": { "type": "string" },
      "Contract ID": { "type": "integer" }
  },
  "required": [
      "Contract Type",
      "Start Date",
      "End Date",
      "Renewal Notice (Days)",
      "Contract Value",
      "Status"
  ]
}
```

```markdown
| CSV column | Notion property | Set after import |
|---|---|---|
| Contract Title | Text | Leave as Text |
| Counterparty | Text | Leave as Text |
| Contract Type | Select (add options after import) | Convert to Select, add options: "Customer", "Vendor", "Employment", "Lease", "Service", "NDA" |
| Owner | Text | Leave as Text |
| Department | Text | Leave as Text |
| Start Date | Date | Convert to Date |
| End Date | Date | Convert to Date |
| Renewal Notice (Days) | Number | Convert to Number |
| Auto-Renew | Checkbox | Convert to Checkbox |
| Contract Value | Number (format: currency) | Convert to Number, set format to Currency |
| Currency | Text | Leave as Text |
| Linked Legal Record | Relation (link to the target database) | Convert to Relation, link to the target database |
| Status | Select (add options after import) | Convert to Select, add options: "Active", "Expiring Soon", "In Renewal", "Renewed", "Expired", "Terminated" |
| Contract ID | Text (or Notion auto-ID) | Delete the column and switch the primary column to auto-ID, or keep as Text |
```

One example row per artifact, visibly fake. Money stays `currency`, dates stay `date`,
and anything pointing at another table stays `relation`.

## Field Reference

| # | Field | Type | SQL | JSON Schema | Notion | CSV example |
|---:|---|---|---|---|---|---|
| 1 | Contract Title | `text` | `VARCHAR(255)` | `string` | Text | `Northwind MSA` |
| 2 | Counterparty | `text` | `VARCHAR(255)` | `string` | Text | `Acme Corp` |
| 3 | Contract Type | `select` | `VARCHAR(100)` | `string` | Select (add options after import) | `Customer` |
| 4 | Owner | `text` | `VARCHAR(255)` | `string` | Text | `Sneha Iyer` |
| 5 | Department | `text` | `VARCHAR(255)` | `string` | Text | `Delivery` |
| 6 | Start Date | `date` | `DATE` | `string, format: date` | Date | `2025-10-01` |
| 7 | End Date | `date` | `DATE` | `string, format: date` | Date | `2026-09-30` |
| 8 | Renewal Notice (Days) | `number` | `NUMERIC` | `number` | Number | `60` |
| 9 | Auto-Renew | `checkbox` | `BOOLEAN` | `boolean` | Checkbox | `FALSE` |
| 10 | Contract Value | `currency` | `NUMERIC(14,2)` | `number` | Number (format: currency) | `450000.00` |
| 11 | Currency | `text` | `VARCHAR(255)` | `string` | Text | `INR` |
| 12 | Linked Legal Record | `relation` | `VARCHAR(255)` | `string` | Relation (link to the target database) | `LEG-2026-007` |
| 13 | Status | `select` | `VARCHAR(100)` | `string` | Select (add options after import) | `In Renewal` |
| 14 | Contract ID | `id` | `SERIAL PRIMARY KEY` | `integer` | Text (or Notion auto-ID) | `(blank)` |

## Select Options

**Contract Type**

```
Customer | Vendor | Employment | Lease | Service | NDA
```
**Status**

```
Active | Expiring Soon | In Renewal | Renewed | Expired | Terminated
```

## Relations

Link fields: `Linked Legal Record`

## Examples

**Prompt**

```
A vendor contract renewed automatically at a higher price because nobody tracked it.
```

**Context first** - one question per message, nothing already answered:

> **Q:** How many contracts?
> **A:** Around fifteen.
>
> **Q:** Notice period?
> **A:** Thirty days on most.
>
> **Q:** Tracked today?
> **A:** In a spreadsheet, partly.

**Recommended next step** - offered, not built:

> Track the renewal date, the notice deadline and the owner as one record. Set the notice date as the trigger, not the renewal date.
>
> Workflow: Contract recorded → Notice window → Reminder → Review → Renewed, amended or ended
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
- Does not review contract terms or provide legal advice.
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
I want to set up renewal management for my company.
Ask me one short question at a time, and only about what I have not already told you.
Then recommend the smallest setup that fits, and wait for me to ask before you build it.
When I ask, output CSV, SQL DDL, JSON Schema and a Notion property mapping. Data only.
```

