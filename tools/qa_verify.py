#!/usr/bin/env python3
"""QA verifier for every module SKILL.md in the repo.

Checks the rules in references/qa-fix-contract.md mechanically. Run from the repo root:

    python3 tools/qa_verify.py            # all packs
    python3 tools/qa_verify.py --pack accounting-audit-system-builder
    python3 tools/qa_verify.py --verbose

Exit code 1 if any ERROR is found. WARN does not fail the run.
"""

import argparse
import csv
import io
import json
import os
import re
import sys

ERRORS: list[str] = []
WARNS: list[str] = []
CURRENT = ""


def err(msg):
    ERRORS.append(f"{CURRENT}: {msg}")


def warn(msg):
    WARNS.append(f"{CURRENT}: {msg}")


REQUIRED_SECTIONS = [
    "## Overview",
    "## When to Use This Skill",
    "## How It Works",
    "### Step 1 - Identify intent",
    "### Step 3 - Hold the internal context",
    "### Step 4 - Recommend the smallest workflow",
    "### Step 5 - Build only on request",
    "## Field Reference",
    "## Select Options",
    "## Relations",
    "## Examples",
    "## Best Practices",
    "## Limitations",
    "## Security & Safety Notes",
    "## Common Pitfalls",
    "## Related Skills",
    "## Reusable Prompt",
]

FRONTMATTER_KEYS = [
    "name", "description", "category", "risk", "source",
    "source_type", "date_added", "author", "tags", "tools",
]

# Real-looking identifiers and names that must never appear in example data.
BANNED_IDENTIFIERS = [
    r"\b[0-9]{5}[A-Z]{1,3}[0-9]{4}[A-Z][0-9][A-Z]Z[0-9]\b",   # IN PAN format
    r"\b\d{2}[A-Z]{5}\d{4}[A-Z]\d[A-Z]Z[A-Z0-9]\b",             # GSTIN format
]
FAKE_TOKEN = re.compile(r"EXAMPLE-|\bExample\b|ILLUSTRATIVE|illustrative")

# Terms that must be qualified, not asserted.
BANNED_TAX_CLAIMS = [
    (r"\bis (?:definitely |always )?(?:IRD|CBMS)[- ]compliant\b", "compliance asserted without evidence"),
    (r"\bVAT rate is 18\b", "tax rate asserted"),
    (r"\bthe (?:correct|applicable) (?:VAT|TDS) rate is\b", "tax rate asserted"),
    (r"\bguarantee[sd]? (?:compliance|approval|acceptance)\b", "guarantee language"),
    (r"\bI recommend (?:buying|choosing|selecting) \w+ because it is best\b", "module-level recommendation"),
    (r"\bis the best (?:software|vendor|package)\b", "verdict"),
]

GENERIC_OPENERS = [
    r"biggest expense category",
    r"What is your biggest",
    r"describe your business in one line",
]


def read(path):
    with open(path, encoding="utf-8") as fh:
        return fh.read()


def fenced_blocks(text, lang):
    return re.findall(r"```" + lang + r"\n(.*?)```", text, re.S)


def parse_frontmatter(text):
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not m:
        return None
    try:
        return yaml_load(m.group(1))
    except Exception:
        return None


def yaml_load(block):
    """Minimal YAML reader: enough for flat keys and inline lists."""
    out = {}
    for line in block.split("\n"):
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if ":" not in line or line.startswith((" ", "\t", "-")):
            continue
        key, _, val = line.partition(":")
        val = val.strip().strip('"').strip("'")
        if val.startswith("[") and val.endswith("]"):
            val = [v.strip().strip('"').strip("'") for v in val[1:-1].split(",") if v.strip()]
        out[key.strip()] = val
    return out


def check_frontmatter(text, path):
    meta = parse_frontmatter(text)
    if meta is None:
        err("missing or unparseable YAML frontmatter")
        return None
    for key in FRONTMATTER_KEYS:
        if key not in meta:
            err(f"frontmatter missing '{key}'")
    name = meta.get("name")
    if name and name != os.path.basename(os.path.dirname(path)):
        err(f"frontmatter name '{name}' does not match directory")
    return meta


def check_sections(text):
    for sec in REQUIRED_SECTIONS:
        if sec not in text:
            err(f"missing section: {sec}")


