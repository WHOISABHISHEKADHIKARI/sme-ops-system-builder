---
name: team-calendar
description: "Team Calendar: context-first intake, then CSV, SQL, JSON Schema and Notion on request. One short question per message. Use for team calendar."
category: business
risk: safe
source: self
source_type: self
date_added: "2026-09-26"
author: WHOISABHISHEKADHIKARI
tags: [sme, business, operations, database, csv, notion, sql, manage]
tools: []
---

# Team Calendar

**What it is:** Unified view.

## Overview

Works out the smallest useful **Team Calendar** setup for the business in front of it, then
builds it only when asked. The default output is a short recommendation, not a
spreadsheet. Artifacts - CSV, SQL DDL, JSON Schema, Notion mapping - are produced on
request, from one field list so they cannot drift apart.

Layer: Layer 4: Manage. Fits: Growth stage. Table code: n/a.

## When to Use This Skill

- team calendar
- shared events calendar
- who is available

Also use it when the user says "unified view", or describes the same process happening in a
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

> **Q:** What should appear on the shared calendar?

### Step 2 - Ask only what is missing

Skip anything the user already answered, in any earlier message. Ask the rest one at a
time, and stop as soon as the remaining answers would not change the output.

- **Content** - Which events? / Holidays included? / Personal events excluded?
- **Visibility** - Who sees what? / Department calendars? / Private items?
- **Sync** - Synced with Google? / Two-way? / Who owns it?
- **Current process** - How do you share now? / Which calendar? / What is missing?
- **Outcome** - What do you need? / A calendar view, a feed or conflict rules?

Never invent an answer. If the user does not know, record it as unknown and carry on.

### Step 3 - Hold the internal context

Hold the answers in this shape. It stays internal - it is not shown to the user unless
they ask, and it never carries a value the user did not give.

```yaml
module: team-calendar
intent: null            # set in Step 1, one of: set up, fix, review, report, import
scale: null             # Starter | Growth | Scale, only if the answer changes it
areas:
  "Content": null
  "Visibility": null
  "Sync": null
  "Current process": null
  "Outcome": null
requested_outputs: []   # csv | sql | json | notion - only what was explicitly asked for
confirmed_facts: []     # only what the user actually said
open_questions: []      # the unanswered ones, in the order worth asking
```

### Step 4 - Recommend the smallest workflow

Give a short recommendation, then ask whether to build it. Do not build unprompted. Ask: "Want me to build the CSV, SQL DDL, JSON Schema, Notion mapping, or an Excel workbook from these confirmed rules?"

**Recommended approach:** Keep the calendar in the tool already used and make the database a thin index of it, not a second calendar.

**Why this one:** Two calendars is worse than one. If a shared calendar already exists, the useful output is a record of key events, not a scheduler.

**Workflow:** Event created → Calendar entry → Attendance or RSVP → Reminder

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
Event,Event Type,Date,Start Time,End Time,Time Zone,Department,Attendees,Organizer,Source Module,Location or Link,Notes,Event ID
Q1 Town Hall,Meeting,2026-01-15,10:00,11:00,IST (UTC+5:30),Delivery,All employees,Karan Malhotra,Invoices & Billing,https://example.com/calendar/launch-week,February all-hands moved for the client call; the room is double-booked until March.,
```

```sql
CREATE TABLE team_calendar (
  event VARCHAR(255),
  event_type VARCHAR(100) NOT NULL,
  date DATE NOT NULL,
  start_time VARCHAR(255),
  end_time VARCHAR(255),
  time_zone VARCHAR(255),
  department VARCHAR(255),
  attendees VARCHAR(255),
  organizer VARCHAR(255),
  source_module VARCHAR(255),
  location_or_link TEXT,
  notes TEXT,
  event_id SERIAL PRIMARY KEY,
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);
```

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "Team Calendar",
  "type": "object",
  "additionalProperties": false,
  "properties": {
      "Event": { "type": "string" },
      "Event Type": { "type": "string" },
      "Date": { "type": "string", "format": "date" },
      "Start Time": { "type": "string" },
      "End Time": { "type": "string" },
      "Time Zone": { "type": "string" },
      "Department": { "type": "string" },
      "Attendees": { "type": "string" },
      "Organizer": { "type": "string" },
      "Source Module": { "type": "string" },
      "Location or Link": { "type": "string", "format": "uri" },
      "Notes": { "type": "string" },
      "Event ID": { "type": "integer" }
  },
  "required": [
      "Event Type",
      "Date"
  ]
}
```

