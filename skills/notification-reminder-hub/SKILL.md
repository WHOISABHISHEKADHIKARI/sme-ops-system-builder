---
name: notification-reminder-hub
description: "Notification & Reminder Hub: context-first intake, then CSV, SQL, JSON Schema and Notion on request. One short question per message. Use for reminder hub."
category: business
risk: safe
source: self
source_type: self
date_added: "2026-09-26"
author: WHOISABHISHEKADHIKARI
tags: [sme, business, operations, database, csv, notion, sql, analyze]
tools: []
---

# Notification & Reminder Hub

**What it is:** Automated alerts.

## Overview

Works out the smallest useful **Notification & Reminder Hub** setup for the business in front of it, then
builds it only when asked. The default output is a short recommendation, not a
spreadsheet. Artifacts - CSV, SQL DDL, JSON Schema, Notion mapping - are produced on
request, from one field list so they cannot drift apart.

Layer: Layer 9: Analyze. Fits: Growth stage. Table code: n/a.

## When to Use This Skill

- reminder hub
- notification tracker
- automated alerts log
- task reminder system

Also use it when the user says "automated alerts", or describes the same process happening in a
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

> **Q:** Which reminders are people missing?

### Step 2 - Ask only what is missing

Skip anything the user already answered, in any earlier message. Ask the rest one at a
time, and stop as soon as the remaining answers would not change the output.

- **Reminders** - Which ones? / How many? / How often each?
- **Delivery** - Which channel? / How often can you message people? / Any quiet hours?
- **Ownership** - Who owns each reminder? / What data triggers it? / Opt-outs?
- **Current process** - Anything automated? / Calendar or manual? / What gets missed?
- **Outcome** - What do you need? / A reminder list, a rule set or both?

Never invent an answer. If the user does not know, record it as unknown and carry on.

### Step 3 - Hold the internal context

Hold the answers in this shape. It stays internal - it is not shown to the user unless
they ask, and it never carries a value the user did not give.

```yaml
module: notification-reminder-hub
intent: null            # set in Step 1, one of: set up, fix, review, report, import
scale: null             # Starter | Growth | Scale, only if the answer changes it
areas:
  "Reminders": null
  "Delivery": null
  "Ownership": null
  "Current process": null
  "Outcome": null
requested_outputs: []   # csv | sql | json | notion - only what was explicitly asked for
confirmed_facts: []     # only what the user actually said
open_questions: []      # the unanswered ones, in the order worth asking
```

### Step 4 - Recommend the smallest workflow

Give a short recommendation, then ask whether to build it. Do not build unprompted. Ask: "Want me to build the CSV, SQL DDL, JSON Schema, Notion mapping, or an Excel workbook from these confirmed rules?"

**Recommended approach:** Map each reminder to a trigger, an owner and a channel, and drop any reminder nobody acts on. Reminder volume decays fast.

**Why this one:** Reminder systems fail from volume and repetition. Start with the few that change behaviour, and make each one owned.

