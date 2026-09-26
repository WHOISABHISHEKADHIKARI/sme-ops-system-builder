---
name: dei-dashboard
description: "DEI Dashboard: context-first intake, then CSV, SQL, JSON Schema and Notion on request. One short question per message. Use for dei dashboard."
category: business
risk: safe
source: self
source_type: self
date_added: "2026-09-26"
author: WHOISABHISHEKADHIKARI
tags: [sme, business, operations, database, csv, notion, sql, engage]
tools: [claude, cursor, gemini, antigravity]
---

# DEI Dashboard

**What it is:** Diversity & inclusion.

## Overview

Works out the smallest useful **DEI Dashboard** setup for the business in front of it, then
builds it only when asked. The default output is a short recommendation, not a
spreadsheet. Artifacts - CSV, SQL DDL, JSON Schema, Notion mapping - are produced on
request, from one field list so they cannot drift apart.

Layer: Layer 6: Engage. Fits: Scale stage. Table code: n/a.

## When to Use This Skill

- dei dashboard
- diversity reporting
- workforce diversity metrics
- inclusion tracker

Also use it when the user says "diversity & inclusion", or describes the same process happening in a
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

> **Q:** Which stages of hiring do you want to look at?

### Step 2 - Ask only what is missing

Skip anything the user already answered, in any earlier message. Ask the rest one at a
time, and stop as soon as the remaining answers would not change the output.

- **Scope** - Hiring, progression or both? / Which stages? / By department or overall?
- **Data** - What data exists today? / Voluntary self-ID? / Anonymised?
- **Baselines** - Compare against what? / External benchmark? / Internal target?
- **Current process** - Anything tracked now? / HRIS or a sheet? / Is it anonymised?
- **Outcome** - What do you need? / A metric set or a dashboard view?

Never invent an answer. If the user does not know, record it as unknown and carry on.

### Step 3 - Build the internal context

Hold the answers in this shape. It stays internal - it is not shown to the user unless
they ask, and it never carries a value the user did not give.

```yaml
module: dei-dashboard
intent: null            # set in Step 1, one of: set up, fix, review, report, import
scale: null             # Starter | Growth | Scale, only if the answer changes it
areas:
  "Scope": null
  "Data": null
  "Baselines": null
  "Current process": null
  "Outcome": null
requested_outputs: []   # csv | sql | json | notion - only what was explicitly asked for
confirmed_facts: []     # only what the user actually said
open_questions: []      # the unanswered ones, in the order worth asking
```

### Step 4 - Recommend the smallest workflow

Give a short recommendation, then ask whether to build it. Do not build unprompted. Ask: "Want me to build the CSV, SQL DDL, JSON Schema, Notion mapping, or an Excel workbook from these confirmed rules?"

**Recommended approach:** Use voluntary, anonymised data and aggregate to groups large enough to protect people. Skip any breakdown that would identify someone.

**Why this one:** Diversity data is easy to collect and easy to misuse. Anonymity and minimum group size are conditions of doing it at all, not nice-to-haves.

**Workflow:** Voluntary data → Anonymised aggregation → Stage metrics → Review → Action

### Step 5 - Build only on request

Once the user asks for it, derive the fields from the confirmed context and emit the
artifacts as data only. No preamble, no summary, no closing line.

An Excel workbook is the CSV emitted with a UTF-8 byte order mark, so Excel opens it with
correct text and no import dialog. A CSV carries no types, so after it, name the columns
that need a number, date or currency format applied.

```csv
Metric,Department,Period,Measure Type,Value,Target,Group Size,Minimum Group Size Met,Data Source,Notes,Metric ID
Net revenue,Delivery,2026-03,Count,139240,95,12,TRUE,Manual,"Baseline captured in February; headcount denominators still exclude the contract workforce.",
```

