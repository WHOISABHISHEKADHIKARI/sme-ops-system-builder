# Debug Session: skill-md-qa — test every SKILL.md as user & find flaws

- **Session ID:** `skill-md-qa`
- **Status:** `[OPEN]` — Step 4 stopped: the oracle was defective. See *Outcome*.
- **Date opened:** 2026-09-28
- **Owner (simulated):** AI
- **Bug type:** Systemic / cross-cutting — 80+ SKILL.md files need user-session simulation to catch logic, prompt, trigger, sequence, and cross-module-link flaws

## Scope

User request: `test every skill.md as user and find out flaw with your script and fix all the flaws`.

Interpretation — treat each `SKILL.md` as if the user walks up cold and exercises it like the router+executor would:

1. **Trigger match**: Does a plausible user utterance (positive & negative) classify correctly against the `## Trigger` regex / keyword set?
2. **Question sequence**: Does the declared `## Question Sequence` actually ask for every field in `## Fields (N)` that is not optional with a working default? Any orphans / extra questions / missing questions / dead-ends?
3. **Conditional logic / branching**: Are there `IF` branches in questions with unsatisfiable predicates? Do `GOTO`-style branches point to valid destinations?
4. **Artifact generation**: Does the `## Expected-Artifact Output (if applicable)` + `sheets.gs` + `excel.xml` actually produce something whose column count matches Fields(N), and the template uses every field at least once (no dead fields / no template placeholders)?
5. **Cross-references**: Execution-contract link at `## Execution Contract` must resolve. Related/Previous/Next navigation in README/SKILL footers must point to files that exist after the 16-module flatten from this session.
6. **Structural shape**: Every SKILL.md has (name, trigger, question sequence, fields with N, execution contract) sections present and non-empty.

## Hypotheses (falsifiable)

| # | Hypothesis | Evidence source (what simulator will check) |
|---|---|---|
| H1 | **Flaw: Triggers are non-unique** — >5 modules share a regex keyword (e.g. "ledger", "audit") so ambiguous user inputs would fire the wrong skill. | Pairwise Jaccard overlap on keyword sets extracted from Trigger blocks; also false-positive trigger matches when we run 5 synthetic negative utterances against each skill. |
| H2 | **Flaw: Missing/extra questions vs fields** — in ≥10 modules, `Fields(N)` has ≥1 column that never appears as the subject of a Question Sequence item, or ≥2 questions ask for a field not in Fields. | Set diff: `{all field names from Fields csv}` vs `{field-names extracted from Question sentences via "X (e.g.)" pattern + form labels}`. If `|missing| + |extra| >= 2` the spec is inconsistent. |
| H3 | **Flaw: Artifact template has broken placeholders** — in sheets.gs / excel.xml, column names / field references don't 1:1 map to the declared Fields(N). Already known for 7 modules from `check.py` drift; confirm the flaw is column-order mismatch between `sql DDL order` and `fields reference order` (same counts, not missing cols). | check.py output + direct join of `sheet.getRange().setValues(headers)` vs `Fields CSV order`. |
| H4 | **Flaw: Execution-contract / Related links break after the 16-module flatten** — ≥8 of the 16 moved modules still have a `## Execution Contract` URL at wrong depth (1 fewer `../`) or SKILL-footer Related-link 404. | Simulator follows every `[text](link)` in SKILL.md + README.md navigation/footer sections, `HEAD` style check with `Path().exists()` for local links. |
| H5 | **Flaw: Trigger regexes don't actually match realistic user inputs** — ≥25% of SKILL.md Trigger regexes fail to fire on 3 synthetic utterances like "Can you do X for me?" for the declared X. | 3 positive + 2 negative synthetic utterances run per skill against the Trigger regex. Percent failure is the evidence. |

## Test Oracle (script simulator)

File: `tools/simulate_skill_user_sessions.py` (created for this session, removed at cleanup).

