---
name: internal-communication
description: "Internal Communication: context-first intake, then CSV, SQL, JSON Schema and Notion on request. One short question per message. Use for internal comms log."
category: business
risk: safe
source: self
source_type: self
date_added: "2026-09-26"
author: WHOISABHISHEKADHIKARI
tags: [sme, business, operations, database, csv, notion, sql, engage]
tools: [claude, cursor, gemini, antigravity]
---

# Internal Communication

**What it is:** Structured comms.

## Overview

Works out the smallest useful **Internal Communication** setup for the business in front of it, then
builds it only when asked. The default output is a short recommendation, not a
spreadsheet. Artifacts - CSV, SQL DDL, JSON Schema, Notion mapping - are produced on
request, from one field list so they cannot drift apart.

Layer: Layer 6: Engage. Fits: Scale stage. Table code: n/a.

## When to Use This Skill

- internal comms log
- meeting tracker
- town hall minutes
- communication record

Also use it when the user says "structured comms", or describes the same process happening in a
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

> **Q:** How do people get company news today?

### Step 2 - Ask only what is missing

Skip anything the user already answered, in any earlier message. Ask the rest one at a
time, and stop as soon as the remaining answers would not change the output.

- **Channels** - Which channels? / How many groups? / Email included?
- **Cadence** - Daily digest or weekly? / Who writes it? / Any standing sections?
- **Ownership** - Who owns each channel? / Moderation? / What gets removed?
- **Current process** - How is it done now? / Scattered or one place? / What gets missed?
- **Outcome** - What do you need? / A channel list, a cadence or templates?

Never invent an answer. If the user does not know, record it as unknown and carry on.

### Step 3 - Build the internal context

Hold the answers in this shape. It stays internal - it is not shown to the user unless
they ask, and it never carries a value the user did not give.

```yaml
module: internal-communication
intent: null            # set in Step 1, one of: set up, fix, review, report, import
scale: null             # Starter | Growth | Scale, only if the answer changes it
areas:
  "Channels": null
  "Cadence": null
  "Ownership": null
  "Current process": null
  "Outcome": null
requested_outputs: []   # csv | sql | json | notion - only what was explicitly asked for
confirmed_facts: []     # only what the user actually said
open_questions: []      # the unanswered ones, in the order worth asking
```

### Step 4 - Recommend the smallest workflow

Give a short recommendation, then ask whether to build it. Do not build unprompted.

**Recommended approach:** Fix the ownership and the cadence first. Channels follow from that, and consolidating channels is usually the useful change.

**Why this one:** Internal comms rarely fail for lack of channels. They fail because nobody owns one and the format is inconsistent.

**Workflow:** Channel owned → Cadence set → Message drafted → Published → Read or acknowledged

### Step 5 - Build only on request

Once the user asks for it, derive the fields from the confirmed context and emit the
artifacts as data only. No preamble, no summary, no closing line.

```csv
Communication Title,Type,Date,Department,Host,Attendees,Agenda,Action Items,Follow-up Date,Meeting Link,Status,Communication ID
March All Hands,Announcement,2026-01-15,Delivery,Karan Malhotra,All employees,1. All-hands 2. Policy change 3. New joiners,Confirm budget with finance; circulate the revised scope.,2026-01-15,https://meet.example.com/abc,Sent,
```

