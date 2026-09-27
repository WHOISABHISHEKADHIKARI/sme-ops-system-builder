# QA Fix Contract

Binding rewrite rules for every module SKILL.md in this repository. Derived from the
`SKILL TABLE QA` review of the Accounting & Audit pack. A module that violates any rule
here is a defect, regardless of how good the rest of the file reads.

## 1. Intake must be decision-relevant

- One short question per message. Never batch.
- Never open with a generic question that does not change the output. `What is your
  biggest expense category this month?` is banned. The first question targets the most
  important *missing* fact that affects the requested output.
- Skip anything the user already supplied, in any earlier message.
- Stop as soon as the remaining unknowns would not change the recommendation or the
  requested artifact.
- Record `Unknown` and move on when the user does not know. Never re-ask the same
  unknown.

## 2. Ambiguous answers are not answers

`yes`, `no`, `maybe`, `same`, `okay`, `fine` are **not** an answer to a
multiple-choice question. Re-ask as an explicit choice:

> **Q:** Which do you mean: **full count of all items** or **cycle count of selected
> items**?

Partial answers keep only the answered part. `20 to 50` to "how many items, and when did
you last count?" records the count range and leaves the date `Unknown`.

## 3. Never invent a business fact

Never supply, assume or imply: names, addresses, phone numbers, dates, amounts,
quantities, invoice numbers, PAN/VAT/TAN numbers, bank details, tax rates, tax
treatment, account numbers, currencies, credit limits, benchmarks, scores, approval
names, roles, document types, categories, department names, percentages, or any other
business value.

If it is not supplied by the user or derived by a documented formula from supplied data,
it is `Unknown`, blank, or optional. **Never turn `Unknown` into `0`.**

## 4. Registration is not capability

Being VAT-registered does not tell you the rate, whether the expense is taxable, whether
input tax is recoverable, or whether the amount is tax-inclusive. Being TDS-registered
does not tell you the section or the rate. Do not assume any of it.

## 5. Scope discipline - no field creep

- Expense-only request: no `Payment Mode`, `Payment Date`, `Payment Reference`,
  `Net Payable`, `TDS Rate %`, `TDS Amount`, `Department` unless the user asked for
  payment/withholding/department tracking.
- TDS unused: TDS fields are absent from the minimum schema, not optional-but-present.
- Do not add `Bank`, `Cheque No` or `Payee PAN` because a similar module has them.
- Add a field only when a confirmed requirement justifies it. Say why in the SKILL.md.

## 6. One canonical field list, four artifacts

The Field Reference table is the single source. CSV header, SQL DDL, JSON Schema
properties and Notion mapping are all derived from it. Rules:

- Identical field names, spelling and order in all four.
- A field present in one artifact must be present in all four.
- `required` in JSON Schema is derived from business necessity, not from user data
  availability. A calculated value is never required when its source may legitimately be
  missing.
- Technical metadata (`created_at`, `updated_at`, primary key) is labelled as technical
  and is not a business field. It is the only permitted artifact-only addition.
- No artifact silently introduces a business field absent from the Field Reference.

## 7. Portable SQL unless the engine is known

- `DATE`, `NUMERIC`, `NUMERIC(14,2)`, `VARCHAR(n)`, `TEXT`, `BOOLEAN`, `TIMESTAMP`.
- `SERIAL PRIMARY KEY` only when the engine is known; otherwise a portable
  `id <type> PRIMARY KEY` plus a note. State the engine assumption in one line.
- Enforce `CHECK` where cheap: `period_start <= period_end`, non-negative money,
  controlled values via `CHECK (col IN (...))`.
- Index the field the module filters and reports on, and the status field.
- No `FOREIGN KEY` unless the target table is defined in the same artifact set.

## 8. Relations are real or they are text

Use `relation` only when the field genuinely points at another record in this pack. In
SQL a relation is `VARCHAR(255)` with a comment. In Notion it becomes `Relation` **only**
when the target database exists or is explicitly created by the same build. Otherwise
it is `Text` with a note naming the intended target. Never invent a database.

## 9. Example data must be unmistakably fake

Use:

```
EXP-EXAMPLE-001 | Example Supplier | PAN-EXAMPLE-001 | VAT-EXAMPLE-001
INV-EXAMPLE-001 | DOC-EXAMPLE-001 | PAY-EXAMPLE-001 | 2026-01-15
Example Reviewer | Example Customer | 1,000.00
```

Banned: real-looking person names, real company names, real tax identifiers that could
pass a format check, realistic invoice or reference numbers, real amounts.

## 10. Controlled values are defaults, never confirmed facts

Every `Select` option list is introduced as a starting set. The Notion column always
says **add options after import** and lists them as suggestions, not as the business's
confirmed taxonomy. If the user supplied their own values, the user's values win.

