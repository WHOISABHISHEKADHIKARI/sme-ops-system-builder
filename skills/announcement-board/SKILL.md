---
name: announcement-board
description: "Announcement Board: context-first intake, then CSV, SQL, JSON Schema and Notion on request. One short question per message. Use for announcement board."
category: business
risk: safe
source: self
source_type: self
date_added: "2026-09-26"
author: WHOISABHISHEKADHIKARI
tags: [sme, business, operations, database, csv, notion, sql, engage]
tools: []
---

# Announcement Board

**What it is:** News distribution.

## Overview

Works out the smallest useful **Announcement Board** setup for the business in front of it, then
builds it only when asked. The default output is a short recommendation, not a
spreadsheet. Artifacts - CSV, SQL DDL, JSON Schema, Notion mapping - are produced on
request, from one field list so they cannot drift apart.

Layer: Layer 6: Engage. Fits: Starter stage. Table code: n/a.

## When to Use This Skill

- announcement board
- company news feed
- notice board
- internal announcements

Also use it when the user says "news distribution", or describes the same process happening in a
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

> **Q:** Who needs to read your announcements?

### Step 2 - Ask only what is missing

Skip anything the user already answered, in any earlier message. Ask the rest one at a
time, and stop as soon as the remaining answers would not change the output.

- **Audience** - Who reads these? / Whole company or a team? / Any external readers?
- **Content** - What gets posted? / Announcements or both? / Attachments used?
- **Approval** - Who writes them? / Approval needed? / Scheduled posts?
- **Current process** - How do you share news now? / Email, chat or both? / What gets missed?
- **Outcome** - What do you need? / A board, a schedule or archives?

Never invent an answer. If the user does not know, record it as unknown and carry on.

### Step 3 - Hold the internal context

Hold the answers in this shape. It stays internal - it is not shown to the user unless
they ask, and it never carries a value the user did not give.

```yaml
module: announcement-board
intent: null            # set in Step 1, one of: set up, fix, review, report, import
scale: null             # Starter | Growth | Scale, only if the answer changes it
areas:
  "Audience": null
  "Content": null
  "Approval": null
  "Current process": null
  "Outcome": null
requested_outputs: []   # csv | sql | json | notion - only what was explicitly asked for
confirmed_facts: []     # only what the user actually said
open_questions: []      # the unanswered ones, in the order worth asking
```

### Step 4 - Recommend the smallest workflow

Give a short recommendation, then ask whether to build it. Do not build unprompted. Ask: "Want me to build the CSV, SQL DDL, JSON Schema, Notion mapping, or an Excel workbook from these confirmed rules?"

**Recommended approach:** Publish in one place and keep an expiry date, so old announcements stop looking current. Target the audience rather than broadcasting.

**Why this one:** Announcement boards fail from clutter, not from missing posts. An expiry date and a clear owner keep the board readable.

**Workflow:** Draft → Approval → Publish → Read or acknowledged → Expiry

### Step 5 - Build only on request

Once the user asks for it, derive the fields from the confirmed context and emit the
artifacts as data only. No preamble, no summary, no closing line.

For an Excel-compatible CSV, use UTF-8 with a byte order mark so Excel opens the
text correctly. A CSV is not an `.xlsx` workbook; create `.xlsx` only when the user
requests a workbook.
A CSV carries no types, so after it, name the columns
that need a number, date or currency format applied.

```csv
Announcement Title,Acknowledged By,Ann ID,Author,Category,Department,Expiry Date,Priority,Publish Date,Status,Summary,Target Audience,Views
Office closed on 15th,"Example Person 1, Example Person 2",,Example Author,Company,Delivery,2026-01-15,Low,2026-01-15,Published,Office closed on the 15th for the public holiday.,All employees,184
```

