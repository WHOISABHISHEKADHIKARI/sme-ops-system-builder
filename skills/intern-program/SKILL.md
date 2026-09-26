---
name: intern-program
description: "Intern Program: context-first intake, then CSV, SQL, JSON Schema and Notion on request. One short question per message. Use for intern tracker."
category: business
risk: safe
source: self
source_type: self
date_added: "2026-09-26"
author: WHOISABHISHEKADHIKARI
tags: [sme, business, operations, database, csv, notion, sql, onboard]
tools: [claude, cursor, gemini, antigravity]
---

# Intern Program

**What it is:** Interns from start to certificate or full-time offer.

## Overview

Works out the smallest useful **Intern Program** setup for the business in front of it, then
builds it only when asked. The default output is a short recommendation, not a
spreadsheet. Artifacts - CSV, SQL DDL, JSON Schema, Notion mapping - are produced on
request, from one field list so they cannot drift apart.

Layer: Layer 3: Onboard. Fits: Growth stage. Table code: n/a.

## When to Use This Skill

- intern tracker
- internship management
- intern program database
- intern onboarding and conversion

Also use it when the user says "interns from start to certificate or full-time offer", or describes the same process happening in a
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

> **Q:** How many interns do you take at a time?

### Step 2 - Ask only what is missing

Skip anything the user already answered, in any earlier message. Ask the rest one at a
time, and stop as soon as the remaining answers would not change the output.

- **Volume** - How many interns? / Any time of year? / Paid or unpaid?
- **Programme** - Duration? / Mentor assigned? / Certificate needed?
- **Conversion** - Any full-time offers? / Criteria? / Who decides?
- **Current process** - How is it tracked now? / Spreadsheet or nothing? / What gets missed?
- **Outcome** - What do you need? / Records, progress tracking or conversion?

Never invent an answer. If the user does not know, record it as unknown and carry on.

### Step 3 - Build the internal context

Hold the answers in this shape. It stays internal - it is not shown to the user unless
they ask, and it never carries a value the user did not give.

```yaml
module: intern-program
intent: null            # set in Step 1, one of: set up, fix, review, report, import
scale: null             # Starter | Growth | Scale, only if the answer changes it
areas:
  "Volume": null
  "Programme": null
  "Conversion": null
  "Current process": null
  "Outcome": null
requested_outputs: []   # csv | sql | json | notion - only what was explicitly asked for
confirmed_facts: []     # only what the user actually said
open_questions: []      # the unanswered ones, in the order worth asking
```

### Step 4 - Recommend the smallest workflow

Give a short recommendation, then ask whether to build it. Do not build unprompted. Ask: "Want me to build the CSV, SQL DDL, JSON Schema, Notion mapping, or an Excel workbook from these confirmed rules?"

**Recommended approach:** Treat the intern as a light employee record plus a progress log, and only build conversion tracking if interns actually convert.

**Why this one:** Most intern programmes need three things: dates, a supervisor, and a mid and final score. Everything else is optional.

**Workflow:** Offer → Intern record → Mid review → Final review → Certificate or offer

### Step 5 - Build only on request

Once the user asks for it, derive the fields from the confirmed context and emit the
artifacts as data only. No preamble, no summary, no closing line.

An Excel workbook is the CSV emitted with a UTF-8 byte order mark, so Excel opens it with
correct text and no import dialog. A CSV carries no types, so after it, name the columns
that need a number, date or currency format applied.

```csv
Intern Name,Department,Supervisor,Mentor,School or University,Program Type,Start Date,End Date,Duration (Days),Stipend,Currency,Learning Goals,Weekly Log Link,Mid-term Score,Final Score,Certificate Issued,Offer for Full-Time,Converted to Employee,Status,Intern ID
Karan Malhotra,Delivery,Sneha Iyer,Rohit Verma,Anna University,Internship,2026-06-01,2026-11-30,30,25000.00,INR,Ship one feature end to end,https://example.com/log,4,4.2,FALSE,FALSE,Aarav Sharma,In Progress,
```

