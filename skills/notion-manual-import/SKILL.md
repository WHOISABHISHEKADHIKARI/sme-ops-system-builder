---
name: notion-manual-import
description: "Notion Manual Import: CSV, property mapping and import steps for a database the user uploads themselves. Use when Notion is not connected or the user wants to import manually."
category: business
risk: safe
source: self
source_type: self
date_added: "2026-09-28"
author: WHOISABHISHEKADHIKARI
tags: [notion, csv, import, manual, operations, template, helper]
tools: []
table: none
---

# Notion Manual Import

**What it is:** the unconnected path into Notion - a CSV, a property mapping and the
click-path to import, for a user who will upload the database themselves.

## Overview

Prepares a database so the user can upload it into Notion by hand. It handles the
confirmed fields, the CSV, the Notion property mapping, select and status options, the
manual import steps, and the post-import verification.

It does not require a connected Notion workspace, and it never asks for one. This is a
helper: it defines no table of its own and renders whatever field list the active module
already confirmed, so its CSV and mapping are derived, never re-invented.

Layer: n/a. Fits: every stage. Table code: n/a - it renders the active module's table.

## When to Use This Skill

- upload this to Notion
- give me a Notion template
- I will upload it manually
- create a CSV for Notion
- give me Notion import instructions
- Notion is not connected
- make this Notion-ready
- show me how to create this database manually

Also use it when another skill produces a database structure but direct Notion creation is
unavailable, or when the user declines the connection prerequisite and asks for the manual
route instead.

Do not use it when the workspace is connected and the user wants the database built for
them. That is the module skill's own Notion build; this skill only formats the file.

## How It Works

Follow the [shared execution contract](../../references/execution-contract.md). The module-specific rules below define only domain fields, decisions, calculations, and safety constraints.

### Step 1 - Identify intent

Read the request and pick the intent before asking anything.

- "I will upload it myself", "Notion is not connected", "show me how" -> manual setup; go
  to Step 2.
- "just give me the CSV" -> import file only. Output: CSV alone.
- "I already have the CSV, what do I set" -> mapping only. Output: property mapping alone.
- "it imported but everything is Text" -> fix existing import. Output: correction
  instructions for the properties that are wrong, and nothing else unless asked.
- "Notion connected" -> the connection exists. Say so, hand back to the module skill, and
  stop. This skill is not the connected path and does not restate the prerequisite.

Never rebuild everything when a correction is what was asked for.

### Step 2 - Ask only what is missing

Skip anything the user already answered, in any earlier message, including answers given
to the module skill that owns the field list. Reuse the database name, the field names and
types, the select options, the statuses, the relations, the currency fields, the date
fields and the IDs. Never ask for information the user has already provided.

Ask one short question per message, and only when the answer changes the output:

> **Q:** Do you want an empty template or example rows?

If it does not materially change the requested output, do not ask, and default to no
example rows:

```yaml
example_rows: false
```

### Step 3 - Hold the internal context

Hold the answers in this shape. It stays internal - it is not shown to the user unless
they ask, and it never carries a value the user did not give.

```yaml
module: notion-manual-import
intent: null              # set in Step 1, one of: manual setup, import file, mapping, fix
source_module: null       # the module whose field list this renders
notion_connected: null    # true | false | unknown - never assumed either way
requested_outputs: []     # csv | mapping | instructions | verification
example_rows: false
confirmed_facts: []       # only what the user actually said
open_questions: []        # the unanswered ones, in the order worth asking
```

`source_module` is the only field this skill needs that a module skill does not have. If
it is unknown, ask which database to prepare, because a CSV without a confirmed field list
is a guess.

### Step 4 - Recommend the smallest workflow

Give a short recommendation, then ask whether to produce it. Do not build unprompted.

**Recommended approach:** One CSV with a header of the exact field names, one property
mapping table beside it, and the import click-path. Nothing else is needed to get a
working database.

**Why this one:** a CSV carries no types, so the import is the easy half and the property
configuration is the half that silently goes wrong. Doing the mapping up front is the
difference between a database that filters and one that is a wall of Text.

**Workflow:** Field list confirmed -> CSV exported -> Database created -> CSV imported ->
Properties converted -> Verified

Never force a connected integration and never force automation. If the user would rather
connect, that is the module skill's build, not this one.

### Step 5 - Build only on request

Once the user asks, emit only the pieces they requested, as data only. No preamble, no
summary, no closing line. Every column name comes from the source module's field list, in
the same order, in the CSV and in the mapping.

**This skill is the unconnected path.** It never emits the connection prerequisite from the
shared contract, and it never blocks a build on a connection. If the user asks to connect,
hand off to the module skill, which owns that step.

#### CSV

UTF-8, with a byte order mark so Excel opens the text correctly. The first row holds the
exact field names. Do not add fake records.

```csv
Field 1,Field 2,Field 3
```

