---
name: sme-ops-system-builder
description: "Route SME operations, tracker, and Notion-system requests to two or three relevant modules. Use when a business needs help choosing what to track."
category: business
risk: safe
source: self
source_type: self
date_added: "2026-09-26"
author: WHOISABHISHEKADHIKARI
tags: [sme, business-operations, hr, finance, database, notion, csv, sql, router]
tools: []
---

# SME Ops System Builder

**What it is:** Picks the two or three operational modules a small business should run.

Router for 71 operational skills covering people, hiring, leave, finance, projects,
governance, analytics, and exit. It identifies the smallest useful shortlist and hands
the selected workflow to its module skill. It never builds artifacts itself.

## Overview

A business does not need 71 databases. It needs the two or three it will actually keep
current. This skill identifies the intent, asks only what is still missing one question at
a time, stops as soon as the answers stop changing the route, then recommends two or
three modules and waits for the user to pick.

Each module skill then runs the same contract: context first, a recommendation, and
artifacts only on request. This skill never emits a schema, a CSV or a Notion template.

## When to Use This Skill

- Use when the user asks to set up systems for a company.
- Use when the user asks what a small business should track.
- Use when the user names two or more operational needs and needs the matching modules.
- Use when the user wants to turn an operational spreadsheet into a maintained system.

Do not use it when the user has already named one specific tracker and just wants the
file - go straight to that module skill.

## How It Works

Follow the [shared execution contract](references/execution-contract.md). The module-specific rules below define only domain fields, decisions, calculations, and safety constraints.

### Step 1 - Identify intent, then ask only what is missing

Read the request first. If the user already named a module, skip to Step 2.

Ask one question per message, and only the ones still unanswered:

- Ask what the business does when its activity is the highest-value missing routing fact.
- Ask which operational need or workflow to track when the business activity is known or
  would not narrow the route as much as the missing need.

Never batch two questions into one message, and ask at most four in total. Stop as soon as
the remaining answers would not change the route.

If an answer is ambiguous, keep the route unresolved and clarify only one routing
dimension at a time. Ask the highest-value explicit choice first; never ask for both the
business type and the operational need in the same message.

### Step 2 - Recommend two or three modules

Match on what the user named, not on what the tier allows. Tier only widens the shortlist,
it never blocks a request.

**Starter** - 17 modules, the usual starting set:

- Organization Design, Policy Acknowledgement, Policy Library, Company Email & Accounts, People Directory, Attendance
- Expense Management, Issue & Grievance Tracker, Leave Management, Payroll & Finance, Time Tracking, Announcement Board
- Tax Register, Clients & Accounts, Invoices & Billing, Payments Received, Projects & Work Management

**Growth** - Starter plus more, once headcount or volume justifies it.

**Scale** - all 71, once the business runs on them rather than around them.

Present the shortlist, say why each one fits in a single line, and ask which to start.
A list of 71 is not a recommendation. Full index: `references/catalog.md`.

### Step 3 - Hand off

Read `skills/<slug>/SKILL.md` for the module the user picks and let that file run its own
intake from there. This skill stops at the shortlist: it does not answer the module's
questions, build its fields, or run a second module in the same conversation. Never merge
two modules into one questionnaire.

If a listed path is missing, stop and report the missing module instead of guessing a
replacement. If no catalog entry clearly matches, say so and ask one question that
distinguishes the closest candidates.

### Step 4 - Output

One line per module in the shortlist: the slug and the path to its skill. That line list is
the whole data output. No schemas, no CSV, no field lists.

A one-line reason per module and a closing question are framing, not output, and are
allowed. Anything that describes a table belongs to the module skill, not to this file.

## Examples

**Prompt**

```
I run a 12 person design studio. Need a leave tracker and something for invoices.
```

**Answered in one message, no intake needed** - both modules were named:

```
leave-management -> skills/leave-management/SKILL.md
invoices-billing  -> skills/invoices-billing/SKILL.md
```

**Prompt**

```
I run a 14 person consultancy and we have nothing in place yet. Set up HR systems.
```

The business activity is already known, so the highest-value missing routing fact is
the need itself, asked as an explicit choice:

```
> **Q:** Which HR process do you want tracked first: **leave requests**, **who is owed
> what at period end**, or **joiners and leavers**?
```

**User**

```
Leave requests first.
```

**Recommended**

```
people-directory    -> skills/people-directory/SKILL.md    every module links to it
leave-management    -> skills/leave-management/SKILL.md    the need they named
onboarding-playbook -> skills/onboarding-playbook/SKILL.md  nothing in place, so joiners come next
```

**Which one should we start with?**

## Best Practices

- Batched questions read as a form and get answered badly. One question, then wait.
- Recommend at most three modules, each with a one-line reason.
- Route on what the user named, not on what the tier allows.
- Keep each module intake separate - do not merge them into one questionnaire.
- Let the module skill own its schema. Never restate a field list here.

## Limitations

- Routing only. It does not build, compare or merge schemas.
- It cannot judge local compliance. Leave, tax and payroll rules vary by country.
- Tier is a hint, not a gate. A 3 person company may genuinely need the ESOP tracker.
- 71 near-identical skills is a lot of catalog surface. Prefer this router over reading
  all module files.

## Security & Safety Notes

- Ask for headcount and function only. Never ask for names, salaries or client data.
- This skill runs no commands, calls no APIs, and writes no files.
- Documentation examples use fictional rows, never real records. Emitted templates
  stay empty unless the user requests examples; real data is the user to enter.
- Modules touching privacy, legal, payroll or disciplinary matters carry an explicit
  human-review requirement in their own skill file.

## Common Pitfalls

- **Problem:** it recommends a module the user never asked about, with no reason given.
  **Solution:** every recommended module carries a one-line reason tied to what the user
  said, and anything ungrounded is offered as a question rather than a finding.
- **Problem:** it treats an unstated answer as fact.
  **Solution:** record it as unknown and keep going; never fill a gap with a guess.
- **Problem:** a module gets generated with real employee names in it.
  **Solution:** placeholders only - `name@example.com`, `2026-01-15`.

## Related Skills

- `@people-directory` - the employee master record most modules link to.
- `@clients-accounts` - the customer record invoicing and payments link to.
- `@notification-reminder-hub` - turns due dates across modules into reminders.

### Sub-packs

These are routers of their own, not modules. Route to them when the question is outside
the operational process, and read the pack's own catalog rather than loading all of it.

- `accounting-audit-system-builder` - 16 modules, one per stage of the accounting cycle.
  Use for the entry, the reconciliation and the audit trail. Where a topic exists in both
  places, this pack owns the cycle and the flat modules own the ongoing process.
- `brand-growth-system-builder` - 13 modules covering how the business looks and how it is
  found: design tokens, the mark and its rights, print collateral, the page register, the
  Business Profile, citations, email, decks and social. It routes on three jobs -
  consistent, findable, credible - and orders upstream first, because tokens and the mark
  are inherited by everything downstream.

## Reusable Prompt

```
I run a [size] [industry] business. Help me set up operational trackers.
Ask me up to 4 short questions, one at a time, and only about what I have not said.
Then recommend the 2 or 3 modules that fit, and wait for me to pick before building.
```
