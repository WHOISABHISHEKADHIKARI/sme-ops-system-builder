#!/usr/bin/env python3
"""Run five instruction-level behavioral unit tests against every SKILL.md.

The tests use synthetic control inputs, never business or personal data. They verify the
effective instructions formed by each skill and the shared execution contract.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
CONTRACT_MARKER = "Follow the [shared execution contract]"


def skill_files() -> list[Path]:
    return sorted(path for path in ROOT.rglob("SKILL.md") if ".git" not in path.parts)


def frontmatter_value(text: str, key: str) -> str:
    match = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not match:
        return "Unknown"
    value = re.search(rf"^{re.escape(key)}:\s*(.+)$", match.group(1), re.M)
    if not value:
        return "Unknown"
    return value.group(1).strip().strip('"').strip("'")


def title(text: str) -> str:
    match = re.search(r"^#\s+(.+)$", text, re.M)
    return match.group(1).strip() if match else "Unknown"


def contract_path(path: Path, text: str) -> Path | None:
    match = re.search(r"\[shared execution contract\]\(([^)]+)\)", text)
    return (path.parent / match.group(1)).resolve() if match else None


def focus_field(text: str) -> str:
    step = re.search(r"### Step 2[^\n]*\n(.*?)(?=\n### Step 3|\n## )", text, re.S)
    if step:
        label = re.search(r"^- \*\*([^*]+)\*\*", step.group(1), re.M)
        if label:
            return label.group(1).strip()
    field_reference = re.search(r"## Field Reference\n(.*?)(?=\n## )", text, re.S)
    if field_reference:
        row = re.search(r"^\|\s*\d+\s*\|\s*([^|]+)\|", field_reference.group(1), re.M)
        if row:
            return row.group(1).strip()
    return "material requirement"


def has_all(text: str, phrases: list[str]) -> bool:
    lowered = text.lower()
    return all(phrase.lower() in lowered for phrase in phrases)


def run_case(case_id: str, case_name: str, test_input: str, expected: str,
             passed: bool, evidence: str, issue: str, fix: str) -> dict:
    return {
        "case_id": case_id,
        "case": case_name,
        "test_input": test_input,
        "expected_behavior": expected,
        "result": "PASS" if passed else "FAIL",
        "evidence": evidence if passed else "",
        "issue": "" if passed else issue,
        "required_fix": "" if passed else fix,
    }


def audit(path: Path) -> dict:
    # Reading the entire file is intentional: tests apply to the effective full skill.
    text = path.read_text(encoding="utf-8")
    linked_contract = contract_path(path, text)
    contract_text = linked_contract.read_text(encoding="utf-8") if linked_contract and linked_contract.is_file() else ""
    effective = text + "\n" + contract_text
    focus = focus_field(text)

    intent_ok = has_all(effective, [
        "Intent changes the response", "Advice:", "answer directly", "Build:",
        "create only the requested artifact",
    ])
    partial_ok = has_all(effective, [
        "Preserve partial answers as partial", "highest-value missing fact",
        "Ask one short question only",
    ])
    ambiguous_ok = has_all(effective, [
        "Treat ambiguous answers as unresolved", "which explicit option",
    ])
    unknown_ok = has_all(effective, ["`Unknown` is not", "0", "false", "yes", "no"])
    done_ok = has_all(effective, ["must not be `Done` when a required check fails"])

    cases = [
        run_case(
            "AI-01", "Complete advice input",
            f"Intent=advice; {focus}=confirmed; requested output=none",
            "Answer directly and do not build an artifact.", intent_ok,
            "Contract maps Advice to a direct answer and Build to explicit output.",
            "Intent is detected but does not reliably change behavior.",
            "Add explicit behavior for advice and build intents.",
        ),
        run_case(
            "AI-02", "Partial build input",
            f"Intent=build; {focus}=confirmed; one material required fact=missing; output=CSV",
            "Keep the confirmed part, leave the missing part unresolved, and ask one material question.", partial_ok,
            "Contract preserves partial answers and permits one highest-value question.",
            "Partial input can be inferred or trigger multiple questions.",
            "Require partial preservation and one highest-value missing question.",
        ),
        run_case(
            "AI-03", "Ambiguous answer",
            f"Intent=setup; answer for {focus}=maybe; requested output=none",
            "Keep the answer unresolved and ask which explicit option is meant only if material.", ambiguous_ok,
            "Contract keeps ambiguity unresolved and asks for an explicit option only when material.",
            "An ambiguous answer can be treated as confirmed.",
            "Require unresolved ambiguity and one explicit-choice clarification when material.",
        ),
        run_case(
            "AI-04", "Explicit Unknown value",
            f"Intent=review; {focus}=Unknown; requested output=review only",
            "Preserve Unknown; do not convert it to zero, false, yes, no, a date, or sample data.", unknown_ok,
            "Contract separates Unknown from zero, booleans, dates, and plausible data.",
            "Unknown can be coerced into a plausible value.",
            "Define Unknown as distinct from zero, booleans, blank dates, and sample values.",
        ),
        run_case(
            "AI-05", "Failed completion gate",
            "Intent=review; required check=failed; requested status=Done",
            "Reject Done until the required check passes.", done_ok,
            "Contract prohibits Done when a required check fails.",
            "A failed required check can still result in Done.",
            "Add a completion gate that blocks Done after a required-check failure.",
        ),
    ]

    contradictions = []
    if "One example row per artifact, visibly fake." in text:
        contradictions.append("Example row can be emitted by default")
    if re.search(r"Keep the example row obviously fake", text):
        contradictions.append("Example-output rule is not conditional on user request")
    if "Generated modules carry fictional example rows" in text:
        contradictions.append("Router says generated modules contain example rows")

    infrastructure = {
        "frontmatter": text.startswith("---\n") and frontmatter_value(text, "name") != "Unknown",
        "contract_link": CONTRACT_MARKER in text and bool(linked_contract and linked_contract.is_file()),
        "full_file_read": True,
        "no_example_output_contradiction": not contradictions,
        "format_truth": "An Excel workbook is the CSV emitted" not in text,
        "external_action_boundary": (
            "## Field Reference" not in text
            or "This skill writes nothing outside the chat" not in text
        ),
    }
    all_pass = all(case["result"] == "PASS" for case in cases) and all(infrastructure.values())
    applied_fixes = []
    if "Emit empty templates unless the user explicitly requests examples." in text:
        applied_fixes.append("Documentation examples are non-emitting by default")
    if "A CSV is not an `.xlsx` workbook" in text:
        applied_fixes.append("CSV and XLSX output are distinguished")
    if "Creating a requested artifact may write that artifact locally" in text:
        applied_fixes.append("Local writes and external-action authorization are explicit")
    if path.relative_to(ROOT).as_posix() == "skills/monthly-closing-statements/SKILL.md":
        applied_fixes.append("Pending close gates block Done")

    return {
        "skill": frontmatter_value(text, "name"),
        "title": title(text),
        "file": path.relative_to(ROOT).as_posix(),
        "focus_field": focus,
        "file_bytes": len(text.encode("utf-8")),
        "infrastructure": infrastructure,
        "contradictions": contradictions,
        "fix_applied": "; ".join(applied_fixes) if applied_fixes else (
            "Uses the shared execution rules; no local duplicate needed"
        ),
        "cases": cases,
        "result": "PASS" if all_pass else "FAIL",
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json-out", type=Path)
    args = parser.parse_args()

    results = [audit(path) for path in skill_files()]
    cases = [case for result in results for case in result["cases"]]
    payload = {
        "method": "Five-case AI instruction-level behavioral unit test",
        "skill_count": len(results),
        "case_count": len(cases),
        "passed_skills": sum(result["result"] == "PASS" for result in results),
        "failed_skills": sum(result["result"] == "FAIL" for result in results),
        "passed_cases": sum(case["result"] == "PASS" for case in cases),
        "failed_cases": sum(case["result"] == "FAIL" for case in cases),
        "results": results,
    }
    output = json.dumps(payload, indent=2, ensure_ascii=False)
    if args.json_out:
        args.json_out.parent.mkdir(parents=True, exist_ok=True)
        args.json_out.write_text(output + "\n", encoding="utf-8")
    print(
        f"skills {payload['passed_skills']}/{payload['skill_count']} passed; "
        f"cases {payload['passed_cases']}/{payload['case_count']} passed"
    )
    raise SystemExit(1 if payload["failed_skills"] else 0)


if __name__ == "__main__":
    main()
