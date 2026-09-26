---
name: gamification-engine
description: "Gamification Engine: context-first intake, then CSV, SQL, JSON Schema and Notion on request. One short question per message. Use for employee gamification."
category: business
risk: safe
source: self
source_type: self
date_added: "2026-09-26"
author: WHOISABHISHEKADHIKARI
tags: [sme, business, operations, database, csv, notion, sql, develop]
tools: [claude, cursor, gemini, antigravity]
---

# Gamification Engine

**What it is:** Engagement.

## Overview

Works out the smallest useful **Gamification Engine** setup for the business in front of it, then
builds it only when asked. The default output is a short recommendation, not a
spreadsheet. Artifacts - CSV, SQL DDL, JSON Schema, Notion mapping - are produced on
request, from one field list so they cannot drift apart.

Layer: Layer 5: Develop. Fits: Scale stage. Table code: n/a.

## When to Use This Skill

- employee gamification
- points and badges
- engagement points system
- reward points tracker

Also use it when the user says "engagement", or describes the same process happening in a
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

> **Q:** What behaviour are you trying to change?

### Step 2 - Ask only what is missing

Skip anything the user already answered, in any earlier message. Ask the rest one at a
time, and stop as soon as the remaining answers would not change the output.

- **Behaviour** - What should increase? / Who takes part? / All staff or a team?
- **Mechanic** - Points, badges or leaderboard? / Monthly reset? / Public or private?
- **Rules** - Point values? / What is excluded? / Who can award?
- **Current process** - Anything in place now? / Tool or manual? / Does it get ignored?
- **Outcome** - What do you need? / Points, a leaderboard or reporting?

Never invent an answer. If the user does not know, record it as unknown and carry on.

### Step 3 - Build the internal context

Hold the answers in this shape. It stays internal - it is not shown to the user unless
they ask, and it never carries a value the user did not give.

```yaml
module: gamification-engine
intent: null            # set in Step 1, one of: set up, fix, review, report, import
scale: null             # Starter | Growth | Scale, only if the answer changes it
areas:
  "Behaviour": null
  "Mechanic": null
  "Rules": null
  "Current process": null
  "Outcome": null
requested_outputs: []   # csv | sql | json | notion - only what was explicitly asked for
confirmed_facts: []     # only what the user actually said
open_questions: []      # the unanswered ones, in the order worth asking
```

### Step 4 - Recommend the smallest workflow

Give a short recommendation, then ask whether to build it. Do not build unprompted.

**Recommended approach:** Use points for the behaviour you want and nothing else. A leaderboard only works if most people can appear on it.

**Why this one:** Gamification fails when the points do not connect to something people care about. Start with one behaviour and a monthly reset.

**Workflow:** Behaviour → Award points → Balance → Leaderboard or summary → Review

### Step 5 - Build only on request

Once the user asks for it, derive the fields from the confirmed context and emit the
artifacts as data only. No preamble, no summary, no closing line.

```csv
Player,Employee Name,Department,Points Balance,Points This Month,Level,Badges,Source Module,Last Updated,Notes,Player ID
Aarav Sharma,Aarav Sharma,Delivery,340,120,L1,First responder,Invoices & Billing,2026-01-15,"Points rules changed in February, so the leaderboard reset and nobody has hit a badge yet.",
```

```sql
CREATE TABLE gamification_engine (
  player VARCHAR(255),
  employee_name VARCHAR(255),
  department VARCHAR(255),
  points_balance NUMERIC NOT NULL,
  points_this_month NUMERIC NOT NULL,
  level VARCHAR(100) NOT NULL,
  badges VARCHAR(255),
  source_module VARCHAR(255),
  last_updated DATE NOT NULL,
  notes TEXT,
  player_id SERIAL PRIMARY KEY,
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);
```

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "Gamification Engine",
  "type": "object",
  "additionalProperties": false,
  "properties": {
      "Player": { "type": "string" },
      "Employee Name": { "type": "string" },
      "Department": { "type": "string" },
      "Points Balance": { "type": "number" },
      "Points This Month": { "type": "number" },
      "Level": { "type": "string" },
      "Badges": { "type": "string" },
      "Source Module": { "type": "string" },
      "Last Updated": { "type": "string", "format": "date" },
      "Notes": { "type": "string" },
      "Player ID": { "type": "integer" }
  },
  "required": [
      "Points Balance",
      "Points This Month",
      "Level",
      "Last Updated"
  ]
}
```

```markdown
| CSV column | Notion property | Set after import |
|---|---|---|
| Player | Text | Leave as Text |
| Employee Name | Text | Leave as Text |
| Department | Text | Leave as Text |
| Points Balance | Number | Convert to Number |
| Points This Month | Number | Convert to Number |
| Level | Select (add options after import) | Convert to Select, add options: "L1", "L2", "L3", "L4", "L5", "M1", "M2" |
| Badges | Text | Leave as Text |
| Source Module | Text | Leave as Text |
| Last Updated | Date | Convert to Date |
| Notes | Text | Leave as Text |
| Player ID | Text (or Notion auto-ID) | Delete the column and switch the primary column to auto-ID, or keep as Text |
```

One example row per artifact, visibly fake. Money stays `currency`, dates stay `date`,
and anything pointing at another table stays `relation`.

## Field Reference

| # | Field | Type | SQL | JSON Schema | Notion | CSV example |
|---:|---|---|---|---|---|---|
| 1 | Player | `text` | `VARCHAR(255)` | `string` | Text | `Aarav Sharma` |
| 2 | Employee Name | `text` | `VARCHAR(255)` | `string` | Text | `Aarav Sharma` |
| 3 | Department | `text` | `VARCHAR(255)` | `string` | Text | `Delivery` |
| 4 | Points Balance | `number` | `NUMERIC` | `number` | Number | `340` |
| 5 | Points This Month | `number` | `NUMERIC` | `number` | Number | `120` |
| 6 | Level | `select` | `VARCHAR(100)` | `string` | Select (add options after import) | `L1` |
| 7 | Badges | `text` | `VARCHAR(255)` | `string` | Text | `First responder` |
| 8 | Source Module | `text` | `VARCHAR(255)` | `string` | Text | `Invoices & Billing` |
| 9 | Last Updated | `date` | `DATE` | `string, format: date` | Date | `2026-01-15` |
| 10 | Notes | `long_text` | `TEXT` | `string` | Text | `Points rules changed in February, so the leaderboard reset and nobody has hit a badge yet.` |
| 11 | Player ID | `id` | `SERIAL PRIMARY KEY` | `integer` | Text (or Notion auto-ID) | `(blank)` |

## Select Options

**Level**

```
L1 | L2 | L3 | L4 | L5 | M1 | M2
```

## Relations

Link fields: none

## Examples

**Prompt**

```
We want more people to share knowledge internally.
```

**Context first** - one question per message, nothing already answered:

> **Q:** How many people?
> **A:** Around 30.
>
> **Q:** Points or badges?
> **A:** Points.
>
> **Q:** Leaderboard?
> **A:** No, too small a team.

**Recommended next step** - offered, not built:

> Use points for the behaviour you want and nothing else. A leaderboard only works if most people can appear on it.
>
> Workflow: Behaviour → Award points → Balance → Leaderboard or summary → Review
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
- Does not run recognition programmes or deliver rewards.
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
I want to set up engagement for my company.
Ask me one short question at a time, and only about what I have not already told you.
Then recommend the smallest setup that fits, and wait for me to ask before you build it.
When I ask, output CSV, SQL DDL, JSON Schema and a Notion property mapping. Data only.
```

