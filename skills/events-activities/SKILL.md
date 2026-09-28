---
name: events-activities
description: "Events & Activities: context-first intake, then CSV, SQL, JSON Schema and Notion on request. One short question per message. Use for event tracker."
category: business
risk: safe
source: self
source_type: self
date_added: "2026-09-26"
author: WHOISABHISHEKADHIKARI
tags: [sme, business, operations, database, csv, notion, sql, engage]
tools: []
---

# Events & Activities

**What it is:** Town halls, trainings, outings and celebrations with budget and attendance.

## Overview

Works out the smallest useful **Events & Activities** setup for the business in front of it, then
builds it only when asked. The default output is a short recommendation, not a
spreadsheet. Artifacts - CSV, SQL DDL, JSON Schema, Notion mapping - are produced on
request, from one field list so they cannot drift apart.

Layer: Layer 6: Engage. Fits: Growth stage. Table code: n/a.

## When to Use This Skill

- event tracker
- town hall planner
- team outing register
- company events database

Also use it when the user says "town halls, trainings, outings and celebrations with budget and attendance", or describes the same process happening in a
spreadsheet, a document or someone inboxes.

Do not use it for: payroll calculation, tax filing, or legal advice. This skill produces
empty templates only - it never holds or processes real employee or customer data.

## How It Works

Follow the [shared execution contract](../../references/execution-contract.md). The module-specific rules below define only domain fields, decisions, calculations, and safety constraints.

### Step 1 - Identify intent

Read the request and pick the intent before asking anything.

- "set up" or "build" or "create" -> the user wants artifacts; go to Step 2.
- "our process is ..." or "it is in a sheet" -> the user wants to move an existing process; capture it, then Step 2.
- "is this right" or "review" or "audit" -> the user wants a check, not a build; answer from what they share.
- "how do I ..." -> advice question; answer directly and offer the build only if it helps.

One message, one question, no batching. Open with:

> **Q:** What is the next event?

### Step 2 - Ask only what is missing

Skip anything the user already answered, in any earlier message. Ask the rest one at a
time, and stop as soon as the remaining answers would not change the output.

- **Events** - How many a year? / Internal or external? / Recurring or one-off?
- **Details** - Date, venue and owner? / Budget per event? / Capacity limit?
- **Registration** - Sign-up needed? / Open or invite only? / Track RSVPs?
- **Current process** - How do you organise now? / Calendar or sheet? / What gets missed?
- **Outcome** - What do you need? / An event list, RSVPs or a budget view?

Never invent an answer. If the user does not know, record it as unknown and carry on.

### Step 3 - Hold the internal context

Hold the answers in this shape. It stays internal - it is not shown to the user unless
they ask, and it never carries a value the user did not give.

```yaml
module: events-activities
intent: null            # set in Step 1, one of: set up, fix, review, report, import
scale: null             # Starter | Growth | Scale, only if the answer changes it
areas:
  "Events": null
  "Details": null
  "Registration": null
  "Current process": null
  "Outcome": null
requested_outputs: []   # csv | sql | json | notion - only what was explicitly asked for
confirmed_facts: []     # only what the user actually said
open_questions: []      # the unanswered ones, in the order worth asking
```

### Step 4 - Recommend the smallest workflow

Give a short recommendation, then ask whether to build it. Do not build unprompted. Ask: "Want me to build the CSV, SQL DDL, JSON Schema, Notion mapping, or an Excel workbook from these confirmed rules?"

**Recommended approach:** One record per event with an owner, a date and a sign-up count, and a budget line only for events that have one.

**Why this one:** Events are planned in chat and lost by the week of. A single event record with an owner is the minimum that survives.

**Workflow:** Event listed → Sign-ups → Budget → Run → Feedback captured

### Step 5 - Build only on request

Once the user asks for it, derive the fields from the confirmed context and emit the
artifacts as data only. No preamble, no summary, no closing line.

**Notion needs a connected workspace first.** When the user selects Notion as the
output, emit the connection prerequisite from the
[shared execution contract](../../references/execution-contract.md) verbatim before
the Notion mapping, then stop and wait for the reply "Notion connected." If the user
would rather not connect, emit the mapping as text, add one line saying it is
unverified until the workspace is connected, and offer
[notion-manual-import](../notion-manual-import/SKILL.md) for the full manual path.
Never claim a connection exists, and never ask for a Notion password or token.

For an Excel-compatible CSV, use UTF-8 with a byte order mark so Excel opens the
text correctly. A CSV is not an `.xlsx` workbook; create `.xlsx` only when the user
requests a workbook.
A CSV carries no types, so after it, name the columns
that need a number, date or currency format applied.

