---
name: okr-system
description: "OKR System: context-first intake, then CSV, SQL, JSON Schema and Notion on request. One short question per message. Use for okr tracker."
category: business
risk: safe
source: self
source_type: self
date_added: "2026-09-26"
author: WHOISABHISHEKADHIKARI
tags: [sme, business, operations, database, csv, notion, sql, manage]
tools: []
---

# OKR System

**What it is:** Goal alignment.

## Overview

Works out the smallest useful **OKR System** setup for the business in front of it, then
builds it only when asked. The default output is a short recommendation, not a
spreadsheet. Artifacts - CSV, SQL DDL, JSON Schema, Notion mapping - are produced on
request, from one field list so they cannot drift apart.

Layer: Layer 4: Manage. Fits: Growth stage. Table code: n/a.

## When to Use This Skill

- okr tracker
- goal setting template
- objective key result sheet
- company goals tracker

Also use it when the user says "goal alignment", or describes the same process happening in a
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

> **Q:** How many objectives are you setting this quarter?

### Step 2 - Ask only what is missing

Skip anything the user already answered, in any earlier message. Ask the rest one at a
time, and stop as soon as the remaining answers would not change the output.

- **Goals** - How many objectives? / Company or team first? / Who owns each?
- **Shape** - Key results each? / Measured how? / Ambitious or committed?
- **Cadence** - Weekly or monthly check-in? / Who reviews? / Public or internal?
- **Current process** - How do you set goals now? / Document or meeting? / Is it reviewed?
- **Outcome** - What do you need? / Goal setting, tracking or reporting?

Never invent an answer. If the user does not know, record it as unknown and carry on.

### Step 3 - Hold the internal context

Hold the answers in this shape. It stays internal - it is not shown to the user unless
they ask, and it never carries a value the user did not give.

```yaml
module: okr-system
intent: null            # set in Step 1, one of: set up, fix, review, report, import
scale: null             # Starter | Growth | Scale, only if the answer changes it
areas:
  "Goals": null
  "Shape": null
  "Cadence": null
  "Current process": null
  "Outcome": null
requested_outputs: []   # csv | sql | json | notion - only what was explicitly asked for
confirmed_facts: []     # only what the user actually said
open_questions: []      # the unanswered ones, in the order worth asking
```

### Step 4 - Recommend the smallest workflow

Give a short recommendation, then ask whether to build it. Do not build unprompted. Ask: "Want me to build the CSV, SQL DDL, JSON Schema, Notion mapping, or an Excel workbook from these confirmed rules?"

**Recommended approach:** Cascade company to team to person, and review progress on a fixed cadence. Three key results per objective is the practical limit.

**Why this one:** OKRs fail when objectives have no key results or no review date. Enforce both at creation rather than reviewing for them later.

