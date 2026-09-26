---
name: 360-feedback-system
description: "360° Feedback System: context-first intake, then CSV, SQL, JSON Schema and Notion on request. One short question per message. Use for 360 feedback."
category: business
risk: safe
source: self
source_type: self
date_added: "2026-09-26"
author: WHOISABHISHEKADHIKARI
tags: [sme, business, operations, database, csv, notion, sql, manage]
tools: [claude, cursor, gemini, antigravity]
---

# 360° Feedback System

**What it is:** Holistic feedback.

## Overview

Works out the smallest useful **360° Feedback System** setup for the business in front of it, then
builds it only when asked. The default output is a short recommendation, not a
spreadsheet. Artifacts - CSV, SQL DDL, JSON Schema, Notion mapping - are produced on
request, from one field list so they cannot drift apart.

Layer: Layer 4: Manage. Fits: Growth stage. Table code: n/a.

## When to Use This Skill

- 360 feedback
- feedback system
- peer review tool
- 360 degree feedback tracker

Also use it when the user says "holistic feedback", or describes the same process happening in a
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

> **Q:** How many people are on your team?

### Step 2 - Ask only what is missing

Skip anything the user already answered, in any earlier message. Ask the rest one at a
time, and stop as soon as the remaining answers would not change the output.

- **Team** - How many people? / Who gives feedback? / Who receives it?
- **Purpose** - What is the feedback for? / Regular reviews or a project? / How often?
- **Feedback** - Anonymous? / Scores, comments or both? / Which areas?
- **Current process** - How do you collect it today? / What goes wrong? / Which tools exist?
- **Outcome** - What should happen after? / Summaries, reports or actions?

Never invent an answer. If the user does not know, record it as unknown and carry on.

### Step 3 - Build the internal context

Hold the answers in this shape. It stays internal - it is not shown to the user unless
they ask, and it never carries a value the user did not give.

```yaml
module: 360-feedback-system
intent: null            # set in Step 1, one of: set up, fix, review, report, import
scale: null             # Starter | Growth | Scale, only if the answer changes it
areas:
  "Team": null
  "Purpose": null
  "Feedback": null
  "Current process": null
  "Outcome": null
requested_outputs: []   # csv | sql | json | notion - only what was explicitly asked for
confirmed_facts: []     # only what the user actually said
open_questions: []      # the unanswered ones, in the order worth asking
```

### Step 4 - Recommend the smallest workflow

Give a short recommendation, then ask whether to build it. Do not build unprompted.

**Recommended approach:** Keep the existing collection tool and add an analysis layer. Only build scores if the reviewers need to be compared on a scale.

**Why this one:** Feedback volume and privacy drive the design more than team size. If collection already works, the missing piece is usually analysis and follow-up.

**Workflow:** Form → Sheet → AI analysis → Manager review → Feedback discussion → Actions

### Step 5 - Build only on request

Once the user asks for it, derive the fields from the confirmed context and emit the
artifacts as data only. No preamble, no summary, no closing line.

```csv
Feedback Record,Anonymous,Collaboration Score,Communication Score,Department,Due Date,Feedback ID,Feedback Type,Key Improvements,Key Strengths,Leadership Score,Notes,Overall Score,Review Cycle,Reviewer,Status,Subject Employee,Submitted Date,Technical Score
FB-2026-Q1-004,FALSE,5,4,Delivery,2026-01-22,,Peer,"Earlier status updates, and one named owner per client account.",Reliable follow-through and clear ownership of her accounts.,4,Reviewer asked for a follow-up chat in the next cycle.,4.2,Q1 2026,Sneha Iyer,Collecting,Aarav Sharma,2026-01-15,4
```

