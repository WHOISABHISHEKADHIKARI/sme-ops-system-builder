---
name: template-library
description: "Template Library: context-first intake, then CSV, SQL, JSON Schema and Notion on request. One short question per message. Use for document template library."
category: business
risk: safe
source: self
source_type: self
date_added: "2026-09-26"
author: WHOISABHISHEKADHIKARI
tags: [sme, business, operations, database, csv, notion, sql, protect]
tools: [claude, cursor, gemini, antigravity]
---

# Template Library

**What it is:** Central templates.

## Overview

Works out the smallest useful **Template Library** setup for the business in front of it, then
builds it only when asked. The default output is a short recommendation, not a
spreadsheet. Artifacts - CSV, SQL DDL, JSON Schema, Notion mapping - are produced on
request, from one field list so they cannot drift apart.

Layer: Layer 7: Protect. Fits: Growth stage. Table code: n/a.

## When to Use This Skill

- document template library
- template repository
- policy template store

Also use it when the user says "central templates", or describes the same process happening in a
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

> **Q:** Which documents do you write repeatedly?

### Step 2 - Ask only what is missing

Skip anything the user already answered, in any earlier message. Ask the rest one at a
time, and stop as soon as the remaining answers would not change the output.

- **Templates** - Which documents? / How many? / Used by one person or many?
- **Structure** - Fields fixed or variable? / Any required sections? / Standard naming?
- **Ownership** - Who approves changes? / Version kept? / Where published?
- **Current process** - Where do templates live now? / Email attachments or a drive? / Which version is current?
- **Outcome** - What do you need? / A library, a naming rule or a review cycle?

Never invent an answer. If the user does not know, record it as unknown and carry on.

### Step 3 - Build the internal context

Hold the answers in this shape. It stays internal - it is not shown to the user unless
they ask, and it never carries a value the user did not give.

```yaml
module: template-library
intent: null            # set in Step 1, one of: set up, fix, review, report, import
scale: null             # Starter | Growth | Scale, only if the answer changes it
areas:
  "Templates": null
  "Structure": null
  "Ownership": null
  "Current process": null
  "Outcome": null
requested_outputs: []   # csv | sql | json | notion - only what was explicitly asked for
confirmed_facts: []     # only what the user actually said
open_questions: []      # the unanswered ones, in the order worth asking
```

### Step 4 - Recommend the smallest workflow

Give a short recommendation, then ask whether to build it. Do not build unprompted.

**Recommended approach:** Keep one current version per template with a named owner, and start the library with the documents people actually reuse.

**Why this one:** Template libraries sprawl when every variant is kept. Keep one current version and an explicit owner, and archive the rest.

**Workflow:** Template catalogued → Fields defined → Approved version → Published → Usage or update

### Step 5 - Build only on request

Once the user asks for it, derive the fields from the confirmed context and emit the
artifacts as data only. No preamble, no summary, no closing line.

```csv
Template Name,Template Type,Module,Department,Owner,Last Updated,Content Link,Status,Template ID
Invoice Template,Checklist,Invoices & Billing,Delivery,Sneha Iyer,2026-01-15,https://example.com/template,Published,
```

```sql
CREATE TABLE template_library (
  template_name VARCHAR(255),
  template_type VARCHAR(100) NOT NULL,
  module VARCHAR(255),
  department VARCHAR(255),
  owner VARCHAR(255),
  last_updated DATE NOT NULL,
  content_link TEXT,
  status VARCHAR(100) NOT NULL,
  template_id SERIAL PRIMARY KEY,
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_template_library_status ON template_library (status);
```

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "Template Library",
  "type": "object",
  "additionalProperties": false,
  "properties": {
      "Template Name": { "type": "string" },
      "Template Type": { "type": "string" },
      "Module": { "type": "string" },
      "Department": { "type": "string" },
      "Owner": { "type": "string" },
      "Last Updated": { "type": "string", "format": "date" },
      "Content Link": { "type": "string", "format": "uri" },
      "Status": { "type": "string" },
      "Template ID": { "type": "integer" }
  },
  "required": [
      "Template Type",
      "Last Updated",
      "Status"
  ]
}
```

```markdown
| CSV column | Notion property | Set after import |
|---|---|---|
| Template Name | Text | Leave as Text |
| Template Type | Select (add options after import) | Convert to Select, add options: "Policy", "Process", "Checklist", "Contract", "Report", "Invoice" |
| Module | Text | Leave as Text |
| Department | Text | Leave as Text |
| Owner | Text | Leave as Text |
| Last Updated | Date | Convert to Date |
| Content Link | URL | Convert to URL |
| Status | Select (add options after import) | Convert to Select, add options: "Draft", "In Review", "Published", "Retired" |
| Template ID | Text (or Notion auto-ID) | Delete the column and switch the primary column to auto-ID, or keep as Text |
```

One example row per artifact, visibly fake. Money stays `currency`, dates stay `date`,
and anything pointing at another table stays `relation`.

## Field Reference

| # | Field | Type | SQL | JSON Schema | Notion | CSV example |
|---:|---|---|---|---|---|---|
| 1 | Template Name | `text` | `VARCHAR(255)` | `string` | Text | `Invoice Template` |
| 2 | Template Type | `select` | `VARCHAR(100)` | `string` | Select (add options after import) | `Checklist` |
| 3 | Module | `text` | `VARCHAR(255)` | `string` | Text | `Invoices & Billing` |
| 4 | Department | `text` | `VARCHAR(255)` | `string` | Text | `Delivery` |
| 5 | Owner | `text` | `VARCHAR(255)` | `string` | Text | `Sneha Iyer` |
| 6 | Last Updated | `date` | `DATE` | `string, format: date` | Date | `2026-01-15` |
| 7 | Content Link | `url` | `TEXT` | `string, format: uri` | URL | `https://example.com/template` |
| 8 | Status | `select` | `VARCHAR(100)` | `string` | Select (add options after import) | `Published` |
| 9 | Template ID | `id` | `SERIAL PRIMARY KEY` | `integer` | Text (or Notion auto-ID) | `(blank)` |

## Select Options

**Template Type**

```
Policy | Process | Checklist | Contract | Report | Invoice
```
**Status**

```
Draft | In Review | Published | Retired
```

## Relations

Link fields: none

## Examples

**Prompt**

```
Half the team uses an old version of the proposal template.
```

**Context first** - one question per message, nothing already answered:

> **Q:** Which documents?
> **A:** Proposals, invoices and handover notes.
>
> **Q:** How many?
> **A:** Maybe fifteen.
>
> **Q:** Where do they live?
> **A:** Email attachments and a drive.

**Recommended next step** - offered, not built:

> Keep one current version per template with a named owner, and start the library with the documents people actually reuse.
>
> Workflow: Template catalogued → Fields defined → Approved version → Published → Usage or update
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
- Does not create or send documents, and does not store files itself.
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
I want to set up central templates for my company.
Ask me one short question at a time, and only about what I have not already told you.
Then recommend the smallest setup that fits, and wait for me to ask before you build it.
When I ask, output CSV, SQL DDL, JSON Schema and a Notion property mapping. Data only.
```

