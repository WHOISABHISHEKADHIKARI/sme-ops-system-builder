---
name: alumni-re-hire-tracker
description: "Alumni & Re-hire Tracker: context-first intake, then CSV, SQL, JSON Schema and Notion on request. One short question per message. Use for alumni tracker."
category: business
risk: safe
source: self
source_type: self
date_added: "2026-09-26"
author: WHOISABHISHEKADHIKARI
tags: [sme, business, operations, database, csv, notion, sql, exit]
tools: [claude, cursor, gemini, antigravity]
---

# Alumni & Re-hire Tracker

**What it is:** Former employees.

## Overview

Works out the smallest useful **Alumni & Re-hire Tracker** setup for the business in front of it, then
builds it only when asked. The default output is a short recommendation, not a
spreadsheet. Artifacts - CSV, SQL DDL, JSON Schema, Notion mapping - are produced on
request, from one field list so they cannot drift apart.

Layer: Layer 10: Exit. Fits: Scale stage. Table code: n/a.

## When to Use This Skill

- alumni tracker
- rehire tracker
- former employee register
- past employee list

Also use it when the user says "former employees", or describes the same process happening in a
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

> **Q:** How many people have left the company?

### Step 2 - Ask only what is missing

Skip anything the user already answered, in any earlier message. Ask the rest one at a
time, and stop as soon as the remaining answers would not change the output.

- **Alumni** - How many ex-employees? / How long ago? / Any warm contacts?
- **Fit** - Why would you re-hire? / Roles they held? / Skills worth recording?
- **Reach** - How do you stay in touch? / Any consent on file? / How often to check in?
- **Current process** - Is anything recorded? / LinkedIn or a sheet? / What gets missed?
- **Outcome** - What do you need? / An alumni register, a re-hire view or both?

Never invent an answer. If the user does not know, record it as unknown and carry on.

### Step 3 - Build the internal context

Hold the answers in this shape. It stays internal - it is not shown to the user unless
they ask, and it never carries a value the user did not give.

```yaml
module: alumni-re-hire-tracker
intent: null            # set in Step 1, one of: set up, fix, review, report, import
scale: null             # Starter | Growth | Scale, only if the answer changes it
areas:
  "Alumni": null
  "Fit": null
  "Reach": null
  "Current process": null
  "Outcome": null
requested_outputs: []   # csv | sql | json | notion - only what was explicitly asked for
confirmed_facts: []     # only what the user actually said
open_questions: []      # the unanswered ones, in the order worth asking
```

### Step 4 - Recommend the smallest workflow

Give a short recommendation, then ask whether to build it. Do not build unprompted. Ask: "Want me to build the CSV, SQL DDL, JSON Schema, Notion mapping, or an Excel workbook from these confirmed rules?"

**Recommended approach:** Keep a small alumni record with the exit date, the role held and one line on why they left, and revisit it only when a role opens.

**Why this one:** Alumni records are only worth maintaining if something triggers a revisit. Tie it to open roles instead of a standing newsletter.

**Workflow:** Departure recorded → Details kept → Re-hire considered when a role opens → Rejoined or contacted

### Step 5 - Build only on request

Once the user asks for it, derive the fields from the confirmed context and emit the
artifacts as data only. No preamble, no summary, no closing line.

An Excel workbook is the CSV emitted with a UTF-8 byte order mark, so Excel opens it with
correct text and no import dialog. A CSV carries no types, so after it, name the columns
that need a number, date or currency format applied.

```csv
Alumni Name,Former Department,Former Job Title,Last Working Day,Rehire Eligible,Personal Email,LinkedIn,Current Company,Last Contact,Re-engage Date,Notes,Alumni ID
Karan Malhotra,Delivery,Delivery Manager,2026-03-31,TRUE,aarav.personal@example.com,https://linkedin.com/in/priya-nair-example,Bluepeak Systems,2026-01-20,2026-07-01,"Reached out in February; interested in returning once the current notice period ends.",
```

