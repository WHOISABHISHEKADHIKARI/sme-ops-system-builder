---
name: reports-analytics
description: "Reports & Analytics: context-first intake, then CSV, SQL, JSON Schema and Notion on request. One short question per message. Use for report builder."
category: business
risk: safe
source: self
source_type: self
date_added: "2026-09-26"
author: WHOISABHISHEKADHIKARI
tags: [sme, business, operations, database, csv, notion, sql, analyze]
tools: [claude, cursor, gemini, antigravity]
---

# Reports & Analytics

**What it is:** Insights hub.

## Overview

Works out the smallest useful **Reports & Analytics** setup for the business in front of it, then
builds it only when asked. The default output is a short recommendation, not a
spreadsheet. Artifacts - CSV, SQL DDL, JSON Schema, Notion mapping - are produced on
request, from one field list so they cannot drift apart.

Layer: Layer 9: Analyze. Fits: Scale stage. Table code: n/a.

## When to Use This Skill

- report builder
- analytics report template
- periodic report tracker
- insight reports

Also use it when the user says "insights hub", or describes the same process happening in a
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

> **Q:** Who reads the reports you produce now?

### Step 2 - Ask only what is missing

Skip anything the user already answered, in any earlier message. Ask the rest one at a
time, and stop as soon as the remaining answers would not change the output.

- **Readers** - Who reads them? / How often? / Monthly or weekly?
- **Content** - Which numbers? / Comparisons included? / Any narrative?
- **Data** - Sources available? / Who prepares it? / How long does it take?
- **Current process** - How produced now? / Manual effort? / Is it trusted?
- **Outcome** - What do you need? / A report set, a template or the underlying data?

Never invent an answer. If the user does not know, record it as unknown and carry on.

### Step 3 - Build the internal context

Hold the answers in this shape. It stays internal - it is not shown to the user unless
they ask, and it never carries a value the user did not give.

```yaml
module: reports-analytics
intent: null            # set in Step 1, one of: set up, fix, review, report, import
scale: null             # Starter | Growth | Scale, only if the answer changes it
areas:
  "Readers": null
  "Content": null
  "Data": null
  "Current process": null
  "Outcome": null
requested_outputs: []   # csv | sql | json | notion - only what was explicitly asked for
confirmed_facts: []     # only what the user actually said
open_questions: []      # the unanswered ones, in the order worth asking
```

### Step 4 - Recommend the smallest workflow

Give a short recommendation, then ask whether to build it. Do not build unprompted.

**Recommended approach:** Build a fixed monthly pack with a small set of numbers and one comment per number, and stop producing reports nobody reads.

**Why this one:** Reporting effort goes into formatting, not analysis. A fixed template plus a comment per metric is the smallest useful version.

**Workflow:** Data gathered → Metric calculated → Comment written → Circulated → Action noted

### Step 5 - Build only on request

Once the user asks for it, derive the fields from the confirmed context and emit the
artifacts as data only. No preamble, no summary, no closing line.

```csv
Report Name,Report Type,Source Modules,Owner,Audience,Frequency,Last Run,Next Run,Report Link,Status,Report ID
Monthly Delivery Report,Operational,"Payments Received, Invoices & Billing",Sneha Iyer,All employees,Daily,2026-01-15 09:30,2026-01-15 09:30,https://example.com/reports/monthly-ops,Published,
```

