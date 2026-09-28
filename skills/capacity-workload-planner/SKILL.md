---
name: capacity-workload-planner
description: "Capacity & Workload Planner: context-first intake, then CSV, SQL, JSON Schema and Notion on request. One short question per message. Use for capacity planning."
category: business
risk: safe
source: self
source_type: self
date_added: "2026-09-26"
author: WHOISABHISHEKADHIKARI
tags: [sme, business, operations, database, csv, notion, sql, manage]
tools: [claude, cursor, gemini, antigravity]
---

# Capacity & Workload Planner

**What it is:** Resource management.

## Overview

Works out the smallest useful **Capacity & Workload Planner** setup for the business in front of it, then
builds it only when asked. The default output is a short recommendation, not a
spreadsheet. Artifacts - CSV, SQL DDL, JSON Schema, Notion mapping - are produced on
request, from one field list so they cannot drift apart.

Layer: Layer 4: Manage. Fits: Scale stage. Table code: n/a.

## When to Use This Skill

- capacity planning
- workload planner
- resource allocation sheet
- utilization tracker

Also use it when the user says "resource management", or describes the same process happening in a
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

> **Q:** How many people are billable?

### Step 2 - Ask only what is missing

Skip anything the user already answered, in any earlier message. Ask the rest one at a
time, and stop as soon as the remaining answers would not change the output.

- **Capacity** - How many people? / Billable or not? / Weekly hours?
- **Demand** - How many live projects? / Who allocates? / Fixed dates?
- **Method** - Weekly or daily? / Utilisation target? / Overtime allowed?
- **Current process** - How do you plan now? / Spreadsheet or guess? / When is it too late?
- **Outcome** - What do you need? / A plan, alerts or a forecast?

Never invent an answer. If the user does not know, record it as unknown and carry on.

### Step 3 - Hold the internal context

Hold the answers in this shape. It stays internal - it is not shown to the user unless
they ask, and it never carries a value the user did not give.

```yaml
module: capacity-workload-planner
intent: null            # set in Step 1, one of: set up, fix, review, report, import
scale: null             # Starter | Growth | Scale, only if the answer changes it
areas:
  "Capacity": null
  "Demand": null
  "Method": null
  "Current process": null
  "Outcome": null
requested_outputs: []   # csv | sql | json | notion - only what was explicitly asked for
confirmed_facts: []     # only what the user actually said
open_questions: []      # the unanswered ones, in the order worth asking
```

### Step 4 - Recommend the smallest workflow

Give a short recommendation, then ask whether to build it. Do not build unprompted. Ask: "Want me to build the CSV, SQL DDL, JSON Schema, Notion mapping, or an Excel workbook from these confirmed rules?"

**Recommended approach:** Plan by week, not by day, and flag over-allocation rather than trying to optimise it. Nobody acts on a daily capacity model.

**Why this one:** Weekly capacity is the smallest unit people actually plan in. If the model is daily it will be ignored within a fortnight.

**Workflow:** People → Available hours → Allocation by week → Over-allocation flag → Rebalance

**Derived values - calculate, never ask for and never accept as typed:**

```
Utilisation %    = Allocated Hours / Available Hours x 100, rounded once to the nearest whole number
Allocation Check = Over-allocated  when Utilisation % > 100
                   Within capacity when Utilisation % is 100 or less
                   Under-allocated when Utilisation % < 100
```

The percentage is stored as a whole number: `80` means 80%, never `0.8`. Round once, at this
step, and use the rounded value everywhere so the stored number and the flag can never
disagree. If `Available Hours` is `0` the ratio is undefined: leave `Utilisation %` and
`Allocation Check` empty and flag the row for a human rather than dividing by zero or
defaulting to 0. A person on full leave has no capacity, which is not the same as having
spare capacity.

**Approval gate:** a week may only be `Approved` when `Allocation Check` is `Within capacity`.
An over-allocated week is a real finding, not a rounding error - raise it, do not approve it,
and do not quietly trim `Allocated Hours` to make it fit. Reallocate with the people affected,
or record why the over-allocation is accepted.

### Step 5 - Build only on request

Once the user asks for it, derive the fields from the confirmed context and emit the
artifacts as data only. No preamble, no summary, no closing line.

An Excel workbook is the CSV emitted with a UTF-8 byte order mark, so Excel opens it with
correct text and no import dialog. A CSV carries no types, so after it, name the columns
that need a number, date or currency format applied.

```csv
Employee Name,Department,Project,Week Start,Available Hours,Allocated Hours,Utilisation %,Allocation Check,Leave Days,Status,Notes,Capacity ID
Example Employee,Delivery,Website Redesign,2026-01-05,32,38,119,Over-allocated,3,Draft,"Allocated 38 hours against 32 available, so this week needs a trade before it can be approved.",
```

