---
name: remote-work-tracker
description: "Remote Work Tracker: context-first intake, then CSV, SQL, JSON Schema and Notion on request. One short question per message. Use for remote work tracker."
category: business
risk: safe
source: self
source_type: self
date_added: "2026-09-26"
author: WHOISABHISHEKADHIKARI
tags: [sme, business, operations, database, csv, notion, sql, operate]
tools: []
---

# Remote Work Tracker

**What it is:** Location management.

## Overview

Works out the smallest useful **Remote Work Tracker** setup for the business in front of it, then
builds it only when asked. The default output is a short recommendation, not a
spreadsheet. Artifacts - CSV, SQL DDL, JSON Schema, Notion mapping - are produced on
request, from one field list so they cannot drift apart.

Layer: Layer 8: Operate. Fits: Scale stage. Table code: n/a.

## When to Use This Skill

- remote work tracker
- hybrid work log
- work from home register
- location tracker

Also use it when the user says "location management", or describes the same process happening in a
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

> **Q:** How many people work remotely?

### Step 2 - Ask only what is missing

Skip anything the user already answered, in any earlier message. Ask the rest one at a
time, and stop as soon as the remaining answers would not change the output.

- **People** - How many remote? / Fully or hybrid? / Any location changes?
- **Availability** - Core hours? / Overlap required? / How communicated?
- **Equipment** - Equipment provided? / Who approves? / Any cost to the company?
- **Current process** - Is it tracked now? / Sheet or nothing? / What gets missed?
- **Outcome** - What do you need? / A roster, a policy record or both?

Never invent an answer. If the user does not know, record it as unknown and carry on.

### Step 3 - Hold the internal context

Hold the answers in this shape. It stays internal - it is not shown to the user unless
they ask, and it never carries a value the user did not give.

```yaml
module: remote-work-tracker
intent: null            # set in Step 1, one of: set up, fix, review, report, import
scale: null             # Starter | Growth | Scale, only if the answer changes it
areas:
  "People": null
  "Availability": null
  "Equipment": null
  "Current process": null
  "Outcome": null
requested_outputs: []   # csv | sql | json | notion - only what was explicitly asked for
confirmed_facts: []     # only what the user actually said
open_questions: []      # the unanswered ones, in the order worth asking
```

### Step 4 - Recommend the smallest workflow

Give a short recommendation, then ask whether to build it. Do not build unprompted. Ask: "Want me to build the CSV, SQL DDL, JSON Schema, Notion mapping, or an Excel workbook from these confirmed rules?"

**Recommended approach:** Track the roster and the agreement, not daily presence. If you need working hours, record the agreed window per person.

**Why this one:** Remote tracking degrades into monitoring and stops being trusted. Record agreements and the roster, and leave presence out of it.

**Workflow:** Person recorded → Location and agreement → Equipment issued → Review

### Step 5 - Build only on request

Once the user asks for it, derive the fields from the confirmed context and emit the
artifacts as data only. No preamble, no summary, no closing line.

**Notion needs a connected workspace first.** When the user selects Notion as the
output, emit the connection prerequisite from the
[shared execution contract](../../references/execution-contract.md) verbatim before
the Notion mapping, then stop and wait for the reply "Notion connected." If the user
would rather not connect, emit the mapping as text, add one line saying it is
unverified until the workspace is connected, and offer
[notion-manual-import](../notion-manual-import/SKILL.md) for the full manual path.
Never claim a connection exists, and never ask for a Notion password or token.

For an Excel-compatible CSV, use UTF-8 with a byte order mark so Excel opens the
text correctly. A CSV is not an `.xlsx` workbook; create `.xlsx` only when the user
requests a workbook.
A CSV carries no types, so after it, name the columns
that need a number, date or currency format applied.

```csv
Remote Work Entry,Employee Name,Department,Work Location,Week Start,HQ Days,Remote Days,Core Hours Met,Manager,Approved,Notes,Remote ID
"Home, Tue 3 Mar",Aarav Sharma,Delivery,Bengaluru,2026-01-05,3,2,TRUE,Sneha Iyer,TRUE,"February shows two split-location weeks; the travel policy needs a decision either way.",
```