```sql
CREATE TABLE internal_communication (
  communication_title VARCHAR(255),
  type VARCHAR(100) NOT NULL,
  date DATE NOT NULL,
  department VARCHAR(255),
  host VARCHAR(255),
  attendees VARCHAR(255),
  agenda VARCHAR(255),
  action_items VARCHAR(255),
  follow_up_date DATE NOT NULL,
  meeting_link TEXT,
  status VARCHAR(100) NOT NULL,
  communication_id SERIAL PRIMARY KEY,
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_internal_communication_status ON internal_communication (status);
```

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "Internal Communication",
  "type": "object",
  "additionalProperties": false,
  "properties": {
      "Communication Title": { "type": "string" },
      "Type": { "type": "string" },
      "Date": { "type": "string", "format": "date" },
      "Department": { "type": "string" },
      "Host": { "type": "string" },
      "Attendees": { "type": "string" },
      "Agenda": { "type": "string" },
      "Action Items": { "type": "string" },
      "Follow-up Date": { "type": "string", "format": "date" },
      "Meeting Link": { "type": "string", "format": "uri" },
      "Status": { "type": "string" },
      "Communication ID": { "type": "integer" }
  },
  "required": [
      "Type",
      "Date",
      "Follow-up Date",
      "Status"
  ]
}
```

```markdown
| CSV column | Notion property | Set after import |
|---|---|---|
| Communication Title | Text | Leave as Text |
| Type | Select (add options after import) | Convert to Select, add options: "Announcement", "Update", "Policy", "Newsletter", "Escalation" |
| Date | Date | Convert to Date |
| Department | Text | Leave as Text |
| Host | Text | Leave as Text |
| Attendees | Text | Leave as Text |
| Agenda | Text | Leave as Text |
| Action Items | Text | Leave as Text |
| Follow-up Date | Date | Convert to Date |
| Meeting Link | URL | Convert to URL |
| Status | Select (add options after import) | Convert to Select, add options: "Draft", "Scheduled", "Sent", "Acknowledged", "Archived" |
| Communication ID | Text (or Notion auto-ID) | Delete the column and switch the primary column to auto-ID, or keep as Text |
```

One example row per artifact, visibly fake. Money stays `currency`, dates stay `date`,
and anything pointing at another table stays `relation`.

## Field Reference

| # | Field | Type | SQL | JSON Schema | Notion | CSV example |
|---:|---|---|---|---|---|---|
| 1 | Communication Title | `text` | `VARCHAR(255)` | `string` | Text | `March All Hands` |
| 2 | Type | `select` | `VARCHAR(100)` | `string` | Select (add options after import) | `Announcement` |
| 3 | Date | `date` | `DATE` | `string, format: date` | Date | `2026-01-15` |
| 4 | Department | `text` | `VARCHAR(255)` | `string` | Text | `Delivery` |
| 5 | Host | `text` | `VARCHAR(255)` | `string` | Text | `Karan Malhotra` |
| 6 | Attendees | `text` | `VARCHAR(255)` | `string` | Text | `All employees` |
| 7 | Agenda | `text` | `VARCHAR(255)` | `string` | Text | `1. All-hands 2. Policy change 3. New joiners` |
| 8 | Action Items | `text` | `VARCHAR(255)` | `string` | Text | `Confirm budget with finance; circulate the revised scope.` |
| 9 | Follow-up Date | `date` | `DATE` | `string, format: date` | Date | `2026-01-15` |
| 10 | Meeting Link | `url` | `TEXT` | `string, format: uri` | URL | `https://meet.example.com/abc` |
| 11 | Status | `select` | `VARCHAR(100)` | `string` | Select (add options after import) | `Sent` |
| 12 | Communication ID | `id` | `SERIAL PRIMARY KEY` | `integer` | Text (or Notion auto-ID) | `(blank)` |

## Select Options

**Type**

```
Announcement | Update | Policy | Newsletter | Escalation
```
**Status**

```
Draft | Scheduled | Sent | Acknowledged | Archived
```

## Relations

Link fields: none

## Examples

**Prompt**

```
News is scattered across five chats and nobody knows what is official.
```

**Context first** - one question per message, nothing already answered:

> **Q:** Which channels?
> **A:** Two chats and email.
>
> **Q:** Cadence?
> **A:** No set cadence.
>
> **Q:** Who owns them?
> **A:** Nobody specific.

**Recommended next step** - offered, not built:

> Fix the ownership and the cadence first. Channels follow from that, and consolidating channels is usually the useful change.
>
> Workflow: Channel owned → Cadence set → Message drafted → Published → Read or acknowledged
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
- Does not send messages or connect to chat platforms.
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
I want to set up structured comms for my company.
Ask me one short question at a time, and only about what I have not already told you.
Then recommend the smallest setup that fits, and wait for me to ask before you build it.
When I ask, output CSV, SQL DDL, JSON Schema and a Notion property mapping. Data only.
```

