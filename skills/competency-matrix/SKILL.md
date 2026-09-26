---
name: competency-matrix
description: "Competency Matrix: context-first intake, then CSV, SQL, JSON Schema and Notion on request. One short question per message. Use for competency matrix."
category: business
risk: safe
source: self
source_type: self
date_added: "2026-09-26"
author: WHOISABHISHEKADHIKARI
tags: [sme, business, operations, database, csv, notion, sql, develop]
tools: [claude, cursor, gemini, antigravity]
---

# Competency Matrix

**What it is:** Skill levels.

## Overview

Works out the smallest useful **Competency Matrix** setup for the business in front of it, then
builds it only when asked. The default output is a short recommendation, not a
spreadsheet. Artifacts - CSV, SQL DDL, JSON Schema, Notion mapping - are produced on
request, from one field list so they cannot drift apart.

Layer: Layer 5: Develop. Fits: Scale stage. Table code: n/a.

## When to Use This Skill

- competency matrix
- skills framework
- role competency model
- capability matrix

Also use it when the user says "skill levels", or describes the same process happening in a
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

> **Q:** Which roles need a competency model?

### Step 2 - Ask only what is missing

Skip anything the user already answered, in any earlier message. Ask the rest one at a
time, and stop as soon as the remaining answers would not change the output.

- **Roles** - Which roles? / How many levels? / Technical or general?
- **Competencies** - Which competencies? / How many per role? / Derived from what?
- **Assessment** - Who assesses? / Self or manager? / How often?
- **Current process** - Is anything documented? / Training linked? / What is missing?
- **Outcome** - What do you need? / A matrix, an assessment or a gap link?

Never invent an answer. If the user does not know, record it as unknown and carry on.

### Step 3 - Build the internal context

Hold the answers in this shape. It stays internal - it is not shown to the user unless
they ask, and it never carries a value the user did not give.

```yaml
module: competency-matrix
intent: null            # set in Step 1, one of: set up, fix, review, report, import
scale: null             # Starter | Growth | Scale, only if the answer changes it
areas:
  "Roles": null
  "Competencies": null
  "Assessment": null
  "Current process": null
  "Outcome": null
requested_outputs: []   # csv | sql | json | notion - only what was explicitly asked for
confirmed_facts: []     # only what the user actually said
open_questions: []      # the unanswered ones, in the order worth asking
```

### Step 4 - Recommend the smallest workflow

Give a short recommendation, then ask whether to build it. Do not build unprompted.

**Recommended approach:** Define a small set of levels and attach them to roles, then link the assessment result to the skill gap record.

**Why this one:** A competency matrix is only useful if it is attached to something that changes, usually training or a promotion request.

**Workflow:** Roles → Competencies → Level expectations → Assessment → Gap and training link

### Step 5 - Build only on request

Once the user asks for it, derive the fields from the confirmed context and emit the
artifacts as data only. No preamble, no summary, no closing line.

```csv
Competency,Category,Job Title,Grade Level,Expected Level,Description,Assessment Method,Linked Skill Area,Competency ID
Stakeholder Management,General,Delivery Manager,L1,1 - Beginner,"Maps each role to the competencies it must show, with the level expected at each grade.",Manager observation plus a practical task,SKL-SQL,
```

