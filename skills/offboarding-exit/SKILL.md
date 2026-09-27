---
name: offboarding-exit
description: "Offboarding & Exit: context-first intake, then CSV, SQL, JSON Schema and Notion on request. One short question per message. Use for offboarding checklist."
category: business
risk: safe
source: self
source_type: self
date_added: "2026-09-26"
author: WHOISABHISHEKADHIKARI
tags: [sme, business, operations, database, csv, notion, sql, exit]
tools: [claude, cursor, gemini, antigravity]
---

# Offboarding & Exit

**What it is:** Structured departure.

## Overview

Works out the smallest useful **Offboarding & Exit** setup for the business in front of it, then
builds it only when asked. The default output is a short recommendation, not a
spreadsheet. Artifacts - CSV, SQL DDL, JSON Schema, Notion mapping - are produced on
request, from one field list so they cannot drift apart.

Layer: Layer 10: Exit. Fits: Growth stage. Table code: n/a.

## When to Use This Skill

- offboarding checklist
- exit interview tracker
- employee exit process
- departure checklist

Also use it when the user says "structured departure", or describes the same process happening in a
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

> **Q:** What is the most recent exit?

### Step 2 - Ask only what is missing

Skip anything the user already answered, in any earlier message. Ask the rest one at a
time, and stop as soon as the remaining answers would not change the output.

- **Exit** - How many people? / Last day known? / Resignation or termination?
- **Process** - Who owns it? / Which steps? / Any interview?
- **Access** - Accounts cut when? / Equipment returned? / Final pay handled?
- **Current process** - Is it tracked now? / Checklist or memory? / What gets missed?
- **Outcome** - What do you need? / A checklist, a record or reporting?

Never invent an answer. If the user does not know, record it as unknown and carry on.

### Step 3 - Hold the internal context

Hold the answers in this shape. It stays internal - it is not shown to the user unless
they ask, and it never carries a value the user did not give.

```yaml
module: offboarding-exit
intent: null            # set in Step 1, one of: set up, fix, review, report, import
scale: null             # Starter | Growth | Scale, only if the answer changes it
areas:
  "Exit": null
  "Process": null
  "Access": null
  "Current process": null
  "Outcome": null
requested_outputs: []   # csv | sql | json | notion - only what was explicitly asked for
confirmed_facts: []     # only what the user actually said
open_questions: []      # the unanswered ones, in the order worth asking
```

### Step 4 - Recommend the smallest workflow

Give a short recommendation, then ask whether to build it. Do not build unprompted. Ask: "Want me to build the CSV, SQL DDL, JSON Schema, Notion mapping, or an Excel workbook from these confirmed rules?"

**Recommended approach:** Run a dated checklist from the agreed last day, and record the exit reason while the person can still be asked for feedback.

**Why this one:** Offboarding is the step everyone drops. A dated checklist with a named owner is what stops access, equipment and pay being left open.

**Workflow:** Exit agreed → Checklist started → Access and equipment closed → Final pay confirmed → Exit recorded and reviewed

### Step 5 - Build only on request

Once the user asks for it, derive the fields from the confirmed context and emit the
artifacts as data only. No preamble, no summary, no closing line.

An Excel workbook is the CSV emitted with a UTF-8 byte order mark, so Excel opens it with
correct text and no import dialog. A CSV carries no types, so after it, name the columns
that need a number, date or currency format applied.

```csv
Exit Record,Employee Name,Department,Manager,Exit Type,Notice Date,Last Working Day,Reason,Handover Owner,Knowledge Transfer Done,Assets Returned,Access Removed,Accounts to Close,Final Settlement Done,Exit Interview Done,Rehire Eligible,Status,Exit ID
EXIT-2026-002,Aarav Sharma,Delivery,Sneha Iyer,Resignation,2026-01-15,2026-03-31,Relocating to a new city,Sneha Iyer,FALSE,FALSE,FALSE,6,FALSE,FALSE,TRUE,In Progress,
```

