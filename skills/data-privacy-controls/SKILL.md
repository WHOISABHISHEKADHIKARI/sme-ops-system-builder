---
name: data-privacy-controls
description: "Data Privacy Controls: context-first intake, then CSV, SQL, JSON Schema and Notion on request. One short question per message. Use for gdpr compliance."
category: business
risk: safe
source: self
source_type: self
date_added: "2026-09-26"
author: WHOISABHISHEKADHIKARI
tags: [sme, business, operations, database, csv, notion, sql, protect]
tools: [claude, cursor, gemini, antigravity]
---

# Data Privacy Controls

**What it is:** GDPR/CCPA.

## Overview

Works out the smallest useful **Data Privacy Controls** setup for the business in front of it, then
builds it only when asked. The default output is a short recommendation, not a
spreadsheet. Artifacts - CSV, SQL DDL, JSON Schema, Notion mapping - are produced on
request, from one field list so they cannot drift apart.

Layer: Layer 7: Protect. Fits: Scale stage. Table code: n/a.

## When to Use This Skill

- gdpr compliance
- data privacy register
- ccpa controls
- data protection tracker

Also use it when the user says "gdpr/ccpa", or describes the same process happening in a
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

> **Q:** What personal data do you hold?

### Step 2 - Ask only what is missing

Skip anything the user already answered, in any earlier message. Ask the rest one at a
time, and stop as soon as the remaining answers would not change the output.

- **Data** - Which categories? / Employee, customer or both? / How many people affected?
- **Purpose** - Why is it held? / Consent given? / Any special categories?
- **Controls** - Who can access it? / Retention rules? / Deletion process?
- **Current process** - Is it documented? / Any privacy notice? / Has a breach happened?
- **Outcome** - What do you need? / A data inventory, a control list or both?

Never invent an answer. If the user does not know, record it as unknown and carry on.

### Step 3 - Hold the internal context

Hold the answers in this shape. It stays internal - it is not shown to the user unless
they ask, and it never carries a value the user did not give.

```yaml
module: data-privacy-controls
intent: null            # set in Step 1, one of: set up, fix, review, report, import
scale: null             # Starter | Growth | Scale, only if the answer changes it
areas:
  "Data": null
  "Purpose": null
  "Controls": null
  "Current process": null
  "Outcome": null
requested_outputs: []   # csv | sql | json | notion - only what was explicitly asked for
confirmed_facts: []     # only what the user actually said
open_questions: []      # the unanswered ones, in the order worth asking
```

### Step 4 - Recommend the smallest workflow

Give a short recommendation, then ask whether to build it. Do not build unprompted. Ask: "Want me to build the CSV, SQL DDL, JSON Schema, Notion mapping, or an Excel workbook from these confirmed rules?"

**Recommended approach:** Start with an inventory of what is held and why, then attach an owner and a retention rule to each item.

**Why this one:** Privacy work fails without an inventory, because you cannot protect data you have not listed. The inventory comes first.

**Workflow:** Data category listed → Purpose recorded → Owner and access → Retention rule → Review

### Step 5 - Build only on request

Once the user asks for it, derive the fields from the confirmed context and emit the
artifacts as data only. No preamble, no summary, no closing line.

An Excel workbook is the CSV emitted with a UTF-8 byte order mark, so Excel opens it with
correct text and no import dialog. A CSV carries no types, so after it, name the columns
that need a number, date or currency format applied.

```csv
Control,Data Category,Module,Legal Basis,Retention Period,Access Roles,Encryption,Consent Required,Owner,Last Reviewed,Status,Control ID
Employee data retention,Personal,Invoices & Billing,Contractual necessity,24 months after last activity,"People team, Finance",At rest and in transit,FALSE,Sneha Iyer,2026-01-15,Implemented,
```

