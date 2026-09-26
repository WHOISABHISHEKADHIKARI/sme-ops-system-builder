---
name: health-wellness
description: "Health & Wellness: context-first intake, then CSV, SQL, JSON Schema and Notion on request. One short question per message. Use for employee wellbeing."
category: business
risk: safe
source: self
source_type: self
date_added: "2026-09-26"
author: WHOISABHISHEKADHIKARI
tags: [sme, business, operations, database, csv, notion, sql, engage]
tools: [claude, cursor, gemini, antigravity]
---

# Health & Wellness

**What it is:** Wellbeing tracking.

## Overview

Works out the smallest useful **Health & Wellness** setup for the business in front of it, then
builds it only when asked. The default output is a short recommendation, not a
spreadsheet. Artifacts - CSV, SQL DDL, JSON Schema, Notion mapping - are produced on
request, from one field list so they cannot drift apart.

Layer: Layer 6: Engage. Fits: Scale stage. Table code: n/a.

## When to Use This Skill

- employee wellbeing
- health check in tracker
- wellness survey
- mental health support log

Also use it when the user says "wellbeing tracking", or describes the same process happening in a
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

> **Q:** Is this for employees or a team?

### Step 2 - Ask only what is missing

Skip anything the user already answered, in any earlier message. Ask the rest one at a
time, and stop as soon as the remaining answers would not change the output.

- **Scope** - Who is it for? / How many people? / Perks or programmes?
- **Use** - What is offered? / Optional or mandatory? / Any medical data?
- **Privacy** - Is it anonymous? / Who can see participation? / Any health details held?
- **Current process** - Anything offered now? / How is it communicated? / Is uptake tracked?
- **Outcome** - What do you need? / A benefits list, participation counts or both?

Never invent an answer. If the user does not know, record it as unknown and carry on.

### Step 3 - Build the internal context

Hold the answers in this shape. It stays internal - it is not shown to the user unless
they ask, and it never carries a value the user did not give.

```yaml
module: health-wellness
intent: null            # set in Step 1, one of: set up, fix, review, report, import
scale: null             # Starter | Growth | Scale, only if the answer changes it
areas:
  "Scope": null
  "Use": null
  "Privacy": null
  "Current process": null
  "Outcome": null
requested_outputs: []   # csv | sql | json | notion - only what was explicitly asked for
confirmed_facts: []     # only what the user actually said
open_questions: []      # the unanswered ones, in the order worth asking
```

### Step 4 - Recommend the smallest workflow

Give a short recommendation, then ask whether to build it. Do not build unprompted. Ask: "Want me to build the CSV, SQL DDL, JSON Schema, Notion mapping, or an Excel workbook from these confirmed rules?"

**Recommended approach:** Track benefits and uptake only. Do not store any individual health information, since the benefit does not need it.

**Why this one:** Wellness programmes create risk the moment individual health data is held. Keep participation counts and leave the details out.

**Workflow:** Benefit offered → Uptake count → Anonymous feedback → Review

### Step 5 - Build only on request

Once the user asks for it, derive the fields from the confirmed context and emit the
artifacts as data only. No preamble, no summary, no closing line.

An Excel workbook is the CSV emitted with a UTF-8 byte order mark, so Excel opens it with
correct text and no import dialog. A CSV carries no types, so after it, name the columns
that need a number, date or currency format applied.

```csv
Check-in Title,Employee Name,Anonymous,Department,Check-in Date,Wellbeing Score,Stress Level,Energy Level,Support Requested,Resource Shared,Confidential,Status,Wellness ID
Weekly wellbeing check,Aarav Sharma,FALSE,Delivery,2026-01-15,4,Low,Low,FALSE,FALSE,Internal,Completed,
```

