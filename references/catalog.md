# Module Catalog

100 operational database skills. Each one identifies intent, asks only what is missing,
recommends the smallest workflow, and builds CSV + SQL DDL + JSON Schema + Notion
template only when asked.
Route from `sme-ops-system-builder`; do not load this file at runtime unless the user
asks what is available.

## Companion view: accounting & audit

The 16 modules of the accounting cycle were a sub-pack until 158fc1e flattened them into
the layers below, so they are listed here like every other module. What is left under
`skills/accounting-audit-system-builder/` is the router and its catalog, which order the
same 16 by cycle stage rather than by layer: route an accounting request from
`skills/accounting-audit-system-builder/SKILL.md` and read
`skills/accounting-audit-system-builder/catalog.md` for the stage-by-stage list. Where a
topic exists in both views, use the pack for the entry, the reconciliation or the audit
trail, and the layers here for the ongoing operational process.

## Helper

Four skills own no table and so are not in a layer or in the totals below. Each one
formats the field list of whichever module is active, in a different output format:

| Helper | Format | What it does | Skill |
|---|---|---|---|
| Notion Manual Import | CSV + Notion | The Notion step for every module: CSV, property mapping, import steps and verification, for a user who connects a workspace or uploads the database by hand. | `skills/notion-manual-import/SKILL.md` |
| Spreadsheet Manual Build | `.xlsx` / CSV | An empty, formatted workbook: one sheet, frozen and filtered header, number and date formats, and data validation on confirmed select fields. No rows unless asked. | `skills/spreadsheet-manual-build/SKILL.md` |
| CSV Manual Export | CSV | One UTF-8 file, exact headers in canonical order, no invented rows, and correct quoting for commas, quotes and line breaks. | `skills/csv-manual-export/SKILL.md` |
| JSON Schema Manual | JSON Schema 2020-12 | A validation contract: one property per confirmed field, `required` and `enum` only where confirmed, strictness only where the contract is closed. | `skills/json-schema-manual/SKILL.md` |

Reached through a module, not routed to: when a user selects a format, the module points
at the helper for it. A module still emits its own artifacts - DDL, DDL notes, integration
code, app views - and a helper never replaces them; the helper is the file form of the
same confirmed field list. None of them connects to anything, and none decides the schema.

## Layer 1: Foundation

Policy, org shape and who-can-see-what.

| Module | Code | Fits | Fields | Skill |
|---|---|---|---:|---|
| Access Matrix | - | Growth | 16 | `skills/access-matrix/SKILL.md` |
| Organization Design | - | Starter | 13 | `skills/organization-design/SKILL.md` |
| Policy Acknowledgement | - | Starter | 12 | `skills/policy-acknowledgement/SKILL.md` |
| Policy Library | - | Starter | 14 | `skills/policy-library/SKILL.md` |
| SOP & Company Wiki | - | Growth | 12 | `skills/sop-company-wiki/SKILL.md` |
| Accounting Software Selection | - | Growth | 57 | `skills/accounting-software-selection/SKILL.md` |

## Layer 2: Acquire

Finding and choosing candidates.

| Module | Code | Fits | Fields | Skill |
|---|---|---|---:|---|
| Candidate Talent Pool | - | Growth | 17 | `skills/candidate-talent-pool/SKILL.md` |
| Recruitment Pipeline | - | Growth | 21 | `skills/recruitment-pipeline/SKILL.md` |
| Salary Benchmarking | - | Scale | 13 | `skills/salary-benchmarking/SKILL.md` |

## Layer 3: Onboard

Getting a new person productive.

| Module | Code | Fits | Fields | Skill |
|---|---|---|---:|---|
| Asset & IT Management | - | Growth | 19 | `skills/asset-it-management/SKILL.md` |
| Buddy Program Manager | - | Scale | 12 | `skills/buddy-program-manager/SKILL.md` |
| Company Email & Accounts | - | Starter | 23 | `skills/company-email-accounts/SKILL.md` |
| Intern Program | - | Growth | 20 | `skills/intern-program/SKILL.md` |
| Offer & Appointment | - | Growth | 18 | `skills/offer-appointment/SKILL.md` |
| Onboarding Playbook | - | Growth | 9 | `skills/onboarding-playbook/SKILL.md` |
| People Directory | - | Starter | 28 | `skills/people-directory/SKILL.md` |
| Pre-boarding | - | Growth | 14 | `skills/pre-boarding/SKILL.md` |
| Probation Tracker | - | Growth | 19 | `skills/probation-tracker/SKILL.md` |