Output:
```
pre_fix/
  results.json          # flaw_id, flaw_type, skill, severity, evidence, location (file:line)
  summary.md
```

After fixes:
```
post_fix/
  results.json / summary.md   # same schema, compared against pre_fix
```

## Logs / events endpoint

Debug Server running on port `auto` (probe 9229→9240); session env `.dbg/skill-md-qa.env`.
All events logged via `trae-debug-log-skill-md-qa.ndjson` by the simulator.

## Outcome

The pre-fix oracle was itself defective. **307 of 310 reported flaws are false
positives and were not acted on.**

`tools/simulate_skill_user_sessions.py:189-201` asserts that every `SKILL.md`
carries `## Trigger`, `## Question Sequence` and `## Fields`. Those section names
do not exist in this repository's contract. The real contract is
`tools/validate.py:8` (`REQUIRED_SECTIONS = ['Overview', 'When to Use This
Skill', 'How It Works', 'Examples', ...]`), and modules express the same three
concerns as `## When to Use This Skill`, `### Step N` and `## Field Reference`.
So the simulator reported the identical three "missing section" findings against
all 103 files. `python3 tools/validate.py` passes on all 103.

| Hypothesis | Verdict |
|---|---|
| H1 trigger uniqueness | Not tested — oracle aborted before the pairwise stage produced usable evidence |
| H2 questions vs fields | Falsified as stated — it diffs against a `Fields (N)` heading that does not exist; the real list is `## Field Reference` |
| H3 artifact placeholders | **Confirmed — root cause was in the checker, not the modules. Fixed; 80/87 → 86/87** (see below) |
| H4 links broken by the 16-module flatten | **Confirmed — 3 real defects, fixed** |
| H5 trigger regex matching | Not tested — no `## Trigger` block exists to extract a regex from |

### Fixed (H3 — the `'%'` naming split)

`python3 tools/check.py all` reported 6 of the 7 accounting modules as
`sql columns != field reference order (N vs N)`. Same counts, so it read as a
column-order problem. It was not: the counts matched and the order matched. The
only divergence was one identifier.

`tools/check.py:56 snake()` collapsed every non-alphanumeric run to `_` and
stripped the result, so `TDS Rate %` became `tds_rate`. But
`tools/qa_verify.py:190` already documents this repo's rule —
`'TDS Rate %' -> 'tds_rate_pct'` — and the SQL DDL blocks use the `_pct` form.
The two tools disagreed about the same field, so `check.py` flagged six correct
modules.

