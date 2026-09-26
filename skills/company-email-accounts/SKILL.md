---
name: company-email-accounts
description: "Company Email & Accounts: context-first intake, then CSV, SQL, JSON Schema and Notion on request. One short question per message. Use for company email accounts."
category: business
risk: safe
source: self
source_type: self
date_added: "2026-09-26"
author: WHOISABHISHEKADHIKARI
tags: [sme, business, operations, database, csv, notion, sql, onboard]
tools: [claude, cursor, gemini, antigravity]
---

# Company Email & Accounts

**What it is:** Work email, groups and tool accounts for every person.

## Overview

Works out the smallest useful **Company Email & Accounts** setup for the business in front of it, then
builds it only when asked. The default output is a short recommendation, not a
spreadsheet. Artifacts - CSV, SQL DDL, JSON Schema, Notion mapping - are produced on
request, from one field list so they cannot drift apart.

Layer: Layer 3: Onboard. Fits: Starter stage. Table code: n/a.

## When to Use This Skill

- company email accounts
- work account register
- google workspace account list
- tool account tracker

Also use it when the user says "work email, groups and tool accounts for every person", or describes the same process happening in a
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

> **Q:** Which tools need an account per person?

### Step 2 - Ask only what is missing

Skip anything the user already answered, in any earlier message. Ask the rest one at a
time, and stop as soon as the remaining answers would not change the output.

- **Tools** - Which systems? / Google Workspace? / Any paid tools?
- **Accounts** - Who is admin? / Backup admin? / Per user or per device?
- **Security** - Two-factor required? / Password manager? / Shared logins in use?
- **Current process** - Where is the list now? / Admin console or nothing? / Orphaned accounts?
- **Outcome** - What do you need? / An account register, provisioning or removal?

Never invent an answer. If the user does not know, record it as unknown and carry on.

### Step 3 - Build the internal context

Hold the answers in this shape. It stays internal - it is not shown to the user unless
they ask, and it never carries a value the user did not give.

```yaml
module: company-email-accounts
intent: null            # set in Step 1, one of: set up, fix, review, report, import
scale: null             # Starter | Growth | Scale, only if the answer changes it
areas:
  "Tools": null
  "Accounts": null
  "Security": null
  "Current process": null
  "Outcome": null
requested_outputs: []   # csv | sql | json | notion - only what was explicitly asked for
confirmed_facts: []     # only what the user actually said
open_questions: []      # the unanswered ones, in the order worth asking
```

### Step 4 - Recommend the smallest workflow

Give a short recommendation, then ask whether to build it. Do not build unprompted. Ask: "Want me to build the CSV, SQL DDL, JSON Schema, Notion mapping, or an Excel workbook from these confirmed rules?"

**Recommended approach:** Build an account register tied to people records, then provision and remove from that one list.

**Why this one:** Account sprawl is a security problem, not an admin problem. One register per person, with join and leave dates, is the whole fix.

**Workflow:** Joiner → Create accounts → Assign tools → Leave → Remove access → Log

### Step 5 - Build only on request

Once the user asks for it, derive the fields from the confirmed context and emit the
artifacts as data only. No preamble, no summary, no closing line.

An Excel workbook is the CSV emitted with a UTF-8 byte order mark, so Excel opens it with
correct text and no import dialog. A CSV carries no types, so after it, name the columns
that need a number, date or currency format applied.

```csv
Account Record,Employee Name,Department,Account Type,Work Email,Aliases,Email Groups,Tool or System,Licence Type,Licence Cost,Currency,Created Date,Created By,Two Factor On,Recovery Email Set,Password Policy Met,Last Access Review,Access Removed Date,Handover To,Status,Notes,Account ID
ACC-204,Aarav Sharma,Delivery,Work Email,aarav.sharma@example.com,"aarav.sharma, a.sharma","all-staff, delivery-team",Zoho Mail,Per User,144000.00,INR,2026-01-15,Ananya Rao,TRUE,FALSE,FALSE,2026-01-15,2026-01-15,Vikram Singh,Active,Shared team mailbox still has two people on it; both were removed in February.,
```