## Layer 4: Manage

Day-to-day people management and money in.

| Module | Code | Fits | Fields | Skill |
|---|---|---|---:|---|
| 360° Feedback System | - | Growth | 11 | `skills/360-feedback-system/SKILL.md` |
| Attendance | - | Starter | 15 | `skills/attendance/SKILL.md` |
| Capacity & Workload Planner | - | Scale | 12 | `skills/capacity-workload-planner/SKILL.md` |
| Disciplinary & PIP Tracker | - | Growth | 17 | `skills/disciplinary-pip-tracker/SKILL.md` |
| Expense Management | - | Starter | 18 | `skills/expense-management/SKILL.md` |
| Issue & Grievance Tracker | - | Starter | 19 | `skills/issue-grievance-tracker/SKILL.md` |
| KPI Tracker | - | Growth | 18 | `skills/kpi-tracker/SKILL.md` |
| Leave Management | - | Starter | 17 | `skills/leave-management/SKILL.md` |
| OKR System | - | Growth | 20 | `skills/okr-system/SKILL.md` |
| Payroll & Finance | - | Starter | 19 | `skills/payroll-finance/SKILL.md` |
| Performance Management | - | Growth | 22 | `skills/performance-management/SKILL.md` |
| Team Calendar | - | Growth | 13 | `skills/team-calendar/SKILL.md` |
| Time Tracking | - | Starter | 20 | `skills/time-tracking/SKILL.md` |
| Expense Accounting | - | Starter | 22 | `skills/expense-accounting/SKILL.md` |
| Salary & Wage Accounting | - | Growth | 27 | `skills/salary-wage-accounting/SKILL.md` |

## Layer 5: Develop

Skills, training and growth.

| Module | Code | Fits | Fields | Skill |
|---|---|---|---:|---|
| Competency Matrix | - | Scale | 9 | `skills/competency-matrix/SKILL.md` |
| Course & Upskilling Requests | - | Growth | 22 | `skills/course-upskilling-requests/SKILL.md` |
| Gamification Engine | - | Scale | 11 | `skills/gamification-engine/SKILL.md` |
| Knowledge Base | - | Scale | 12 | `skills/knowledge-base/SKILL.md` |
| Learning & Career Development | - | Growth | 19 | `skills/learning-career-development/SKILL.md` |
| Mentorship Program | - | Scale | 16 | `skills/mentorship-program/SKILL.md` |
| Promotion & Upgrade Requests | - | Growth | 25 | `skills/promotion-upgrade-requests/SKILL.md` |
| Recognition & Rewards | - | Growth | 14 | `skills/recognition-rewards/SKILL.md` |
| Skill Gap Analysis | - | Growth | 14 | `skills/skill-gap-analysis/SKILL.md` |

## Layer 6: Engage

Culture, voice and wellbeing.

| Module | Code | Fits | Fields | Skill |
|---|---|---|---:|---|
| Announcement Board | - | Starter | 13 | `skills/announcement-board/SKILL.md` |
| Culture & Retention | - | Growth | 18 | `skills/culture-retention/SKILL.md` |
| DEI Dashboard | - | Scale | 11 | `skills/dei-dashboard/SKILL.md` |
| Employee Suggestion Hub | - | Scale | 13 | `skills/employee-suggestion-hub/SKILL.md` |
| Events & Activities | - | Growth | 20 | `skills/events-activities/SKILL.md` |
| Health & Wellness | - | Scale | 13 | `skills/health-wellness/SKILL.md` |
| Internal Communication | - | Scale | 12 | `skills/internal-communication/SKILL.md` |

## Layer 7: Protect

Legal, tax, access and records.

