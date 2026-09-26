---
name: promotion-upgrade-requests
description: "Promotion & Upgrade Requests: context-first intake, then CSV, SQL, JSON Schema and Notion on request. One short question per message. Use for promotion request."
category: business
risk: safe
source: self
source_type: self
date_added: "2026-09-26"
author: WHOISABHISHEKADHIKARI
tags: [sme, business, operations, database, csv, notion, sql, develop]
tools: [claude, cursor, gemini, antigravity]
---

# Promotion & Upgrade Requests

**What it is:** Promotion, grade upgrade, role change and salary revision requests.

## Overview

Works out the smallest useful **Promotion & Upgrade Requests** setup for the business in front of it, then
builds it only when asked. The default output is a short recommendation, not a
spreadsheet. Artifacts - CSV, SQL DDL, JSON Schema, Notion mapping - are produced on
request, from one field list so they cannot drift apart.

Layer: Layer 5: Develop. Fits: Growth stage. Table code: n/a.

## When to Use This Skill

- promotion request
- grade upgrade tracker
- salary revision request
- internal mobility tracker

Also use it when the user says "promotion, grade upgrade, role change and salary revision requests", or describes the same process happening in a
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

> **Q:** Who can request a promotion?

### Step 2 - Ask only what is missing

Skip anything the user already answered, in any earlier message. Ask the rest one at a
time, and stop as soon as the remaining answers would not change the output.

- **Requests** - Who requests? / How often? / Any grade or role change?
- **Criteria** - Fixed criteria? / Performance score needed? / Time in role?
- **Approval** - Who approves? / One or two levels? / Effective date set by?
- **Current process** - How do you handle it now? / Email or nothing? / What gets delayed?
- **Outcome** - What do you need? / A request form, approvals or a record?

Never invent an answer. If the user does not know, record it as unknown and carry on.

### Step 3 - Build the internal context

Hold the answers in this shape. It stays internal - it is not shown to the user unless
they ask, and it never carries a value the user did not give.

```yaml
module: promotion-upgrade-requests
intent: null            # set in Step 1, one of: set up, fix, review, report, import
scale: null             # Starter | Growth | Scale, only if the answer changes it
areas:
  "Requests": null
  "Criteria": null
  "Approval": null
  "Current process": null
  "Outcome": null
requested_outputs: []   # csv | sql | json | notion - only what was explicitly asked for
confirmed_facts: []     # only what the user actually said
open_questions: []      # the unanswered ones, in the order worth asking
```

### Step 4 - Recommend the smallest workflow

Give a short recommendation, then ask whether to build it. Do not build unprompted. Ask: "Want me to build the CSV, SQL DDL, JSON Schema, Notion mapping, or an Excel workbook from these confirmed rules?"

**Recommended approach:** Require a written request with evidence, route it by grade, and record the decision and effective date as one object.

**Why this one:** Promotion decisions drift when the request, the evidence and the decision live in different places. One record with a decision field fixes the trail.

**Workflow:** Request submitted → Criteria check → Approval → Decision → People and payroll update

### Step 5 - Build only on request

Once the user asks for it, derive the fields from the confirmed context and emit the
artifacts as data only. No preamble, no summary, no closing line.

An Excel workbook is the CSV emitted with a UTF-8 byte order mark, so Excel opens it with
correct text and no import dialog. A CSV carries no types, so after it, name the columns
that need a number, date or currency format applied.

```csv
Request Title,Employee Name,Department,Request Type,Current Job Title,Current Grade,Requested Job Title,Requested Grade,Requested By,Justification,Linked Performance Review,OKR Score,Behaviour Score,Courses Completed,Time in Role (Months),Criteria Met,Current Salary,Proposed Salary,Currency,Increase %,Approver,Decision,Effective Date,Status,Upgrade ID
Promotion to L3,Aarav Sharma,Delivery,Promotion,HR Executive,L2,Finance Analyst,L3,Rohit Verma,Consistent delivery over 12 months,REV-2026-Q1,0.7,4,"Advanced SQL, Workplace Safety",18,FALSE,1450000.00,1624000.00,INR,12,Sneha Iyer,Approved,2026-01-15,Under Review,
```