```sql
CREATE TABLE competency_matrix (
  competency VARCHAR(255),
  category VARCHAR(100) NOT NULL,
  job_title VARCHAR(255),
  grade_level VARCHAR(100) NOT NULL,
  expected_level VARCHAR(100) NOT NULL,
  description TEXT,
  assessment_method VARCHAR(255),
  linked_skill_area VARCHAR(255),  -- relation -> target record
  competency_id SERIAL PRIMARY KEY,
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);
```

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "Competency Matrix",
  "type": "object",
  "additionalProperties": false,
  "properties": {
      "Competency": { "type": "string" },
      "Category": { "type": "string" },
      "Job Title": { "type": "string" },
      "Grade Level": { "type": "string" },
      "Expected Level": { "type": "string" },
      "Description": { "type": "string" },
      "Assessment Method": { "type": "string" },
      "Linked Skill Area": { "type": "string" },
      "Competency ID": { "type": "integer" }
  },
  "required": [
      "Category",
      "Grade Level",
      "Expected Level"
  ]
}
```

```markdown
| CSV column | Notion property | Set after import |
|---|---|---|
| Competency | Text | Leave as Text |
| Category | Select (add options after import) | Convert to Select, add options: "General", "Operations", "Finance", "People", "Compliance" |
| Job Title | Text | Leave as Text |
| Grade Level | Select (add options after import) | Convert to Select, add options: "L1", "L2", "L3", "L4", "L5", "M1", "M2" |
| Expected Level | Select (add options after import) | Convert to Select, add options: "1 - Beginner", "2 - Basic", "3 - Proficient", "4 - Advanced", "5 - Expert" |
| Description | Text | Leave as Text |
| Assessment Method | Text | Leave as Text |
| Linked Skill Area | Relation (link to the target database) | Convert to Relation, link to the target database |
| Competency ID | Text (or Notion auto-ID) | Delete the column and switch the primary column to auto-ID, or keep as Text |
```

One example row per artifact, visibly fake. Money stays `currency`, dates stay `date`,
and anything pointing at another table stays `relation`.

## Field Reference

| # | Field | Type | SQL | JSON Schema | Notion | CSV example |
|---:|---|---|---|---|---|---|
| 1 | Competency | `text` | `VARCHAR(255)` | `string` | Text | `Stakeholder Management` |
| 2 | Category | `select` | `VARCHAR(100)` | `string` | Select (add options after import) | `General` |
| 3 | Job Title | `text` | `VARCHAR(255)` | `string` | Text | `Delivery Manager` |
| 4 | Grade Level | `select` | `VARCHAR(100)` | `string` | Select (add options after import) | `L1` |
| 5 | Expected Level | `select` | `VARCHAR(100)` | `string` | Select (add options after import) | `1 - Beginner` |
| 6 | Description | `long_text` | `TEXT` | `string` | Text | `Maps each role to the competencies it must show, with the level expected at each grade.` |
| 7 | Assessment Method | `text` | `VARCHAR(255)` | `string` | Text | `Manager observation plus a practical task` |
| 8 | Linked Skill Area | `relation` | `VARCHAR(255)` | `string` | Relation (link to the target database) | `SKL-SQL` |
| 9 | Competency ID | `id` | `SERIAL PRIMARY KEY` | `integer` | Text (or Notion auto-ID) | `(blank)` |

## Select Options

**Category**

```
General | Operations | Finance | People | Compliance
```
**Grade Level**

```
L1 | L2 | L3 | L4 | L5 | M1 | M2
```
**Expected Level**

```
1 - Beginner | 2 - Basic | 3 - Proficient | 4 - Advanced | 5 - Expert
```

## Relations

Link fields: `Linked Skill Area`

## Examples

**Prompt**

```
We want a consistent way to describe what good looks like per role.
```

**Context first** - one question per message, nothing already answered:

> **Q:** Which roles?
> **A:** Delivery and support.
>
> **Q:** How many levels?
> **A:** Four.
>
> **Q:** Who assesses?
> **A:** The manager.

**Recommended next step** - offered, not built:

> Define a small set of levels and attach them to roles, then link the assessment result to the skill gap record.
>
> Workflow: Roles → Competencies → Level expectations → Assessment → Gap and training link
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
- Does not assess or certify competence.
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
I want to set up skill levels for my company.
Ask me one short question at a time, and only about what I have not already told you.
Then recommend the smallest setup that fits, and wait for me to ask before you build it.
When I ask, output CSV, SQL DDL, JSON Schema and a Notion property mapping. Data only.
```

