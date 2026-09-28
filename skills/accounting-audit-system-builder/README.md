# Accounting & Audit System Builder

**Router for:** 16 accounting and audit modules
**Skill:** `SKILL.md`
**Catalog:** `catalog.md`
**Companion pack:** `../../` - 71 operational modules (`sme-ops-system-builder`)

## What it is

The accounting cycle, one module per stage: software selection, source documents,
purchase, sales, receipt, payment, petty cash, day book, ledger reconciliation, expense,
payroll, TDS, inventory, monthly closing, credit cycle, audit preparation.

## When to use it

- "Set up our accounting system"
- "We need books of accounts for the business"
- "Help us prepare for the auditor"
- "Our accountant asks for things every month"

## How it starts

Places the request on the cycle, then asks one question.

> **Q:** Where in the accounting cycle is the business right now?

- **Business** - What does the business do? / Trading, service or both? / Monthly
  transaction count?
- **Systems** - Which accounting software today? / Spreadsheets? / Internal or
  accountant does the entries?
- **Compliance** - Which taxes registered? / VAT or GST? / TDS, payroll obligations?
- **Position** - Anything outstanding or unreconciled? / Known differences?
- **Outcome** - Ongoing books, a month-end pack or an audit file?

## The cycle

```
Software selected
  -> Source document filed
    -> Transaction recorded (purchase | sales)
      -> Cash or bank movement recorded (receipt | payment)
        -> Cash counted and day book closed
          -> Ledgers, stock and statutory balances reconciled
            -> Month closed and statements produced
              -> Credit cycle analysed
                -> Audit file assembled
```

## Modules

| Layer | Module | Fits | Fields |
|---|---|---|---:|
| Foundation | Accounting Software Selection | Growth | 57 |
| Document | Source Document & Filing | Growth | 22 |
| Record | Purchase Accounting | Growth | 29 |
| Record | Sales Accounting | Starter | 33 |
| Record | Receipt Accounting | Starter | 23 |
| Record | Payment Accounting | Starter | 24 |
| Cash | Petty Cash Management | Starter | 24 |
| Cash | Day Book | Starter | 30 |
| Expense & Payroll | Expense Accounting | Starter | 22 |
| Expense & Payroll | Salary & Wage Accounting | Growth | 27 |
| Statutory | TDS Booking & Payment | Starter | 25 |
| Reconcile | Party / Ledger Reconciliation | Growth | 27 |
| Reconcile | Inventory / Stock Reconciliation | Growth | 28 |
| Close & Analyse | Monthly Closing & Statements | Growth | 32 |
| Close & Analyse | Debtor & Creditor Credit-Cycle Analysis | Growth | 24 |
| Audit | Audit Preparation | Growth | 19 |

Full index: `catalog.md`.

## Rules every module holds to

- A receipt is not sales income - it may be a receivable collection, advance, loan or
  capital.
- A payment voucher is not a universal substitute for a receipt note.
- Day-book debit/credit presentation follows the software's format, not a fixed rule.
- A missing invoice does not justify a "Kharche/Kharpai" document.
- Internal supporting documents are acceptable only where tax rules allow.
- TDS reconciles at least monthly. Physical cash counts are periodic by design.

## Owner and cadence

- Owner: whoever runs the accounting day to day.
- Cadence: the router runs per request; each module reviews its schema when the process
  changes, not on a fixed date.

## Troubleshooting

- The route is wrong - answer the stage question literally; the cycle order is the route.
- Two modules look equally right - pick the one that produces the evidence, the other
  usually depends on it.
- Notion columns show as Text - expected, apply the mapping table in the module skill.