```csv
Event Name,Event Type,Date,Start Time,End Time,Venue or Link,Organizer,Department,Audience,Budget,Actual Cost,Currency,RSVP Count,Attended Count,Attendance %,Feedback Score,Linked Calendar Entry,Status,Notes,Event ID
Q1 Town Hall,Team Meeting,2026-01-15,10:00,11:00,https://example.com/venue,Karan Malhotra,Delivery,All employees,250000.00,98000.00,INR,38,38,96,4,CAL-2026-W03,Held,February session moved to a larger room; feedback asked for shorter sessions.,
```

```sql
CREATE TABLE events_activities (
  event_name VARCHAR(255),
  event_type VARCHAR(100) NOT NULL,
  date DATE NOT NULL,
  start_time VARCHAR(255),
  end_time VARCHAR(255),
  venue_or_link TEXT,
  organizer VARCHAR(255),
  department VARCHAR(255),
  audience VARCHAR(255),
  budget NUMERIC(14,2) NOT NULL,
  actual_cost NUMERIC(14,2) NOT NULL,
  currency VARCHAR(255),
  rsvp_count NUMERIC NOT NULL,
  attended_count NUMERIC NOT NULL,
  attendance_pct NUMERIC NOT NULL,
  feedback_score NUMERIC NOT NULL,
  linked_calendar_entry VARCHAR(255),  -- relation -> target record
  status VARCHAR(100) NOT NULL,
  notes TEXT,
  event_id SERIAL PRIMARY KEY,
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_events_activities_status ON events_activities (status);
```

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "Events & Activities",
  "type": "object",
  "additionalProperties": false,
  "properties": {
      "Event Name": { "type": "string" },
      "Event Type": { "type": "string" },
      "Date": { "type": "string", "format": "date" },
      "Start Time": { "type": "string" },
      "End Time": { "type": "string" },
      "Venue or Link": { "type": "string", "format": "uri" },
      "Organizer": { "type": "string" },
      "Department": { "type": "string" },
      "Audience": { "type": "string" },
      "Budget": { "type": "number" },
      "Actual Cost": { "type": "number" },
      "Currency": { "type": "string" },
      "RSVP Count": { "type": "number" },
      "Attended Count": { "type": "number" },
      "Attendance %": { "type": "number" },
      "Feedback Score": { "type": "number" },
      "Linked Calendar Entry": { "type": "string" },
      "Status": { "type": "string" },
      "Notes": { "type": "string" },
      "Event ID": { "type": "integer" }
  },
  "required": [
      "Event Type",
      "Date",
      "Budget",
      "Actual Cost",
      "RSVP Count",
      "Attended Count",
      "Attendance %",
      "Feedback Score",
      "Status"
  ]
}
```

```markdown
| CSV column | Notion property | Set after import |
|---|---|---|
| Event Name | Text | Leave as Text |
| Event Type | Select (add options after import) | Convert to Select, add options: "Team Meeting", "Training", "Workshop", "Social", "Offsite", "Review" |
| Date | Date | Convert to Date |
| Start Time | Text | Leave as Text |
| End Time | Text | Leave as Text |
| Venue or Link | URL | Convert to URL |
| Organizer | Text | Leave as Text |
| Department | Text | Leave as Text |
| Audience | Text | Leave as Text |
| Budget | Number (format: currency) | Convert to Number, set format to Currency |
| Actual Cost | Number (format: currency) | Convert to Number, set format to Currency |
| Currency | Text | Leave as Text |
| RSVP Count | Number | Convert to Number |
| Attended Count | Number | Convert to Number |
| Attendance % | Number | Convert to Number |
| Feedback Score | Number | Convert to Number |
| Linked Calendar Entry | Relation (link to the target database) | Convert to Relation, link to the target database |
| Status | Select (add options after import) | Convert to Select, add options: "Planned", "Confirmed", "Held", "Postponed", "Cancelled" |
| Notes | Text | Leave as Text |
| Event ID | Text (or Notion auto-ID) | Delete the column and switch the primary column to auto-ID, or keep as Text |
```

The rows above are documentation examples only. Emit empty templates unless the user explicitly requests examples. Money stays `currency`, dates stay `date`,
and anything pointing at another table stays `relation`.

## Field Reference

| # | Field | Type | SQL | JSON Schema | Notion | CSV example |
|---:|---|---|---|---|---|---|
| 1 | Event Name | `text` | `VARCHAR(255)` | `string` | Text | `Q1 Town Hall` |
| 2 | Event Type | `select` | `VARCHAR(100)` | `string` | Select (add options after import) | `Team Meeting` |
| 3 | Date | `date` | `DATE` | `string, format: date` | Date | `2026-01-15` |
| 4 | Start Time | `text` | `VARCHAR(255)` | `string` | Text | `10:00` |
| 5 | End Time | `text` | `VARCHAR(255)` | `string` | Text | `11:00` |
| 6 | Venue or Link | `url` | `TEXT` | `string, format: uri` | URL | `https://example.com/venue` |
| 7 | Organizer | `text` | `VARCHAR(255)` | `string` | Text | `Karan Malhotra` |
| 8 | Department | `text` | `VARCHAR(255)` | `string` | Text | `Delivery` |
| 9 | Audience | `text` | `VARCHAR(255)` | `string` | Text | `All employees` |
| 10 | Budget | `currency` | `NUMERIC(14,2)` | `number` | Number (format: currency) | `250000.00` |
| 11 | Actual Cost | `currency` | `NUMERIC(14,2)` | `number` | Number (format: currency) | `98000.00` |
| 12 | Currency | `text` | `VARCHAR(255)` | `string` | Text | `INR` |
| 13 | RSVP Count | `number` | `NUMERIC` | `number` | Number | `38` |
| 14 | Attended Count | `number` | `NUMERIC` | `number` | Number | `38` |
| 15 | Attendance % | `number` | `NUMERIC` | `number` | Number | `96` |
| 16 | Feedback Score | `number` | `NUMERIC` | `number` | Number | `4` |
| 17 | Linked Calendar Entry | `relation` | `VARCHAR(255)` | `string` | Relation (link to the target database) | `CAL-2026-W03` |
| 18 | Status | `select` | `VARCHAR(100)` | `string` | Select (add options after import) | `Held` |
| 19 | Notes | `long_text` | `TEXT` | `string` | Text | `February session moved to a larger room; feedback asked for shorter sessions.` |
| 20 | Event ID | `id` | `SERIAL PRIMARY KEY` | `integer` | Text (or Notion auto-ID) | `(blank)` |

