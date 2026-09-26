---
name: learning-career-development
description: "Learning & Career Development: context-first intake, then CSV, SQL, JSON Schema and Notion on request. One short question per message. Use for lms tracker."
category: business
risk: safe
source: self
source_type: self
date_added: "2026-09-26"
author: WHOISABHISHEKADHIKARI
tags: [sme, business, operations, database, csv, notion, sql, develop]
tools: [claude, cursor, gemini, antigravity]
---

# Learning & Career Development

**What it is:** Learning management.

## Overview

Works out the smallest useful **Learning & Career Development** setup for the business in front of it, then
builds it only when asked. The default output is a short recommendation, not a
spreadsheet. Artifacts - CSV, SQL DDL, JSON Schema, Notion mapping - are produced on
request, from one field list so they cannot drift apart.

Layer: Layer 5: Develop. Fits: Growth stage. Table code: n/a.

## When to Use This Skill

- lms tracker
- learning management
- course completion tracker
- employee training record

Also use it when the user says "learning management", or describes the same process happening in a
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

> **Q:** How many people are learning something right now?

### Step 2 - Ask only what is missing

Skip anything the user already answered, in any earlier message. Ask the rest one at a
time, and stop as soon as the remaining answers would not change the output.

- **Learning** - Internal or external courses? / Mandatory or optional? / How many people?
- **Records** - Certificates tracked? / Progress visible? / Completion required?
- **Process** - Who approves enrolment? / Budget per person? / LMS in use?
- **Current process** - How do you track now? / Files or nothing? / What gets missed?
- **Outcome** - What do you need? / A record, dashboards or mandatory tracking?

Never invent an answer. If the user does not know, record it as unknown and carry on.

### Step 3 - Build the internal context

Hold the answers in this shape. It stays internal - it is not shown to the user unless
they ask, and it never carries a value the user did not give.

```yaml
module: learning-career-development
intent: null            # set in Step 1, one of: set up, fix, review, report, import
scale: null             # Starter | Growth | Scale, only if the answer changes it
areas:
  "Learning": null
  "Records": null
  "Process": null
  "Current process": null
  "Outcome": null
requested_outputs: []   # csv | sql | json | notion - only what was explicitly asked for
confirmed_facts: []     # only what the user actually said
open_questions: []      # the unanswered ones, in the order worth asking
```

### Step 4 - Recommend the smallest workflow

Give a short recommendation, then ask whether to build it. Do not build unprompted. Ask: "Want me to build the CSV, SQL DDL, JSON Schema, Notion mapping, or an Excel workbook from these confirmed rules?"

**Recommended approach:** Track enrolment, completion and certificate per person, and only add mandatory flags if something is actually enforced.

**Why this one:** Learning records matter later for probation and promotion. Keep them per person with a completion date and a link to the certificate.

**Workflow:** Enrolment → Progress → Completion → Certificate → Record

### Step 5 - Build only on request

Once the user asks for it, derive the fields from the confirmed context and emit the
artifacts as data only. No preamble, no summary, no closing line.

An Excel workbook is the CSV emitted with a UTF-8 byte order mark, so Excel opens it with
correct text and no import dialog. A CSV carries no types, so after it, name the columns
that need a number, date or currency format applied.

```csv
Course / Training,Certificate Earned,Completion Date,Course Category,Course URL,Delivery Method,Department,Duration (Hours),Employee Name,Course Request,LMS ID,Mandatory,Notes,Progress %,Provider,Score,Skills Gained,Start Date,Status
Advanced SQL,FALSE,2026-10-30,General,https://example.com/courses/leadership,Self-paced online,Delivery,2.5,Aarav Sharma,CRS-2026-018,,FALSE,Course completion tracked to the February cohort; one learner has not started.,60, Udemy,4,"Advanced SQL, stakeholder mapping, contract review.",2026-08-03,In Progress
```

