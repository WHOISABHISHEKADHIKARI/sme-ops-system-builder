# Running QA Context

## Objective

Review, optimize and standardize every repository `SKILL.md` for simple, logical,
reusable, safe behavior with low hallucination risk. For each skill: precommit five real
user scenarios, execute them independently, document evidence, make only supported fixes,
and retest the same prompts.

## Scope and safety

- Repository: `/Users/abhi/Downloads/untitled folder 3`
- Files in scope: 103 `SKILL.md` files.
- Do not invent facts, default missing data, add country/tool assumptions, expose secrets,
  or change a skill before evidence supports the change.
- Work one skill at a time. A failed or invalid test design is logged; it is not treated as
  a skill failure.
- Do not use Python. QA and reports use Node.js tooling.

## Backup

Pre-change snapshot, verified with `unzip -t`:

`/Users/abhi/Downloads/sme-ops-system-builder-backups/sme-ops-system-builder-20260928-013815-+0545.zip`

## QA protocol

- Runner: `tools/real_skill_poc_qa.mjs` v3.6.0.
- Five categories per skill: normal, missing, edge, failure, hallucination.
- Models: supported designer `gpt-5.6-luna`, target `gpt-5.6-luna`, independent design
  auditor and judge `gpt-5.6-terra`.
- Cases run in opaque isolated workspaces. The runner records prompts, full visible chat,
  tool traces, file changes, artifact validation, objective protocol findings, and scores.
- Retests preserve `case_id`, category and user prompt byte-for-byte.
- A case automatically fails for prohibited Python, outside-workspace reads, unauthorized
  external activity, changed fixtures, unexpected files, missing artifacts, or malformed
  artifacts.

## Completed skill

### `skills/360-feedback-system/SKILL.md`

- Baseline: 2/5 pass.
- Supported fixes: precise artifact-only reply; no unconditional team-size question;
  consistent intent/output labels; explicit Unknown score-calculation inputs; aligned
  CSV/JSON/SQL field and enum rules; lifecycle gates; hard stops for out-of-scope payroll,
  tax, leave and employment decisions; human review for unknown legal claims; minimal setup
  recommendation boundary.
- Final retest: 5/5 pass.
- Latest evidence:
  `/private/tmp/user-poc-qa/retest-360-protocol-3.5-2026-09-28-a4/skill-reports/001-360-feedback-system.json`

## Current skill

### Root `SKILL.md` — SME Ops System Builder router

- No target scenario has run yet.
- Three prechange audited design rounds exist under
  `/private/tmp/user-poc-qa/baseline-root-protocol-3.5-2026-09-28-a2/raw/001-sme-ops-system-builder/`
  (designer rounds 1/2/3 + auditor rounds 1/2/3).
  Round-3 M1 case precommitted that a broad "help me choose an operational system, needs
  not stated, headcount supplied" prompt produces a single concise question about the
  MISSING OPERATIONAL NEED (not the hard-coded opener "What does the business do?").
  The prechange auditor rejected M1 against the then-current hard-coded wording. The
  SKILL.md was subsequently rewritten to the conditional highest-value-routing-fact rule,
  so the saved round-3 five-case set is NOW semantically aligned with the current router
  wording for case M1. The design set may be reused with `--seed-report` after extracting
  and converting the round-3 precommitted-design.json; or a fresh five-case chain is fine.
- Supported repository change already made: the root skill now directs the router to ask
  business activity or the operational need according to which is the highest-value missing
  routing fact.
- Fresh 3.6.0 baseline attempted on 2026-09-28 04:58 UTC under
  `/private/tmp/user-poc-qa/runs/2026-09-28T04-58-22-483Z-09c970be-df6d-4184-9e24-b8c15e561e50/`
  — aborted before target execution because the ChatGPT-auth account-wide Codex CLI usage
  cap was reached. Reset time is 2026-10-28 10:21 AM local.
- Next action: after the 2026-10-28 10:21 AM local Codex CLI quota resets, re-verify with
  `node --check tools/real_skill_poc_qa.mjs` and `git diff --check` using the bundled
  runtime Node, then rerun the root-router 3.6.0 five-case baseline from a fresh
  `--run-dir` with `--only "SKILL.md"` and the documented model/env vars. Append the
  resulting evidence path to `references/skill-qa-progress-log.md` before any further
  router change is claimed or a further skill is selected.

## Live documents

- Status and evidence index: `references/skill-qa-progress-log.md`
- Detailed running context: this file.
- Earlier broad standardization record: `references/skill-optimization-report.md`

## Handoff procedure

1. Read this file and `references/skill-qa-progress-log.md`.
2. Verify `node --check tools/real_skill_poc_qa.mjs` and `git diff --check` using the
   bundled Node executable.
3. Continue only with the current skill's baseline → evidence → minimal fix → same-prompt
   retest cycle.
4. Append every result, design rejection, model/configuration issue and exact evidence path
   to the progress log before proceeding to the next skill.