## Select Options

**Event Type**

```
Team Meeting | Training | Workshop | Social | Offsite | Review
```
**Status**

```
Planned | Confirmed | Held | Postponed | Cancelled
```

## Relations

Link fields: `Linked Calendar Entry`

## Examples

**Prompt**

```
We run about eight events a year and plan them in chat.
```

**Context first** - one question per message, nothing already answered:

> **Q:** How many events?
> **A:** Eight a year.
>
> **Q:** Sign-ups needed?
> **A:** Yes, for most.
>
> **Q:** Budget tracked?
> **A:** Not properly.

**Recommended next step** - offered, not built:

> One record per event with an owner, a date and a sign-up count, and a budget line only for events that have one.
>
> Workflow: Event listed → Sign-ups → Budget → Run → Feedback captured
>
> Want the CSV, SQL, JSON Schema and Notion mapping for this?

## Best Practices

- Recommend before building. The recommendation is the product; the files are the follow-up.
- One question per message. A batched intake reads as a form and gets guessed at.
- Keep every field name identical across CSV, SQL and JSON Schema.
- Use `relation` for anything that points at another table, `text` only for free text.
- Money fields are `currency`, never `text`. Dates are `date`, never free text.
- If the user requests an example row, keep it obviously fake so nobody imports it as real data.

## Limitations

- Empty template only. It does not compute payroll, tax, leave balances or KPIs.
- Notion relations need both databases imported before the link column resolves.
- Select options are a starting set. Rename them to match how the business talks.
- No automation, reminders or sync. Those need the integration layer.
- Does not book venues, send invitations or process payments.
- Legal, tax and HR review is still required before this drives real decisions.

## Security & Safety Notes

- Never fill in real names, salaries, medical or banking data. Placeholders only.
- Never mark an example row `Confidential`, and keep bank details masked.
- Creating a requested artifact may write that artifact locally. Do not run commands,
  call APIs, provision infrastructure, or make other external changes unless the user
  explicitly requests and authorizes them.
- If the user pastes real employee data, generate the template and tell them to delete
  the pasted data from the conversation.
- Privacy, legal and disciplinary cases need a qualified human reviewer before anything
  is acted on.

## Common Pitfalls

- **Problem:** the Notion mapping is handed over with no workspace connected.
  **Solution:** the connection prerequisite goes first, and a mapping handed over as
  text is labelled unverified until the workspace is connected.
- **Problem:** asked all six questions in one message.
  **Solution:** ask one, wait, and drop any the first answer already covered.
- **Problem:** built a full system when one table was asked for.
  **Solution:** build what was requested; mention the parent skill separately.
- **Problem:** all four artifacts drift apart.
  **Solution:** derive all four from the field list in this file, never by hand.
- **Problem:** Notion import shows every column as Text.
  **Solution:** that is expected. Apply the property mapping table once, after import.

## Related Skills

- [SME Ops System Builder](../../SKILL.md) - routes to this skill and the other 70 modules.
- [People Directory](../people-directory/SKILL.md) - the employee master record most modules link to.
- [Notification & Reminder Hub](../notification-reminder-hub/SKILL.md) - turns due dates in this module into reminders.

## Reusable Prompt

```
I want to set up town halls, trainings, outings and celebrations with budget and attendance for my company.
Ask me one short question at a time, and only about what I have not already told you.
Then recommend the smallest setup that fits, and wait for me to ask before you build it.
When I ask, output CSV, SQL DDL, JSON Schema, a Notion property mapping or an Excel workbook. Data only.
```

