---
name: policy-acknowledgement
description: "Policy Acknowledgement: context-first intake, then CSV, SQL, JSON Schema and Notion on request. One short question per message. Use for policy sign off tracker."
category: business
risk: safe
source: self
source_type: self
date_added: "2026-09-26"
author: WHOISABHISHEKADHIKARI
tags: [sme, business, operations, database, csv, notion, sql, foundation]
tools: [claude, cursor, gemini, antigravity]
---

# Policy Acknowledgement

**What it is:** Who has read and signed each policy and the Code of Conduct.

## Overview

Works out the smallest useful **Policy Acknowledgement** setup for the business in front of it, then
builds it only when asked. The default output is a short recommendation, not a
spreadsheet. Artifacts - CSV, SQL DDL, JSON Schema, Notion mapping - are produced on
request, from one field list so they cannot drift apart.

Layer: Layer 1: Foundation. Fits: Starter stage. Table code: n/a.

## When to Use This Skill

- policy sign off tracker
- policy acknowledgement log
- code of conduct sign off
- policy compliance tracker

Also use it when the user says "who has read and signed each policy and the code of conduct", or describes the same process happening in a
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

> **Q:** How many policies need to be signed?

### Step 2 - Ask only what is missing

Skip anything the user already answered, in any earlier message. Ask the rest one at a
time, and stop as soon as the remaining answers would not change the output.

- **Policies** - Which policies? / Code of conduct included? / Versioned or single?
- **People** - Who must sign? / All staff or some? / Contractors too?
- **Process** - Sign or just read? / Reminder schedule? / Deadline after issue?
- **Current process** - How do you chase sign-off now? / Email or nothing? / What gets missed?
- **Outcome** - What do you need to prove? / An audit trail or a tracker?

Never invent an answer. If the user does not know, record it as unknown and carry on.

### Step 3 - Hold the internal context

Hold the answers in this shape. It stays internal - it is not shown to the user unless
they ask, and it never carries a value the user did not give.

```yaml
module: policy-acknowledgement
intent: null            # set in Step 1, one of: set up, fix, review, report, import
scale: null             # Starter | Growth | Scale, only if the answer changes it
areas:
  "Policies": null
  "People": null
  "Process": null
  "Current process": null
  "Outcome": null
requested_outputs: []   # csv | sql | json | notion - only what was explicitly asked for
confirmed_facts: []     # only what the user actually said
open_questions: []      # the unanswered ones, in the order worth asking
```

### Step 4 - Recommend the smallest workflow

Give a short recommendation, then ask whether to build it. Do not build unprompted. Ask: "Want me to build the CSV, SQL DDL, JSON Schema, Notion mapping, or an Excel workbook from these confirmed rules?"

**Recommended approach:** Issue the policy once, then track acknowledgement per person per version. A shared sign-off sheet beats individual emails.

**Why this one:** The failure mode is not missing policies, it is not knowing who has read the current version. Tracking by version fixes that.

**Workflow:** Policy issue → Assign to people → Reminder → Sign-off record → Overdue report

### Step 5 - Build only on request

Once the user asks for it, derive the fields from the confirmed context and emit the
artifacts as data only. No preamble, no summary, no closing line.

An Excel workbook is the CSV emitted with a UTF-8 byte order mark, so Excel opens it with
correct text and no import dialog. A CSV carries no types, so after it, name the columns
that need a number, date or currency format applied.

```csv
Acknowledgement,Employee Name,Policy,Policy Version,Sent Date,Due Date,Acknowledged Date,Acknowledged,Days Overdue,Reminder Sent,Status,Acknowledgement ID
Signed,Aarav Sharma,Code of Conduct,v2.1,2026-08-14,2026-08-28,2026-09-02,TRUE,5,TRUE,Acknowledged,
```