```markdown
| CSV column | Notion property | Set after import |
|---|---|---|
| Event | Text | Leave as Text |
| Event Type | Select (add options after import) | Convert to Select, add options: "Meeting", "Deadline", "Leave", "Training", "Travel", "Review" |
| Date | Date | Convert to Date |
| Start Time | Text | Leave as Text |
| End Time | Text | Leave as Text |
| Time Zone | Text | Leave as Text |
| Department | Text | Leave as Text |
| Attendees | Text | Leave as Text |
| Organizer | Text | Leave as Text |
| Source Module | Text | Leave as Text |
| Location or Link | URL | Convert to URL |
| Notes | Text | Leave as Text |
| Event ID | Text (or Notion auto-ID) | Delete the column and switch the primary column to auto-ID, or keep as Text |
```

The rows above are documentation examples only. Emit empty templates unless the user explicitly requests examples. Money stays `currency`, dates stay `date`,
and anything pointing at another table stays `relation`.

## Field Reference

| # | Field | Type | SQL | JSON Schema | Notion | CSV example |
|---:|---|---|---|---|---|---|
| 1 | Event | `text` | `VARCHAR(255)` | `string` | Text | `Q1 Town Hall` |
| 2 | Event Type | `select` | `VARCHAR(100)` | `string` | Select (add options after import) | `Meeting` |
| 3 | Date | `date` | `DATE` | `string, format: date` | Date | `2026-01-15` |
| 4 | Start Time | `text` | `VARCHAR(255)` | `string` | Text | `10:00` |
| 5 | End Time | `text` | `VARCHAR(255)` | `string` | Text | `11:00` |
| 6 | Time Zone | `text` | `VARCHAR(255)` | `string` | Text | `IST (UTC+5:30)` |
| 7 | Department | `text` | `VARCHAR(255)` | `string` | Text | `Delivery` |
| 8 | Attendees | `text` | `VARCHAR(255)` | `string` | Text | `All employees` |
| 9 | Organizer | `text` | `VARCHAR(255)` | `string` | Text | `Karan Malhotra` |
| 10 | Source Module | `text` | `VARCHAR(255)` | `string` | Text | `Invoices & Billing` |
| 11 | Location or Link | `url` | `TEXT` | `string, format: uri` | URL | `https://example.com/calendar/launch-week` |
| 12 | Notes | `long_text` | `TEXT` | `string` | Text | `February all-hands moved for the client call; the room is double-booked until March.` |
| 13 | Event ID | `id` | `SERIAL PRIMARY KEY` | `integer` | Text (or Notion auto-ID) | `(blank)` |

## Select Options

**Event Type**

```
Meeting | Deadline | Leave | Training | Travel | Review
```

## Relations

Link fields: none

## Examples

**Prompt**

```
We share a Google Calendar but nobody knows who is on leave.
```

**Context first** - one question per message, nothing already answered:

> **Q:** Do you use Google Calendar?
> **A:** Yes, one shared one.
>
> **Q:** What should be tracked?
> **A:** Leave and events.
>
> **Q:** Who sees it?
> **A:** Everyone.

**Recommended next step** - offered, not built:

> Keep the calendar in the tool already used and make the database a thin index of it, not a second calendar.
>
> Workflow: Event created → Calendar entry → Attendance or RSVP → Reminder
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
- Does not create calendar events in Google or resolve scheduling conflicts.
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
I want to set up unified view for my company.
Ask me one short question at a time, and only about what I have not already told you.
Then recommend the smallest setup that fits, and wait for me to ask before you build it.
When I ask, output CSV, SQL DDL, JSON Schema, a Notion property mapping or an Excel workbook. Data only.
```

