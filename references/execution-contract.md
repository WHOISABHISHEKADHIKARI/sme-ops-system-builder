# Shared Skill Execution Contract

Apply this contract to every router and module in this repository. Module-specific
instructions define domain logic; they do not weaken these rules.

## Request flow

1. Detect only the relevant intent: setup, review, fix, advice, build, convert, or export.
2. Extract confirmed facts using the user's terminology.
3. Identify the highest-value missing fact that would materially change the result.
4. Ask one short question only when that fact is required.
5. Repeat only while another answer would materially change the result.
6. For setup or consulting, recommend the smallest useful solution before building unless
   the user explicitly requested a build.
7. Build only the requested output, validate it, then stop.
8. If the requested output is Notion, run the connection gate below before the build.

Intent changes the response:

- **Setup:** recommend the smallest workable setup; build only when explicitly requested.
- **Review:** assess only the supplied material and report supported findings.
- **Fix:** correct confirmed defects within the requested scope, then validate the repair.
- **Advice:** answer directly; offer a build only when it would help.
- **Build:** create only the requested artifact from confirmed facts.
- **Convert:** preserve meaning and the canonical schema; leave unsupported values unresolved.
- **Export:** emit only the requested format and content.

## Facts and questions

- Never invent a fact. Keep unsupported values `Unknown`, blank, or optional as allowed by
  the requested format.
- `Unknown` is not `0`, `false`, `yes`, `no`, an empty date, or plausible example data.
- Preserve partial answers as partial. Do not infer the missing parts.
- Treat ambiguous answers as unresolved. Ask which explicit option the user means only when
  the distinction changes the result.
- Do not repeat a question already answered or recorded as unknown.
- Stop asking when remaining unknowns do not affect the recommendation, schema, validation,
  or requested output.

## Scope and neutrality

- Use the user's terminology unless a technical identifier requires normalization.
- Stay country-neutral and tool-neutral unless the user or module explicitly requires a
  jurisdiction or tool.
- Avoid unnecessary legal, standards, enterprise, framework, architecture, or compliance
  complexity.
- Keep roles separate. Never infer an approver, reviewer, owner, preparer, payer, recipient,
  or decision-maker from another role.
- Never request or expose secrets, tokens, passwords, private keys, banking details, or
  unnecessary personal data.

## Notion runs through `notion-manual-import`

A selected `notion` output is one workflow, and it lives in one file:
`skills/notion-manual-import/SKILL.md`. The module confirms the fields; the helper renders
them as the CSV, the property mapping, the import steps and the verification checklist. It
is not a fallback for the unconnected case - it is the Notion step for every module, so
there is one place where the mapping and the click-path can be right.

- When the user selects Notion, route that step to `notion-manual-import`. Do not restate
  the mapping inside the module and do not improvise the import steps; the helper renders
  the active module's Field Reference and the module says so at its own Step 5.
- A `notion` request is also the one output that cannot be produced as text alone:
  creating or updating a Notion database needs an authorized workspace connection. When
  the platform exposes a Notion connector, the connection comes before the build and the
  helper then builds in the workspace. This section is the single source of the
  prerequisite; the module repeats the rule, not the wording.
- Never claim a connection exists. Check whether the platform exposes a Notion connector;
  use it when it does.
- If it does not, emit the block below verbatim, once, as the prerequisite, before any
  Notion artifact, then stop and wait for the reply. Do not paraphrase it, drop a step,
  renumber it, or skip it because the user mentioned Notion in passing.
- It is a numbered instruction list, not a questionnaire, so it does not break the
  one-question-per-message rule. Do not append a second question to it.
- If the user replies `Notion connected.`, or says the equivalent, build in Notion and
  apply the module's property mapping.
- If the user declines or defers, the helper's manual route is already the plan: the CSV,
  the mapping, the import click-path and the verification checklist, with no connection
  asked for. Add one line saying the mapping is unverified until the workspace is
  connected. A static mapping is a real artifact and is never withheld.
- The mapping table on its own is never described as a connected or created database.
- Ask which Notion workspace to write to. Never choose a page, parent or database location
  for the user, and never open, share or move anything they did not name.
- Never ask for a Notion password, token, cookie, or internal integration secret. The
  connection is made by the user, in Notion's own UI.

Emit this prerequisite:

> **Notion needs a connected workspace before I can build this.** To enable automatic
> Notion setup (in ChatGPT: **Settings -> Apps / Connectors**; the label varies by
> assistant):
>
> 1. **Open the assistant's Settings.**
> 2. Go to **Apps / Connectors** (the exact label can vary).
> 3. Search for **Notion**.
> 4. Select **Connect**.
> 5. Sign in to your Notion account.
> 6. **Authorize the requested permissions** so the assistant can work with your Notion
>    workspace.
> 7. Select the **Notion workspace** you want to use.
> 8. Return to this chat and tell me **"Notion connected."**
> 9. I can then check what Notion actions are available and, if supported, set up this
>    module's database and its properties.

## A format on its own

Four skills own no field list. Each one takes the field list a module has already
confirmed and emits it in a single file format, and none of them connects to anything:

| Requested format | Skill | What it emits |
|---|---|---|
| Notion, unconnected | `notion-manual-import` | CSV, property mapping, import click-path, verification checklist |
| Excel or spreadsheet | `spreadsheet-manual-build` | An empty `.xlsx` workbook, or a UTF-8 CSV with a format note |
| CSV, import, staging, handoff | `csv-manual-export` | One UTF-8 file, exact headers in canonical order, no invented rows |
| JSON Schema or API contract | `json-schema-manual` | A draft 2020-12 object schema over the same field list |

- Use them when the user asks for a file in one of these formats, and hand off as soon as
  the format is named.
- A module still emits its own artifacts - DDL, DDL notes, integration code, app views.
  A helper never replaces them; it is the same confirmed field list in a file the user can
  open, fill and hand on.
- They take the field list as given. None of them decides, adds, or removes a field, and
  none of them has a Field Reference of its own: the active module's is the single source.
- Requiredness, options, and formats come from the field list. An unconfirmed rule stays
  out, and a rule invented in a file format rejects real data.
- Empty is the default. Example rows or example payloads are emitted only when the user
  asks for them, and then they are obviously fake.
- Output only the format requested. Do not add SQL, JSON, or a mapping beside a file the
  user asked to have on its own.
- They write text and files. Never claim a workbook was built in a system, a CSV was
  uploaded, a schema was published, or a file was imported anywhere.

## Data and workflow integrity

- The Field Reference is the canonical source for field names, order, types, requiredness,
  statuses, enums, calculations, and validation across every emitted format.
- Do not add a field, status, enum, formula, or default to one format only.
- State calculation inputs, conditions, rounding, and failure behavior explicitly.
- Keep statuses minimal and define transitions, blockers, completion gates, and exit states.
- A record must not be `Done` when a required check fails.
- Templates are empty unless the user requests examples. Documentation examples remain
  illustrative and must never be emitted as user data by default.
- Output only what the user requested.

## Final check

Before responding, silently check for contradictions, duplicate or circular rules, missing
exit conditions, hidden assumptions, irrelevant questions, inconsistent statuses,
conflicting calculations, country or tool assumptions, invented defaults, schema drift,
broken examples, and unnecessary complexity.