Example rows only when the user explicitly asked for them, and then obviously fake.

#### Property mapping

CSV cannot preserve Notion property types, so the mapping is always emitted separately,
in this shape:

| CSV column | Notion property | After import |
|---|---|---|
| Name | Title | Set as database title |
| Description | Text | Leave as Text |
| Status | Select | Convert to Select |
| Due Date | Date | Convert to Date |
| Amount | Number | Set number format |
| Notes | Text | Leave as Text |

Use the actual confirmed fields, not this illustration.

#### Property type rules

| Canonical type | Notion property |
|---|---|
| id | Unique ID or Text |
| title | Title |
| text | Text |
| long_text | Text |
| number | Number |
| currency | Number with currency format |
| percentage | Number with percent format |
| date | Date |
| datetime | Date |
| checkbox | Checkbox |
| select | Select |
| multi_select | Multi-select |
| url | URL |
| email | Email |
| phone | Phone |
| person | Person |
| relation | Relation |
| files | Files |

Never map money to Text. Never map dates to Text unless the source explicitly requires
it. A currency format is a format choice, never a currency assumption: do not pick the
currency for the user.

#### Manual import steps

Give the shortest click-path that works. Notion's labels move between versions, so name
the action and say the label may differ rather than claiming a button exists.

1. Open Notion and open the page the database should live on.
2. Type `/database` and choose **Table - Full page** or **Table - Inline**.
3. Open **Settings & members** or the page menu, choose **Import**, choose **CSV**, and
   select the generated file.
4. Let Notion create the database from the header row.

#### Property configuration order

After import, tell the user to convert properties in this order, and only the ones that
exist:

```text
Title
→ Dates
→ Numbers
→ Currency
→ Select fields
→ Status fields
→ IDs
→ Relations
```

#### Select options

For every `select` or `multi_select` field, list only the confirmed options, as
suggestions the user adds after import. Do not invent statuses.

#### IDs

If the schema contains an ID field, recommend Notion's automatic Unique ID property with
the source module's prefix, and offer keeping the imported ID as Text as the alternative.
Never generate production IDs for real records unless requested.

#### Relations

A CSV import does not create a working relation. If a field is a relation:

1. import the base database first
2. import the related database
3. convert the field to Relation
4. select the target database
5. verify the linked records by hand

Never pretend a text column became a working relation automatically.

#### Calculations

Do not place business calculations inside the CSV unless explicitly requested. For a
value such as `Net Tax Payable`, `Days to Due`, `Balance`, `Variance` or `Total`, decide
first whether the source module defines it as an entered value, a formula, or something
computed elsewhere, and preserve that. Never invent a formula. If the parent skill says a
calculation belongs in accounting or tax software, that rule stands.

#### Output modes

| The user asks for | Emit |
|---|---|
| the CSV | the CSV alone |
| the mapping | the mapping alone |
| instructions | the shortest useful manual setup steps |
| everything | CSV, mapping, options, import steps, verification checklist |

#### Verification

After the import, ask the user to verify the database name, the field names, the property
types, the date and currency formatting, the select and status options, the ID setup and
the relations. The imported database is not verified until those match the source schema.

## Field Reference

This skill has no Field Reference of its own, and it must not grow one. The active
module's Field Reference is the single source: its CSV header, its SQL, its JSON Schema
and its Notion mapping are the four artifacts, and this skill reformats the same field
list for a manual import rather than defining a fifth.

If the source module's field list is not in front of you, read `skills/<slug>/SKILL.md`
for the module in play. If it is missing or ambiguous, ask which database to prepare and
stop - a header built from a guess imports as a wall of Text that the user then has to
fix by hand.

## Select Options

Option lists belong to the source module, not to this skill. Emit them as a starting set
to add after import, and never as a confirmed taxonomy. Where the user has supplied their
own values, the user's values win.

## Relations

Relations are configured after both databases exist, in the order above. In a manual
import the target database has to exist first, so a relation column arrives as Text and
is converted by hand. Say so rather than promising a working link.

## Examples

**Prompt**

```
Notion is not connected. I want to build my tax register myself - what do I do?
```

**Answered in one message, no intake needed** - the module and the route were both named:

```
Read skills/tax-register/SKILL.md for the field list, then emit the header-only CSV, the
property mapping and the import steps.
```

**Prompt**

```
I already imported my tax register but every column came in as Text.
```

**Mapping only** - correction instructions, no rebuild:

> Convert `Tax Period Start` and `Tax Period End` to Date, `Tax Collected on Sales`,
> `Tax Paid on Purchases`, `Withholding Tax Deducted`, `Withholding Tax Paid to Us` and
> `Net Tax Payable` to Number and set the currency format to the currency your business
> uses, `Status` and `Tax Type` to Select, and `Tax ID` to Unique ID with the prefix from
> the source schema. Leave `Tax Period`, `Tax Filing Reference` and `Notes` as Text.