```sql
CREATE TABLE learning_career_development (
  course_training VARCHAR(255),
  certificate_earned BOOLEAN NOT NULL,
  completion_date DATE NOT NULL,
  course_category VARCHAR(100) NOT NULL,
  course_url TEXT,
  delivery_method VARCHAR(255),
  department VARCHAR(255),
  duration_hours NUMERIC NOT NULL,
  employee_name VARCHAR(255),
  course_request VARCHAR(255),  -- relation -> target record
  lms_id SERIAL PRIMARY KEY,
  mandatory BOOLEAN NOT NULL,
  notes TEXT,
  progress NUMERIC NOT NULL,
  provider VARCHAR(255),
  score NUMERIC NOT NULL,
  skills_gained VARCHAR(255),
  start_date DATE NOT NULL,
  status VARCHAR(100) NOT NULL,
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_learning_career_development_status ON learning_career_development (status);
```

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "Learning & Career Development",
  "type": "object",
  "additionalProperties": false,
  "properties": {
      "Course / Training": { "type": "string" },
      "Certificate Earned": { "type": "boolean" },
      "Completion Date": { "type": "string", "format": "date" },
      "Course Category": { "type": "string" },
      "Course URL": { "type": "string", "format": "uri" },
      "Delivery Method": { "type": "string" },
      "Department": { "type": "string" },
      "Duration (Hours)": { "type": "number" },
      "Employee Name": { "type": "string" },
      "Course Request": { "type": "string" },
      "LMS ID": { "type": "integer" },
      "Mandatory": { "type": "boolean" },
      "Notes": { "type": "string" },
      "Progress %": { "type": "number" },
      "Provider": { "type": "string" },
      "Score": { "type": "number" },
      "Skills Gained": { "type": "string" },
      "Start Date": { "type": "string", "format": "date" },
      "Status": { "type": "string" }
  },
  "required": [
      "Completion Date",
      "Course Category",
      "Duration (Hours)",
      "Progress %",
      "Score",
      "Start Date",
      "Status"
  ]
}
```

```markdown
| CSV column | Notion property | Set after import |
|---|---|---|
| Course / Training | Text | Leave as Text |
| Certificate Earned | Checkbox | Convert to Checkbox |
| Completion Date | Date | Convert to Date |
| Course Category | Select (add options after import) | Convert to Select, add options: "General", "Operations", "Finance", "People", "Compliance" |
| Course URL | URL | Convert to URL |
| Delivery Method | Text | Leave as Text |
| Department | Text | Leave as Text |
| Duration (Hours) | Number | Convert to Number |
| Employee Name | Text | Leave as Text |
| Course Request | Relation (link to the target database) | Convert to Relation, link to the target database |
| LMS ID | Text (or Notion auto-ID) | Delete the column and switch the primary column to auto-ID, or keep as Text |
| Mandatory | Checkbox | Convert to Checkbox |
| Notes | Text | Leave as Text |
| Progress % | Number | Convert to Number |
| Provider | Text | Leave as Text |
| Score | Number | Convert to Number |
| Skills Gained | Text | Leave as Text |
| Start Date | Date | Convert to Date |
| Status | Select (add options after import) | Convert to Select, add options: "Not Started", "Enrolled", "In Progress", "Completed", "Failed", "Expired" |
```

One example row per artifact, visibly fake. Money stays `currency`, dates stay `date`,
and anything pointing at another table stays `relation`.

## Field Reference

| # | Field | Type | SQL | JSON Schema | Notion | CSV example |
|---:|---|---|---|---|---|---|
| 1 | Course / Training | `text` | `VARCHAR(255)` | `string` | Text | `Advanced SQL` |
| 2 | Certificate Earned | `checkbox` | `BOOLEAN` | `boolean` | Checkbox | `FALSE` |
| 3 | Completion Date | `date` | `DATE` | `string, format: date` | Date | `2026-10-30` |
| 4 | Course Category | `select` | `VARCHAR(100)` | `string` | Select (add options after import) | `General` |
| 5 | Course URL | `url` | `TEXT` | `string, format: uri` | URL | `https://example.com/courses/leadership` |
| 6 | Delivery Method | `text` | `VARCHAR(255)` | `string` | Text | `Self-paced online` |
| 7 | Department | `text` | `VARCHAR(255)` | `string` | Text | `Delivery` |
| 8 | Duration (Hours) | `number` | `NUMERIC` | `number` | Number | `2.5` |
| 9 | Employee Name | `text` | `VARCHAR(255)` | `string` | Text | `Aarav Sharma` |
| 10 | Course Request | `relation` | `VARCHAR(255)` | `string` | Relation (link to the target database) | `CRS-2026-018` |
| 11 | LMS ID | `id` | `SERIAL PRIMARY KEY` | `integer` | Text (or Notion auto-ID) | `(blank)` |
| 12 | Mandatory | `checkbox` | `BOOLEAN` | `boolean` | Checkbox | `FALSE` |
| 13 | Notes | `long_text` | `TEXT` | `string` | Text | `Course completion tracked to the February cohort; one learner has not started.` |
| 14 | Progress % | `number` | `NUMERIC` | `number` | Number | `60` |
| 15 | Provider | `text` | `VARCHAR(255)` | `string` | Text | ` Udemy` |
| 16 | Score | `number` | `NUMERIC` | `number` | Number | `4` |
| 17 | Skills Gained | `text` | `VARCHAR(255)` | `string` | Text | `Advanced SQL, stakeholder mapping, contract review.` |
| 18 | Start Date | `date` | `DATE` | `string, format: date` | Date | `2026-08-03` |
| 19 | Status | `select` | `VARCHAR(100)` | `string` | Select (add options after import) | `In Progress` |

## Select Options

**Course Category**

```
General | Operations | Finance | People | Compliance
```
**Status**

```
Not Started | Enrolled | In Progress | Completed | Failed | Expired
```

## Relations

Link fields: `Course Request`

## Examples

**Prompt**

```
We send people to courses and lose the certificates.
```

**Context first** - one question per message, nothing already answered:

> **Q:** How many people?
> **A:** About 20.
>
> **Q:** Certificates?
> **A:** Yes, worth keeping.
>
> **Q:** Mandatory training?
> **A:** Two courses a year.

**Recommended next step** - offered, not built:

> Track enrolment, completion and certificate per person, and only add mandatory flags if something is actually enforced.
>
> Workflow: Enrolment → Progress → Completion → Certificate → Record
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
- Does not host courses or send learners anywhere.
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
I want to set up learning management for my company.
Ask me one short question at a time, and only about what I have not already told you.
Then recommend the smallest setup that fits, and wait for me to ask before you build it.
When I ask, output CSV, SQL DDL, JSON Schema, a Notion property mapping or an Excel workbook. Data only.
```

