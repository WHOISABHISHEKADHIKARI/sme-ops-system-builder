#!/usr/bin/env python3
"""Apply the shared execution contract link and tool-neutral metadata to every skill."""

from pathlib import Path
import os
import re


ROOT = Path(__file__).resolve().parent.parent
CONTRACT = ROOT / "references" / "execution-contract.md"
MARKER = "Follow the [shared execution contract]"
EXAMPLE_PREFIX = "One example row per artifact, visibly fake."
EMPTY_TEMPLATE_RULE = (
    "The rows above are documentation examples only. Emit empty templates unless the "
    "user explicitly requests examples."
)
EXCEL_COMPATIBLE_CSV_RULE = (
    "For an Excel-compatible CSV, use UTF-8 with a byte order mark so Excel opens the\n"
    "text correctly. A CSV is not an `.xlsx` workbook; create `.xlsx` only when the user\n"
    "requests a workbook."
)
EXTERNAL_ACTION_RULE = (
    "- Creating a requested artifact may write that artifact locally. Do not run commands,\n"
    "  call APIs, provision infrastructure, or make other external changes unless the user\n"
    "  explicitly requests and authorizes them."
)


def skill_files():
    return sorted(
        path for path in ROOT.rglob("SKILL.md")
        if ".git" not in path.parts
    )


def contract_link(path):
    return Path(os.path.relpath(CONTRACT, path.parent)).as_posix()


def standardize(path):
    text = path.read_text(encoding="utf-8")
    original = text

    text = re.sub(r"^tools:\s*\[[^\n]*\]$", "tools: []", text, count=1, flags=re.M)

    if MARKER not in text:
        heading = "## How It Works\n"
        if heading not in text:
            raise ValueError(f"missing How It Works heading: {path}")
        paragraph = (
            f"\nFollow the [shared execution contract]({contract_link(path)}). "
            "The module-specific rules below define only domain fields, decisions, "
            "calculations, and safety constraints.\n"
        )
        text = text.replace(heading, heading + paragraph, 1)

    # Documentation examples help maintainers inspect schema alignment, but they are not
    # default output data. Keep the examples while making the emission rule unambiguous.
    text = text.replace(EXAMPLE_PREFIX, EMPTY_TEMPLATE_RULE)
    text = text.replace(
        "Keep the example row obviously fake so nobody imports it as real data.",
        "If the user requests an example row, keep it obviously fake so nobody imports "
        "it as real data.",
    )
    text = text.replace(
        "Keep the example row obviously fake so nobody imports it as a real item.",
        "If the user requests an example row, keep it obviously fake so nobody imports "
        "it as a real item.",
    )
    text = text.replace(
        "Keep the example row obviously fake so nobody imports it as a real citation.",
        "If the user requests an example row, keep it obviously fake so nobody imports "
        "it as a real citation.",
    )
    text = text.replace(
        "Keep the example row obviously fake so nobody imports it as a real post.",
        "If the user requests an example row, keep it obviously fake so nobody imports "
        "it as a real post.",
    )
    text = re.sub(
        r"Keep the example row obviously fake so nobody imports it as a real ([^.]+)\.",
        r"If the user requests an example row, keep it obviously fake so nobody imports "
        r"it as a real \1.",
        text,
    )
    text = text.replace(
        "Generated modules carry fictional example rows, never real records. Real data is the\n"
        "  user to enter.",
        "Documentation examples use fictional rows, never real records. Emitted templates\n"
        "  stay empty unless the user requests examples; real data is the user to enter.",
    )
    text = re.sub(
        r"An Excel workbook is the CSV emitted\s+with a UTF-8 byte order mark, so Excel "
        r"opens it with\s+correct text and no import dialog\.",
        EXCEL_COMPATIBLE_CSV_RULE,
        text,
    )
    text = re.sub(
        r"- This skill writes nothing outside the chat\. It runs no commands and calls no "
        r"APIs(?: unless\s+the surrounding platform explicitly provides them)?\.",
        EXTERNAL_ACTION_RULE,
        text,
    )
    text = re.sub(
        r"- This skill writes nothing outside the chat\. It runs no commands, calls no APIs, "
        r"and\s+provisions no infrastructure\.",
        EXTERNAL_ACTION_RULE,
        text,
    )
    text = re.sub(
        r"For an Excel-compatible CSV, use UTF-8 with a byte order mark so Excel opens the\s+"
        r"text correctly\. A CSV is not an `\.xlsx` workbook; create `\.xlsx` only when the "
        r"user\s+requests a workbook\.\s+(?=A CSV carries)",
        EXCEL_COMPATIBLE_CSV_RULE + "\n",
        text,
    )
    text = re.sub(
        r"- Creating a requested artifact may write that artifact locally\. Do not run "
        r"commands,\s+call APIs, provision infrastructure, or make other external changes "
        r"unless the user\s+explicitly requests and authorizes them\.",
        EXTERNAL_ACTION_RULE,
        text,
    )

    if text != original:
        path.write_text(text, encoding="utf-8")
        return True
    return False


def main():
    files = skill_files()
    changed = [path for path in files if standardize(path)]
    print(f"checked {len(files)} SKILL.md files; changed {len(changed)}")


if __name__ == "__main__":
    main()
