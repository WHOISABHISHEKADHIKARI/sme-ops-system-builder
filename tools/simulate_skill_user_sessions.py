#!/usr/bin/env python3
"""
#region debug-point skill-simulator-v1
Instrumentation-only simulator that tests every SKILL.md file as a user would,
reporting flaws (not fixing them) via POST to Debug Server and writing results JSON.

Outputs:
  .dbg/pre_fix/results.json
  .dbg/pre_fix/summary.md
Reports every flaw event to http://127.0.0.1:9229/event with session=skill-md-qa.
#endregion
"""
import os, sys, re, json, urllib.request, urllib.parse, itertools
from pathlib import Path
from collections import defaultdict, Counter

ROOT = Path(__file__).resolve().parent.parent
DBG = ROOT / ".dbg"
OUT = DBG / "pre_fix"
OUT.mkdir(parents=True, exist_ok=True)

ENV_FILE = DBG / "skill-md-qa.env"
DEBUG_SERVER_URL = None
DEBUG_SESSION_ID = None
if ENV_FILE.exists():
    for line in ENV_FILE.read_text().splitlines():
        if line.startswith("DEBUG_SERVER_URL="): DEBUG_SERVER_URL = line.split("=",1)[1].strip()
        if line.startswith("DEBUG_SESSION_ID="): DEBUG_SESSION_ID = line.split("=",1)[1].strip()

def report(flaw_type, severity, skill, evidence, location=None):
    evt = {
        "session": DEBUG_SESSION_ID or "skill-md-qa",
        "type": f"skill-flaw:{flaw_type}",
        "severity": severity,
        "skill": str(skill),
        "evidence": evidence,
        "location": location,
    }
    if DEBUG_SERVER_URL:
        try:
            req = urllib.request.Request(DEBUG_SERVER_URL, data=json.dumps(evt).encode(),
                                         headers={"Content-Type":"application/json"}, method="POST")
            urllib.request.urlopen(req, timeout=2).read()
        except Exception:
            pass
    return evt

# ----- Helpers -----

def read_skill_sections(skill_path: Path):
    """Return dict: section_name (lower) -> (raw_text, start_line_number)."""
    text = skill_path.read_text()
    lines = text.splitlines()
    sections = {}
    cur_name = None
    cur_start = None
    cur_buf = []
    for i, line in enumerate(lines, 1):
        m = re.match(r"^##\s+(.+?)\s*$", line)
        if m:
            if cur_name:
                sections[cur_name.lower()] = ("\n".join(cur_buf).strip(), cur_start)
            cur_name = m.group(1).strip()
            cur_start = i
            cur_buf = []
        elif cur_name:
            cur_buf.append(line)
    if cur_name:
        sections[cur_name.lower()] = ("\n".join(cur_buf).strip(), cur_start)
    return text, sections, lines

def extract_fields_from_csv(section_text):
    """Parse fenced CSV in a Fields section:
    ## Fields (N)
    ```
    Col1, Col2, ...
    ```
    OR detect table rows like | # | Field name | Type | ... |
    Return list of field names.
    """
    # CSV fence first
    m = re.search(r"```\n([^\n]+)\n```", section_text)
    if m:
        cols = [c.strip() for c in m.group(1).split(",") if c.strip()]
        return cols, "csv"
    # Pipe table with columns "#","Field","Type"
    tbl = re.findall(r"^\s*\|\s*(\d+)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|", section_text, re.M)
    if tbl:
        # only keep rows where col 1 is integer + col2 is non-header. Reject the header row if captured.
        cols = []
        for row in tbl:
            num_s, field, ty = row
            if not num_s.isdigit(): continue
            try:
                if 1 <= int(num_s) <= 200:
                    cols.append(field.strip())
            except: pass
        return cols, "table"
    return [], "none"

def extract_declared_fields_number(section_header_line: str):
    m = re.search(r"Fields\s*\((\d+)\)", section_header_line, re.I)
    return int(m.group(1)) if m else None