Percentages: state the representation once (`97` for 97%, not `0.97`) and never mix
conventions. Money is numeric with no currency symbol in the cell. Dates are ISO
`YYYY-MM-DD` in real date fields.

## 11. Money semantics must be explicit

- State whether an amount is tax-inclusive or tax-exclusive, or add separate
  `Amount Before Tax` / `Tax Amount` / `Gross Amount` fields.
- Never silently assume `Net Payable = Amount + Tax - TDS`. If the formula is not stated
  and defined, do not use the field.
- `Debit` / `Credit` presentation is software-dependent. Keep it descriptive
  (`Receipt` / `Payment`, `Dr` / `Cr` marked software-dependent) and never hardcode
  "all receipts are debit".
- Round once, at the end, and say so.

## 12. Reconciliation and control rules belong in the module

Wherever a record can be checked, state the check and the status values:

```
Closing = Opening + Movement - Counter-movement +/- Adjustments
Reconciliation Status: Reconciled | Needs Review | Unreconciled | Unknown
Data Quality Status:    Complete | Incomplete | Needs Review | Blocked
Status:                 Not started | In progress | Blocked | Done | Cancelled
```

A record must not be `Done` when a required check fails. Never silently correct a
difference to force a tie-out - record it and mark it.

## 13. Keep separate things separate

Wherever a module conflates two concepts, split them:

| Conflated | Split into |
|---|---|
| Receipt vs income | `Receipt Type` + a separate sales income record |
| Contractual terms vs actual behaviour | `Contractual Terms Days` vs `Actual ... Days` |
| Benchmark vs target vs actual | three fields, three sources |
| Aging bucket on a party row | bucket amounts on the summary, buckets on the invoice detail |
| Counting vs verifying vs approving | three separate role fields |
| Warranty claim vs goodwill claim | `Claim Type` |
| Depreciation method vs useful life vs residual | three fields |
| Provision raised vs provision used | `Provision Raised`, `Provision Used` |
| Selection status vs selection decision | `Evaluation Status` + `Selection Decision` + `Rejection Reason` |
| Prepared by vs reviewed by vs approved by | three fields |
| Movement rows vs day-end control rows | a `Row Type` discriminator, or an explicit separate control table |

## 14. Never decide for the user

Selection, sign-off, approval, filing, and legal or tax conclusions stay with a human.
The module may summarise evidence and state a deal-breaker; it must not announce a
winner, a compliance verdict, or a filing outcome.

## 15. House structure every SKILL.md must keep

YAML frontmatter with `name`, `description`, `category`, `risk`, `source`,
`source_type`, `date_added`, `author`, `tags`, `tools`. Then, in order:

```
# <Module Name>
**What it is:** <one line>
## Overview
## When to Use This Skill
## How It Works
  ### Step 1 - Identify intent
  ### Step 2 - Ask only what is missing
  ### Step 3 - Hold the internal context
  ### Step 4 - Recommend the smallest workflow
  ### Step 5 - Build only on request
## Field Reference
## Select Options
## Relations
## Examples
## Best Practices
## Limitations
## Security & Safety Notes
## Common Pitfalls
## Related Skills
## Reusable Prompt
```

Step 5 shows the four artifacts for a *documented shape*, not necessarily the final
output: the CSV is a header plus one clearly labelled illustrative row, SQL is DDL only,
JSON Schema is a schema, and the Notion block is a mapping table. The skill's contract
is still "output only what was asked for, and never invent values".

## 16. Internal context block

```yaml
module: <slug>
intent: null            # set up | fix | review | report | import
scale: null             # Starter | Growth | Scale, only when the answer changes it
areas:
  "<Area>": null
requested_outputs: []   # csv | sql | json | notion - only what was explicitly asked
confirmed_facts: []     # only what the user actually said
unknowns: []            # asked and not answered
open_questions: []      # the unanswered ones, in the order worth asking
```

Internal only. Never shown unless requested. Never carries an invented value.

## 17. Self-check before a file is considered done

1. First question changes the output.
2. No generic opening question.
3. Ambiguous-answer rule stated.
4. No invented business value anywhere, including the example row.
5. Example identifiers use the `-EXAMPLE-` pattern.
6. No assumed tax rate, tax treatment, or accounting treatment.
7. Scope respected: no unrequested payment / TDS / department fields.
8. Same field names, same order, in all four artifacts.
9. JSON `required` justified field by field.
10. SQL types portable or the engine named.
11. Relations are text unless the target exists.
12. Select options labelled as defaults with "add options after import".
13. Money basis stated; percentages representation stated once.
14. Reconciliation / control rules and status values present where checkable.
15. Conflations from rule 13 split.
16. No module-level recommendation, verdict or sign-off.
17. Human review required for legal, tax, payroll, disciplinary and audit matters.
18. Limitations section states what the module does not do.