def check_artifacts(text):
    csvs = fenced_blocks(text, "csv")
    sqls = fenced_blocks(text, "sql")
    jsons = fenced_blocks(text, "json")
    mds = [b for b in fenced_blocks(text, "markdown") if "CSV column" in b]

    if not csvs:
        err("no CSV artifact block")
        return
    if not sqls:
        err("no SQL artifact block")
    if not jsons:
        err("no JSON Schema block")
    if not mds:
        err("no Notion property-mapping table")

    # ---- CSV header is the canonical order
    header = csvs[0].split("\n")[0].strip()
    cols = [c.strip() for c in header.split(",")]
    cols = [c for c in cols if c]
    if len(cols) != len(set(cols)):
        err("CSV header has duplicate column names")
    canon = cols

    # ---- every CSV block has the same header
    for i, blk in enumerate(csvs[1:], start=2):
        h = [c.strip() for c in blk.split("\n")[0].split(",") if c.strip()]
        if h != canon:
            err(f"CSV block {i} header differs from the canonical header")

    # ---- SQL columns, in order
    sql = sqls[0]
    m = re.search(r"CREATE TABLE\s+\w+\s*\((.*?)\n\);", sql, re.S)
    if not m:
        err("SQL block has no parsable CREATE TABLE body")
        return
    body = m.group(1)
    sql_cols = []
    for line in body.split("\n"):
        line = line.strip().rstrip(",")
        if not line or line.startswith("--"):
            continue
        if re.match(r"^(CONSTRAINT|PRIMARY KEY|UNIQUE|CHECK|FOREIGN KEY)\b", line, re.I):
            continue
        if "(" in line and line.split("(")[0].strip() in ("PRIMARY KEY", "UNIQUE"):
            continue
        name_m = re.match(r"^([a-z0-9_]+)\s+([A-Z])", line)
        if name_m:
            sql_cols.append((name_m.group(1), name_m.group(2)))

    def to_snake(name):
        """'TDS Rate %' -> 'tds_rate_pct'; 'UOM' -> 'uom'; 'PAN/VAT' -> 'pan_vat'."""
        n = name.replace("%", " Pct")
        n = re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", n)
        n = re.sub(r"([A-Z]+)([A-Z][a-z])", r"\1_\2", n)
        n = re.sub(r"[^A-Za-z0-9]+", "_", n)
        return n.strip("_").lower()

    TECHNICAL = {"created_at", "updated_at"}
    expected_snake = [to_snake(c) for c in canon]
    got_snake = [c for c, _ in sql_cols if c not in TECHNICAL]
    if got_snake != expected_snake:
        missing = [c for c in expected_snake if c not in got_snake]
        extra = [c for c in got_snake if c not in expected_snake]
        if missing:
            err(f"SQL is missing CSV fields: {missing}")
        if extra:
            err(f"SQL has business fields absent from the CSV header: {extra}")
        else:
            err("SQL column order does not match the CSV header order")

    # ---- SQL type sanity
    for col, typ in sql_cols:
        if typ == "S":
            continue
        if col in ("id",) or col.endswith("_id"):
            continue
    if re.search(r"\bAUTO_INCREMENT\b", sql):
        warn("SQL uses AUTO_INCREMENT - name the engine assumption instead")
    for fk in re.findall(r"REFERENCES\s+(\w+)", sql):
        if re.search(r"CREATE TABLE\s+" + fk + r"\b", sql) is None:
            err(f"SQL declares a foreign key to '{fk}' but never creates that table")

    # ---- JSON Schema
    try:
        schema = json.loads(jsons[0])
    except Exception as exc:
        err(f"JSON Schema does not parse: {exc}")
        return
    if schema.get("$schema") != "https://json-schema.org/draft/2020-12/schema":
        err("JSON Schema is not draft 2020-12")
    props = list(schema.get("properties", {}).keys())
    if props != canon:
        missing = [c for c in canon if c not in props]
        extra = [c for c in props if c not in canon]
        if missing:
            err(f"JSON Schema is missing CSV fields: {missing}")
        if extra:
            err(f"JSON Schema has fields absent from the CSV header: {extra}")
        else:
            err("JSON Schema property order does not match the CSV header order")
    for req in schema.get("required", []):
        if req not in canon:
            err(f"JSON Schema requires unknown field '{req}'")
    money_like = [p for p, s in schema.get("properties", {}).items()
                  if s.get("type") == "number" and ("amount" in p.lower() or "payable" in p.lower()
                                                     or "balance" in p.lower() or "total" in p.lower())]
    for p in money_like:
        if p in schema.get("required", []) and "rate" in p.lower():
            err(f"'{p}' looks like a rate but is a money field")

    # ---- Notion mapping covers every column, in order
    md = mds[0]
    md_rows = [ln for ln in md.split("\n") if ln.strip().startswith("|")]
    md_cols = []
    for ln in md_rows[2:]:
        cells = [c.strip() for c in ln.strip().strip("|").split("|")]
        if len(cells) >= 2:
            md_cols.append(cells[0])
    if md_cols != canon:
        missing = [c for c in canon if c not in md_cols]
        extra = [c for c in md_cols if c not in canon]
        if missing:
            err(f"Notion mapping is missing CSV fields: {missing}")
        if extra:
            err(f"Notion mapping has columns absent from the CSV: {extra}")
        else:
            err("Notion mapping order does not match the CSV header order")

    # ---- Field Reference must list every field, in order
    m = re.search(r"## Field Reference\n(.*?)\n## ", text, re.S)
    if not m:
        err("no Field Reference section body")
    else:
        ref = [r for r in m.group(1).split("\n") if re.match(r"^\|\s*\d+\s*\|", r)]
        ref_cols = []
        for r in ref:
            cells = [c.strip() for c in r.strip().strip("|").split("|")]
            if len(cells) >= 2:
                ref_cols.append(cells[1].strip("`"))
        if ref_cols != canon:
            err("Field Reference does not match the CSV header (name or order)")

    return canon