def trigger_keywords(section_text):
    """Split on common separators in Trigger keyword lists/regex, return token set."""
    words = set()
    for bullet in re.findall(r"-\s+(.+)", section_text):
        tokens = re.split(r"[\s,;|/+]", bullet)
        for t in tokens:
            t = t.strip().strip("`").strip("'\"").lower()
            if len(t) >= 3 and not t.startswith("http"):
                words.add(t)
    # Also extract any /regexp/ bodies or parenthetical keyword groups
    for m in re.findall(r"/([^/\n]{2,80})/", section_text):
        tokens = re.split(r"[^A-Za-z0-9_ ]+", m)
        for t in tokens:
            if len(t) >= 3: words.add(t.lower())
    return words

SYNTHETIC_POSITIVE_TEMPLATES = [
    "I need help with {topic} for my business",
    "Can you set up {topic} in my accounting system",
    "I want to do {topic} for the first time",
    "Please create a {topic} template",
    "How do I manage {topic} correctly",
]

SYNTHETIC_NEGATIVE = [
    "Recommend me a good lunch restaurant near me",
    "Write a Python program to sort an array",
    "Fix my broken wifi connection",
    "Draft a birthday card for my friend",
    "What's the weather like in Tokyo tomorrow",
]

def topic_from_skill(rel, section_title):
    """Best-effort human topic name from folder name or skill title."""
    folder_topic = rel.parts[-2].replace("-", " ")
    # Or use the title from the first # line if provided
    return folder_topic