```sql
CREATE TABLE policy_acknowledgement (
  acknowledgement VARCHAR(255),
  employee_name VARCHAR(255),
  policy VARCHAR(255),
  policy_version VARCHAR(255),
  sent_date DATE NOT NULL,
  due_date DATE NOT NULL,
  acknowledged_date DATE NOT NULL,
  acknowledged BOOLEAN NOT NULL,
  days_overdue NUMERIC NOT NULL,
  reminder_sent BOOLEAN NOT NULL,
  status VARCHAR(100) NOT NULL,
  acknowledgement_id SERIAL PRIMARY KEY,
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_policy_acknowledgement_status ON policy_acknowledgement (status);
```

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "Policy Acknowledgement",
  "type": "object",
  "additionalProperties": false,
  "properties": {
      "Acknowledgement": { "type": "string" },
      "Employee Name": { "type": "string" },
      "Policy": { "type": "string" },
      "Policy Version": { "type": "string" },
      "Sent Date": { "type": "string", "format": "date" },
      "Due Date": { "type": "string", "format": "date" },
      "Acknowledged Date": { "type": "string", "format": "date" },
      "Acknowledged": { "type": "boolean" },
      "Days Overdue": { "type": "number" },
      "Reminder Sent": { "type": "boolean" },
      "Status": { "type": "string" },
      "Acknowledgement ID": { "type": "integer" }
  },
  "required": [
      "Sent Date",
      "Due Date",
      "Acknowledged Date",
      "Days Overdue",
      "Status"
  ]
}
```

```markdown
| CSV column | Notion property | Set after import |
|---|---|---|
| Acknowledgement | Text | Leave as Text |
| Employee Name | Text | Leave as Text |
| Policy | Text | Leave as Text |
| Policy Version | Text | Leave as Text |
| Sent Date | Date | Convert to Date |
| Due Date | Date | Convert to Date |
| Acknowledged Date | Date | Convert to Date |
| Acknowledged | Checkbox | Convert to Checkbox |
| Days Overdue | Number | Convert to Number |
| Reminder Sent | Checkbox | Convert to Checkbox |
| Status | Select (add options after import) | Convert to Select, add options: "Sent", "Viewed", "Acknowledged", "Overdue", "Waived" |
| Acknowledgement ID | Text (or Notion auto-ID) | Delete the column and switch the primary column to auto-ID, or keep as Text |
```

One example row per artifact, visibly fake. Money stays `currency`, dates stay `date`,
and anything pointing at another table stays `relation`.

## Field Reference

| # | Field | Type | SQL | JSON Schema | Notion | CSV example |
|---:|---|---|---|---|---|---|
| 1 | Acknowledgement | `text` | `VARCHAR(255)` | `string` | Text | `Signed` |
| 2 | Employee Name | `text` | `VARCHAR(255)` | `string` | Text | `Aarav Sharma` |
| 3 | Policy | `text` | `VARCHAR(255)` | `string` | Text | `Code of Conduct` |
| 4 | Policy Version | `text` | `VARCHAR(255)` | `string` | Text | `v2.1` |
| 5 | Sent Date | `date` | `DATE` | `string, format: date` | Date | `2026-08-14` |
| 6 | Due Date | `date` | `DATE` | `string, format: date` | Date | `2026-08-28` |
| 7 | Acknowledged Date | `date` | `DATE` | `string, format: date` | Date | `2026-09-02` |
| 8 | Acknowledged | `checkbox` | `BOOLEAN` | `boolean` | Checkbox | `TRUE` |
| 9 | Days Overdue | `number` | `NUMERIC` | `number` | Number | `5` |
| 10 | Reminder Sent | `checkbox` | `BOOLEAN` | `boolean` | Checkbox | `TRUE` |
| 11 | Status | `select` | `VARCHAR(100)` | `string` | Select (add options after import) | `Acknowledged` |
| 12 | Acknowledgement ID | `id` | `SERIAL PRIMARY KEY` | `integer` | Text (or Notion auto-ID) | `(blank)` |

## Select Options

**Status**

```
Sent | Viewed | Acknowledged | Overdue | Waived
```

## Relations

Link fields: none

## Examples

**Prompt**

```
We have 6 policies and no idea who signed the latest code of conduct.
```

**Context first** - one question per message, nothing already answered:

> **Q:** Who must sign?
> **A:** Everyone, including contractors.
>
> **Q:** Do you need a reminder?
> **A:** Yes, weekly.
>
> **Q:** What do you use?
> **A:** Google Drive.

**Recommended next step** - offered, not built:

> Issue the policy once, then track acknowledgement per person per version. A shared sign-off sheet beats individual emails.
>
> Workflow: Policy issue → Assign to people → Reminder → Sign-off record → Overdue report
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
- Does not host documents or capture legally binding e-signatures.
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
I want to set up who has read and signed each policy and the code of conduct for my company.
Ask me one short question at a time, and only about what I have not already told you.
Then recommend the smallest setup that fits, and wait for me to ask before you build it.
When I ask, output CSV, SQL DDL, JSON Schema, a Notion property mapping or an Excel workbook. Data only.
```

