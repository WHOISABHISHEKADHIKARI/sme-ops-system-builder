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
tools: [claude-code, codex-cli, cursor, gemini-cli]
---

# SME Ops System Builder

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

### Step 1 - Identify intent, then ask only what is missing

Read the request first. If the user already named a module, skip to Step 2.

Ask one question per message, and only the ones still unanswered:

> **Q:** What does the business do?

Never batch two questions into one message, and ask at most four in total. Stop as soon as
the remaining answers would not change the route.

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
Set up HR systems for my company
```

```
> **Q:** What does the business do?
```

**User**

```
A 14 person consultancy. We have nothing in place yet.
```

**Recommended**

```
people-directory    -> skills/people-directory/SKILL.md    every module links to it
leave-management    -> skills/leave-management/SKILL.md    14 people means leave gets requested
onboarding-playbook -> skills/onboarding-playbook/SKILL.md  nothing in place, so start with joiners
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
- Generated modules carry fictional example rows, never real records. Real data is the
  user to enter.
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

## Reusable Prompt

```
I run a [size] [industry] business. Help me set up operational trackers.
Ask me up to 4 short questions, one at a time, and only about what I have not said.
Then recommend the 2 or 3 modules that fit, and wait for me to pick before building.
```