```sql
CREATE TABLE reports_analytics (
  report_name VARCHAR(255),
  report_type VARCHAR(100) NOT NULL,
  source_modules VARCHAR(255),
  owner VARCHAR(255),
  audience VARCHAR(255),
  frequency VARCHAR(100) NOT NULL,
  last_run TIMESTAMP NOT NULL,
  next_run TIMESTAMP NOT NULL,
  report_link TEXT,
  status VARCHAR(100) NOT NULL,
  report_id SERIAL PRIMARY KEY,
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_reports_analytics_status ON reports_analytics (status);
```

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "Reports & Analytics",
  "type": "object",
  "additionalProperties": false,
  "properties": {
      "Report Name": { "type": "string" },
      "Report Type": { "type": "string" },
      "Source Modules": { "type": "string" },
      "Owner": { "type": "string" },
      "Audience": { "type": "string" },
      "Frequency": { "type": "string" },
      "Last Run": { "type": "string", "format": "date-time" },
      "Next Run": { "type": "string", "format": "date-time" },
      "Report Link": { "type": "string", "format": "uri" },
      "Status": { "type": "string" },
      "Report ID": { "type": "integer" }
  },
  "required": [
      "Report Type",
      "Frequency",
      "Last Run",
      "Next Run",
      "Status"
  ]
}
```

```markdown
| CSV column | Notion property | Set after import |
|---|---|---|
| Report Name | Text | Leave as Text |
| Report Type | Select (add options after import) | Convert to Select, add options: "Operational", "Financial", "Management", "Compliance", "Custom" |
| Source Modules | Text | Leave as Text |
| Owner | Text | Leave as Text |
| Audience | Text | Leave as Text |
| Frequency | Select (add options after import) | Convert to Select, add options: "Daily", "Weekly", "Monthly", "Quarterly", "Half Yearly", "Annual" |
| Last Run | Date (include time) | Convert to Date (include time) |
| Next Run | Date (include time) | Convert to Date (include time) |
| Report Link | URL | Convert to URL |
| Status | Select (add options after import) | Convert to Select, add options: "Scheduled", "Running", "Published", "Failed" |
| Report ID | Text (or Notion auto-ID) | Delete the column and switch the primary column to auto-ID, or keep as Text |
```

One example row per artifact, visibly fake. Money stays `currency`, dates stay `date`,
and anything pointing at another table stays `relation`.

## Field Reference

| # | Field | Type | SQL | JSON Schema | Notion | CSV example |
|---:|---|---|---|---|---|---|
| 1 | Report Name | `text` | `VARCHAR(255)` | `string` | Text | `Monthly Delivery Report` |
| 2 | Report Type | `select` | `VARCHAR(100)` | `string` | Select (add options after import) | `Operational` |
| 3 | Source Modules | `text` | `VARCHAR(255)` | `string` | Text | `Payments Received, Invoices & Billing` |
| 4 | Owner | `text` | `VARCHAR(255)` | `string` | Text | `Sneha Iyer` |
| 5 | Audience | `text` | `VARCHAR(255)` | `string` | Text | `All employees` |
| 6 | Frequency | `select` | `VARCHAR(100)` | `string` | Select (add options after import) | `Daily` |
| 7 | Last Run | `datetime` | `TIMESTAMP` | `string, format: date-time` | Date (include time) | `2026-01-15 09:30` |
| 8 | Next Run | `datetime` | `TIMESTAMP` | `string, format: date-time` | Date (include time) | `2026-01-15 09:30` |
| 9 | Report Link | `url` | `TEXT` | `string, format: uri` | URL | `https://example.com/reports/monthly-ops` |
| 10 | Status | `select` | `VARCHAR(100)` | `string` | Select (add options after import) | `Published` |
| 11 | Report ID | `id` | `SERIAL PRIMARY KEY` | `integer` | Text (or Notion auto-ID) | `(blank)` |

## Select Options

**Report Type**

```
Operational | Financial | Management | Compliance | Custom
```
**Frequency**

```
Daily | Weekly | Monthly | Quarterly | Half Yearly | Annual
```
**Status**

```
Scheduled | Running | Published | Failed
```

## Relations

Link fields: none

## Examples

**Prompt**

```
We spend two days a month assembling reports nobody comments on.
```

**Context first** - one question per message, nothing already answered:

> **Q:** Who reads them?
> **A:** Directors.
>
> **Q:** How often?
> **A:** Monthly.
>
> **Q:** How produced?
> **A:** Manually, from accounting exports.

**Recommended next step** - offered, not built:

> Build a fixed monthly pack with a small set of numbers and one comment per number, and stop producing reports nobody reads.
>
> Workflow: Data gathered → Metric calculated → Comment written → Circulated → Action noted
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
- Does not gather data from source systems or verify accuracy.
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
I want to set up insights hub for my company.
Ask me one short question at a time, and only about what I have not already told you.
Then recommend the smallest setup that fits, and wait for me to ask before you build it.
When I ask, output CSV, SQL DDL, JSON Schema and a Notion property mapping. Data only.
```

