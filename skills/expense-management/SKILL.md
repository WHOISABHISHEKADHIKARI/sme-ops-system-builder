---
name: expense-management
description: "Expense Management: context-first intake, then CSV, SQL, JSON Schema and Notion on request. One short question per message. Use for expense tracker."
category: business
risk: safe
source: self
source_type: self
date_added: "2026-09-26"
author: WHOISABHISHEKADHIKARI
tags: [sme, business, operations, database, csv, notion, sql, manage]
tools: []
---

# Expense Management

**What it is:** Claims.

## Overview

Works out the smallest useful **Expense Management** setup for the business in front of it, then
builds it only when asked. The default output is a short recommendation, not a
spreadsheet. Artifacts - CSV, SQL DDL, JSON Schema, Notion mapping - are produced on
request, from one field list so they cannot drift apart.

Layer: Layer 4: Manage. Fits: Starter stage. Table code: n/a.

## When to Use This Skill

- expense tracker
- expense claim form
- reimbursement tracker
- spend claim database

Also use it when the user says "claims", or describes the same process happening in a
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

> **Q:** What is your expense approval limit?

### Step 2 - Ask only what is missing

Skip anything the user already answered, in any earlier message. Ask the rest one at a
time, and stop as soon as the remaining answers would not change the output.

- **Policy** - Approval limit per claim? / Receipt required above? / Category rules?
- **Flow** - Who approves first? / Finance second? / Reimbursed how?
- **Data** - Tax claimed? / Project or cost centre? / Currency?
- **Current process** - How do you track claims now? / Spreadsheet or app? / What gets rejected?
- **Outcome** - What do you need? / A claim form, approvals or reconciliation?

Never invent an answer. If the user does not know, record it as unknown and carry on.

### Step 3 - Hold the internal context

Hold the answers in this shape. It stays internal - it is not shown to the user unless
they ask, and it never carries a value the user did not give.

```yaml
module: expense-management
intent: null            # set in Step 1, one of: set up, fix, review, report, import
scale: null             # Starter | Growth | Scale, only if the answer changes it
areas:
  "Policy": null
  "Flow": null
  "Data": null
  "Current process": null
  "Outcome": null
requested_outputs: []   # csv | sql | json | notion - only what was explicitly asked for
confirmed_facts: []     # only what the user actually said
open_questions: []      # the unanswered ones, in the order worth asking
```

### Step 4 - Recommend the smallest workflow

Give a short recommendation, then ask whether to build it. Do not build unprompted. Ask: "Want me to build the CSV, SQL DDL, JSON Schema, Notion mapping, or an Excel workbook from these confirmed rules?"

**Recommended approach:** Build a claim form that forces receipt and amount, then route by limit. Keep the finance reconciliation as a separate monthly step.

**Why this one:** Most expense problems are missing receipts and unclear limits, both of which can be enforced at data entry rather than at approval.

**Workflow:** Claim submitted → Manager approval → Finance check → Reimbursement → Monthly reconciliation

### Step 5 - Build only on request

Once the user asks for it, derive the fields from the confirmed context and emit the
artifacts as data only. No preamble, no summary, no closing line.

**A selected Notion output is rendered by `notion-manual-import`, so route the
Notion step there.** When the user selects Notion, hand that step to
[notion-manual-import](../notion-manual-import/SKILL.md): it holds the CSV, the property
mapping, the import steps and the verification checklist, and it renders the Field
Reference below instead of defining a table of its own. Do not restate the mapping
here and do not improvise the import steps. If the platform exposes a Notion
connector, emit the connection prerequisite from the
[shared execution contract](../../references/execution-contract.md) verbatim first, then stop and
wait for the reply "Notion connected." and let the helper build in the workspace.
Never claim a connection exists, and never ask for a Notion password or token.

For an Excel-compatible CSV, use UTF-8 with a byte order mark so Excel opens the
text correctly. A CSV is not an `.xlsx` workbook; create `.xlsx` only when the user
requests a workbook.
A CSV carries no types, so after it, name the columns
that need a number, date or currency format applied.

```csv
Expense Claim,Amount,Tax Amount,Approver,Approval Level,Category,Currency,Date of Expense,Department,Employee Name,Expense ID,Notes,Project/Cost Centre,Budget Line,Receipt Attached,Reimbursement Date,Status,Submission Date
EXP-2026-014,45000.00,8100.00,Sneha Iyer,Manager,General,INR,2026-01-15,Delivery,Aarav Sharma,,February claims reconciled against the bank feed; two receipts were missing.,CC-200 Website Redesign,BL-114 Travel,FALSE,2026-01-15,Approved,2026-01-15
```