```sql
CREATE TABLE intern_program (
  intern_name VARCHAR(255),
  department VARCHAR(255),
  supervisor VARCHAR(255),
  mentor VARCHAR(255),
  school_or_university VARCHAR(255),
  program_type VARCHAR(100) NOT NULL,
  start_date DATE NOT NULL,
  end_date DATE NOT NULL,
  duration_days NUMERIC NOT NULL,
  stipend NUMERIC(14,2) NOT NULL,
  currency VARCHAR(255),
  learning_goals VARCHAR(255),
  weekly_log_link TEXT,
  mid_term_score NUMERIC NOT NULL,
  final_score NUMERIC NOT NULL,
  certificate_issued BOOLEAN NOT NULL,
  offer_for_full_time BOOLEAN NOT NULL,
  converted_to_employee VARCHAR(255),
  status VARCHAR(100) NOT NULL,
  intern_id SERIAL PRIMARY KEY,
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_intern_program_status ON intern_program (status);
```

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "Intern Program",
  "type": "object",
  "additionalProperties": false,
  "properties": {
      "Intern Name": { "type": "string" },
      "Department": { "type": "string" },
      "Supervisor": { "type": "string" },
      "Mentor": { "type": "string" },
      "School or University": { "type": "string" },
      "Program Type": { "type": "string" },
      "Start Date": { "type": "string", "format": "date" },
      "End Date": { "type": "string", "format": "date" },
      "Duration (Days)": { "type": "number" },
      "Stipend": { "type": "number" },
      "Currency": { "type": "string" },
      "Learning Goals": { "type": "string" },
      "Weekly Log Link": { "type": "string", "format": "uri" },
      "Mid-term Score": { "type": "number" },
      "Final Score": { "type": "number" },
      "Certificate Issued": { "type": "boolean" },
      "Offer for Full-Time": { "type": "boolean" },
      "Converted to Employee": { "type": "string" },
      "Status": { "type": "string" },
      "Intern ID": { "type": "integer" }
  },
  "required": [
      "Program Type",
      "Start Date",
      "End Date",
      "Duration (Days)",
      "Stipend",
      "Mid-term Score",
      "Final Score",
      "Status"
  ]
}
```

```markdown
| CSV column | Notion property | Set after import |
|---|---|---|
| Intern Name | Text | Leave as Text |
| Department | Text | Leave as Text |
| Supervisor | Text | Leave as Text |
| Mentor | Text | Leave as Text |
| School or University | Text | Leave as Text |
| Program Type | Select (add options after import) | Convert to Select, add options: "Internship", "Apprenticeship", "Graduate Program", "Returnship" |
| Start Date | Date | Convert to Date |
| End Date | Date | Convert to Date |
| Duration (Days) | Number | Convert to Number |
| Stipend | Number (format: currency) | Convert to Number, set format to Currency |
| Currency | Text | Leave as Text |
| Learning Goals | Text | Leave as Text |
| Weekly Log Link | URL | Convert to URL |
| Mid-term Score | Number | Convert to Number |
| Final Score | Number | Convert to Number |
| Certificate Issued | Checkbox | Convert to Checkbox |
| Offer for Full-Time | Checkbox | Convert to Checkbox |
| Converted to Employee | Text | Leave as Text |
| Status | Select (add options after import) | Convert to Select, add options: "Onboarding", "In Progress", "Completed", "Terminated" |
| Intern ID | Text (or Notion auto-ID) | Delete the column and switch the primary column to auto-ID, or keep as Text |
```

One example row per artifact, visibly fake. Money stays `currency`, dates stay `date`,
and anything pointing at another table stays `relation`.

## Field Reference

| # | Field | Type | SQL | JSON Schema | Notion | CSV example |
|---:|---|---|---|---|---|---|
| 1 | Intern Name | `text` | `VARCHAR(255)` | `string` | Text | `Karan Malhotra` |
| 2 | Department | `text` | `VARCHAR(255)` | `string` | Text | `Delivery` |
| 3 | Supervisor | `text` | `VARCHAR(255)` | `string` | Text | `Sneha Iyer` |
| 4 | Mentor | `text` | `VARCHAR(255)` | `string` | Text | `Rohit Verma` |
| 5 | School or University | `text` | `VARCHAR(255)` | `string` | Text | `Anna University` |
| 6 | Program Type | `select` | `VARCHAR(100)` | `string` | Select (add options after import) | `Internship` |
| 7 | Start Date | `date` | `DATE` | `string, format: date` | Date | `2026-06-01` |
| 8 | End Date | `date` | `DATE` | `string, format: date` | Date | `2026-11-30` |
| 9 | Duration (Days) | `number` | `NUMERIC` | `number` | Number | `30` |
| 10 | Stipend | `currency` | `NUMERIC(14,2)` | `number` | Number (format: currency) | `25000.00` |
| 11 | Currency | `text` | `VARCHAR(255)` | `string` | Text | `INR` |
| 12 | Learning Goals | `text` | `VARCHAR(255)` | `string` | Text | `Ship one feature end to end` |
| 13 | Weekly Log Link | `url` | `TEXT` | `string, format: uri` | URL | `https://example.com/log` |
| 14 | Mid-term Score | `number` | `NUMERIC` | `number` | Number | `4` |
| 15 | Final Score | `number` | `NUMERIC` | `number` | Number | `4.2` |
| 16 | Certificate Issued | `checkbox` | `BOOLEAN` | `boolean` | Checkbox | `FALSE` |
| 17 | Offer for Full-Time | `checkbox` | `BOOLEAN` | `boolean` | Checkbox | `FALSE` |
| 18 | Converted to Employee | `text` | `VARCHAR(255)` | `string` | Text | `Aarav Sharma` |
| 19 | Status | `select` | `VARCHAR(100)` | `string` | Select (add options after import) | `In Progress` |
| 20 | Intern ID | `id` | `SERIAL PRIMARY KEY` | `integer` | Text (or Notion auto-ID) | `(blank)` |

## Select Options

**Program Type**

```
Internship | Apprenticeship | Graduate Program | Returnship
```
**Status**

```
Onboarding | In Progress | Completed | Terminated
```

## Relations

Link fields: none

## Examples

**Prompt**

```
We take 5 interns each summer and track everything in a notebook.
```

**Context first** - one question per message, nothing already answered:

> **Q:** How long?
> **A:** 3 months.
>
> **Q:** Mentor assigned?
> **A:** Yes.
>
> **Q:** Do interns convert?
> **A:** Sometimes, two last year.

**Recommended next step** - offered, not built:

> Treat the intern as a light employee record plus a progress log, and only build conversion tracking if interns actually convert.
>
> Workflow: Offer → Intern record → Mid review → Final review → Certificate or offer
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
- Does not run the internship or assess intern performance on its own.
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
I want to set up interns from start to certificate or full-time offer for my company.
Ask me one short question at a time, and only about what I have not already told you.
Then recommend the smallest setup that fits, and wait for me to ask before you build it.
When I ask, output CSV, SQL DDL, JSON Schema, a Notion property mapping or an Excel workbook. Data only.
```