def check_example_row(canon, text):
    csvs = fenced_blocks(text, "csv")
    for blk in csvs:
        lines = [l for l in blk.split("\n") if l.strip()]
        if len(lines) < 3:
            continue
        row = lines[2] if len(lines) > 2 else ""
        if not row.strip():
            continue
        if not FAKE_TOKEN.search(row):
            err("example row is not labelled as illustrative/fake")
        for pat in BANNED_IDENTIFIERS:
            if re.search(pat, row):
                err("example row contains a realistic tax identifier")


def check_intake_rules(text):
    if "one short question per message" not in text.lower() and "one question per message" not in text.lower():
        err("does not state the one-question-per-message rule")
    if re.search(r"Q:\*\* What is your biggest", text):
        for pat in GENERIC_OPENERS:
            if re.search(pat, text, re.I):
                err(f"uses a generic opening question: {pat}")
    # ambiguity rule
    if not re.search(r"ambiguous|multiple-choice|which do you mean", text, re.I):
        warn("no rule for ambiguous / multiple-choice answers")
    # unknown-not-zero
    if not re.search(r"[Nn]ever turn .{0,40}[Uu]nknown into (?:zero|0)", text) and \
       not re.search(r"[Uu]nknown.{0,40}(?:not|never) .{0,10}zero", text):
        warn("no explicit 'Unknown is not zero' rule")
    if not re.search(r"never invent", text, re.I):
        err("no anti-invention rule")


def check_scope(text):
    """Fields that imply payment/withholding must be justified if present."""
    for field in ("Net Payable", "TDS Rate %", "TDS Amount", "Payment Mode", "Department"):
        if re.search(r"^\|\s*\d+\s*\|" + re.escape(field) + r"\s*\|", text, re.M):
            if not re.search(r"scope change|only if|only when|added (?:only|deliberately)|not part of", text, re.I):
                warn(f"'{field}' is in the field reference but no scope justification is stated")


def check_claims(text):
    for pat, why in BANNED_TAX_CLAIMS:
        for m in re.finditer(pat, text, re.I):
            line = text[:m.start()].count("\n") + 1
            err(f"prohibited claim at line {line}: {why}")


def check_relations(text):
    """A Notion Relation must name a real target; otherwise it must be Text."""
    m = re.search(r"## Relations\n(.*?)\n## ", text, re.S)
    rel = m.group(1) if m else ""
    for ln in rel.split("\n"):
        if "->" not in ln and "→" not in ln:
            continue
        target = re.split(r"->|→", ln, maxsplit=1)[-1].strip().strip("`").rstrip(".")
        # A relation line may legitimately be prose; only flag backticked slug targets
        # that do not look like a module slug.
        for tok in re.findall(r"`([^`]+)`", ln):
            if " " in tok or "/" in tok or "(" in tok or tok.isupper():
                continue
            if not re.match(r"^[a-z0-9]+(-[a-z0-9]+)+$", tok):
                err(f"relation target '{tok}' is not a module-slug form")


def check_status_values(text):
    if re.search(r"not be `Done`", text):
        pass
    elif re.search(r"## Select Options", text) and "Done" in text:
        warn("no rule preventing 'Done' while a required check fails")


def check_file(path):
    global CURRENT
    CURRENT = os.path.relpath(path, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    text = read(path)
    check_frontmatter(text, path)
    check_sections(text)
    check_intake_rules(text)
    check_claims(text)
    canon = check_artifacts(text)
    if canon:
        check_example_row(canon, text)
        check_scope(text)
    check_relations(text)
    check_status_values(text)
    return CURRENT


def find_skills(root):
    out = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in (".git", "node_modules", "references", "tools")]
        if "SKILL.md" in filenames and os.path.basename(dirpath) != os.path.basename(root):
            out.append(os.path.join(dirpath, "SKILL.md"))
    return sorted(out)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pack", default=None)
    ap.add_argument("--verbose", action="store_true")
    args = ap.parse_args()

    here = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if args.pack:
        roots = [os.path.join(here, args.pack)]
    else:
        roots = [os.path.join(here, d) for d in sorted(os.listdir(here))
                 if os.path.isdir(os.path.join(here, d)) and not d.startswith(".")
                 and d not in ("references", "tools")]
        roots = [r for r in roots if os.path.isdir(os.path.join(r, "skills"))]

    files = []
    for r in roots:
        files += find_skills(r)

    for f in files:
        try:
            check_file(f)
        except Exception as exc:  # noqa: BLE001
            err(f"verifier crashed: {exc}")

    print(f"checked {len(files)} SKILL.md files")
    if args.verbose:
        for e in ERRORS:
            print("  ERROR", e)
    if WARNS:
        for w in WARNS:
            print("  WARN ", w)
    if ERRORS:
        print(f"\nFAIL: {len(ERRORS)} error(s), {len(WARNS)} warning(s)")
        for e in ERRORS:
            print("  ERROR", e)
        return 1
    print(f"PASS: 0 errors, {len(WARNS)} warning(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