```sql
CREATE TABLE expense_management (
  expense_claim VARCHAR(255),
  amount NUMERIC(14,2) NOT NULL,
  tax_amount NUMERIC(14,2) NOT NULL,
  approver VARCHAR(255),
  approval_level VARCHAR(100) NOT NULL,
  category VARCHAR(100) NOT NULL,
  currency VARCHAR(255),
  date_of_expense DATE NOT NULL,
  department VARCHAR(255),
  employee_name VARCHAR(255),
  expense_id SERIAL PRIMARY KEY,
  notes TEXT,
  project_cost_centre VARCHAR(255),
  budget_line VARCHAR(255),
  receipt_attached BOOLEAN NOT NULL,
  reimbursement_date DATE NOT NULL,
  status VARCHAR(100) NOT NULL,
  submission_date DATE NOT NULL,
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_expense_management_status ON expense_management (status);
```

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "Expense Management",
  "type": "object",
  "additionalProperties": false,
  "properties": {
      "Expense Claim": { "type": "string" },
      "Amount": { "type": "number" },
      "Tax Amount": { "type": "number" },
      "Approver": { "type": "string" },
      "Approval Level": { "type": "string" },
      "Category": { "type": "string" },
      "Currency": { "type": "string" },
      "Date of Expense": { "type": "string", "format": "date" },
      "Department": { "type": "string" },
      "Employee Name": { "type": "string" },
      "Expense ID": { "type": "integer" },
      "Notes": { "type": "string" },
      "Project/Cost Centre": { "type": "string" },
      "Budget Line": { "type": "string" },
      "Receipt Attached": { "type": "boolean" },
      "Reimbursement Date": { "type": "string", "format": "date" },
      "Status": { "type": "string" },
      "Submission Date": { "type": "string", "format": "date" }
  },
  "required": [
      "Amount",
      "Tax Amount",
      "Approval Level",
      "Category",
      "Date of Expense",
      "Reimbursement Date",
      "Status",
      "Submission Date"
  ]
}
```

```markdown
| CSV column | Notion property | Set after import |
|---|---|---|
| Expense Claim | Text | Leave as Text |
| Amount | Number (format: currency) | Convert to Number, set format to Currency |
| Tax Amount | Number (format: currency) | Convert to Number, set format to Currency |
| Approver | Text | Leave as Text |
| Approval Level | Select (add options after import) | Convert to Select, add options: "Manager", "Finance", "Owner", "Auto Approved" |
| Category | Select (add options after import) | Convert to Select, add options: "General", "Operations", "Finance", "People", "Compliance" |
| Currency | Text | Leave as Text |
| Date of Expense | Date | Convert to Date |
| Department | Text | Leave as Text |
| Employee Name | Text | Leave as Text |
| Expense ID | Text (or Notion auto-ID) | Delete the column and switch the primary column to auto-ID, or keep as Text |
| Notes | Text | Leave as Text |
| Project/Cost Centre | Text | Leave as Text |
| Budget Line | Text | Leave as Text |
| Receipt Attached | Checkbox | Convert to Checkbox |
| Reimbursement Date | Date | Convert to Date |
| Status | Select (add options after import) | Convert to Select, add options: "Draft", "Submitted", "Approved", "Reimbursed", "Rejected" |
| Submission Date | Date | Convert to Date |
```

The rows above are documentation examples only. Emit empty templates unless the user explicitly requests examples. Money stays `currency`, dates stay `date`,
and anything pointing at another table stays `relation`.

## Field Reference

| # | Field | Type | SQL | JSON Schema | Notion | CSV example |
|---:|---|---|---|---|---|---|
| 1 | Expense Claim | `text` | `VARCHAR(255)` | `string` | Text | `EXP-2026-014` |
| 2 | Amount | `currency` | `NUMERIC(14,2)` | `number` | Number (format: currency) | `45000.00` |
| 3 | Tax Amount | `currency` | `NUMERIC(14,2)` | `number` | Number (format: currency) | `8100.00` |
| 4 | Approver | `text` | `VARCHAR(255)` | `string` | Text | `Sneha Iyer` |
| 5 | Approval Level | `select` | `VARCHAR(100)` | `string` | Select (add options after import) | `Manager` |
| 6 | Category | `select` | `VARCHAR(100)` | `string` | Select (add options after import) | `General` |
| 7 | Currency | `text` | `VARCHAR(255)` | `string` | Text | `INR` |
| 8 | Date of Expense | `date` | `DATE` | `string, format: date` | Date | `2026-01-15` |
| 9 | Department | `text` | `VARCHAR(255)` | `string` | Text | `Delivery` |
| 10 | Employee Name | `text` | `VARCHAR(255)` | `string` | Text | `Aarav Sharma` |
| 11 | Expense ID | `id` | `SERIAL PRIMARY KEY` | `integer` | Text (or Notion auto-ID) | `(blank)` |
| 12 | Notes | `long_text` | `TEXT` | `string` | Text | `February claims reconciled against the bank feed; two receipts were missing.` |
| 13 | Project/Cost Centre | `text` | `VARCHAR(255)` | `string` | Text | `CC-200 Website Redesign` |
| 14 | Budget Line | `text` | `VARCHAR(255)` | `string` | Text | `BL-114 Travel` |
| 15 | Receipt Attached | `checkbox` | `BOOLEAN` | `boolean` | Checkbox | `FALSE` |
| 16 | Reimbursement Date | `date` | `DATE` | `string, format: date` | Date | `2026-01-15` |
| 17 | Status | `select` | `VARCHAR(100)` | `string` | Select (add options after import) | `Approved` |
| 18 | Submission Date | `date` | `DATE` | `string, format: date` | Date | `2026-01-15` |

## Select Options

**Approval Level**

```
Manager | Finance | Owner | Auto Approved
```
**Category**

```
General | Operations | Finance | People | Compliance
```
**Status**

```
Draft | Submitted | Approved | Reimbursed | Rejected
```

## Relations

Link fields: none

## Examples

**Prompt**

```
Claims come on paper and nobody knows what was reimbursed.
```

**Context first** - one question per message, nothing already answered:

> **Q:** Approval limit?
> **A:** 5,000 per claim.
>
> **Q:** Receipt required?
> **A:** Always.
>
> **Q:** How do you track it?
> **A:** A paper register.

**Recommended next step** - offered, not built:

> Build a claim form that forces receipt and amount, then route by limit. Keep the finance reconciliation as a separate monthly step.
>
> Workflow: Claim submitted → Manager approval → Finance check → Reimbursement → Monthly reconciliation
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
- Does not pay anything or connect to a bank or accounting system.
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
I want to set up claims for my company.
Ask me one short question at a time, and only about what I have not already told you.
Then recommend the smallest setup that fits, and wait for me to ask before you build it.
When I ask, output CSV, SQL DDL, JSON Schema, a Notion property mapping or an Excel workbook. Data only.
```

