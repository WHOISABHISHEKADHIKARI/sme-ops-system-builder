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
