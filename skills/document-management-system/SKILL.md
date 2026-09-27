---
name: document-management-system
description: "Document Management System: context-first intake, then CSV, SQL, JSON Schema and Notion on request. One short question per message. Use for document management system."
category: business
risk: safe
source: self
source_type: self
date_added: "2026-09-26"
author: WHOISABHISHEKADHIKARI
tags: [sme, business, operations, database, csv, notion, sql, protect]
tools: [claude, cursor, gemini, antigravity]
---

# Document Management System

**What it is:** Storage & signing.

## Overview

Works out the smallest useful **Document Management System** setup for the business in front of it, then
builds it only when asked. The default output is a short recommendation, not a
spreadsheet. Artifacts - CSV, SQL DDL, JSON Schema, Notion mapping - are produced on
request, from one field list so they cannot drift apart.

Layer: Layer 7: Protect. Fits: Growth stage. Table code: n/a.

## When to Use This Skill

- document management system
- document register
- e signature tracker
- shared drive index

Also use it when the user says "storage & signing", or describes the same process happening in a
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

> **Q:** Where do your documents live now?

### Step 2 - Ask only what is missing

Skip anything the user already answered, in any earlier message. Ask the rest one at a
time, and stop as soon as the remaining answers would not change the output.

- **Documents** - Which types? / How many? / Any that must never be edited?
- **Structure** - Folders or tags? / Naming convention? / Any access levels?
- **Lifecycle** - Who approves? / Versions or final only? / When archived?
- **Current process** - Where do they live? / Shared drive or scattered? / What is missing?
- **Outcome** - What do you need? / A structure, a naming rule or an index?

Never invent an answer. If the user does not know, record it as unknown and carry on.

### Step 3 - Hold the internal context

Hold the answers in this shape. It stays internal - it is not shown to the user unless
they ask, and it never carries a value the user did not give.

```yaml
module: document-management-system
intent: null            # set in Step 1, one of: set up, fix, review, report, import
scale: null             # Starter | Growth | Scale, only if the answer changes it
areas:
  "Documents": null
  "Structure": null
  "Lifecycle": null
  "Current process": null
  "Outcome": null
requested_outputs: []   # csv | sql | json | notion - only what was explicitly asked for
confirmed_facts: []     # only what the user actually said
open_questions: []      # the unanswered ones, in the order worth asking
```

### Step 4 - Recommend the smallest workflow

Give a short recommendation, then ask whether to build it. Do not build unprompted. Ask: "Want me to build the CSV, SQL DDL, JSON Schema, Notion mapping, or an Excel workbook from these confirmed rules?"

**Recommended approach:** Fix naming, ownership and a final-versus-draft rule before adding any new tool. Structure without ownership stays chaotic.

**Why this one:** Document systems fail at versioning and ownership, not at storage. A naming rule plus one owner per document type is the practical fix.

**Workflow:** Document captured → Named and tagged → Owner assigned → Approved version → Archived

### Step 5 - Build only on request

Once the user asks for it, derive the fields from the confirmed context and emit the
artifacts as data only. No preamble, no summary, no closing line.

An Excel workbook is the CSV emitted with a UTF-8 byte order mark, so Excel opens it with
correct text and no import dialog. A CSV carries no types, so after it, name the columns
that need a number, date or currency format applied.

```csv
Document Title,Document Type,Employee Name,Department,Uploaded By,Upload Date,Signature Required,Signed Date,Version,Storage Link,Confidentiality,Status,Document ID
Master Services Agreement,Contract,Aarav Sharma,Delivery,Sneha Iyer,2026-01-15,FALSE,2026-01-15,v1.0,https://example.com/doc,Internal,Published,
```

