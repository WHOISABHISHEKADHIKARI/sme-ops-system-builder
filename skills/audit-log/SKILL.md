---
name: audit-log
description: "Audit Log: context-first intake, then CSV, SQL, JSON Schema and Notion on request. One short question per message. Use for audit log."
category: business
risk: safe
source: self
source_type: self
date_added: "2026-09-26"
author: WHOISABHISHEKADHIKARI
tags: [sme, business, operations, database, csv, notion, sql, protect]
tools: []
---

# Audit Log

**What it is:** Compliance trail.

## Overview

Works out the smallest useful **Audit Log** setup for the business in front of it, then
builds it only when asked. The default output is a short recommendation, not a
spreadsheet. Artifacts - CSV, SQL DDL, JSON Schema, Notion mapping - are produced on
request, from one field list so they cannot drift apart.

Layer: Layer 7: Protect. Fits: Scale stage. Table code: n/a.

## When to Use This Skill

- audit log
- change history tracker
- activity log database
- compliance trail

Also use it when the user says "compliance trail", or describes the same process happening in a
spreadsheet, a document or someone inboxes.

Do not use it for: payroll calculation, tax filing, or legal advice. This skill produces
empty templates only - it never holds or processes real employee or customer data.

## How It Works

Follow the [shared execution contract](../../references/execution-contract.md). The module-specific rules below define only domain fields, decisions, calculations, and safety constraints.

### Step 1 - Identify intent

Read the request and pick the intent before asking anything.

- "set up" or "build" or "create" -> the user wants artifacts; go to Step 2.
- "our process is ..." or "it is in a sheet" -> the user wants to move an existing process; capture it, then Step 2.
- "is this right" or "review" or "audit" -> the user wants a check, not a build; answer from what they share.
- "how do I ..." -> advice question; answer directly and offer the build only if it helps.

One message, one question, no batching. Open with:

> **Q:** What do you need to be able to prove?

### Step 2 - Ask only what is missing

Skip anything the user already answered, in any earlier message. Ask the rest one at a
time, and stop as soon as the remaining answers would not change the output.

- **Purpose** - Which decision or process? / Internal or external? / Who asks for it?
- **Events** - What must be recorded? / Approvals or changes? / How far back?
- **Evidence** - Who can read it? / Tamper evidence needed? / Retention period?
- **Current process** - Is anything logged now? / Email or spreadsheet? / Is it complete?
- **Outcome** - What do you need? / A log definition, a register or reporting?

Never invent an answer. If the user does not know, record it as unknown and carry on.

### Step 3 - Hold the internal context

Hold the answers in this shape. It stays internal - it is not shown to the user unless
they ask, and it never carries a value the user did not give.

```yaml
module: audit-log
intent: null            # set in Step 1, one of: set up, fix, review, report, import
scale: null             # Starter | Growth | Scale, only if the answer changes it
areas:
  "Purpose": null
  "Events": null
  "Evidence": null
  "Current process": null
  "Outcome": null
requested_outputs: []   # csv | sql | json | notion - only what was explicitly asked for
confirmed_facts: []     # only what the user actually said
open_questions: []      # the unanswered ones, in the order worth asking
```

### Step 4 - Recommend the smallest workflow

Give a short recommendation, then ask whether to build it. Do not build unprompted. Ask: "Want me to build the CSV, SQL DDL, JSON Schema, Notion mapping, or an Excel workbook from these confirmed rules?"

**Recommended approach:** Define the small set of events worth keeping and record who did what and when. Depth follows the question you need to answer.

**Why this one:** Audit logs become useless when everything is captured. Start from the question you need to answer, then record only what answers it.

**Workflow:** Event recorded → Actor and time → Stored → Periodically reviewed → Evidence produced

### Step 5 - Build only on request

Once the user asks for it, derive the fields from the confirmed context and emit the
artifacts as data only. No preamble, no summary, no closing line.

For an Excel-compatible CSV, use UTF-8 with a byte order mark so Excel opens the
text correctly. A CSV is not an `.xlsx` workbook; create `.xlsx` only when the user
requests a workbook.
A CSV carries no types, so after it, name the columns
that need a number, date or currency format applied.

```csv
Log Entry,Date and Time,User,Module,Record,Action,Field Changed,Old Value,New Value,Reason,Log ID
Policy updated,2026-01-15 09:30,Example User,Invoices & Billing,INV-EXAMPLE-001,Update,Status,Draft,Sent,Correction made after a review query,
```