```sql
CREATE TABLE dei_dashboard (
  metric VARCHAR(255),
  department VARCHAR(255),
  period VARCHAR(255),
  measure_type VARCHAR(100) NOT NULL,
  value NUMERIC NOT NULL,
  target NUMERIC NOT NULL,
  group_size NUMERIC NOT NULL,
  minimum_group_size_met BOOLEAN NOT NULL,
  data_source VARCHAR(255),
  notes TEXT,
  metric_id SERIAL PRIMARY KEY,
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);
```

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "DEI Dashboard",
  "type": "object",
  "additionalProperties": false,
  "properties": {
      "Metric": { "type": "string" },
      "Department": { "type": "string" },
      "Period": { "type": "string" },
      "Measure Type": { "type": "string" },
      "Value": { "type": "number" },
      "Target": { "type": "number" },
      "Group Size": { "type": "number" },
      "Minimum Group Size Met": { "type": "boolean" },
      "Data Source": { "type": "string" },
      "Notes": { "type": "string" },
      "Metric ID": { "type": "integer" }
  },
  "required": [
      "Measure Type",
      "Value",
      "Target",
      "Group Size"
  ]
}
```

```markdown
| CSV column | Notion property | Set after import |
|---|---|---|
| Metric | Text | Leave as Text |
| Department | Text | Leave as Text |
| Period | Text | Leave as Text |
| Measure Type | Select (add options after import) | Convert to Select, add options: "Count", "Percentage", "Ratio", "Average" |
| Value | Number | Convert to Number |
| Target | Number | Convert to Number |
| Group Size | Number | Convert to Number |
| Minimum Group Size Met | Checkbox | Convert to Checkbox |
| Data Source | Text | Leave as Text |
| Notes | Text | Leave as Text |
| Metric ID | Text (or Notion auto-ID) | Delete the column and switch the primary column to auto-ID, or keep as Text |
```

One example row per artifact, visibly fake. Money stays `currency`, dates stay `date`,
and anything pointing at another table stays `relation`.

## Field Reference

| # | Field | Type | SQL | JSON Schema | Notion | CSV example |
|---:|---|---|---|---|---|---|
| 1 | Metric | `text` | `VARCHAR(255)` | `string` | Text | `Net revenue` |
| 2 | Department | `text` | `VARCHAR(255)` | `string` | Text | `Delivery` |
| 3 | Period | `text` | `VARCHAR(255)` | `string` | Text | `2026-03` |
| 4 | Measure Type | `select` | `VARCHAR(100)` | `string` | Select (add options after import) | `Count` |
| 5 | Value | `number` | `NUMERIC` | `number` | Number | `139240` |
| 6 | Target | `number` | `NUMERIC` | `number` | Number | `95` |
| 7 | Group Size | `number` | `NUMERIC` | `number` | Number | `12` |
| 8 | Minimum Group Size Met | `checkbox` | `BOOLEAN` | `boolean` | Checkbox | `TRUE` |
| 9 | Data Source | `text` | `VARCHAR(255)` | `string` | Text | `Manual` |
| 10 | Notes | `long_text` | `TEXT` | `string` | Text | `Baseline captured in February; headcount denominators still exclude the contract workforce.` |
| 11 | Metric ID | `id` | `SERIAL PRIMARY KEY` | `integer` | Text (or Notion auto-ID) | `(blank)` |

## Select Options

**Measure Type**

```
Count | Percentage | Ratio | Average
```

## Relations

Link fields: none

## Examples

**Prompt**

```
We want to see where our hiring process drops people out.
```

**Context first** - one question per message, nothing already answered:

> **Q:** Which stages?
> **A:** Apply to offer.
>
> **Q:** Voluntary self-ID?
> **A:** Yes, at joining.
>
> **Q:** Anonymised?
> **A:** Not yet.

**Recommended next step** - offered, not built:

> Use voluntary, anonymised data and aggregate to groups large enough to protect people. Skip any breakdown that would identify someone.
>
> Workflow: Voluntary data → Anonymised aggregation → Stage metrics → Review → Action
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
- Does not collect personal data, make hiring decisions or set targets on your behalf.
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
I want to set up diversity & inclusion for my company.
Ask me one short question at a time, and only about what I have not already told you.
Then recommend the smallest setup that fits, and wait for me to ask before you build it.
When I ask, output CSV, SQL DDL, JSON Schema, a Notion property mapping or an Excel workbook. Data only.
```