```sql
CREATE TABLE health_wellness (
  check_in_title VARCHAR(255),
  employee_name VARCHAR(255),
  anonymous BOOLEAN NOT NULL,
  department VARCHAR(255),
  check_in_date DATE NOT NULL,
  wellbeing_score NUMERIC NOT NULL,
  stress_level VARCHAR(100) NOT NULL,
  energy_level VARCHAR(100) NOT NULL,
  support_requested BOOLEAN NOT NULL,
  resource_shared BOOLEAN NOT NULL,
  confidential VARCHAR(100) NOT NULL,
  status VARCHAR(100) NOT NULL,
  wellness_id SERIAL PRIMARY KEY,
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_health_wellness_status ON health_wellness (status);
```

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "Health & Wellness",
  "type": "object",
  "additionalProperties": false,
  "properties": {
      "Check-in Title": { "type": "string" },
      "Employee Name": { "type": "string" },
      "Anonymous": { "type": "boolean" },
      "Department": { "type": "string" },
      "Check-in Date": { "type": "string", "format": "date" },
      "Wellbeing Score": { "type": "number" },
      "Stress Level": { "type": "string" },
      "Energy Level": { "type": "string" },
      "Support Requested": { "type": "boolean" },
      "Resource Shared": { "type": "boolean" },
      "Confidential": { "type": "string" },
      "Status": { "type": "string" },
      "Wellness ID": { "type": "integer" }
  },
  "required": [
      "Check-in Date",
      "Wellbeing Score",
      "Stress Level",
      "Energy Level",
      "Confidential",
      "Status"
  ]
}
```

```markdown
| CSV column | Notion property | Set after import |
|---|---|---|
| Check-in Title | Text | Leave as Text |
| Employee Name | Text | Leave as Text |
| Anonymous | Checkbox | Convert to Checkbox |
| Department | Text | Leave as Text |
| Check-in Date | Date | Convert to Date |
| Wellbeing Score | Number | Convert to Number |
| Stress Level | Select (add options after import) | Convert to Select, add options: "Low", "Medium", "High", "Critical" |
| Energy Level | Select (add options after import) | Convert to Select, add options: "Low", "Medium", "High" |
| Support Requested | Checkbox | Convert to Checkbox |
| Resource Shared | Checkbox | Convert to Checkbox |
| Confidential | Select (add options after import) | Convert to Select, add options: "Public", "Internal", "Restricted", "Highly Restricted" |
| Status | Select (add options after import) | Convert to Select, add options: "Scheduled", "Completed", "Missed", "Follow-up Due" |
| Wellness ID | Text (or Notion auto-ID) | Delete the column and switch the primary column to auto-ID, or keep as Text |
```

One example row per artifact, visibly fake. Money stays `currency`, dates stay `date`,
and anything pointing at another table stays `relation`.

## Field Reference

| # | Field | Type | SQL | JSON Schema | Notion | CSV example |
|---:|---|---|---|---|---|---|
| 1 | Check-in Title | `text` | `VARCHAR(255)` | `string` | Text | `Weekly wellbeing check` |
| 2 | Employee Name | `text` | `VARCHAR(255)` | `string` | Text | `Aarav Sharma` |
| 3 | Anonymous | `checkbox` | `BOOLEAN` | `boolean` | Checkbox | `FALSE` |
| 4 | Department | `text` | `VARCHAR(255)` | `string` | Text | `Delivery` |
| 5 | Check-in Date | `date` | `DATE` | `string, format: date` | Date | `2026-01-15` |
| 6 | Wellbeing Score | `number` | `NUMERIC` | `number` | Number | `4` |
| 7 | Stress Level | `select` | `VARCHAR(100)` | `string` | Select (add options after import) | `Low` |
| 8 | Energy Level | `select` | `VARCHAR(100)` | `string` | Select (add options after import) | `Low` |
| 9 | Support Requested | `checkbox` | `BOOLEAN` | `boolean` | Checkbox | `FALSE` |
| 10 | Resource Shared | `checkbox` | `BOOLEAN` | `boolean` | Checkbox | `FALSE` |
| 11 | Confidential | `select` | `VARCHAR(100)` | `string` | Select (add options after import) | `Internal` |
| 12 | Status | `select` | `VARCHAR(100)` | `string` | Select (add options after import) | `Completed` |
| 13 | Wellness ID | `id` | `SERIAL PRIMARY KEY` | `integer` | Text (or Notion auto-ID) | `(blank)` |

## Select Options

**Stress Level**

```
Low | Medium | High | Critical
```
**Energy Level**

```
Low | Medium | High
```
**Confidential**

```
Public | Internal | Restricted | Highly Restricted
```
**Status**

```
Scheduled | Completed | Missed | Follow-up Due
```

## Relations

Link fields: none

## Examples

**Prompt**

```
We want a wellness benefit but do not know whether anyone uses it.
```

**Context first** - one question per message, nothing already answered:

> **Q:** Who is it for?
> **A:** All employees.
>
> **Q:** Do you store health data?
> **A:** No, and I do not want to.
>
> **Q:** What is offered?
> **A:** A gym allowance and counselling.

**Recommended next step** - offered, not built:

> Track benefits and uptake only. Do not store any individual health information, since the benefit does not need it.
>
> Workflow: Benefit offered → Uptake count → Anonymous feedback → Review
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
- Does not provide medical advice, cover or any health service.
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
I want to set up wellbeing tracking for my company.
Ask me one short question at a time, and only about what I have not already told you.
Then recommend the smallest setup that fits, and wait for me to ask before you build it.
When I ask, output CSV, SQL DDL, JSON Schema, a Notion property mapping or an Excel workbook. Data only.
```

