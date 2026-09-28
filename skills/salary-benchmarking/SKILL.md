---
name: salary-benchmarking
description: "Salary Benchmarking: context-first intake, then CSV, SQL, JSON Schema and Notion on request. One short question per message. Use for salary benchmark."
category: business
risk: safe
source: self
source_type: self
date_added: "2026-09-26"
author: WHOISABHISHEKADHIKARI
tags: [sme, business, operations, database, csv, notion, sql, acquire]
tools: []
---

# Salary Benchmarking

**What it is:** Market intelligence.

## Overview

Works out the smallest useful **Salary Benchmarking** setup for the business in front of it, then
builds it only when asked. The default output is a short recommendation, not a
spreadsheet. Artifacts - CSV, SQL DDL, JSON Schema, Notion mapping - are produced on
request, from one field list so they cannot drift apart.

Layer: Layer 2: Acquire. Fits: Scale stage. Table code: n/a.

## When to Use This Skill

- salary benchmark
- compensation benchmarking
- market pay research
- salary band planner

Also use it when the user says "market intelligence", or describes the same process happening in a
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

> **Q:** Which roles need benchmarking?

### Step 2 - Ask only what is missing

Skip anything the user already answered, in any earlier message. Ask the rest one at a
time, and stop as soon as the remaining answers would not change the output.

- **Roles** - Which roles? / How many grades? / All roles or a few?
- **Market** - Which market or city? / Currency? / Industry benchmark?
- **Bands** - Do you have bands now? / Fixed or negotiable? / Who approves?
- **Current process** - Where does pay data come from? / Last reviewed when? / Gaps?
- **Outcome** - What do you need? / Market ranges, internal bands or a comparison?

Never invent an answer. If the user does not know, record it as unknown and carry on.

### Step 3 - Hold the internal context

Hold the answers in this shape. It stays internal - it is not shown to the user unless
they ask, and it never carries a value the user did not give.

```yaml
module: salary-benchmarking
intent: null            # set in Step 1, one of: set up, fix, review, report, import
scale: null             # Starter | Growth | Scale, only if the answer changes it
areas:
  "Roles": null
  "Market": null
  "Bands": null
  "Current process": null
  "Outcome": null
requested_outputs: []   # csv | sql | json | notion - only what was explicitly asked for
confirmed_facts: []     # only what the user actually said
open_questions: []      # the unanswered ones, in the order worth asking
```

### Step 4 - Recommend the smallest workflow

Give a short recommendation, then ask whether to build it. Do not build unprompted. Ask: "Want me to build the CSV, SQL DDL, JSON Schema, Notion mapping, or an Excel workbook from these confirmed rules?"

**Recommended approach:** Benchmark the roles that are hardest to fill first, and store market range beside internal band so the gap is visible.

**Why this one:** Benchmarking everything at once never finishes. Three hard-to-fill roles tell you more than fifty that are already correctly paid.

**Workflow:** Role list → Market data → Internal band → Gap analysis → Band decision

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
Role Title,Benchmark ID,Currency,Data Source,Department,Grade Level,Internal Max,Internal Min,Last Updated,Market Max,Market Median,Market Min,Notes
Delivery Manager,,INR,Manual,Delivery,L1,1600000.00,1200000.00,2026-01-15,1700000.00,1450000.00,1250000.00,"Benchmarks refreshed in February; two grades sit below the market midpoint."
```

```sql
CREATE TABLE salary_benchmarking (
  role_title VARCHAR(255),
  benchmark_id SERIAL PRIMARY KEY,
  currency VARCHAR(255),
  data_source VARCHAR(255),
  department VARCHAR(255),
  grade_level VARCHAR(100) NOT NULL,
  internal_max NUMERIC(14,2) NOT NULL,
  internal_min NUMERIC(14,2) NOT NULL,
  last_updated DATE NOT NULL,
  market_max NUMERIC(14,2) NOT NULL,
  market_median NUMERIC(14,2) NOT NULL,
  market_min NUMERIC(14,2) NOT NULL,
  notes TEXT,
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);
```

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "Salary Benchmarking",
  "type": "object",
  "additionalProperties": false,
  "properties": {
      "Role Title": { "type": "string" },
      "Benchmark ID": { "type": "integer" },
      "Currency": { "type": "string" },
      "Data Source": { "type": "string" },
      "Department": { "type": "string" },
      "Grade Level": { "type": "string" },
      "Internal Max": { "type": "number" },
      "Internal Min": { "type": "number" },
      "Last Updated": { "type": "string", "format": "date" },
      "Market Max": { "type": "number" },
      "Market Median": { "type": "number" },
      "Market Min": { "type": "number" },
      "Notes": { "type": "string" }
  },
  "required": [
      "Grade Level",
      "Internal Max",
      "Internal Min",
      "Last Updated",
      "Market Max",
      "Market Median",
      "Market Min"
  ]
}
```

