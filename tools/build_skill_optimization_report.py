#!/usr/bin/env python3
"""Generate the requested one-row-per-skill optimization report."""

from pathlib import Path
import re


ROOT = Path(__file__).resolve().parent.parent
REPORT = ROOT / "references" / "skill-optimization-report.md"

SPECIAL = {
    "skills/accounting-software-selection/SKILL.md":
        "kept evidence and human-decision boundaries; made SQL checks parser-safe",
    "skills/credit-cycle-analysis/SKILL.md":
        "made aging fields portable and self-describing; aligned the utilisation percentage field",
    "skills/expense-accounting/SKILL.md":
        "removed the irrelevant category opener; aligned the VAT percentage field",
    "skills/payment-accounting/SKILL.md":
        "aligned the TDS percentage field across formats",
    "skills/purchase-accounting/SKILL.md":
        "aligned VAT and TDS percentage fields across formats",
    "skills/sales-accounting/SKILL.md":
        "aligned VAT and TDS percentage fields across formats",
    "skills/tds-booking-payment/SKILL.md":
        "aligned the TDS percentage field across formats",
}


def files():
    return sorted(path for path in ROOT.rglob("SKILL.md") if ".git" not in path.parts)


def title(text):
    match = re.search(r"^# (.+)$", text, re.M)
    return match.group(1).strip() if match else "Unknown"


def optimization(path):
    rel = path.relative_to(ROOT).as_posix()
    text = path.read_text(encoding="utf-8")
    changes = [
        "Linked the canonical execution contract",
        "removed tool assumptions",
    ]

    if rel == "SKILL.md" or rel.count("/") == 2 and "system-builder" in rel:
        changes.append("preserved concise routing and handoff boundaries")
    elif rel.startswith("skills/") and rel.count("/") == 2 and rel.split("/")[1] in {"accounting-software-selection", "audit-preparation", "credit-cycle-analysis", "day-book", "expense-accounting", "inventory-stock-reconciliation", "monthly-closing-statements", "party-ledger-reconciliation", "payment-accounting", "petty-cash-management", "purchase-accounting", "receipt-accounting", "salary-wage-accounting", "sales-accounting", "source-document-filing", "tds-booking-payment"}:
        changes.extend([
            "made ambiguity and partial-answer handling explicit",
            "enforced Unknown ≠ 0 and the Done completion gate",
        ])
    elif "brand-growth-system-builder/" in rel:
        changes.append("kept the stricter artifact contract and safety boundaries")
    else:
        changes.append("kept the canonical field list and output-only-on-request behavior")

    if "Emit empty templates unless the user explicitly requests examples." in text:
        changes.append("made documentation examples non-emitting by default")
    if "A CSV is not an `.xlsx` workbook" in text:
        changes.append("separated Excel-compatible CSV from real XLSX output")
    if "Creating a requested artifact may write that artifact locally" in text:
        changes.append("made local artifact writes explicit and kept other external actions opt-in")
    if rel == "skills/monthly-closing-statements/SKILL.md":
        changes.append("made pending close gates block Done")

    if rel in SPECIAL:
        changes.append(SPECIAL[rel])

    return "; ".join(changes) + "."


def main():
    rows = []
    for path in files():
        text = path.read_text(encoding="utf-8")
        rel = path.relative_to(ROOT).as_posix()
        rows.append((rel, title(text), optimization(path)))

    lines = [
        "# SKILL.md Optimization Report",
        "",
        "One row per reviewed skill. All files retain their original purpose, scope, business",
        "logic, and safety boundaries while sharing one execution contract.",
        "",
        "| # | Skill | File | Optimizations |",
        "|---:|---|---|---|",
    ]
    for index, (rel, name, changes) in enumerate(rows, 1):
        lines.append(f"| {index} | {name} | `{rel}` | {changes} |")

    lines.extend([
        "",
        "## Validation",
        "",
        "- Operational modules: `python3 tools/check.py all`",
        "- Accounting modules: `python3 tools/qa_verify.py --pack skills/accounting-audit-system-builder`",
        "- Brand-growth modules: `python3 tools/qa_verify.py --pack skills/brand-growth-system-builder`",
        "- Repository structure: `python3 tools/validate.py`",
        "- SEO and references: `python3 tools/seo.py --check`",
    ])
    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"wrote {REPORT.relative_to(ROOT)} with {len(rows)} skill rows")


if __name__ == "__main__":
    main()