**Workflow:** Trigger → Rule checked → Message sent → Acknowledged → Escalated if ignored

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
Notification Title,Department,Message,Notification ID,Priority,Recipient,Related Record,Scheduled Date,Sent Date,Status,Trigger Module,Type
Probation review due,Delivery,Probation review due on 28 Sep. Book a slot with your manager.,,Low,Rohit Verma,REC-2026-042,2026-09-24,2026-09-24,Delivered,Contract & Document Renewal,Email
```

```sql
CREATE TABLE notification_reminder_hub (
  notification_title VARCHAR(255),
  department VARCHAR(255),
  message TEXT,
  notification_id SERIAL PRIMARY KEY,
  priority VARCHAR(100) NOT NULL,
  recipient VARCHAR(255),
  related_record VARCHAR(255),  -- relation -> target record
  scheduled_date DATE NOT NULL,
  sent_date DATE NOT NULL,
  status VARCHAR(100) NOT NULL,
  trigger_module VARCHAR(255),
  type VARCHAR(100) NOT NULL,
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_notification_reminder_hub_status ON notification_reminder_hub (status);
```

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "Notification & Reminder Hub",
  "type": "object",
  "additionalProperties": false,
  "properties": {
      "Notification Title": { "type": "string" },
      "Department": { "type": "string" },
      "Message": { "type": "string" },
      "Notification ID": { "type": "integer" },
      "Priority": { "type": "string" },
      "Recipient": { "type": "string" },
      "Related Record": { "type": "string" },
      "Scheduled Date": { "type": "string", "format": "date" },
      "Sent Date": { "type": "string", "format": "date" },
      "Status": { "type": "string" },
      "Trigger Module": { "type": "string" },
      "Type": { "type": "string" }
  },
  "required": [
      "Priority",
      "Scheduled Date",
      "Sent Date",
      "Status",
      "Type"
  ]
}
```

```markdown
| CSV column | Notion property | Set after import |
|---|---|---|
| Notification Title | Text | Leave as Text |
| Department | Text | Leave as Text |
| Message | Text | Leave as Text |
| Notification ID | Text (or Notion auto-ID) | Delete the column and switch the primary column to auto-ID, or keep as Text |
| Priority | Select (add options after import) | Convert to Select, add options: "Low", "Medium", "High", "Urgent" |
| Recipient | Text | Leave as Text |
| Related Record | Relation (link to the target database) | Convert to Relation, link to the target database |
| Scheduled Date | Date | Convert to Date |
| Sent Date | Date | Convert to Date |
| Status | Select (add options after import) | Convert to Select, add options: "Scheduled", "Sent", "Delivered", "Failed", "Cancelled" |
| Trigger Module | Text | Leave as Text |
| Type | Select (add options after import) | Convert to Select, add options: "Email", "WhatsApp", "Slack", "Calendar", "Task" |
```

The rows above are documentation examples only. Emit empty templates unless the user explicitly requests examples. Money stays `currency`, dates stay `date`,
and anything pointing at another table stays `relation`.

## Field Reference

| # | Field | Type | SQL | JSON Schema | Notion | CSV example |
|---:|---|---|---|---|---|---|
| 1 | Notification Title | `text` | `VARCHAR(255)` | `string` | Text | `Probation review due` |
| 2 | Department | `text` | `VARCHAR(255)` | `string` | Text | `Delivery` |
| 3 | Message | `long_text` | `TEXT` | `string` | Text | `Probation review due on 28 Sep. Book a slot with your manager.` |
| 4 | Notification ID | `id` | `SERIAL PRIMARY KEY` | `integer` | Text (or Notion auto-ID) | `(blank)` |
| 5 | Priority | `select` | `VARCHAR(100)` | `string` | Select (add options after import) | `Low` |
| 6 | Recipient | `text` | `VARCHAR(255)` | `string` | Text | `Rohit Verma` |
| 7 | Related Record | `relation` | `VARCHAR(255)` | `string` | Relation (link to the target database) | `REC-2026-042` |
| 8 | Scheduled Date | `date` | `DATE` | `string, format: date` | Date | `2026-09-24` |
| 9 | Sent Date | `date` | `DATE` | `string, format: date` | Date | `2026-09-24` |
| 10 | Status | `select` | `VARCHAR(100)` | `string` | Select (add options after import) | `Delivered` |
| 11 | Trigger Module | `text` | `VARCHAR(255)` | `string` | Text | `Contract & Document Renewal` |
| 12 | Type | `select` | `VARCHAR(100)` | `string` | Select (add options after import) | `Email` |

## Select Options

**Priority**

```
Low | Medium | High | Urgent
```
**Status**

```
Scheduled | Sent | Delivered | Failed | Cancelled
```
**Type**

```
Email | WhatsApp | Slack | Calendar | Task
```

## Relations

Link fields: `Related Record`

## Examples

**Prompt**

```
Three people now miss contract renewal dates and we hear about it after the fact.
```

**Context first** - one question per message, nothing already answered:

> **Q:** Which reminders?
> **A:** Renewals, reviews and follow-ups.
>
> **Q:** Channel?
> **A:** Email today, manually.
>
> **Q:** How many?
> **A:** Maybe six.

**Recommended next step** - offered, not built:

> Map each reminder to a trigger, an owner and a channel, and drop any reminder nobody acts on. Reminder volume decays fast.
>
> Workflow: Trigger → Rule checked → Message sent → Acknowledged → Escalated if ignored
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
- Does not send messages itself or connect to a messaging platform.
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
- [Notification & Reminder Hub](SKILL.md) - turns due dates in this module into reminders.

## Reusable Prompt

```
I want to set up automated alerts for my company.
Ask me one short question at a time, and only about what I have not already told you.
Then recommend the smallest setup that fits, and wait for me to ask before you build it.
When I ask, output CSV, SQL DDL, JSON Schema, a Notion property mapping or an Excel workbook. Data only.
```