```sql
CREATE TABLE remote_work_tracker (
  remote_work_entry VARCHAR(255),
  employee_name VARCHAR(255),
  department VARCHAR(255),
  work_location VARCHAR(255),
  week_start DATE NOT NULL,
  hq_days NUMERIC NOT NULL,
  remote_days NUMERIC NOT NULL,
  core_hours_met BOOLEAN NOT NULL,
  manager VARCHAR(255),
  approved BOOLEAN NOT NULL,
  notes TEXT,
  remote_id SERIAL PRIMARY KEY,
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);
```

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "Remote Work Tracker",
  "type": "object",
  "additionalProperties": false,
  "properties": {
      "Remote Work Entry": { "type": "string" },
      "Employee Name": { "type": "string" },
      "Department": { "type": "string" },
      "Work Location": { "type": "string" },
      "Week Start": { "type": "string", "format": "date" },
      "HQ Days": { "type": "number" },
      "Remote Days": { "type": "number" },
      "Core Hours Met": { "type": "boolean" },
      "Manager": { "type": "string" },
      "Approved": { "type": "boolean" },
      "Notes": { "type": "string" },
      "Remote ID": { "type": "integer" }
  },
  "required": [
      "Week Start",
      "HQ Days",
      "Remote Days"
  ]
}
```

```markdown
| CSV column | Notion property | Set after import |
|---|---|---|
| Remote Work Entry | Text | Leave as Text |
| Employee Name | Text | Leave as Text |
| Department | Text | Leave as Text |
| Work Location | Text | Leave as Text |
| Week Start | Date | Convert to Date |
| HQ Days | Number | Convert to Number |
| Remote Days | Number | Convert to Number |
| Core Hours Met | Checkbox | Convert to Checkbox |
| Manager | Text | Leave as Text |
| Approved | Checkbox | Convert to Checkbox |
| Notes | Text | Leave as Text |
| Remote ID | Text (or Notion auto-ID) | Delete the column and switch the primary column to auto-ID, or keep as Text |
```

The rows above are documentation examples only. Emit empty templates unless the user explicitly requests examples. Money stays `currency`, dates stay `date`,
and anything pointing at another table stays `relation`.

## Field Reference

| # | Field | Type | SQL | JSON Schema | Notion | CSV example |
|---:|---|---|---|---|---|---|
| 1 | Remote Work Entry | `text` | `VARCHAR(255)` | `string` | Text | `Home, Tue 3 Mar` |
| 2 | Employee Name | `text` | `VARCHAR(255)` | `string` | Text | `Aarav Sharma` |
| 3 | Department | `text` | `VARCHAR(255)` | `string` | Text | `Delivery` |
| 4 | Work Location | `text` | `VARCHAR(255)` | `string` | Text | `Bengaluru` |
| 5 | Week Start | `date` | `DATE` | `string, format: date` | Date | `2026-01-05` |
| 6 | HQ Days | `number` | `NUMERIC` | `number` | Number | `3` |
| 7 | Remote Days | `number` | `NUMERIC` | `number` | Number | `2` |
| 8 | Core Hours Met | `checkbox` | `BOOLEAN` | `boolean` | Checkbox | `TRUE` |
| 9 | Manager | `text` | `VARCHAR(255)` | `string` | Text | `Sneha Iyer` |
| 10 | Approved | `checkbox` | `BOOLEAN` | `boolean` | Checkbox | `TRUE` |
| 11 | Notes | `long_text` | `TEXT` | `string` | Text | `February shows two split-location weeks; the travel policy needs a decision either way.` |
| 12 | Remote ID | `id` | `SERIAL PRIMARY KEY` | `integer` | Text (or Notion auto-ID) | `(blank)` |

## Select Options

_No Select fields._

## Relations

Link fields: none

## Examples

**Prompt**

```
We have remote staff across four cities and no record of who is where.
```

**Context first** - one question per message, nothing already answered:

> **Q:** How many remote?
> **A:** Nine.
>
> **Q:** Fully or hybrid?
> **A:** Hybrid.
>
> **Q:** Core hours?
> **A:** Four hours overlap.

**Recommended next step** - offered, not built:

> Track the roster and the agreement, not daily presence. If you need working hours, record the agreed window per person.
>
> Workflow: Person recorded → Location and agreement → Equipment issued → Review
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
- Does not monitor activity, track location automatically or set policy for you.
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

- **Problem:** the Notion mapping is handed over with no workspace connected.
  **Solution:** the connection prerequisite goes first, and a mapping handed over as
  text is labelled unverified until the workspace is connected.
- **Problem:** asked all six questions in one message.
  **Solution:** ask one, wait, and drop any the first answer already covered.
- **Problem:** built a full system when one table was asked for.
  **Solution:** build what was requested; mention the parent skill separately.
- **Problem:** all four artifacts drift apart.
  **Solution:** derive all four from the field list in this file, never by hand.
- **Problem:** Notion import shows every column as Text.
  **Solution:** that is expected. Apply the property mapping table once, after import.

## Related Skills

- [SME Ops System Builder](../../SKILL.md) - routes to this skill and the other 70 modules.
- [People Directory](../people-directory/SKILL.md) - the employee master record most modules link to.
- [Notification & Reminder Hub](../notification-reminder-hub/SKILL.md) - turns due dates in this module into reminders.

## Reusable Prompt

```
I want to set up location management for my company.
Ask me one short question at a time, and only about what I have not already told you.
Then recommend the smallest setup that fits, and wait for me to ask before you build it.
When I ask, output CSV, SQL DDL, JSON Schema, a Notion property mapping or an Excel workbook. Data only.
```