**Workflow:** Objective → Key results → Owner → Progress update → Review → Close

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
Objective,Department,End Date,KR1 Progress %,KR2 Progress %,KR3 Progress %,Key Result 1,Key Result 2,Key Result 3,Last Updated,Level,Notes,OKR ID,Owner,Parent OKR,Progress %,Quarter,Start Date,Status,Year
Make delivery predictable,Delivery,2026-09-30,75,60,40,Reduce churn to 4%,Ship 20 client sites,NPS above 50,2026-01-15,L1,Q2 closed at 60 percent; the two weakest key results were carried into the March review.,,Sneha Iyer,OKR-2026-COMPANY,60,Q1,2026-07-01,Active,2026
```

```sql
CREATE TABLE okr_system (
  objective VARCHAR(255),
  department VARCHAR(255),
  end_date DATE NOT NULL,
  kr1_progress_pct NUMERIC NOT NULL,
  kr2_progress_pct NUMERIC NOT NULL,
  kr3_progress_pct NUMERIC NOT NULL,
  key_result_1 VARCHAR(255),
  key_result_2 VARCHAR(255),
  key_result_3 VARCHAR(255),
  last_updated DATE NOT NULL,
  level VARCHAR(100) NOT NULL,
  notes TEXT,
  okr_id SERIAL PRIMARY KEY,
  owner VARCHAR(255),
  parent_okr VARCHAR(255),  -- relation -> target record
  progress_pct NUMERIC NOT NULL,
  quarter VARCHAR(255),
  start_date DATE NOT NULL,
  status VARCHAR(100) NOT NULL,
  year VARCHAR(255),
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_okr_system_status ON okr_system (status);
```

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "OKR System",
  "type": "object",
  "additionalProperties": false,
  "properties": {
      "Objective": { "type": "string" },
      "Department": { "type": "string" },
      "End Date": { "type": "string", "format": "date" },
      "KR1 Progress %": { "type": "number" },
      "KR2 Progress %": { "type": "number" },
      "KR3 Progress %": { "type": "number" },
      "Key Result 1": { "type": "string" },
      "Key Result 2": { "type": "string" },
      "Key Result 3": { "type": "string" },
      "Last Updated": { "type": "string", "format": "date" },
      "Level": { "type": "string" },
      "Notes": { "type": "string" },
      "OKR ID": { "type": "integer" },
      "Owner": { "type": "string" },
      "Parent OKR": { "type": "string" },
      "Progress %": { "type": "number" },
      "Quarter": { "type": "string" },
      "Start Date": { "type": "string", "format": "date" },
      "Status": { "type": "string" },
      "Year": { "type": "string" }
  },
  "required": [
      "End Date",
      "KR1 Progress %",
      "KR2 Progress %",
      "KR3 Progress %",
      "Last Updated",
      "Level",
      "Progress %",
      "Start Date",
      "Status"
  ]
}
```

```markdown
| CSV column | Notion property | Set after import |
|---|---|---|
| Objective | Text | Leave as Text |
| Department | Text | Leave as Text |
| End Date | Date | Convert to Date |
| KR1 Progress % | Number | Convert to Number |
| KR2 Progress % | Number | Convert to Number |
| KR3 Progress % | Number | Convert to Number |
| Key Result 1 | Text | Leave as Text |
| Key Result 2 | Text | Leave as Text |
| Key Result 3 | Text | Leave as Text |
| Last Updated | Date | Convert to Date |
| Level | Select (add options after import) | Convert to Select, add options: "L1", "L2", "L3", "L4", "L5", "M1", "M2" |
| Notes | Text | Leave as Text |
| OKR ID | Text (or Notion auto-ID) | Delete the column and switch the primary column to auto-ID, or keep as Text |
| Owner | Text | Leave as Text |
| Parent OKR | Relation (link to the target database) | Convert to Relation, link to the target database |
| Progress % | Number | Convert to Number |
| Quarter | Text | Leave as Text |
| Start Date | Date | Convert to Date |
| Status | Select (add options after import) | Convert to Select, add options: "Draft", "Active", "At Risk", "Closed" |
| Year | Text | Leave as Text |
```

The rows above are documentation examples only. Emit empty templates unless the user explicitly requests examples. Money stays `currency`, dates stay `date`,
and anything pointing at another table stays `relation`.

## Field Reference

| # | Field | Type | SQL | JSON Schema | Notion | CSV example |
|---:|---|---|---|---|---|---|
| 1 | Objective | `text` | `VARCHAR(255)` | `string` | Text | `Make delivery predictable` |
| 2 | Department | `text` | `VARCHAR(255)` | `string` | Text | `Delivery` |
| 3 | End Date | `date` | `DATE` | `string, format: date` | Date | `2026-09-30` |
| 4 | KR1 Progress % | `number` | `NUMERIC` | `number` | Number | `75` |
| 5 | KR2 Progress % | `number` | `NUMERIC` | `number` | Number | `60` |
| 6 | KR3 Progress % | `number` | `NUMERIC` | `number` | Number | `40` |
| 7 | Key Result 1 | `text` | `VARCHAR(255)` | `string` | Text | `Reduce churn to 4%` |
| 8 | Key Result 2 | `text` | `VARCHAR(255)` | `string` | Text | `Ship 20 client sites` |
| 9 | Key Result 3 | `text` | `VARCHAR(255)` | `string` | Text | `NPS above 50` |
| 10 | Last Updated | `date` | `DATE` | `string, format: date` | Date | `2026-01-15` |
| 11 | Level | `select` | `VARCHAR(100)` | `string` | Select (add options after import) | `L1` |
| 12 | Notes | `long_text` | `TEXT` | `string` | Text | `Q2 closed at 60 percent; the two weakest key results were carried into the March review.` |
| 13 | OKR ID | `id` | `SERIAL PRIMARY KEY` | `integer` | Text (or Notion auto-ID) | `(blank)` |
| 14 | Owner | `text` | `VARCHAR(255)` | `string` | Text | `Sneha Iyer` |
| 15 | Parent OKR | `relation` | `VARCHAR(255)` | `string` | Relation (link to the target database) | `OKR-2026-COMPANY` |
| 16 | Progress % | `number` | `NUMERIC` | `number` | Number | `60` |
| 17 | Quarter | `text` | `VARCHAR(255)` | `string` | Text | `Q1` |
| 18 | Start Date | `date` | `DATE` | `string, format: date` | Date | `2026-07-01` |
| 19 | Status | `select` | `VARCHAR(100)` | `string` | Select (add options after import) | `Active` |
| 20 | Year | `text` | `VARCHAR(255)` | `string` | Text | `2026` |

## Select Options

**Level**

```
L1 | L2 | L3 | L4 | L5 | M1 | M2
```
**Status**

```
Draft | Active | At Risk | Closed
```

## Relations

Link fields: `Parent OKR`

## Examples

**Prompt**

```
We set goals in January and never looked at them again.
```

**Context first** - one question per message, nothing already answered:

> **Q:** How many objectives?
> **A:** Three for the company.
>
> **Q:** Who owns them?
> **A:** Department heads.
>
> **Q:** How often reviewed?
> **A:** Not at all currently.

**Recommended next step** - offered, not built:

> Cascade company to team to person, and review progress on a fixed cadence. Three key results per objective is the practical limit.
>
> Workflow: Objective → Key results → Owner → Progress update → Review → Close
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
- Does not assess individual performance or connect to compensation.
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

- `sme-ops-system-builder` - routes to this skill and the other 70 modules.
- `people-directory` - the employee master record most modules link to.
- `notification-reminder-hub` - turns due dates in this module into reminders.

## Reusable Prompt

```
I want to set up goal alignment for my company.
Ask me one short question at a time, and only about what I have not already told you.
Then recommend the smallest setup that fits, and wait for me to ask before you build it.
When I ask, output CSV, SQL DDL, JSON Schema, a Notion property mapping or an Excel workbook. Data only.
```