def test_skill(skill_path: Path, all_skills):
    """Return list of flaw events for a single SKILL.md."""
    rel = skill_path.relative_to(ROOT)
    text, sections, lines = read_skill_sections(skill_path)

    flaws = []
    SKIP_ROUTERS = {
        "skills/SKILL.md",
        "skills/accounting-audit-system-builder/SKILL.md",
    }
    is_router = str(rel).replace("\\","/") in SKIP_ROUTERS

    # H4. Broken links in SKILL.md markdown links (also README nav when present)
    for link_target, display in re.findall(r"\[([^\]]+)\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)", text):
        # display is target here; let me fix vars (order is display, target)
        display, target = link_target, display
        pass  # will redo below properly
    # redo link regex correctly
    for m in re.finditer(r"\[(?P<display>[^\]]+)\]\((?P<target>[^)\s]+)(?:\s+\"[^\"]*\")?\)", text):
        target = m.group("target")
        display = m.group("display")
        if target.startswith("http") or target.startswith("#"):
            continue
        # local or relative file path
        base_dir = skill_path.parent
        # strip anchors
        file_part = target.split("#",1)[0]
        resolved = (base_dir / file_part).resolve()
        try:
            rel_resolved = resolved.relative_to(ROOT)
            inside = True
        except ValueError:
            inside = False
        if not inside or not resolved.exists():
            flaws.append(report(
                "broken-skill-link",
                "HIGH" if "execution" in display.lower() or "contract" in display.lower() or "reference" in display.lower() else "MEDIUM",
                str(rel),
                f"Markdown link [{display}]({target}) does not resolve to any existing file in repo",
                location=f"{skill_path.name} line ~{m.start()}",
            ))

    # Structural: check required sections present and non-empty
    REQUIRED = ["trigger", "question sequence", "fields"]
    for sec_name in REQUIRED:
        if is_router:
            # Routers don't need Fields / Question Sequence in the same way, but need Trigger
            if sec_name == "trigger" and sec_name not in sections:
                flaws.append(report("structural-section", "CRITICAL", str(rel),
                    f"Router skill lacks '## Trigger' section", location=None))
            continue
        if sec_name not in sections:
            flaws.append(report("structural-section", "HIGH", str(rel),
                f"Missing required '## {sec_name.title()}' section", location=None))
            continue
        body, start = sections[sec_name]
        if len(body.strip()) < 20:
            flaws.append(report("structural-section", "HIGH", str(rel),
                f"'## {sec_name.title()}' section is suspiciously short/empty ({len(body)} chars)", location=f"{start}"))

    # H5. Trigger regex usefulness test: 3 positive, 2 negative
    if "trigger" in sections and not is_router:
        t_body, t_start = sections["trigger"]
        # Check trigger has both regex + keywords format
        has_regex = bool(re.search(r"###?\s*regex", t_body, re.I))
        has_keywords = bool(re.search(r"###?\s*keyword", t_body, re.I)) or bool(re.search(r"###?\s*vocabulary", t_body, re.I))
        if not (has_regex and has_keywords):
            flaws.append(report("trigger-shape", "MEDIUM", str(rel),
                f"Trigger section missing either Regex or Keyword sub-block (regex={has_regex}, keywords={has_keywords})", location=f"{t_start}"))
        # Check there is actual `### Regex` followed by fenced `^...$` expression
        regex_block = re.search(r"###?\s*[Rr]egex.*?```([^\n]+)```", t_body, re.S)
        if not regex_block:
            regex_block = re.search(r"```\s*\n(.*?)\n```", t_body, re.S)
        re_obj = None
        if regex_block:
            regex_str = regex_block.group(1).strip()
            try:
                re_obj = re.compile(regex_str, re.IGNORECASE)
            except Exception as e:
                flaws.append(report("trigger-regex-compile", "HIGH", str(rel),
                    f"Trigger regex failed to compile: /{regex_str}/  error={e}", location=f"{t_start}"))
        topic = topic_from_skill(rel, None)
        pos_matches = 0
        pos_utts = [t.format(topic=topic) for t in SYNTHETIC_POSITIVE_TEMPLATES[:3]]
        for u in pos_utts:
            if re_obj and re_obj.search(u):
                pos_matches += 1
        neg_matches = 0
        for u in SYNTHETIC_NEGATIVE:
            if re_obj and re_obj.search(u):
                neg_matches += 1
        if re_obj is None:
            flaws.append(report("trigger-no-regex", "HIGH", str(rel),
                "Trigger section has no fenced regex block to classify utterances", location=f"{t_start}"))
        else:
            if pos_matches < 2:
                flaws.append(report("trigger-weak-positives", "HIGH", str(rel),
                    f"Trigger regex matched only {pos_matches}/3 positive utterances (topic='{topic}'): {pos_utts}", location=f"{t_start}"))
            if neg_matches >= 2:
                flaws.append(report("trigger-false-positives", "HIGH", str(rel),
                    f"Trigger regex matched {neg_matches}/2 negative utterances (too broad)", location=f"{t_start}"))

    # H1. Trigger keyword uniqueness vs ALL skills (done after per-skill loop, we'll just stash the sets)
    # Save keywords onto global
    kw_set = set()
    if "trigger" in sections:
        kw_set = trigger_keywords(sections["trigger"][0])

    # H2. Questions vs fields coverage
    if not is_router and "fields" in sections and "question sequence" in sections:
        fields_body, fields_start = sections["fields"]
        q_body, q_start = sections["question sequence"]
        field_names, fmt = extract_fields_from_csv(fields_body)
        declared_n = extract_declared_fields_number(fields_body)
        if declared_n is not None and len(field_names) != declared_n:
            flaws.append(report("fields-declared-vs-actual", "HIGH", str(rel),
                f"## Fields ({declared_n}) declares N={declared_n} but the list has {len(field_names)} entries (format='{fmt}')", location=f"{fields_start}"))
        # extract field names referenced by questions: every `{Field Name}` or bold/italic phrase or the Q's direct object
        q_fields = set()
        for field in field_names:
            f_lo = field.lower()
            # 1. direct mention of field in any question line (case insensitive)
            if f_lo in q_body.lower():
                q_fields.add(field)
            else:
                # 2. match tokens — field with s/ies plurals stripped
                root = re.sub(r"(ies|s)$", "", f_lo)
                if len(root) >= 4 and re.search(rf"\b{re.escape(root)}\b", q_body.lower()):
                    q_fields.add(field)
        missing_from_q = [f for f in field_names if f not in q_fields]
        # Allow some standard auto-generated ones that don't need to be "asked" explicitly: id, Entry date, Created at, Voucher no etc.
        AUTO = {"id", "entry id", "day book id", "voucher id", "receipt id", "payment id", "sales id", "purchase id",
                "credit cycle id", "reconciliation id", "salary id", "audit id", "software id", "filing id", "document id",
                "inventory id", "ledger id", "tds id", "created at", "updated at", "created by"}
        truly_missing = [f for f in missing_from_q if f.lower().strip() not in AUTO]
        if len(truly_missing) >= 2:
            flaws.append(report("questions-missing-field-coverage", "HIGH", str(rel),
                f"{len(truly_missing)} fields never appear in Question Sequence nor are auto: {truly_missing[:10]}", location=f"{q_start}"))

    # H3. Template/artifact: sheets.gs column names vs fields (if files exist)
    if not is_router:
        base_dir = skill_path.parent
        for artifact, which in [("excel.xml", "excel"), ("sheets.gs", "gs")]:
            p = base_dir / artifact
            if not p.exists(): continue
            try:
                at = p.read_text()
            except: continue
            # For excel.xml: count cells in first header row that have Data ss:Type="String"
            artifact_cols = []
            if which == "excel":
                m = re.search(r"<Row[^>]*>(?:\s*<Cell(?:\s+[^>]*)?>(?:<Data[^>]*>[^<]*</Data>)?</Cell>\s*)+</Row>", at, re.S)
                if m:
                    first_row = m.group(0)
                    # extract cells, limit to first row only
                    cell_matches = re.findall(r"<Cell(?:\s+ss:Index=\"(\d+)\")?\s*(?:/>|>\s*(?:<[^>]*>[^<]*</[^>]*>)?\s*</Cell>)", first_row)
                    # simpler: count <Cell occurrences inside the first <Row with >1 cells
                    ncells = len(re.findall(r"<Cell(?:\s+[^>]*)?>", first_row))
                    # Only trust if >5 (something real) — not a 1-cell title
                    if ncells >= 6:
                        # Extract text from header cells
                        datas = re.findall(r"<Cell[^>]*><Data[^>]*>([^<]+)</Data></Cell>", first_row)
                        artifact_cols = [d.strip() for d in datas]
            if which == "gs":
                # Find fields: [...] array objects with "name":"X"
                gs_names = re.findall(r'"name"\s*:\s*"([^"]+)"', at)
                if gs_names:
                    artifact_cols = gs_names
            if artifact_cols and "fields" in sections:
                fnames, _ = extract_fields_from_csv(sections["fields"][0])
                if fnames:
                    # Normalize both to lowercase stripped
                    a_norm = [c.lower().strip().rstrip(":").replace(" ","") for c in artifact_cols]
                    f_norm = [c.lower().strip().rstrip(":").replace(" ","") for c in fnames]
                    if len(a_norm) == len(f_norm) and a_norm != f_norm:
                        # Same count but different order -> H3 confirmed for a module
                        # find first 2 positions where differs
                        diffs = [(i+1, fnames[i], artifact_cols[i]) for i in range(len(a_norm)) if a_norm[i] != f_norm[i]]
                        flaws.append(report("template-column-order-mismatch", "MEDIUM", str(rel),
                            f"{which} has {len(artifact_cols)} columns matching field count {len(fnames)} but ORDER differs at {len(diffs)} positions; first 5: {diffs[:5]}",
                            location=f"{artifact}"))
                    elif len(a_norm) != len(f_norm) and abs(len(a_norm) - len(f_norm)) >= 2:
                        flaws.append(report("template-column-count-mismatch", "HIGH", str(rel),
                            f"{which} has {len(artifact_cols)} columns but Fields declares {len(fnames)} (diff={len(a_norm)-len(fnames)})",
                            location=f"{artifact}"))

    # Also check nav in sibling README for H4 broken links after recent moves
    readme = skill_path.parent / "README.md"
    if readme.exists():
        rtxt = readme.read_text()
        for m in re.finditer(r"\[(?P<display>[^\]]+)\]\((?P<target>[^)\s]+)\)", rtxt):
            tgt = m.group("target").split("#",1)[0]
            if tgt.startswith("http") or tgt.startswith("#") or tgt in (".", "/"):
                continue
            try:
                resolved = (readme.parent / tgt).resolve()
                if str(ROOT) in str(resolved) and not resolved.exists():
                    flaws.append(report("broken-readme-link",
                        "HIGH" if "Previous" in m.group("display") or "Next" in m.group("display") or "Related" in m.group("display") or "index" in tgt.lower() or "skill" in tgt.lower() else "MEDIUM",
                        str(rel),
                        f"README.md link [{m.group('display')}]({m.group('target')}) does not resolve",
                        location=f"README.md line {rtxt.count(chr(10),0,m.start())+1}"))
            except:
                pass

    return flaws, kw_set