```sql
CREATE TABLE data_privacy_controls (
  control VARCHAR(255),
  data_category VARCHAR(100) NOT NULL,
  module VARCHAR(255),
  legal_basis VARCHAR(255),
  retention_period VARCHAR(255),
  access_roles VARCHAR(255),
  encryption VARCHAR(255),
  consent_required BOOLEAN NOT NULL,
  owner VARCHAR(255),
  last_reviewed DATE NOT NULL,
  status VARCHAR(100) NOT NULL,
  control_id SERIAL PRIMARY KEY,
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_data_privacy_controls_status ON data_privacy_controls (status);
```

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "Data Privacy Controls",
  "type": "object",
  "additionalProperties": false,
  "properties": {
      "Control": { "type": "string" },
      "Data Category": { "type": "string" },
      "Module": { "type": "string" },
      "Legal Basis": { "type": "string" },
      "Retention Period": { "type": "string" },
      "Access Roles": { "type": "string" },
      "Encryption": { "type": "string" },
      "Consent Required": { "type": "boolean" },
      "Owner": { "type": "string" },
      "Last Reviewed": { "type": "string", "format": "date" },
      "Status": { "type": "string" },
      "Control ID": { "type": "integer" }
  },
  "required": [
      "Data Category",
      "Last Reviewed",
      "Status"
  ]
}
```

```markdown
| CSV column | Notion property | Set after import |
|---|---|---|
| Control | Text | Leave as Text |
| Data Category | Select (add options after import) | Convert to Select, add options: "Personal", "Sensitive", "Financial", "Health", "Biometric", "Location" |
| Module | Text | Leave as Text |
| Legal Basis | Text | Leave as Text |
| Retention Period | Text | Leave as Text |
| Access Roles | Text | Leave as Text |
| Encryption | Text | Leave as Text |
| Consent Required | Checkbox | Convert to Checkbox |
| Owner | Text | Leave as Text |
| Last Reviewed | Date | Convert to Date |
| Status | Select (add options after import) | Convert to Select, add options: "Draft", "In Review", "Approved", "Implemented", "Retired" |
| Control ID | Text (or Notion auto-ID) | Delete the column and switch the primary column to auto-ID, or keep as Text |
```

One example row per artifact, visibly fake. Money stays `currency`, dates stay `date`,
and anything pointing at another table stays `relation`.

## Field Reference

| # | Field | Type | SQL | JSON Schema | Notion | CSV example |
|---:|---|---|---|---|---|---|
| 1 | Control | `text` | `VARCHAR(255)` | `string` | Text | `Employee data retention` |
| 2 | Data Category | `select` | `VARCHAR(100)` | `string` | Select (add options after import) | `Personal` |
| 3 | Module | `text` | `VARCHAR(255)` | `string` | Text | `Invoices & Billing` |
| 4 | Legal Basis | `text` | `VARCHAR(255)` | `string` | Text | `Contractual necessity` |
| 5 | Retention Period | `text` | `VARCHAR(255)` | `string` | Text | `24 months after last activity` |
| 6 | Access Roles | `text` | `VARCHAR(255)` | `string` | Text | `People team, Finance` |
| 7 | Encryption | `text` | `VARCHAR(255)` | `string` | Text | `At rest and in transit` |
| 8 | Consent Required | `checkbox` | `BOOLEAN` | `boolean` | Checkbox | `FALSE` |
| 9 | Owner | `text` | `VARCHAR(255)` | `string` | Text | `Sneha Iyer` |
| 10 | Last Reviewed | `date` | `DATE` | `string, format: date` | Date | `2026-01-15` |
| 11 | Status | `select` | `VARCHAR(100)` | `string` | Select (add options after import) | `Implemented` |
| 12 | Control ID | `id` | `SERIAL PRIMARY KEY` | `integer` | Text (or Notion auto-ID) | `(blank)` |

## Select Options

**Data Category**

```
Personal | Sensitive | Financial | Health | Biometric | Location
```
**Status**

```
Draft | In Review | Approved | Implemented | Retired
```

## Relations

Link fields: none

## Examples

**Prompt**

```
We hold a lot of employee data and cannot say who owns it.
```

**Context first** - one question per message, nothing already answered:

> **Q:** Which categories?
> **A:** Employee and customer contact details.
>
> **Q:** Consent given?
> **A:** For customers, yes.
>
> **Q:** Is it documented?
> **A:** No.

**Recommended next step** - offered, not built:

> Start with an inventory of what is held and why, then attach an owner and a retention rule to each item.
>
> Workflow: Data category listed → Purpose recorded → Owner and access → Retention rule → Review
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
- Does not provide legal advice, and you should involve a qualified reviewer for compliance obligations.
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
I want to set up gdpr/ccpa for my company.
Ask me one short question at a time, and only about what I have not already told you.
Then recommend the smallest setup that fits, and wait for me to ask before you build it.
When I ask, output CSV, SQL DDL, JSON Schema, a Notion property mapping or an Excel workbook. Data only.
```