```sql
CREATE TABLE audit_log (
  log_entry VARCHAR(255),
  date_and_time TIMESTAMP NOT NULL,
  user_account VARCHAR(255),
  module VARCHAR(255),
  record VARCHAR(255),
  action VARCHAR(255),
  field_changed VARCHAR(255),
  old_value VARCHAR(255),
  new_value VARCHAR(255),
  reason VARCHAR(255),
  log_id SERIAL PRIMARY KEY,
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);
```

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "Audit Log",
  "type": "object",
  "additionalProperties": false,
  "properties": {
      "Log Entry": { "type": "string" },
      "Date and Time": { "type": "string", "format": "date-time" },
      "User": { "type": "string" },
      "Module": { "type": "string" },
      "Record": { "type": "string" },
      "Action": { "type": "string" },
      "Field Changed": { "type": "string" },
      "Old Value": { "type": "string" },
      "New Value": { "type": "string" },
      "Reason": { "type": "string" },
      "Log ID": { "type": "integer" }
  },
  "required": [
      "Date and Time"
  ]
}
```

```markdown
| CSV column | Notion property | Set after import |
|---|---|---|
| Log Entry | Text | Leave as Text |
| Date and Time | Date (include time) | Convert to Date (include time) |
| User | Text | Leave as Text |
| Module | Text | Leave as Text |
| Record | Text | Leave as Text |
| Action | Text | Leave as Text |
| Field Changed | Text | Leave as Text |
| Old Value | Text | Leave as Text |
| New Value | Text | Leave as Text |
| Reason | Text | Leave as Text |
| Log ID | Text (or Notion auto-ID) | Delete the column and switch the primary column to auto-ID, or keep as Text |
```

The rows above are documentation examples only. Emit empty templates unless the user explicitly requests examples. Money stays `currency`, dates stay `date`,
and anything pointing at another table stays `relation`.

## Field Reference

| # | Field | Type | SQL | JSON Schema | Notion | CSV example |
|---:|---|---|---|---|---|---|
| 1 | Log Entry | `text` | `VARCHAR(255)` | `string` | Text | `Policy updated` |
| 2 | Date and Time | `datetime` | `TIMESTAMP` | `string, format: date-time` | Date (include time) | `2026-01-15 09:30` |
| 3 | User | `text` | `VARCHAR(255)` | `string` | Text | `Example User` |
| 4 | Module | `text` | `VARCHAR(255)` | `string` | Text | `Invoices & Billing` |
| 5 | Record | `text` | `VARCHAR(255)` | `string` | Text | `INV-EXAMPLE-001` |
| 6 | Action | `text` | `VARCHAR(255)` | `string` | Text | `Update` |
| 7 | Field Changed | `text` | `VARCHAR(255)` | `string` | Text | `Status` |
| 8 | Old Value | `text` | `VARCHAR(255)` | `string` | Text | `Draft` |
| 9 | New Value | `text` | `VARCHAR(255)` | `string` | Text | `Sent` |
| 10 | Reason | `text` | `VARCHAR(255)` | `string` | Text | `Correction made after a review query` |
| 11 | Log ID | `id` | `SERIAL PRIMARY KEY` | `integer` | Text (or Notion auto-ID) | `(blank)` |

## Select Options

_No Select fields._

## Relations

Link fields: none

## Examples

**Prompt**

```
When a client questioned an approval we had nothing to show.
```

**Context first** - one question per message, nothing already answered:

> **Q:** Which process?
> **A:** Expense approvals.
>
> **Q:** Who asks?
> **A:** Our accountant, at year end.
>
> **Q:** How far back?
> **A:** Three years.

**Recommended next step** - offered, not built:

> Define the small set of events worth keeping and record who did what and when. Depth follows the question you need to answer.
>
> Workflow: Event recorded → Actor and time → Stored → Periodically reviewed → Evidence produced
>
> Want the CSV, SQL, JSON Schema and Notion mapping for this?

## Best Practices

- Recommend before building. The recommendation is the product; the files are the follow-up.
- One question per message. A batched intake reads as a form and gets guessed at.
- Keep every field name identical across CSV, SQL and JSON Schema.
- Use `relation` for anything that points at another table, `text` only for free text.
- Money fields are `currency`, never `text`. Dates are `date`, never free text.
- If the user requests an example row, keep it obviously fake so nobody imports it as real data.

## Limitations

- Empty template only. It does not compute payroll, tax, leave balances or KPIs.
- Notion relations need both databases imported before the link column resolves.
- Select options are a starting set. Rename them to match how the business talks.
- No automation, reminders or sync. Those need the integration layer.
- Does not provide legal assurance of compliance or act as a security control on its own.
- Legal, tax and HR review is still required before this drives real decisions.

## Security & Safety Notes

- Never fill in real names, salaries, medical or banking data. Placeholders only.
- Never mark an example row `Confidential`, and keep bank details masked.
- Creating a requested artifact may write that artifact locally. Do not run commands,
  call APIs, provision infrastructure, or make other external changes unless the user
  explicitly requests and authorizes them.
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
I want to set up compliance trail for my company.
Ask me one short question at a time, and only about what I have not already told you.
Then recommend the smallest setup that fits, and wait for me to ask before you build it.
When I ask, output CSV, SQL DDL, JSON Schema, a Notion property mapping or an Excel workbook. Data only.
```