```sql
CREATE TABLE company_email_accounts (
  account_record VARCHAR(255),
  employee_name VARCHAR(255),
  department VARCHAR(255),
  account_type VARCHAR(100) NOT NULL,
  work_email VARCHAR(255),
  aliases VARCHAR(255),
  email_groups VARCHAR(255),
  tool_or_system VARCHAR(255),
  licence_type VARCHAR(100) NOT NULL,
  licence_cost NUMERIC(14,2) NOT NULL,
  currency VARCHAR(255),
  created_date DATE NOT NULL,
  created_by VARCHAR(255),
  two_factor_on BOOLEAN NOT NULL,
  recovery_email_set BOOLEAN NOT NULL,
  password_policy_met BOOLEAN NOT NULL,
  last_access_review DATE NOT NULL,
  access_removed_date DATE NOT NULL,
  handover_to VARCHAR(255),
  status VARCHAR(100) NOT NULL,
  notes TEXT,
  account_id SERIAL PRIMARY KEY,
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_company_email_accounts_status ON company_email_accounts (status);
```

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "Company Email & Accounts",
  "type": "object",
  "additionalProperties": false,
  "properties": {
      "Account Record": { "type": "string" },
      "Employee Name": { "type": "string" },
      "Department": { "type": "string" },
      "Account Type": { "type": "string" },
      "Work Email": { "type": "string", "format": "email" },
      "Aliases": { "type": "string" },
      "Email Groups": { "type": "string" },
      "Tool or System": { "type": "string" },
      "Licence Type": { "type": "string" },
      "Licence Cost": { "type": "number" },
      "Currency": { "type": "string" },
      "Created Date": { "type": "string", "format": "date" },
      "Created By": { "type": "string" },
      "Two Factor On": { "type": "boolean" },
      "Recovery Email Set": { "type": "boolean" },
      "Password Policy Met": { "type": "boolean" },
      "Last Access Review": { "type": "string", "format": "date" },
      "Access Removed Date": { "type": "string", "format": "date" },
      "Handover To": { "type": "string" },
      "Status": { "type": "string" },
      "Notes": { "type": "string" },
      "Account ID": { "type": "integer" }
  },
  "required": [
      "Account Type",
      "Licence Type",
      "Licence Cost",
      "Created Date",
      "Last Access Review",
      "Access Removed Date",
      "Status"
  ]
}
```

```markdown
| CSV column | Notion property | Set after import |
|---|---|---|
| Account Record | Text | Leave as Text |
| Employee Name | Text | Leave as Text |
| Department | Text | Leave as Text |
| Account Type | Select (add options after import) | Convert to Select, add options: "Work Email", "Email Group", "Tool Account", "Admin Account", "Shared Inbox" |
| Work Email | Email | Convert to Email |
| Aliases | Text | Leave as Text |
| Email Groups | Text | Leave as Text |
| Tool or System | Text | Leave as Text |
| Licence Type | Select (add options after import) | Convert to Select, add options: "Per User", "Per Device", "Enterprise", "Free" |
| Licence Cost | Number (format: currency) | Convert to Number, set format to Currency |
| Currency | Text | Leave as Text |
| Created Date | Date | Convert to Date |
| Created By | Text | Leave as Text |
| Two Factor On | Checkbox | Convert to Checkbox |
| Recovery Email Set | Checkbox | Convert to Checkbox |
| Password Policy Met | Checkbox | Convert to Checkbox |
| Last Access Review | Date | Convert to Date |
| Access Removed Date | Date | Convert to Date |
| Handover To | Text | Leave as Text |
| Status | Select (add options after import) | Convert to Select, add options: "Active", "Suspended", "Pending Offboarding", "Closed" |
| Notes | Text | Leave as Text |
| Account ID | Text (or Notion auto-ID) | Delete the column and switch the primary column to auto-ID, or keep as Text |
```

One example row per artifact, visibly fake. Money stays `currency`, dates stay `date`,
and anything pointing at another table stays `relation`.

## Field Reference

| # | Field | Type | SQL | JSON Schema | Notion | CSV example |
|---:|---|---|---|---|---|---|
| 1 | Account Record | `text` | `VARCHAR(255)` | `string` | Text | `ACC-204` |
| 2 | Employee Name | `text` | `VARCHAR(255)` | `string` | Text | `Aarav Sharma` |
| 3 | Department | `text` | `VARCHAR(255)` | `string` | Text | `Delivery` |
| 4 | Account Type | `select` | `VARCHAR(100)` | `string` | Select (add options after import) | `Work Email` |
| 5 | Work Email | `email` | `VARCHAR(255)` | `string, format: email` | Email | `aarav.sharma@example.com` |
| 6 | Aliases | `text` | `VARCHAR(255)` | `string` | Text | `aarav.sharma, a.sharma` |
| 7 | Email Groups | `text` | `VARCHAR(255)` | `string` | Text | `all-staff, delivery-team` |
| 8 | Tool or System | `text` | `VARCHAR(255)` | `string` | Text | `Zoho Mail` |
| 9 | Licence Type | `select` | `VARCHAR(100)` | `string` | Select (add options after import) | `Per User` |
| 10 | Licence Cost | `currency` | `NUMERIC(14,2)` | `number` | Number (format: currency) | `144000.00` |
| 11 | Currency | `text` | `VARCHAR(255)` | `string` | Text | `INR` |
| 12 | Created Date | `date` | `DATE` | `string, format: date` | Date | `2026-01-15` |
| 13 | Created By | `text` | `VARCHAR(255)` | `string` | Text | `Ananya Rao` |
| 14 | Two Factor On | `checkbox` | `BOOLEAN` | `boolean` | Checkbox | `TRUE` |
| 15 | Recovery Email Set | `checkbox` | `BOOLEAN` | `boolean` | Checkbox | `FALSE` |
| 16 | Password Policy Met | `checkbox` | `BOOLEAN` | `boolean` | Checkbox | `FALSE` |
| 17 | Last Access Review | `date` | `DATE` | `string, format: date` | Date | `2026-01-15` |
| 18 | Access Removed Date | `date` | `DATE` | `string, format: date` | Date | `2026-01-15` |
| 19 | Handover To | `text` | `VARCHAR(255)` | `string` | Text | `Vikram Singh` |
| 20 | Status | `select` | `VARCHAR(100)` | `string` | Select (add options after import) | `Active` |
| 21 | Notes | `long_text` | `TEXT` | `string` | Text | `Shared team mailbox still has two people on it; both were removed in February.` |
| 22 | Account ID | `id` | `SERIAL PRIMARY KEY` | `integer` | Text (or Notion auto-ID) | `(blank)` |

## Select Options

**Account Type**

```
Work Email | Email Group | Tool Account | Admin Account | Shared Inbox
```
**Licence Type**

```
Per User | Per Device | Enterprise | Free
```
**Status**

```
Active | Suspended | Pending Offboarding | Closed
```

## Relations

Link fields: none

## Examples

**Prompt**

```
People leave and their tool logins stay active for months.
```

**Context first** - one question per message, nothing already answered:

> **Q:** Which tools?
> **A:** Google, Slack and the CRM.
>
> **Q:** Who is admin?
> **A:** One person, no backup.
>
> **Q:** How do you track it?
> **A:** Nowhere.

**Recommended next step** - offered, not built:

> Build an account register tied to people records, then provision and remove from that one list.
>
> Workflow: Joiner → Create accounts → Assign tools → Leave → Remove access → Log
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
- Does not create or delete accounts. It only records what should exist.
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
I want to set up work email, groups and tool accounts for every person for my company.
Ask me one short question at a time, and only about what I have not already told you.
Then recommend the smallest setup that fits, and wait for me to ask before you build it.
When I ask, output CSV, SQL DDL, JSON Schema, a Notion property mapping or an Excel workbook. Data only.
```