```sql
CREATE TABLE document_management_system (
  document_title VARCHAR(255),
  document_type VARCHAR(100) NOT NULL,
  employee_name VARCHAR(255),
  department VARCHAR(255),
  uploaded_by VARCHAR(255),
  upload_date DATE NOT NULL,
  signature_required BOOLEAN NOT NULL,
  signed_date DATE NOT NULL,
  version VARCHAR(255),
  storage_link TEXT,
  confidentiality VARCHAR(100) NOT NULL,
  status VARCHAR(100) NOT NULL,
  document_id SERIAL PRIMARY KEY,
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_document_management_system_status ON document_management_system (status);
```

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "Document Management System",
  "type": "object",
  "additionalProperties": false,
  "properties": {
      "Document Title": { "type": "string" },
      "Document Type": { "type": "string" },
      "Employee Name": { "type": "string" },
      "Department": { "type": "string" },
      "Uploaded By": { "type": "string" },
      "Upload Date": { "type": "string", "format": "date" },
      "Signature Required": { "type": "boolean" },
      "Signed Date": { "type": "string", "format": "date" },
      "Version": { "type": "string" },
      "Storage Link": { "type": "string", "format": "uri" },
      "Confidentiality": { "type": "string" },
      "Status": { "type": "string" },
      "Document ID": { "type": "integer" }
  },
  "required": [
      "Document Type",
      "Upload Date",
      "Signed Date",
      "Confidentiality",
      "Status"
  ]
}
```

```markdown
| CSV column | Notion property | Set after import |
|---|---|---|
| Document Title | Text | Leave as Text |
| Document Type | Select (add options after import) | Convert to Select, add options: "Contract", "Policy", "Invoice", "Certificate", "Report", "ID Proof", "Other" |
| Employee Name | Text | Leave as Text |
| Department | Text | Leave as Text |
| Uploaded By | Text | Leave as Text |
| Upload Date | Date | Convert to Date |
| Signature Required | Checkbox | Convert to Checkbox |
| Signed Date | Date | Convert to Date |
| Version | Text | Leave as Text |
| Storage Link | URL | Convert to URL |
| Confidentiality | Select (add options after import) | Convert to Select, add options: "Internal", "Public", "Confidential", "Restricted" |
| Status | Select (add options after import) | Convert to Select, add options: "Draft", "In Review", "Approved", "Published", "Superseded", "Archived" |
| Document ID | Text (or Notion auto-ID) | Delete the column and switch the primary column to auto-ID, or keep as Text |
```

One example row per artifact, visibly fake. Money stays `currency`, dates stay `date`,
and anything pointing at another table stays `relation`.

## Field Reference

| # | Field | Type | SQL | JSON Schema | Notion | CSV example |
|---:|---|---|---|---|---|---|
| 1 | Document Title | `text` | `VARCHAR(255)` | `string` | Text | `Master Services Agreement` |
| 2 | Document Type | `select` | `VARCHAR(100)` | `string` | Select (add options after import) | `Contract` |
| 3 | Employee Name | `text` | `VARCHAR(255)` | `string` | Text | `Aarav Sharma` |
| 4 | Department | `text` | `VARCHAR(255)` | `string` | Text | `Delivery` |
| 5 | Uploaded By | `text` | `VARCHAR(255)` | `string` | Text | `Sneha Iyer` |
| 6 | Upload Date | `date` | `DATE` | `string, format: date` | Date | `2026-01-15` |
| 7 | Signature Required | `checkbox` | `BOOLEAN` | `boolean` | Checkbox | `FALSE` |
| 8 | Signed Date | `date` | `DATE` | `string, format: date` | Date | `2026-01-15` |
| 9 | Version | `text` | `VARCHAR(255)` | `string` | Text | `v1.0` |
| 10 | Storage Link | `url` | `TEXT` | `string, format: uri` | URL | `https://example.com/doc` |
| 11 | Confidentiality | `select` | `VARCHAR(100)` | `string` | Select (add options after import) | `Internal` |
| 12 | Status | `select` | `VARCHAR(100)` | `string` | Select (add options after import) | `Published` |
| 13 | Document ID | `id` | `SERIAL PRIMARY KEY` | `integer` | Text (or Notion auto-ID) | `(blank)` |

## Select Options

**Document Type**

```
Contract | Policy | Invoice | Certificate | Report | ID Proof | Other
```
**Confidentiality**

```
Internal | Public | Confidential | Restricted
```
**Status**

```
Draft | In Review | Approved | Published | Superseded | Archived
```

## Relations

Link fields: none

## Examples

**Prompt**

```
We have the same policy in six folders with different names.
```

**Context first** - one question per message, nothing already answered:

> **Q:** Where do they live?
> **A:** A shared drive with 12 folders.
>
> **Q:** Versions kept?
> **A:** Sometimes.
>
> **Q:** Who owns them?
> **A:** Unclear.

**Recommended next step** - offered, not built:

> Fix naming, ownership and a final-versus-draft rule before adding any new tool. Structure without ownership stays chaotic.
>
> Workflow: Document captured → Named and tagged → Owner assigned → Approved version → Archived
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
- Does not store files itself or replace a document management platform.
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
I want to set up storage & signing for my company.
Ask me one short question at a time, and only about what I have not already told you.
Then recommend the smallest setup that fits, and wait for me to ask before you build it.
When I ask, output CSV, SQL DDL, JSON Schema, a Notion property mapping or an Excel workbook. Data only.
```