```sql
CREATE TABLE "360_feedback_system" (
  feedback_record VARCHAR(255),
  anonymous BOOLEAN NOT NULL,
  collaboration_score NUMERIC NOT NULL,
  communication_score NUMERIC NOT NULL,
  department VARCHAR(255),
  due_date DATE NOT NULL,
  feedback_id SERIAL PRIMARY KEY,
  feedback_type VARCHAR(100) NOT NULL,
  key_improvements VARCHAR(255),
  key_strengths VARCHAR(255),
  leadership_score NUMERIC NOT NULL,
  notes TEXT,
  overall_score NUMERIC NOT NULL,
  review_cycle VARCHAR(255),
  reviewer VARCHAR(255),
  status VARCHAR(100) NOT NULL,
  subject_employee VARCHAR(255),
  submitted_date DATE NOT NULL,
  technical_score NUMERIC NOT NULL,
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_360_feedback_system_status ON "360_feedback_system" (status);
```

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "360° Feedback System",
  "type": "object",
  "additionalProperties": false,
  "properties": {
      "Feedback Record": { "type": "string" },
      "Anonymous": { "type": "boolean" },
      "Collaboration Score": { "type": "number" },
      "Communication Score": { "type": "number" },
      "Department": { "type": "string" },
      "Due Date": { "type": "string", "format": "date" },
      "Feedback ID": { "type": "integer" },
      "Feedback Type": { "type": "string" },
      "Key Improvements": { "type": "string" },
      "Key Strengths": { "type": "string" },
      "Leadership Score": { "type": "number" },
      "Notes": { "type": "string" },
      "Overall Score": { "type": "number" },
      "Review Cycle": { "type": "string" },
      "Reviewer": { "type": "string" },
      "Status": { "type": "string" },
      "Subject Employee": { "type": "string" },
      "Submitted Date": { "type": "string", "format": "date" },
      "Technical Score": { "type": "number" }
  },
  "required": [
      "Collaboration Score",
      "Communication Score",
      "Due Date",
      "Feedback Type",
      "Leadership Score",
      "Overall Score",
      "Status",
      "Submitted Date",
      "Technical Score"
  ]
}
```

```markdown
| CSV column | Notion property | Set after import |
|---|---|---|
| Feedback Record | Text | Leave as Text |
| Anonymous | Checkbox | Convert to Checkbox |
| Collaboration Score | Number | Convert to Number |
| Communication Score | Number | Convert to Number |
| Department | Text | Leave as Text |
| Due Date | Date | Convert to Date |
| Feedback ID | Text (or Notion auto-ID) | Delete the column and switch the primary column to auto-ID, or keep as Text |
| Feedback Type | Select (add options after import) | Convert to Select, add options: "Self", "Peer", "Manager", "Direct Report", "Cross Functional" |
| Key Improvements | Text | Leave as Text |
| Key Strengths | Text | Leave as Text |
| Leadership Score | Number | Convert to Number |
| Notes | Text | Leave as Text |
| Overall Score | Number | Convert to Number |
| Review Cycle | Text | Leave as Text |
| Reviewer | Text | Leave as Text |
| Status | Select (add options after import) | Convert to Select, add options: "Not Launched", "Collecting", "Consolidated", "Shared", "Closed" |
| Subject Employee | Text | Leave as Text |
| Submitted Date | Date | Convert to Date |
| Technical Score | Number | Convert to Number |
```

One example row per artifact, visibly fake. Money stays `currency`, dates stay `date`,
and anything pointing at another table stays `relation`.

## Field Reference

| # | Field | Type | SQL | JSON Schema | Notion | CSV example |
|---:|---|---|---|---|---|---|
| 1 | Feedback Record | `text` | `VARCHAR(255)` | `string` | Text | `FB-2026-Q1-004` |
| 2 | Anonymous | `checkbox` | `BOOLEAN` | `boolean` | Checkbox | `FALSE` |
| 3 | Collaboration Score | `number` | `NUMERIC` | `number` | Number | `5` |
| 4 | Communication Score | `number` | `NUMERIC` | `number` | Number | `4` |
| 5 | Department | `text` | `VARCHAR(255)` | `string` | Text | `Delivery` |
| 6 | Due Date | `date` | `DATE` | `string, format: date` | Date | `2026-01-22` |
| 7 | Feedback ID | `id` | `SERIAL PRIMARY KEY` | `integer` | Text (or Notion auto-ID) | `(blank)` |
| 8 | Feedback Type | `select` | `VARCHAR(100)` | `string` | Select (add options after import) | `Peer` |
| 9 | Key Improvements | `text` | `VARCHAR(255)` | `string` | Text | `Earlier status updates, and one named owner per client account.` |
| 10 | Key Strengths | `text` | `VARCHAR(255)` | `string` | Text | `Reliable follow-through and clear ownership of her accounts.` |
| 11 | Leadership Score | `number` | `NUMERIC` | `number` | Number | `4` |
| 12 | Notes | `long_text` | `TEXT` | `string` | Text | `Reviewer asked for a follow-up chat in the next cycle.` |
| 13 | Overall Score | `number` | `NUMERIC` | `number` | Number | `4.2` |
| 14 | Review Cycle | `text` | `VARCHAR(255)` | `string` | Text | `Q1 2026` |
| 15 | Reviewer | `text` | `VARCHAR(255)` | `string` | Text | `Sneha Iyer` |
| 16 | Status | `select` | `VARCHAR(100)` | `string` | Select (add options after import) | `Collecting` |
| 17 | Subject Employee | `text` | `VARCHAR(255)` | `string` | Text | `Aarav Sharma` |
| 18 | Submitted Date | `date` | `DATE` | `string, format: date` | Date | `2026-01-15` |
| 19 | Technical Score | `number` | `NUMERIC` | `number` | Number | `4` |

## Select Options

**Feedback Type**

```
Self | Peer | Manager | Direct Report | Cross Functional
```
**Status**

```
Not Launched | Collecting | Consolidated | Shared | Closed
```

## Relations

Link fields: none

## Examples

**Prompt**

```
We have 12 people and want managers and peers to give anonymous feedback.
```

**Context first** - one question per message, nothing already answered:

> **Q:** What is the feedback for?
> **A:** Performance and team improvement.
>
> **Q:** How do you collect it today?
> **A:** Google Forms and Sheets.
>
> **Q:** Scores, comments or both?
> **A:** Both.

**Recommended next step** - offered, not built:

> Keep the existing collection tool and add an analysis layer. Only build scores if the reviewers need to be compared on a scale.
>
> Workflow: Form → Sheet → AI analysis → Manager review → Feedback discussion → Actions
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
- Does not replace HR or legal review, and does not make employment decisions.
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
I want to set up holistic feedback for my company.
Ask me one short question at a time, and only about what I have not already told you.
Then recommend the smallest setup that fits, and wait for me to ask before you build it.
When I ask, output CSV, SQL DDL, JSON Schema and a Notion property mapping. Data only.
```

