---
name: candidate-talent-pool
description: "Candidate Talent Pool: context-first intake, then CSV, SQL, JSON Schema and Notion on request. One short question per message. Use for talent pool database."
category: business
risk: safe
source: self
source_type: self
date_added: "2026-09-26"
author: WHOISABHISHEKADHIKARI
tags: [sme, business, operations, database, csv, notion, sql, acquire]
tools: [claude, cursor, gemini, antigravity]
---

# Candidate Talent Pool

**What it is:** Prospect database.

## Overview

Works out the smallest useful **Candidate Talent Pool** setup for the business in front of it, then
builds it only when asked. The default output is a short recommendation, not a
spreadsheet. Artifacts - CSV, SQL DDL, JSON Schema, Notion mapping - are produced on
request, from one field list so they cannot drift apart.

Layer: Layer 2: Acquire. Fits: Growth stage. Table code: n/a.

## When to Use This Skill

- talent pool database
- candidate tracker
- recruiter pipeline spreadsheet
- keep candidates warm

Also use it when the user says "prospect database", or describes the same process happening in a
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

> **Q:** Which roles do you hire for?

### Step 2 - Ask only what is missing

Skip anything the user already answered, in any earlier message. Ask the rest one at a
time, and stop as soon as the remaining answers would not change the output.

- **Roles** - Which roles? / How many open? / Any hard-to-fill roles?
- **Pipeline** - How do you find people now? / Referrals or inbound? / Keep rejects warm?
- **Pool** - How long to keep? / Contact allowed? / Consent to re-engage?
- **Current process** - Where do CVs sit now? / Spreadsheet or inbox? / How many in the pool?
- **Outcome** - What do you need? / A pool, a tracker or alerts?

Never invent an answer. If the user does not know, record it as unknown and carry on.

### Step 3 - Build the internal context

Hold the answers in this shape. It stays internal - it is not shown to the user unless
they ask, and it never carries a value the user did not give.

```yaml
module: candidate-talent-pool
intent: null            # set in Step 1, one of: set up, fix, review, report, import
scale: null             # Starter | Growth | Scale, only if the answer changes it
areas:
  "Roles": null
  "Pipeline": null
  "Pool": null
  "Current process": null
  "Outcome": null
requested_outputs: []   # csv | sql | json | notion - only what was explicitly asked for
confirmed_facts: []     # only what the user actually said
open_questions: []      # the unanswered ones, in the order worth asking
```

### Step 4 - Recommend the smallest workflow

Give a short recommendation, then ask whether to build it. Do not build unprompted. Ask: "Want me to build the CSV, SQL DDL, JSON Schema, Notion mapping, or an Excel workbook from these confirmed rules?"

**Recommended approach:** Keep a warm pool with consent and a re-engage date. It is a contact list with a purpose, not a resume archive.

**Why this one:** Rejected candidates are the cheapest hiring source you have, and the most commonly thrown away. Consent and a re-engage date are what make it reusable.

**Workflow:** Candidate added → Consent → Re-engage date → Reminder → Reopen role

### Step 5 - Build only on request

Once the user asks for it, derive the fields from the confirmed context and emit the
artifacts as data only. No preamble, no summary, no closing line.

An Excel workbook is the CSV emitted with a UTF-8 byte order mark, so Excel opens it with
correct text and no import dialog. A CSV carries no types, so after it, name the columns
that need a number, date or currency format applied.

```csv
Candidate Name,Candidate ID,Department,Email,Experience (Years),Last Contact,LinkedIn URL,Notes,Phone,Re-engage Date,Referred By,Skills,Source,Status,Target Role
Karan Malhotra,,Delivery,aarav.sharma@example.com,6,2026-01-20,https://example.com/in/neha-kapoor,Went cold in February after a counter-offer; worth re-approaching in six months.,+91 98xxxxxx21,2026-07-01,Rohit Verma,"Python, SQL, Stakeholder Management",Referral,Active,Delivery Manager
```