def main():
    # Gather all SKILL.md files
    all_skills = sorted(p for p in ROOT.rglob("SKILL.md") if ".git" not in p.parts and "node_modules" not in p.parts)
    print(f"Found {len(all_skills)} SKILL.md files")

    all_flaws = []
    keyword_map = {}
    for sp in all_skills:
        try:
            flaws, kws = test_skill(sp, all_skills)
        except Exception as e:
            flaws = [report("crash", "CRITICAL", str(sp.relative_to(ROOT)), f"crash: {e}")]
            kws = set()
        keyword_map[str(sp.relative_to(ROOT))] = kws
        all_flaws.extend(flaws)

    # Pairwise trigger keyword overlap test (H1)
    router_keys = {"skills/SKILL.md","skills/accounting-audit-system-builder/SKILL.md"}
    skill_names = [s for s in keyword_map.keys() if s not in router_keys]
    overlap_flaws_ids = set()
    for a, b in itertools.combinations(skill_names, 2):
        sa, sb = keyword_map[a], keyword_map[b]
        if not sa or not sb: continue
        inter = sa & sb
        union = sa | sb
        if len(union) == 0: continue
        j = len(inter)/len(union)
        # Report pairs with significant overlap (>0.6 Jaccard on >=5 shared tokens)
        if j >= 0.6 and len(inter) >= 5:
            if a not in overlap_flaws_ids:
                overlap_flaws_ids.add(a)
                all_flaws.append(report("trigger-keyword-overlap", "MEDIUM", a,
                    f"Jaccard={j:.2f} vs {b} — {len(inter)} shared keywords: {sorted(inter)[:12]}"))
            if b not in overlap_flaws_ids:
                overlap_flaws_ids.add(b)
                all_flaws.append(report("trigger-keyword-overlap", "MEDIUM", b,
                    f"Jaccard={j:.2f} vs {a} — {len(inter)} shared keywords: {sorted(inter)[:12]}"))

    results = {"flaws": all_flaws, "skill_count": len(all_skills)}
    (OUT/"results.json").write_text(json.dumps(results, indent=2))

    # Summary markdown
    lines = [f"# Pre-fix simulator run — {len(all_skills)} SKILL.md files", ""]
    c = Counter(f["type"].split(":")[-1] for f in all_flaws)
    sev = Counter(f["severity"] for f in all_flaws)
    lines.append(f"## Totals")
    lines.append(f"- Files: {len(all_skills)}")
    lines.append(f"- Total flaws: {len(all_flaws)}")
    lines.append(f"- By severity: " + ", ".join(f"{k}={v}" for k,v in sev.most_common()))
    lines.append(f"- By type:")
    for t, n in c.most_common():
        lines.append(f"  - **{t}**: {n}")
    lines.append("")
    # Per skill breakdown of flaws
    by_skill = defaultdict(list)
    for f in all_flaws:
        by_skill[f["skill"]].append(f)
    lines.append("## Per-skill flaws")
    for sk in sorted(by_skill.keys(), key=lambda s: (-len(by_skill[s]), s)):
        fs = by_skill[sk]
        lines.append(f"### {sk} ({len(fs)})")
        for f in fs:
            lines.append(f"- [{f['severity']}] `{f['type'].split(':')[-1]}` — {f['evidence'][:160]}{'…' if len(f['evidence'])>160 else ''}  ({f['location'] or 'n/a'})")
        lines.append("")
    (OUT/"summary.md").write_text("\n".join(lines))
    print(f"Wrote {OUT/'results.json'} ({len(all_flaws)} flaws) and {OUT/'summary.md'}")
    print(f"Severity: {dict(sev)}")
    print(f"Types:    {dict(c)}")

if __name__ == "__main__":
    main()