```sql
CREATE TABLE announcement_board (
  announcement_title VARCHAR(255),
  acknowledged_by VARCHAR(255),
  ann_id SERIAL PRIMARY KEY,
  author VARCHAR(255),
  category VARCHAR(100) NOT NULL,
  department VARCHAR(255),
  expiry_date DATE NOT NULL,
  priority VARCHAR(100) NOT NULL,
  publish_date DATE NOT NULL,
  status VARCHAR(100) NOT NULL,
  summary TEXT,
  target_audience VARCHAR(255),
  views VARCHAR(255),
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_announcement_board_status ON announcement_board (status);
```

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "Announcement Board",
  "type": "object",
  "additionalProperties": false,
  "properties": {
      "Announcement Title": { "type": "string" },
      "Acknowledged By": { "type": "string" },
      "Ann ID": { "type": "integer" },
      "Author": { "type": "string" },
      "Category": { "type": "string" },
      "Department": { "type": "string" },
      "Expiry Date": { "type": "string", "format": "date" },
      "Priority": { "type": "string" },
      "Publish Date": { "type": "string", "format": "date" },
      "Status": { "type": "string" },
      "Summary": { "type": "string" },
      "Target Audience": { "type": "string" },
      "Views": { "type": "string" }
  },
  "required": [
      "Category",
      "Expiry Date",
      "Priority",
      "Publish Date",
      "Status"
  ]
}
```

```markdown
| CSV column | Notion property | Set after import |
|---|---|---|
| Announcement Title | Text | Leave as Text |
| Acknowledged By | Text | Leave as Text |
| Ann ID | Text (or Notion auto-ID) | Delete the column and switch the primary column to auto-ID, or keep as Text |
| Author | Text | Leave as Text |
| Category | Select (add options after import) | Convert to Select, add options: "Company", "Department", "Team", "Location", "Role" |
| Department | Text | Leave as Text |
| Expiry Date | Date | Convert to Date |
| Priority | Select (add options after import) | Convert to Select, add options: "Low", "Medium", "High", "Urgent" |
| Publish Date | Date | Convert to Date |
| Status | Select (add options after import) | Convert to Select, add options: "Draft", "Scheduled", "Published", "Archived" |
| Summary | Text | Leave as Text |
| Target Audience | Text | Leave as Text |
| Views | Text | Leave as Text |
```

The rows above are documentation examples only. Emit empty templates unless the user explicitly requests examples. Money stays `currency`, dates stay `date`,
and anything pointing at another table stays `relation`.

## Field Reference

| # | Field | Type | SQL | JSON Schema | Notion | CSV example |
|---:|---|---|---|---|---|---|
| 1 | Announcement Title | `text` | `VARCHAR(255)` | `string` | Text | `Office closed on 15th` |
| 2 | Acknowledged By | `text` | `VARCHAR(255)` | `string` | Text | `Example Person 1, Example Person 2` |
| 3 | Ann ID | `id` | `SERIAL PRIMARY KEY` | `integer` | Text (or Notion auto-ID) | `(blank)` |
| 4 | Author | `text` | `VARCHAR(255)` | `string` | Text | `Example Author` |
| 5 | Category | `select` | `VARCHAR(100)` | `string` | Select (add options after import) | `Company` |
| 6 | Department | `text` | `VARCHAR(255)` | `string` | Text | `Delivery` |
| 7 | Expiry Date | `date` | `DATE` | `string, format: date` | Date | `2026-01-15` |
| 8 | Priority | `select` | `VARCHAR(100)` | `string` | Select (add options after import) | `Low` |
| 9 | Publish Date | `date` | `DATE` | `string, format: date` | Date | `2026-01-15` |
| 10 | Status | `select` | `VARCHAR(100)` | `string` | Select (add options after import) | `Published` |
| 11 | Summary | `long_text` | `TEXT` | `string` | Text | `Office closed on the 15th for the public holiday.` |
| 12 | Target Audience | `text` | `VARCHAR(255)` | `string` | Text | `All employees` |
| 13 | Views | `text` | `VARCHAR(255)` | `string` | Text | `184` |

## Select Options

**Category**

```
Company | Department | Team | Location | Role
```
**Priority**

```
Low | Medium | High | Urgent
```
**Status**

```
Draft | Scheduled | Published | Archived
```

## Relations

Link fields: none

## Examples

**Prompt**

```
Company news goes out in chat and gets lost in a week.
```

**Context first** - one question per message, nothing already answered:

> **Q:** Audience?
> **A:** Everyone.
>
> **Q:** Approval?
> **A:** HR approves the important ones.
>
> **Q:** Where do you post now?
> **A:** A chat channel.

**Recommended next step** - offered, not built:

> Publish in one place and keep an expiry date, so old announcements stop looking current. Target the audience rather than broadcasting.
>
> Workflow: Draft → Approval → Publish → Read or acknowledged → Expiry
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
- Does not send email or chat messages for you.
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
I want to set up news distribution for my company.
Ask me one short question at a time, and only about what I have not already told you.
Then recommend the smallest setup that fits, and wait for me to ask before you build it.
When I ask, output CSV, SQL DDL, JSON Schema, a Notion property mapping or an Excel workbook. Data only.
```