```sql
CREATE TABLE alumni_re_hire_tracker (
  alumni_name VARCHAR(255),
  former_department VARCHAR(255),
  former_job_title VARCHAR(255),
  last_working_day DATE NOT NULL,
  rehire_eligible BOOLEAN NOT NULL,
  personal_email VARCHAR(255),
  linkedin TEXT,
  current_company VARCHAR(255),
  last_contact DATE NOT NULL,
  re_engage_date DATE NOT NULL,
  notes TEXT,
  alumni_id SERIAL PRIMARY KEY,
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);
```

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "Alumni & Re-hire Tracker",
  "type": "object",
  "additionalProperties": false,
  "properties": {
      "Alumni Name": { "type": "string" },
      "Former Department": { "type": "string" },
      "Former Job Title": { "type": "string" },
      "Last Working Day": { "type": "string", "format": "date" },
      "Rehire Eligible": { "type": "boolean" },
      "Personal Email": { "type": "string", "format": "email" },
      "LinkedIn": { "type": "string", "format": "uri" },
      "Current Company": { "type": "string" },
      "Last Contact": { "type": "string", "format": "date" },
      "Re-engage Date": { "type": "string", "format": "date" },
      "Notes": { "type": "string" },
      "Alumni ID": { "type": "integer" }
  },
  "required": [
      "Last Working Day",
      "Last Contact",
      "Re-engage Date"
  ]
}
```

```markdown
| CSV column | Notion property | Set after import |
|---|---|---|
| Alumni Name | Text | Leave as Text |
| Former Department | Text | Leave as Text |
| Former Job Title | Text | Leave as Text |
| Last Working Day | Date | Convert to Date |
| Rehire Eligible | Checkbox | Convert to Checkbox |
| Personal Email | Email | Convert to Email |
| LinkedIn | URL | Convert to URL |
| Current Company | Text | Leave as Text |
| Last Contact | Date | Convert to Date |
| Re-engage Date | Date | Convert to Date |
| Notes | Text | Leave as Text |
| Alumni ID | Text (or Notion auto-ID) | Delete the column and switch the primary column to auto-ID, or keep as Text |
```

One example row per artifact, visibly fake. Money stays `currency`, dates stay `date`,
and anything pointing at another table stays `relation`.

## Field Reference

| # | Field | Type | SQL | JSON Schema | Notion | CSV example |
|---:|---|---|---|---|---|---|
| 1 | Alumni Name | `text` | `VARCHAR(255)` | `string` | Text | `Karan Malhotra` |
| 2 | Former Department | `text` | `VARCHAR(255)` | `string` | Text | `Delivery` |
| 3 | Former Job Title | `text` | `VARCHAR(255)` | `string` | Text | `Delivery Manager` |
| 4 | Last Working Day | `date` | `DATE` | `string, format: date` | Date | `2026-03-31` |
| 5 | Rehire Eligible | `checkbox` | `BOOLEAN` | `boolean` | Checkbox | `TRUE` |
| 6 | Personal Email | `email` | `VARCHAR(255)` | `string, format: email` | Email | `aarav.personal@example.com` |
| 7 | LinkedIn | `url` | `TEXT` | `string, format: uri` | URL | `https://linkedin.com/in/priya-nair-example` |
| 8 | Current Company | `text` | `VARCHAR(255)` | `string` | Text | `Bluepeak Systems` |
| 9 | Last Contact | `date` | `DATE` | `string, format: date` | Date | `2026-01-20` |
| 10 | Re-engage Date | `date` | `DATE` | `string, format: date` | Date | `2026-07-01` |
| 11 | Notes | `long_text` | `TEXT` | `string` | Text | `Reached out in February; interested in returning once the current notice period ends.` |
| 12 | Alumni ID | `id` | `SERIAL PRIMARY KEY` | `integer` | Text (or Notion auto-ID) | `(blank)` |

## Select Options

_No Select fields._

## Relations

Link fields: none

## Examples

**Prompt**

```
Four good people left last year and we only noticed when a role came up.
```

**Context first** - one question per message, nothing already answered:

> **Q:** How many ex-employees?
> **A:** About twenty in three years.
>
> **Q:** Recorded anywhere?
> **A:** A spreadsheet, mostly empty.
>
> **Q:** Why re-hire?
> **A:** We know who was good.

**Recommended next step** - offered, not built:

> Keep a small alumni record with the exit date, the role held and one line on why they left, and revisit it only when a role opens.
>
> Workflow: Departure recorded → Details kept → Re-hire considered when a role opens → Rejoined or contacted
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
- Does not contact anyone, verify consent or make hiring decisions.
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
I want to set up former employees for my company.
Ask me one short question at a time, and only about what I have not already told you.
Then recommend the smallest setup that fits, and wait for me to ask before you build it.
When I ask, output CSV, SQL DDL, JSON Schema, a Notion property mapping or an Excel workbook. Data only.
```