```sql
CREATE TABLE offboarding_exit (
  exit_record VARCHAR(255),
  employee_name VARCHAR(255),
  department VARCHAR(255),
  manager VARCHAR(255),
  exit_type VARCHAR(100) NOT NULL,
  notice_date DATE NOT NULL,
  last_working_day DATE NOT NULL,
  reason VARCHAR(255),
  handover_owner VARCHAR(255),
  knowledge_transfer_done BOOLEAN NOT NULL,
  assets_returned BOOLEAN NOT NULL,
  access_removed BOOLEAN NOT NULL,
  accounts_to_close NUMERIC NOT NULL,
  final_settlement_done BOOLEAN NOT NULL,
  exit_interview_done BOOLEAN NOT NULL,
  rehire_eligible BOOLEAN NOT NULL,
  status VARCHAR(100) NOT NULL,
  exit_id SERIAL PRIMARY KEY,
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_offboarding_exit_status ON offboarding_exit (status);
```

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "Offboarding & Exit",
  "type": "object",
  "additionalProperties": false,
  "properties": {
      "Exit Record": { "type": "string" },
      "Employee Name": { "type": "string" },
      "Department": { "type": "string" },
      "Manager": { "type": "string" },
      "Exit Type": { "type": "string" },
      "Notice Date": { "type": "string", "format": "date" },
      "Last Working Day": { "type": "string", "format": "date" },
      "Reason": { "type": "string" },
      "Handover Owner": { "type": "string" },
      "Knowledge Transfer Done": { "type": "boolean" },
      "Assets Returned": { "type": "boolean" },
      "Access Removed": { "type": "boolean" },
      "Accounts to Close": { "type": "number" },
      "Final Settlement Done": { "type": "boolean" },
      "Exit Interview Done": { "type": "boolean" },
      "Rehire Eligible": { "type": "boolean" },
      "Status": { "type": "string" },
      "Exit ID": { "type": "integer" }
  },
  "required": [
      "Exit Type",
      "Notice Date",
      "Last Working Day",
      "Accounts to Close",
      "Status"
  ]
}
```

```markdown
| CSV column | Notion property | Set after import |
|---|---|---|
| Exit Record | Text | Leave as Text |
| Employee Name | Text | Leave as Text |
| Department | Text | Leave as Text |
| Manager | Text | Leave as Text |
| Exit Type | Select (add options after import) | Convert to Select, add options: "Resignation", "Termination", "Retirement", "End of Contract", "Other" |
| Notice Date | Date | Convert to Date |
| Last Working Day | Date | Convert to Date |
| Reason | Text | Leave as Text |
| Handover Owner | Text | Leave as Text |
| Knowledge Transfer Done | Checkbox | Convert to Checkbox |
| Assets Returned | Checkbox | Convert to Checkbox |
| Access Removed | Checkbox | Convert to Checkbox |
| Accounts to Close | Number | Convert to Number |
| Final Settlement Done | Checkbox | Convert to Checkbox |
| Exit Interview Done | Checkbox | Convert to Checkbox |
| Rehire Eligible | Checkbox | Convert to Checkbox |
| Status | Select (add options after import) | Convert to Select, add options: "Initiated", "In Progress", "Completed", "Cancelled" |
| Exit ID | Text (or Notion auto-ID) | Delete the column and switch the primary column to auto-ID, or keep as Text |
```

One example row per artifact, visibly fake. Money stays `currency`, dates stay `date`,
and anything pointing at another table stays `relation`.

## Field Reference

| # | Field | Type | SQL | JSON Schema | Notion | CSV example |
|---:|---|---|---|---|---|---|
| 1 | Exit Record | `text` | `VARCHAR(255)` | `string` | Text | `EXIT-2026-002` |
| 2 | Employee Name | `text` | `VARCHAR(255)` | `string` | Text | `Aarav Sharma` |
| 3 | Department | `text` | `VARCHAR(255)` | `string` | Text | `Delivery` |
| 4 | Manager | `text` | `VARCHAR(255)` | `string` | Text | `Sneha Iyer` |
| 5 | Exit Type | `select` | `VARCHAR(100)` | `string` | Select (add options after import) | `Resignation` |
| 6 | Notice Date | `date` | `DATE` | `string, format: date` | Date | `2026-01-15` |
| 7 | Last Working Day | `date` | `DATE` | `string, format: date` | Date | `2026-03-31` |
| 8 | Reason | `text` | `VARCHAR(255)` | `string` | Text | `Relocating to a new city` |
| 9 | Handover Owner | `text` | `VARCHAR(255)` | `string` | Text | `Sneha Iyer` |
| 10 | Knowledge Transfer Done | `checkbox` | `BOOLEAN` | `boolean` | Checkbox | `FALSE` |
| 11 | Assets Returned | `checkbox` | `BOOLEAN` | `boolean` | Checkbox | `FALSE` |
| 12 | Access Removed | `checkbox` | `BOOLEAN` | `boolean` | Checkbox | `FALSE` |
| 13 | Accounts to Close | `number` | `NUMERIC` | `number` | Number | `6` |
| 14 | Final Settlement Done | `checkbox` | `BOOLEAN` | `boolean` | Checkbox | `FALSE` |
| 15 | Exit Interview Done | `checkbox` | `BOOLEAN` | `boolean` | Checkbox | `FALSE` |
| 16 | Rehire Eligible | `checkbox` | `BOOLEAN` | `boolean` | Checkbox | `TRUE` |
| 17 | Status | `select` | `VARCHAR(100)` | `string` | Select (add options after import) | `In Progress` |
| 18 | Exit ID | `id` | `SERIAL PRIMARY KEY` | `integer` | Text (or Notion auto-ID) | `(blank)` |

## Select Options

**Exit Type**

```
Resignation | Termination | Retirement | End of Contract | Other
```
**Status**

```
Initiated | In Progress | Completed | Cancelled
```

## Relations

Link fields: none

## Examples

**Prompt**

```
Our last three exits were handled differently by three different people.
```

**Context first** - one question per message, nothing already answered:

> **Q:** How many people?
> **A:** Three this year.
>
> **Q:** Any checklist?
> **A:** Not a written one.
>
> **Q:** Who owns it?
> **A:** Whoever noticed first.

**Recommended next step** - offered, not built:

> Run a dated checklist from the agreed last day, and record the exit reason while the person can still be asked for feedback.
>
> Workflow: Exit agreed → Checklist started → Access and equipment closed → Final pay confirmed → Exit recorded and reviewed
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
- Does not revoke access itself, terminate employment or provide legal advice on the exit.
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
I want to set up structured departure for my company.
Ask me one short question at a time, and only about what I have not already told you.
Then recommend the smallest setup that fits, and wait for me to ask before you build it.
When I ask, output CSV, SQL DDL, JSON Schema, a Notion property mapping or an Excel workbook. Data only.
```