| Module | Code | Fits | Fields | Skill |
|---|---|---|---:|---|
| Admin Access Register | - | Growth | 22 | `skills/admin-access-register/SKILL.md` |
| Audit Log | - | Scale | 11 | `skills/audit-log/SKILL.md` |
| Board & Governance | - | Growth | 16 | `skills/board-governance/SKILL.md` |
| Contract & Document Renewal | - | Growth | 16 | `skills/contract-document-renewal/SKILL.md` |
| Data Privacy Controls | - | Scale | 12 | `skills/data-privacy-controls/SKILL.md` |
| Document Management System | - | Growth | 13 | `skills/document-management-system/SKILL.md` |
| ESOP & Equity Tracker | - | Scale | 14 | `skills/esop-equity-tracker/SKILL.md` |
| Legal & Compliance Vault | - | Growth | 12 | `skills/legal-compliance-vault/SKILL.md` |
| Tax Register | - | Starter | 21 | `skills/tax-register/SKILL.md` |
| Template Library | - | Growth | 9 | `skills/template-library/SKILL.md` |
| Source Document & Filing | - | Growth | 22 | `skills/source-document-filing/SKILL.md` |
| TDS Booking & Payment | - | Starter | 25 | `skills/tds-booking-payment/SKILL.md` |
| Audit Preparation | - | Growth | 19 | `skills/audit-preparation/SKILL.md` |

## Layer 8: Operate

Clients, delivery and cash.

| Module | Code | Fits | Fields | Skill |
|---|---|---|---:|---|
| Budget & Cash Flow | - | Growth | 15 | `skills/budget-cash-flow/SKILL.md` |
| Clients & Accounts | - | Starter | 21 | `skills/clients-accounts/SKILL.md` |
| Invoices & Billing | - | Starter | 26 | `skills/invoices-billing/SKILL.md` |
| Payments Received | - | Starter | 13 | `skills/payments-received/SKILL.md` |
| Project-Based Performance | - | Scale | 14 | `skills/project-based-performance/SKILL.md` |
| Projects & Work Management | - | Starter | 22 | `skills/projects-work-management/SKILL.md` |
| Remote Work Tracker | - | Scale | 12 | `skills/remote-work-tracker/SKILL.md` |
| Vendor & Contractor Management | - | Scale | 14 | `skills/vendor-contractor-management/SKILL.md` |
| Purchase Accounting | - | Growth | 29 | `skills/purchase-accounting/SKILL.md` |
| Sales Accounting | - | Starter | 33 | `skills/sales-accounting/SKILL.md` |
| Receipt Accounting | - | Starter | 23 | `skills/receipt-accounting/SKILL.md` |
| Payment Accounting | - | Starter | 24 | `skills/payment-accounting/SKILL.md` |
| Petty Cash Management | - | Starter | 24 | `skills/petty-cash-management/SKILL.md` |
| Day Book | - | Starter | 31 | `skills/day-book/SKILL.md` |
| Party / Ledger Reconciliation | - | Growth | 27 | `skills/party-ledger-reconciliation/SKILL.md` |
| Inventory / Stock Reconciliation | - | Growth | 28 | `skills/inventory-stock-reconciliation/SKILL.md` |

## Layer 9: Analyze

Reporting, exports and reminders.

| Module | Code | Fits | Fields | Skill |
|---|---|---|---:|---|
| Advanced Analytics Dashboard | - | Scale | 11 | `skills/advanced-analytics-dashboard/SKILL.md` |
| Data Export Engine | - | Scale | 11 | `skills/data-export-engine/SKILL.md` |
| Notification & Reminder Hub | - | Growth | 12 | `skills/notification-reminder-hub/SKILL.md` |
| Reports & Analytics | - | Scale | 11 | `skills/reports-analytics/SKILL.md` |
| Stakeholder & Investor Reports | - | Scale | 10 | `skills/stakeholder-investor-reports/SKILL.md` |
| Monthly Closing & Statements | - | Growth | 32 | `skills/monthly-closing-statements/SKILL.md` |
| Debtor & Creditor Credit-Cycle Analysis | - | Growth | 33 | `skills/credit-cycle-analysis/SKILL.md` |

## Layer 10: Exit

Offboarding and alumni.

| Module | Code | Fits | Fields | Skill |
|---|---|---|---:|---|
| Alumni & Re-hire Tracker | - | Scale | 12 | `skills/alumni-re-hire-tracker/SKILL.md` |
| Offboarding & Exit | - | Growth | 18 | `skills/offboarding-exit/SKILL.md` |

## Totals

- Modules: 71
- Helpers: 4 (`notion-manual-import`, `spreadsheet-manual-build`, `csv-manual-export`,
  `json-schema-manual`; no table of their own)
- Fields: 1113
- Starter: 17
- Growth: 32
- Scale: 22