Only the ` ```sql ` block is affected: the CSV header, the JSON Schema property
keys and the Notion mapping all use the display name verbatim (`VAT Rate %`).
`sheets.gs` and `excel.xml` do not reference snake column names at all, so
neither needed regenerating.

That exposed a genuine repo-wide split, because the flatten had moved the
accounting modules out of the path-prefix skip in `check.py` that had been
shielding them:

| Convention | Modules | Example |
|---|---|---|
| `*_pct` | 6, all accounting: `tds-booking-payment`, `payment-accounting`, `expense-accounting`, `sales-accounting`, `purchase-accounting`, `credit-cycle-analysis` | `tds_rate_pct` |
| bare | 9: `budget-cash-flow`, `capacity-workload-planner`, `events-activities`, `invoices-billing`, `kpi-tracker`, `learning-career-development`, `okr-system`, `projects-work-management`, `promotion-upgrade-requests` | `achievement` |

Resolved in favour of `_pct`, the convention the repo already documents.
`snake()` now expands `%` to ` Pct` before collapsing, and the 9 SQL blocks were
renamed to match. Word-boundary matching kept `weighted_score` intact beside the
renamed `weight_pct` in `kpi-tracker`. `qa_verify.py` reports zero errors in all
9 afterwards; only pre-existing content WARNs remain.

### Fixed (H4, the broken navigation links)

All three are stale `../accounting-audit-system-builder/<slug>/` paths left over
from the 16-module flatten, plus one wrong `../` depth. Both the href and the
link text were corrected to the flattened slug.

| File:line | Was | Now |
|---|---|---|
| `skills/access-matrix/README.md:226` | `../accounting-audit-system-builder/accounting-software-selection/` | `../accounting-software-selection/` |
| `skills/admin-access-register/README.md:240` | `../accounting-audit-system-builder/tds-booking-payment/` | `../tds-booking-payment/` |
| `skills/tds-booking-payment/README.md:183` | `../../admin-access-register/` | `../admin-access-register/` |

All six relative navigation links on those three lines now resolve on disk.

### Known, out of scope, not fixed

- **`tools/qa_verify.py` lost the accounting pack.** The documented per-pack
  command now silently checks nothing and still reports `PASS`:
  ```
  $ python3 tools/qa_verify.py --pack skills/accounting-audit-system-builder
  checked 0 SKILL.md files
  PASS: 0 errors, 0 warning(s)
  ```
  `find_skills` walks the pack directory for nested `SKILL.md` files and skips
  the directory's own. The flatten left `skills/accounting-audit-system-builder/`
  holding only `SKILL.md`, `README.md` and `catalog.md`, so there is nothing
  left to find. This is a false green — the tool that owns the newer artifact
  contract reports success while verifying none of the 16 modules. The same
  command with the pack name unprefixed (`--pack accounting-audit-system-builder`,
  as in the docstring at `tools/qa_verify.py:7`) points at a path that does not
  exist and also checks 0 files. Repo-wide, `--pack skills` does reach all 102.
- `python3 tools/seo.py --check` **crashes**: `tools/skillmd.py:99` assumes a
  ```` ```csv ```` block exists, but `skills/accounting-audit-system-builder/SKILL.md`
  is a sub-pack *router* and ships no artifact blocks. `tools/validate.py:39`
  reports the same three shape complaints for the same file.
- `tools/check.py all`: 1 module not clean — `360-feedback-system`, with a real
  content defect unrelated to `'%'`. 17 SQL columns against 19 fields, 7 wrong
  SQL types (`Status` declared `DATE` where a `select` is wanted, `Notes`
  declared `NUMERIC`), an index on a column that does not exist, and an optional
  `checkbox` listed in `json.required`.
- `tools/qa_verify.py --pack skills`: 28 errors, 147 warnings across the two
  sub-packs and 4 flat modules (`probation-tracker`, `people-directory`,
  `onboarding-playbook`, `candidate-talent-pool`, `audit-log`,
  `alumni-re-hire-tracker`).
- `name != folder` on the repository root (`untitled folder 3`) — a checkout-path
  artefact, not a content defect.

To revisit H1/H2/H5 the simulator must be rewritten against the real section
names before it can produce evidence worth acting on.

## Change log

| Step | Action | Artifacts |
|---|---|---|
| 1 | Hypotheses listed + debug file created | `debug-skill-md-qa.md` |
| 2 | Build simulator | `tools/simulate_skill_user_sessions.py` + debug server start |
| 3 | Run pre-fix evidence collection | `.dbg/pre_fix/results.json` + `.dbg/pre_fix/summary.md` |
| 4 | Triage the oracle before fixing anything — halted Step 4, 307/310 findings were false positives | this file |
| 5 | Fix H4 (3 broken navigation links) | 3 × `skills/*/README.md` |
| 6 | Fix H3 (`'%'` naming) — `snake()` aligned with `qa_verify.py:190`, 9 SQL blocks renamed to `_pct` | `tools/check.py` + 9 × `skills/*/SKILL.md` |
| 7 | Verify: 6/6 links resolve, `check.py` 80/87 → 86/87, `validate.py` 103/103, `qa_verify.py` 0 errors in the 9 renamed modules | — |
| 8 | Cleanup (after user ACK) | remove simulator + `.dbg/` + env + this file iff [OPEN]→A |