**Documented shape** - a tax register field list, header-only CSV and mapping. The rows
below are documentation examples only. Emit empty templates unless the user explicitly
requests examples.

```csv
Tax Record,Tax Type,Tax Period,Tax Period Start,Tax Period End,Tax Collected on Sales,Tax Paid on Purchases,Withholding Tax Deducted,Withholding Tax Paid to Us,Net Tax Payable,Currency,Tax Filing Due Date,Filed Date,Payment Date,Tax Filing Reference,Prepared By,Reviewed By,Days to Due,Status,Notes,Tax ID
```

| CSV column | Notion property | After import |
|---|---|---|
| Tax Record | Title | Use as database title |
| Tax Type | Select | Add confirmed tax types |
| Tax Period | Text | Leave as Text |
| Tax Period Start | Date | Convert to Date |
| Tax Period End | Date | Convert to Date |
| Tax Collected on Sales | Number | Set currency format |
| Tax Paid on Purchases | Number | Set currency format |
| Withholding Tax Deducted | Number | Set currency format |
| Withholding Tax Paid to Us | Number | Set currency format |
| Net Tax Payable | Number | Set currency format |
| Currency | Text | Leave as Text |
| Tax Filing Due Date | Date | Convert to Date |
| Filed Date | Date | Convert to Date |
| Payment Date | Date | Convert to Date |
| Tax Filing Reference | Text | Leave as Text |
| Prepared By | Text | Leave as Text |
| Reviewed By | Text | Leave as Text |
| Days to Due | Number | Convert to Number |
| Status | Select | Add confirmed statuses |
| Notes | Text | Leave as Text |
| Tax ID | Unique ID | Prefer automatic ID |

## Best Practices

- One question per message, and only one that changes the output.
- Reuse everything already confirmed, including by the module skill that owns the list.
- Keep CSV and Notion field names identical, in the same order.
- Emit the mapping with the CSV every time; a header alone is not an import.
- Recommend the smallest useful solution and never force a connection or an automation.
- No sample records by default, and none that could be mistaken for real ones.
- Separate data storage from business calculations.
- Distinguish the properties Notion sets on import from the ones the user configures.

## Limitations

- It formats another module's schema. It never decides the schema, and it does not create
  the database.
- Everything here is text. Nothing is uploaded, created, converted or connected by this
  skill, and no claim of a completed Notion action may be made on its behalf.
- Property names in the Notion UI change between versions. The click-path is described by
  action, and the user verifies the label.
- Relations, rollups, formulas, permissions and sharing are configured by hand afterwards.
- Select options are a starting set, not the business's confirmed taxonomy.
- A currency format is not a currency. The user names the currency.
- Legal, tax and payroll review is still required before the imported database drives
  real decisions.

## Security & Safety Notes

Never request a Notion password, an authentication token, an API secret, a private
integration secret, or a pasted export of someone's whole workspace.

Never claim the CSV was uploaded, that a database was created, that properties were
changed, or that relations were connected, unless the action actually completed through
an authorized tool. This skill has no such tool, so the honest answer is always that the
user does it.

If the user pastes real employee, client or supplier records, generate the template
instead, and tell them to delete the pasted data from the conversation.

## Common Pitfalls

- **Problem:** every column imported as Text and the user assumes the import failed.
  **Solution:** that is normal. A CSV carries no types. Apply the property mapping once,
  after import, in the order above.
- **Problem:** dates or money behave as free text in the new database.
  **Solution:** convert those properties to Date and to Number with the format the user
  names. Never map money to Text.
- **Problem:** select options are missing, or invented.
  **Solution:** add only the options the confirmed schema defines, and let the user rename
  them to match how the business talks.
- **Problem:** the ID column is plain text, or IDs are generated for records that have
  none.
  **Solution:** convert to Unique ID with the source prefix where that fits, or keep the
  imported value as Text. Never mint production IDs.
- **Problem:** relation columns do not link.
  **Solution:** the target database has to exist first. Import both, then convert the
  column to Relation by hand and verify the links.
- **Problem:** the whole table was rebuilt when a conversion was all that was needed.
  **Solution:** emit only the corrections that were asked for.
- **Problem:** the user is told a Notion action happened.
  **Solution:** this skill only emits text. Say the user does the import and the
  configuration, and say which step they are on.

## Related Skills

- `sme-ops-system-builder` - routes to the module that owns the field list.
- `template-library` - where a reusable starting template belongs once one is proven.

## Reusable Prompt

```
I want to put [database] into Notion by hand, without connecting an integration.
Read the field list I already have and do not ask me for anything I have already told you.
Give me a CSV with a header of the exact field names, the Notion property mapping beside
it, the shortest import steps, and what to verify afterwards. No example rows unless I ask.
```
