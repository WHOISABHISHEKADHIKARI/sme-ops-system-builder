---
name: legal-compliance-vault
description: "Legal & Compliance Vault: context-first intake, then CSV, SQL, JSON Schema and Notion on request. One short question per message. Use for legal document vault."
category: business
risk: safe
source: self
source_type: self
date_added: "2026-09-26"
author: WHOISABHISHEKADHIKARI
tags: [sme, business, operations, database, csv, notion, sql, protect]
tools: []
---

# Legal & Compliance Vault

**What it is:** Legal documents.

## Overview

Works out the smallest useful **Legal & Compliance Vault** setup for the business in front of it, then
builds it only when asked. The default output is a short recommendation, not a
spreadsheet. Artifacts - CSV, SQL DDL, JSON Schema, Notion mapping - are produced on
request, from one field list so they cannot drift apart.

Layer: Layer 7: Protect. Fits: Growth stage. Table code: n/a.

## When to Use This Skill

- legal document vault
- compliance document register
- licence register
- statutory records

Also use it when the user says "legal documents", or describes the same process happening in a
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

> **Q:** What is the most urgent obligation?

### Step 2 - Ask only what is missing

Skip anything the user already answered, in any earlier message. Ask the rest one at a
time, and stop as soon as the remaining answers would not change the output.

- **Obligations** - Which laws or licences apply? / How many? / Any deadlines this year?
- **Evidence** - What proves compliance? / Where held? / Who signs off?
- **Ownership** - Who owns each obligation? / External counsel involved? / Review cadence?
- **Current process** - Is it tracked now? / Calendar or memory? / What is overdue?
- **Outcome** - What do you need? / An obligation register, a document list or both?

Never invent an answer. If the user does not know, record it as unknown and carry on.

### Step 3 - Hold the internal context

Hold the answers in this shape. It stays internal - it is not shown to the user unless
they ask, and it never carries a value the user did not give.

```yaml
module: legal-compliance-vault
intent: null            # set in Step 1, one of: set up, fix, review, report, import
scale: null             # Starter | Growth | Scale, only if the answer changes it
areas:
  "Obligations": null
  "Evidence": null
  "Ownership": null
  "Current process": null
  "Outcome": null
requested_outputs: []   # csv | sql | json | notion - only what was explicitly asked for
confirmed_facts: []     # only what the user actually said
open_questions: []      # the unanswered ones, in the order worth asking
```

### Step 4 - Recommend the smallest workflow

Give a short recommendation, then ask whether to build it. Do not build unprompted. Ask: "Want me to build the CSV, SQL DDL, JSON Schema, Notion mapping, or an Excel workbook from these confirmed rules?"

**Recommended approach:** Record each obligation with a deadline, an owner and the evidence that proves it, and review the overdue list first.

**Why this one:** Compliance risk concentrates in the few items that are due and unowned. A register with owners and dates is the whole control.