```sql
CREATE TABLE capacity_workload_planner (
  employee_name VARCHAR(255),
  department VARCHAR(255),
  project VARCHAR(255),
  week_start DATE NOT NULL,
  available_hours NUMERIC NOT NULL,
  allocated_hours NUMERIC NOT NULL,
  utilisation_pct NUMERIC,
  allocation_check VARCHAR(100),
  leave_days NUMERIC NOT NULL,
  status VARCHAR(100) NOT NULL,
  notes TEXT,
  capacity_id SERIAL PRIMARY KEY,
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW(),
  -- Utilisation and the check are derived, so they stay nullable: zero capacity is undefined, not zero.
  CHECK (allocation_check IS NULL OR allocation_check IN ('Over-allocated', 'Within capacity', 'Under-allocated')),
  -- An over-allocated week is a finding to escalate, not a plan to sign off.
  CHECK (status <> 'Approved' OR allocation_check = 'Within capacity')
);

CREATE INDEX idx_capacity_workload_planner_status ON capacity_workload_planner (status);
CREATE INDEX idx_capacity_workload_planner_week_start ON capacity_workload_planner (week_start);
```
```

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "Capacity Workload Planner",
  "type": "object",
  "additionalProperties": false,
  "properties": {
      "Employee Name": { "type": "string" },
      "Department": { "type": "string" },
      "Project": { "type": "string" },
      "Week Start": { "type": "string", "format": "date" },
      "Available Hours": { "type": "number" },
      "Allocated Hours": { "type": "number" },
      "Utilisation %": { "type": "number" },
      "Allocation Check": { "type": "string" },
      "Leave Days": { "type": "number" },
      "Status": { "type": "string" },
      "Notes": { "type": "string" },
      "Capacity ID": { "type": "integer" }
  },
  "required": [
      "Week Start",
      "Available Hours",
      "Allocated Hours",
      "Leave Days",
      "Status"
  ]
}
```

```markdown
| CSV column | Notion property | Set after import |
|---|---|---|
| Employee Name | Text | Leave as Text |
| Department | Text | Leave as Text |
| Project | Text | Leave as Text |
| Week Start | Date | Convert to Date |
| Available Hours | Number | Convert to Number |
| Allocated Hours | Number | Convert to Number |
| Utilisation % | Number | Convert to Number, and do not type it - it is calculated from Allocated Hours / Available Hours |
| Allocation Check | Select (add options after import) | Convert to Select, add options: "Over-allocated", "Within capacity", "Under-allocated" |
| Leave Days | Number | Convert to Number |
| Status | Select (add options after import) | Convert to Select, add options: "Draft", "Approved", "Active", "Revised", "Closed". Approved is blocked while Allocation Check is Over-allocated |
| Notes | Text | Leave as Text |
| Capacity ID | Text (or Notion auto-ID) | Delete the column and switch the primary column to auto-ID, or keep as Text |
```
```

One example row per artifact, visibly fake. Money stays `currency`, dates stay `date`,
and anything pointing at another table stays `relation`.

## Field Reference

| # | Field | Type | SQL | JSON Schema | Notion | CSV example |
|---:|---|---|---|---|---|---|
| 1 | Employee Name | `text` | `VARCHAR(255)` | `string` | Text | `Example Employee` |
| 2 | Department | `text` | `VARCHAR(255)` | `string` | Text | `Delivery` |
| 3 | Project | `text` | `VARCHAR(255)` | `string` | Text | `Website Redesign` |
| 4 | Week Start | `date` | `DATE` | `string, format: date` | Date | `2026-01-05` |
| 5 | Available Hours | `number` | `NUMERIC` | `number` | Number | `32` |
| 6 | Allocated Hours | `number` | `NUMERIC` | `number` | Number | `38` |
| 7 | Utilisation % | `number` | `NUMERIC` | `number` | Number | `119` |
| 8 | Allocation Check | `select` | `VARCHAR(100)` | `string` | Select (add options after import) | `Over-allocated` |
| 9 | Leave Days | `number` | `NUMERIC` | `number` | Number | `3` |
| 10 | Status | `select` | `VARCHAR(100)` | `string` | Select (add options after import) | `Draft` |
| 11 | Notes | `long_text` | `TEXT` | `string` | Text | `Allocated 38 hours against 32 available, so this week needs a trade before it can be approved.` |
| 12 | Capacity ID | `id` | `SERIAL PRIMARY KEY` | `integer` | Text (or Notion auto-ID) | `(blank)` |

## Select Options

**Allocation Check**

```
Over-allocated | Within capacity | Under-allocated
```

Calculated from `Utilisation %`, not chosen. Leave empty when `Available Hours` is 0.

**Status**

```
Draft | Approved | Active | Revised | Closed
```

`Approved` is blocked while `Allocation Check` is `Over-allocated`.

## Relations

Link fields: none

## Examples

**Prompt**

```
We keep overcommitting and miss delivery dates.
```

**Context first** - one question per message, nothing already answered:

> **Q:** Weekly hours?
> **A:** 40.
>
> **Q:** How many live projects?
> **A:** Six.
>
> **Q:** Do you plan weekly?
> **A:** No, we guess.

**Recommended next step** - offered, not built:

> Plan by week, not by day, and flag over-allocation rather than trying to optimise it. Nobody acts on a daily capacity model.
>
> Workflow: People → Available hours → Allocation by week → Over-allocation flag → Rebalance
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
- Does not schedule people or forecast revenue.
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
- **Problem:** a week reads 80% utilisation while 38 hours sit against 32 available.
  **Solution:** a typed number disagreed with its own arithmetic, so an over-allocated week looked safe. Calculate `Utilisation %` and `Allocation Check` from the hours every time and let the approval gate block the week.
- **Problem:** Notion import shows every column as Text.
  **Solution:** that is expected. Apply the property mapping table once, after import.

## Related Skills

- `sme-ops-system-builder` - routes to this skill and the other 70 modules.
- `people-directory` - the employee master record most modules link to.
- `notification-reminder-hub` - turns due dates in this module into reminders.

## Reusable Prompt

```
I want to set up resource management for my company.
Ask me one short question at a time, and only about what I have not already told you.
Then recommend the smallest setup that fits, and wait for me to ask before you build it.
When I ask, output CSV, SQL DDL, JSON Schema, a Notion property mapping or an Excel workbook. Data only.
```