```sql
CREATE TABLE promotion_upgrade_requests (
  request_title VARCHAR(255),
  employee_name VARCHAR(255),
  department VARCHAR(255),
  request_type VARCHAR(100) NOT NULL,
  current_job_title VARCHAR(255),
  current_grade VARCHAR(255),
  requested_job_title VARCHAR(255),
  requested_grade VARCHAR(255),
  requested_by VARCHAR(255),
  justification VARCHAR(255),
  linked_performance_review VARCHAR(255),  -- relation -> target record
  okr_score NUMERIC NOT NULL,
  behaviour_score NUMERIC NOT NULL,
  courses_completed VARCHAR(255),
  time_in_role_months NUMERIC NOT NULL,
  criteria_met BOOLEAN NOT NULL,
  current_salary NUMERIC(14,2) NOT NULL,
  proposed_salary NUMERIC(14,2) NOT NULL,
  currency VARCHAR(255),
  increase NUMERIC NOT NULL,
  approver VARCHAR(255),
  decision VARCHAR(255),
  effective_date DATE NOT NULL,
  status VARCHAR(100) NOT NULL,
  upgrade_id SERIAL PRIMARY KEY,
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_promotion_upgrade_requests_status ON promotion_upgrade_requests (status);
```

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "Promotion & Upgrade Requests",
  "type": "object",
  "additionalProperties": false,
  "properties": {
      "Request Title": { "type": "string" },
      "Employee Name": { "type": "string" },
      "Department": { "type": "string" },
      "Request Type": { "type": "string" },
      "Current Job Title": { "type": "string" },
      "Current Grade": { "type": "string" },
      "Requested Job Title": { "type": "string" },
      "Requested Grade": { "type": "string" },
      "Requested By": { "type": "string" },
      "Justification": { "type": "string" },
      "Linked Performance Review": { "type": "string" },
      "OKR Score": { "type": "number" },
      "Behaviour Score": { "type": "number" },
      "Courses Completed": { "type": "string" },
      "Time in Role (Months)": { "type": "number" },
      "Criteria Met": { "type": "boolean" },
      "Current Salary": { "type": "number" },
      "Proposed Salary": { "type": "number" },
      "Currency": { "type": "string" },
      "Increase %": { "type": "number" },
      "Approver": { "type": "string" },
      "Decision": { "type": "string" },
      "Effective Date": { "type": "string", "format": "date" },
      "Status": { "type": "string" },
      "Upgrade ID": { "type": "integer" }
  },
  "required": [
      "Request Type",
      "OKR Score",
      "Behaviour Score",
      "Time in Role (Months)",
      "Current Salary",
      "Proposed Salary",
      "Increase %",
      "Effective Date",
      "Status"
  ]
}
```

```markdown
| CSV column | Notion property | Set after import |
|---|---|---|
| Request Title | Text | Leave as Text |
| Employee Name | Text | Leave as Text |
| Department | Text | Leave as Text |
| Request Type | Select (add options after import) | Convert to Select, add options: "Promotion", "Grade Upgrade", "Role Change", "Salary Revision" |
| Current Job Title | Text | Leave as Text |
| Current Grade | Text | Leave as Text |
| Requested Job Title | Text | Leave as Text |
| Requested Grade | Text | Leave as Text |
| Requested By | Text | Leave as Text |
| Justification | Text | Leave as Text |
| Linked Performance Review | Relation (link to the target database) | Convert to Relation, link to the target database |
| OKR Score | Number | Convert to Number |
| Behaviour Score | Number | Convert to Number |
| Courses Completed | Text | Leave as Text |
| Time in Role (Months) | Number | Convert to Number |
| Criteria Met | Checkbox | Convert to Checkbox |
| Current Salary | Number (format: currency) | Convert to Number, set format to Currency |
| Proposed Salary | Number (format: currency) | Convert to Number, set format to Currency |
| Currency | Text | Leave as Text |
| Increase % | Number | Convert to Number |
| Approver | Text | Leave as Text |
| Decision | Text | Leave as Text |
| Effective Date | Date | Convert to Date |
| Status | Select (add options after import) | Convert to Select, add options: "Submitted", "Under Review", "Approved", "Declined", "Implemented" |
| Upgrade ID | Text (or Notion auto-ID) | Delete the column and switch the primary column to auto-ID, or keep as Text |
```

One example row per artifact, visibly fake. Money stays `currency`, dates stay `date`,
and anything pointing at another table stays `relation`.

## Field Reference

| # | Field | Type | SQL | JSON Schema | Notion | CSV example |
|---:|---|---|---|---|---|---|
| 1 | Request Title | `text` | `VARCHAR(255)` | `string` | Text | `Promotion to L3` |
| 2 | Employee Name | `text` | `VARCHAR(255)` | `string` | Text | `Aarav Sharma` |
| 3 | Department | `text` | `VARCHAR(255)` | `string` | Text | `Delivery` |
| 4 | Request Type | `select` | `VARCHAR(100)` | `string` | Select (add options after import) | `Promotion` |
| 5 | Current Job Title | `text` | `VARCHAR(255)` | `string` | Text | `HR Executive` |
| 6 | Current Grade | `text` | `VARCHAR(255)` | `string` | Text | `L2` |
| 7 | Requested Job Title | `text` | `VARCHAR(255)` | `string` | Text | `Finance Analyst` |
| 8 | Requested Grade | `text` | `VARCHAR(255)` | `string` | Text | `L3` |
| 9 | Requested By | `text` | `VARCHAR(255)` | `string` | Text | `Rohit Verma` |
| 10 | Justification | `text` | `VARCHAR(255)` | `string` | Text | `Consistent delivery over 12 months` |
| 11 | Linked Performance Review | `relation` | `VARCHAR(255)` | `string` | Relation (link to the target database) | `REV-2026-Q1` |
| 12 | OKR Score | `number` | `NUMERIC` | `number` | Number | `0.7` |
| 13 | Behaviour Score | `number` | `NUMERIC` | `number` | Number | `4` |
| 14 | Courses Completed | `text` | `VARCHAR(255)` | `string` | Text | `Advanced SQL, Workplace Safety` |
| 15 | Time in Role (Months) | `number` | `NUMERIC` | `number` | Number | `18` |
| 16 | Criteria Met | `checkbox` | `BOOLEAN` | `boolean` | Checkbox | `FALSE` |
| 17 | Current Salary | `currency` | `NUMERIC(14,2)` | `number` | Number (format: currency) | `1450000.00` |
| 18 | Proposed Salary | `currency` | `NUMERIC(14,2)` | `number` | Number (format: currency) | `1624000.00` |
| 19 | Currency | `text` | `VARCHAR(255)` | `string` | Text | `INR` |
| 20 | Increase % | `number` | `NUMERIC` | `number` | Number | `12` |
| 21 | Approver | `text` | `VARCHAR(255)` | `string` | Text | `Sneha Iyer` |
| 22 | Decision | `text` | `VARCHAR(255)` | `string` | Text | `Approved` |
| 23 | Effective Date | `date` | `DATE` | `string, format: date` | Date | `2026-01-15` |
| 24 | Status | `select` | `VARCHAR(100)` | `string` | Select (add options after import) | `Under Review` |
| 25 | Upgrade ID | `id` | `SERIAL PRIMARY KEY` | `integer` | Text (or Notion auto-ID) | `(blank)` |

## Select Options

**Request Type**

```
Promotion | Grade Upgrade | Role Change | Salary Revision
```
**Status**

```
Submitted | Under Review | Approved | Declined | Implemented
```

## Relations

Link fields: `Linked Performance Review`

## Examples

**Prompt**

```
Promotions happen over email and the reasoning is lost.
```

**Context first** - one question per message, nothing already answered:

> **Q:** Who can request?
> **A:** Line managers.
>
> **Q:** Criteria?
> **A:** Performance and time in role.
>
> **Q:** How often?
> **A:** Twice a year.

**Recommended next step** - offered, not built:

> Require a written request with evidence, route it by grade, and record the decision and effective date as one object.
>
> Workflow: Request submitted → Criteria check → Approval → Decision → People and payroll update
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
- Does not decide promotions or change pay. It records and routes the request.
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
I want to set up promotion, grade upgrade, role change and salary revision requests for my company.
Ask me one short question at a time, and only about what I have not already told you.
Then recommend the smallest setup that fits, and wait for me to ask before you build it.
When I ask, output CSV, SQL DDL, JSON Schema, a Notion property mapping or an Excel workbook. Data only.
```