**Workflow:** Obligation listed → Owner assigned → Evidence linked → Due date tracked → Reviewed or filed

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
Document Title,Document Type,Compliance Framework,Owner,Department,Effective Date,Expiry Date,Renewal Required,Storage Link,Confidentiality,Status,Legal ID
Master Services Agreement,Contract,ISO 27001,Sneha Iyer,Delivery,2026-01-15,2026-01-15,TRUE,https://example.com/doc,Internal,Active,
```

```sql
CREATE TABLE legal_compliance_vault (
  document_title VARCHAR(255),
  document_type VARCHAR(100) NOT NULL,
  compliance_framework VARCHAR(255),
  owner VARCHAR(255),
  department VARCHAR(255),
  effective_date DATE NOT NULL,
  expiry_date DATE NOT NULL,
  renewal_required BOOLEAN NOT NULL,
  storage_link TEXT,
  confidentiality VARCHAR(100) NOT NULL,
  status VARCHAR(100) NOT NULL,
  legal_id SERIAL PRIMARY KEY,
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_legal_compliance_vault_status ON legal_compliance_vault (status);
```

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "Legal & Compliance Vault",
  "type": "object",
  "additionalProperties": false,
  "properties": {
      "Document Title": { "type": "string" },
      "Document Type": { "type": "string" },
      "Compliance Framework": { "type": "string" },
      "Owner": { "type": "string" },
      "Department": { "type": "string" },
      "Effective Date": { "type": "string", "format": "date" },
      "Expiry Date": { "type": "string", "format": "date" },
      "Renewal Required": { "type": "boolean" },
      "Storage Link": { "type": "string", "format": "uri" },
      "Confidentiality": { "type": "string" },
      "Status": { "type": "string" },
      "Legal ID": { "type": "integer" }
  },
  "required": [
      "Document Type",
      "Effective Date",
      "Expiry Date",
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
| Compliance Framework | Text | Leave as Text |
| Owner | Text | Leave as Text |
| Department | Text | Leave as Text |
| Effective Date | Date | Convert to Date |
| Expiry Date | Date | Convert to Date |
| Renewal Required | Checkbox | Convert to Checkbox |
| Storage Link | URL | Convert to URL |
| Confidentiality | Select (add options after import) | Convert to Select, add options: "Internal", "Public", "Confidential", "Restricted" |
| Status | Select (add options after import) | Convert to Select, add options: "Draft", "In Review", "Approved", "Active", "Expired", "Superseded" |
| Legal ID | Text (or Notion auto-ID) | Delete the column and switch the primary column to auto-ID, or keep as Text |
```

The rows above are documentation examples only. Emit empty templates unless the user explicitly requests examples. Money stays `currency`, dates stay `date`,
and anything pointing at another table stays `relation`.

## Field Reference

| # | Field | Type | SQL | JSON Schema | Notion | CSV example |
|---:|---|---|---|---|---|---|
| 1 | Document Title | `text` | `VARCHAR(255)` | `string` | Text | `Master Services Agreement` |
| 2 | Document Type | `select` | `VARCHAR(100)` | `string` | Select (add options after import) | `Contract` |
| 3 | Compliance Framework | `text` | `VARCHAR(255)` | `string` | Text | `ISO 27001` |
| 4 | Owner | `text` | `VARCHAR(255)` | `string` | Text | `Sneha Iyer` |
| 5 | Department | `text` | `VARCHAR(255)` | `string` | Text | `Delivery` |
| 6 | Effective Date | `date` | `DATE` | `string, format: date` | Date | `2026-01-15` |
| 7 | Expiry Date | `date` | `DATE` | `string, format: date` | Date | `2026-01-15` |
| 8 | Renewal Required | `checkbox` | `BOOLEAN` | `boolean` | Checkbox | `TRUE` |
| 9 | Storage Link | `url` | `TEXT` | `string, format: uri` | URL | `https://example.com/doc` |
| 10 | Confidentiality | `select` | `VARCHAR(100)` | `string` | Select (add options after import) | `Internal` |
| 11 | Status | `select` | `VARCHAR(100)` | `string` | Select (add options after import) | `Active` |
| 12 | Legal ID | `id` | `SERIAL PRIMARY KEY` | `integer` | Text (or Notion auto-ID) | `(blank)` |

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
Draft | In Review | Approved | Active | Expired | Superseded
```

## Relations

Link fields: none

## Examples

**Prompt**

```
We are not sure what our filing deadlines are.
```

**Context first** - one question per message, nothing already answered:

> **Q:** Which obligations?
> **A:** Annual filings and a few licences.
>
> **Q:** Tracked today?
> **A:** In someone's head.
>
> **Q:** Counsel involved?
> **A:** Yes, for the filings.

**Recommended next step** - offered, not built:

> Record each obligation with a deadline, an owner and the evidence that proves it, and review the overdue list first.
>
> Workflow: Obligation listed → Owner assigned → Evidence linked → Due date tracked → Reviewed or filed
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
- Does not provide legal advice or file anything with any authority.
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

- `sme-ops-system-builder` - routes to this skill and the other 70 modules.
- `people-directory` - the employee master record most modules link to.
- `notification-reminder-hub` - turns due dates in this module into reminders.

## Reusable Prompt

```
I want to set up legal documents for my company.
Ask me one short question at a time, and only about what I have not already told you.
Then recommend the smallest setup that fits, and wait for me to ask before you build it.
When I ask, output CSV, SQL DDL, JSON Schema, a Notion property mapping or an Excel workbook. Data only.
```