```markdown
| CSV column | Notion property | Set after import |
|---|---|---|
| Role Title | Text | Leave as Text |
| Benchmark ID | Text (or Notion auto-ID) | Delete the column and switch the primary column to auto-ID, or keep as Text |
| Currency | Text | Leave as Text |
| Data Source | Text | Leave as Text |
| Department | Text | Leave as Text |
| Grade Level | Select (add options after import) | Convert to Select, add options: "L1", "L2", "L3", "L4", "L5", "M1", "M2" |
| Internal Max | Number (format: currency) | Convert to Number, set format to Currency |
| Internal Min | Number (format: currency) | Convert to Number, set format to Currency |
| Last Updated | Date | Convert to Date |
| Market Max | Number (format: currency) | Convert to Number, set format to Currency |
| Market Median | Number (format: currency) | Convert to Number, set format to Currency |
| Market Min | Number (format: currency) | Convert to Number, set format to Currency |
| Notes | Text | Leave as Text |
```

The rows above are documentation examples only. Emit empty templates unless the user explicitly requests examples. Money stays `currency`, dates stay `date`,
and anything pointing at another table stays `relation`.

## Field Reference

| # | Field | Type | SQL | JSON Schema | Notion | CSV example |
|---:|---|---|---|---|---|---|
| 1 | Role Title | `text` | `VARCHAR(255)` | `string` | Text | `Delivery Manager` |
| 2 | Benchmark ID | `id` | `SERIAL PRIMARY KEY` | `integer` | Text (or Notion auto-ID) | `(blank)` |
| 3 | Currency | `text` | `VARCHAR(255)` | `string` | Text | `INR` |
| 4 | Data Source | `text` | `VARCHAR(255)` | `string` | Text | `Manual` |
| 5 | Department | `text` | `VARCHAR(255)` | `string` | Text | `Delivery` |
| 6 | Grade Level | `select` | `VARCHAR(100)` | `string` | Select (add options after import) | `L1` |
| 7 | Internal Max | `currency` | `NUMERIC(14,2)` | `number` | Number (format: currency) | `1600000.00` |
| 8 | Internal Min | `currency` | `NUMERIC(14,2)` | `number` | Number (format: currency) | `1200000.00` |
| 9 | Last Updated | `date` | `DATE` | `string, format: date` | Date | `2026-01-15` |
| 10 | Market Max | `currency` | `NUMERIC(14,2)` | `number` | Number (format: currency) | `1700000.00` |
| 11 | Market Median | `currency` | `NUMERIC(14,2)` | `number` | Number (format: currency) | `1450000.00` |
| 12 | Market Min | `currency` | `NUMERIC(14,2)` | `number` | Number (format: currency) | `1250000.00` |
| 13 | Notes | `long_text` | `TEXT` | `string` | Text | `Benchmarks refreshed in February; two grades sit below the market midpoint.` |

## Select Options

**Grade Level**

```
L1 | L2 | L3 | L4 | L5 | M1 | M2
```

## Relations

Link fields: none

## Examples

**Prompt**

```
We think our delivery manager is paid below market but have no data.
```

**Context first** - one question per message, nothing already answered:

> **Q:** Which market?
> **A:** Bengaluru, India.
>
> **Q:** Do you have internal bands?
> **A:** Roughly, in a sheet.
>
> **Q:** How many roles?
> **A:** Just delivery roles.

**Recommended next step** - offered, not built:

> Benchmark the roles that are hardest to fill first, and store market range beside internal band so the gap is visible.
>
> Workflow: Role list → Market data → Internal band → Gap analysis → Band decision
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
- Does not provide market data. Pay for the benchmark source separately.
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
I want to set up market intelligence for my company.
Ask me one short question at a time, and only about what I have not already told you.
Then recommend the smallest setup that fits, and wait for me to ask before you build it.
When I ask, output CSV, SQL DDL, JSON Schema, a Notion property mapping or an Excel workbook. Data only.
```