```sql
CREATE TABLE candidate_talent_pool (
  candidate_name VARCHAR(255),
  candidate_id SERIAL PRIMARY KEY,
  department VARCHAR(255),
  email VARCHAR(255),
  experience_years NUMERIC NOT NULL,
  last_contact DATE NOT NULL,
  linkedin_url TEXT,
  notes TEXT,
  phone VARCHAR(255),
  re_engage_date DATE NOT NULL,
  referred_by VARCHAR(255),
  skills VARCHAR(255),
  source VARCHAR(255),
  status VARCHAR(100) NOT NULL,
  target_role VARCHAR(255),
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_candidate_talent_pool_status ON candidate_talent_pool (status);
```

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "Candidate Talent Pool",
  "type": "object",
  "additionalProperties": false,
  "properties": {
      "Candidate Name": { "type": "string" },
      "Candidate ID": { "type": "integer" },
      "Department": { "type": "string" },
      "Email": { "type": "string", "format": "email" },
      "Experience (Years)": { "type": "number" },
      "Last Contact": { "type": "string", "format": "date" },
      "LinkedIn URL": { "type": "string", "format": "uri" },
      "Notes": { "type": "string" },
      "Phone": { "type": "string" },
      "Re-engage Date": { "type": "string", "format": "date" },
      "Referred By": { "type": "string" },
      "Skills": { "type": "string" },
      "Source": { "type": "string" },
      "Status": { "type": "string" },
      "Target Role": { "type": "string" }
  },
  "required": [
      "Experience (Years)",
      "Last Contact",
      "Re-engage Date",
      "Status"
  ]
}
```

```markdown
| CSV column | Notion property | Set after import |
|---|---|---|
| Candidate Name | Text | Leave as Text |
| Candidate ID | Text (or Notion auto-ID) | Delete the column and switch the primary column to auto-ID, or keep as Text |
| Department | Text | Leave as Text |
| Email | Email | Convert to Email |
| Experience (Years) | Number | Convert to Number |
| Last Contact | Date | Convert to Date |
| LinkedIn URL | URL | Convert to URL |
| Notes | Text | Leave as Text |
| Phone | Text | Leave as Text |
| Re-engage Date | Date | Convert to Date |
| Referred By | Text | Leave as Text |
| Skills | Text | Leave as Text |
| Source | Text | Leave as Text |
| Status | Select (add options after import) | Convert to Select, add options: "Active", "Contacted", "Interested", "Not Now", "Closed" |
| Target Role | Text | Leave as Text |
```

One example row per artifact, visibly fake. Money stays `currency`, dates stay `date`,
and anything pointing at another table stays `relation`.

## Field Reference

| # | Field | Type | SQL | JSON Schema | Notion | CSV example |
|---:|---|---|---|---|---|---|
| 1 | Candidate Name | `text` | `VARCHAR(255)` | `string` | Text | `Karan Malhotra` |
| 2 | Candidate ID | `id` | `SERIAL PRIMARY KEY` | `integer` | Text (or Notion auto-ID) | `(blank)` |
| 3 | Department | `text` | `VARCHAR(255)` | `string` | Text | `Delivery` |
| 4 | Email | `email` | `VARCHAR(255)` | `string, format: email` | Email | `aarav.sharma@example.com` |
| 5 | Experience (Years) | `number` | `NUMERIC` | `number` | Number | `6` |
| 6 | Last Contact | `date` | `DATE` | `string, format: date` | Date | `2026-01-20` |
| 7 | LinkedIn URL | `url` | `TEXT` | `string, format: uri` | URL | `https://example.com/in/neha-kapoor` |
| 8 | Notes | `long_text` | `TEXT` | `string` | Text | `Went cold in February after a counter-offer; worth re-approaching in six months.` |
| 9 | Phone | `text` | `VARCHAR(255)` | `string` | Text | `+91 98xxxxxx21` |
| 10 | Re-engage Date | `date` | `DATE` | `string, format: date` | Date | `2026-07-01` |
| 11 | Referred By | `text` | `VARCHAR(255)` | `string` | Text | `Rohit Verma` |
| 12 | Skills | `text` | `VARCHAR(255)` | `string` | Text | `Python, SQL, Stakeholder Management` |
| 13 | Source | `text` | `VARCHAR(255)` | `string` | Text | `Referral` |
| 14 | Status | `select` | `VARCHAR(100)` | `string` | Select (add options after import) | `Active` |
| 15 | Target Role | `text` | `VARCHAR(255)` | `string` | Text | `Delivery Manager` |

## Select Options

**Status**

```
Active | Contacted | Interested | Not Now | Closed
```

## Relations

Link fields: none

## Examples

**Prompt**

```
We keep losing good candidates we rejected 6 months ago.
```

**Context first** - one question per message, nothing already answered:

> **Q:** Which roles?
> **A:** Delivery and support.
>
> **Q:** How long to keep?
> **A:** 12 months.
>
> **Q:** Do you have consent?
> **A:** Not written down.

**Recommended next step** - offered, not built:

> Keep a warm pool with consent and a re-engage date. It is a contact list with a purpose, not a resume archive.
>
> Workflow: Candidate added → Consent → Re-engage date → Reminder → Reopen role
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
- Does not source candidates or send outreach on your behalf.
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
I want to set up prospect database for my company.
Ask me one short question at a time, and only about what I have not already told you.
Then recommend the smallest setup that fits, and wait for me to ask before you build it.
When I ask, output CSV, SQL DDL, JSON Schema, a Notion property mapping or an Excel workbook. Data only.
```

