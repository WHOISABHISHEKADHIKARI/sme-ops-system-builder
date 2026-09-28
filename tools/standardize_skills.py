#!/usr/bin/env python3
"""Apply the shared execution contract link and tool-neutral metadata to every skill."""

from pathlib import Path
import os
import re
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
import skillmd


ROOT = Path(__file__).resolve().parent.parent
CONTRACT = ROOT / "references" / "execution-contract.md"
MARKER = "Follow the [shared execution contract]"
EXAMPLE_PREFIX = "One example row per artifact, visibly fake."
NOTION_GATE_MARKER = "**Notion needs a connected workspace first.**"
ROUTER_NOTION_MARKER = "**Notion is the module's step, not this one's.**"
# The module owns the artifact steps, so the gate goes in the step that emits artifacts.
MODULE_NOTION_STEP = "### Step 5 - Build only on request"
# A router stops at the shortlist, so the gate goes in the step that hands the module off.
ROUTER_NOTION_STEP = ("### Step 3 - Hand off", "### Step 4 - Hand off",
                      "### Step 5 - Never build here", "### Step 5 - Output")
NOTION_PITFALL = (
    "- **Problem:** the Notion mapping is handed over with no workspace connected.\n"
    "  **Solution:** the connection prerequisite goes first, and a mapping handed over as\n"
    "  text is labelled unverified until the workspace is connected.\n"
)
EMPTY_TEMPLATE_RULE = (
    "The rows above are documentation examples only. Emit empty templates unless the "
    "user explicitly requests examples."
)
EXCEL_COMPATIBLE_CSV_RULE = (
    "For an Excel-compatible CSV, use UTF-8 with a byte order mark so Excel opens the\n"
    "text correctly. A CSV is not an `.xlsx` workbook; create `.xlsx` only when the user\n"
    "requests a workbook."
)
INPUT_INDEX_HEADING = "## Input Modules"
CATALOG_ROW = re.compile(
    r"^\| (?P<title>[^|]+?) \| (?P<code>[^|]*) \| (?P<tier>[^|]*) \| (?P<fields>\d+) \| "
    r"`(?P<path>[^`]+)` \|\s*$")
CATALOG_LAYER = re.compile(r"^## (Layer \d+: .+)$")
INPUT_INDEX_INTRO = (
    "A helper has no field list of its own, so its input is a module: the Field Reference\n"
    "that module already confirmed. Read that section - field names, types, order,\n"
    "requiredness, options and calculations - and render exactly that. The list below is\n"
    "every module that owns a field list, grouped by the layer its catalog gives it, and it\n"
    "is generated from those catalogs and the module files, so it cannot name a module that\n"
    "does not exist. `references/catalog.md` is the index to show a user; the module's own\n"
    "`SKILL.md` holds the field list."
)
INPUT_INDEX_FOOTER = (
    "If the user has not named a module, ask which one before building: a file rendered from\n"
    "a guess is the guess again, in a format the user did not choose."
)


def catalog_groups(catalog):
    """Layer -> [(title, fields, slug)], read from a catalog file.

    The catalogs are the repo's own grouping of the modules, so reusing them keeps this
    generator from inventing a second ordering that disagrees with the published one.
    The ``Fields`` column is read but not trusted for the count: the number is taken from
    the module's Field Reference, which is what every other artifact is checked against.
    """
    text = Path(catalog).read_text(encoding="utf-8")
    out, layer = [], None
    for line in text.splitlines():
        heading = CATALOG_LAYER.match(line)
        if heading:
            layer = heading.group(1)
            continue
        row = CATALOG_ROW.match(line)
        if not row or layer is None:
            continue
        slug = os.path.basename(os.path.dirname(row.group("path")))
        out.append([layer, row.group("title").strip(), slug])
    return out


def module_path(slug, pack=None):
    """The real SKILL.md path for a catalog row.

    A catalog row is written pack-relative even when the module has been flattened into
    ``skills/``, so the path is resolved against the filesystem: the pack first, then the
    flat layout. The slug was taken from the row's own path, and no flat module shares a
    name with a pack module, so the two layouts cannot be confused.
    """
    for prefix in ([pack] if pack else []) + [None]:
        path = skillmd.module_dir(ROOT, "%s/%s" % (prefix, slug) if prefix else slug)
        path = os.path.join(path, "SKILL.md")
        if os.path.isfile(path):
            return path
    raise ValueError("no SKILL.md for catalog row %r in %s" % (slug, pack or "the flat layout"))


def input_index_groups():
    """[(group label, [index line, ...])] for every module that owns a field list.

    Read from all three catalogs, because the flat layout is not one catalog: the
    accounting and audit modules were flattened out of their pack and are still listed
    in that pack's catalog. The union is checked against the modules on disk, so a module
    added without a catalog row fails this run rather than being silently absent from the
    index.
    """
    out, seen = [], set()
    sources = [(ROOT / "references" / "catalog.md", None)]
    sources.extend((Path(skillmd.module_dir(ROOT, p)) / "catalog.md", p)
                   for p in skillmd.all_packs(ROOT))
    for catalog, pack in sources:
        rows = catalog_groups(catalog)
        if not rows:
            continue
        by_layer, order = {}, []
        for layer, title, slug in rows:
            path = module_path(slug, pack)
            d = skillmd.read_skill(path)
            rel = os.path.relpath(path, ROOT).replace(os.sep, "/")
            by_layer.setdefault(layer, []).append(
                "- `%s` - %s (%d fields)" % (rel, d['title'], len(d['fields'])))
            if layer not in order:
                order.append(layer)
            # Qualified from the resolved path, not from the catalog the row came from:
            # the accounting pack's catalog still lists its 16 modules after they were
            # flattened into skills/, so the catalog says pack and the disk says flat.
            seen.add(os.path.relpath(os.path.dirname(path),
                                     os.path.join(ROOT, "skills")).replace(os.sep, "/"))
        for layer in order:
            label = "**%s**" % layer
            if pack:
                label = "**Sub-pack `%s` - %s**" % (pack, layer)
            out.append((label, by_layer[layer]))
    missing = set(skillmd.table_slugs(ROOT)) - seen
    if missing:
        raise ValueError("modules missing from every catalog: %s"
                         % ", ".join(sorted(missing)))
    return out


def input_index():
    """The Input Modules section, regenerated from the repo on every run."""
    parts = [INPUT_INDEX_HEADING, "", INPUT_INDEX_INTRO, ""]
    for label, lines in input_index_groups():
        parts.append("%s - %d module%s" % (label, len(lines),
                                            "" if len(lines) == 1 else "s"))
        parts.append("")
        parts.extend(lines)
        parts.append("")
    parts.append(INPUT_INDEX_FOOTER)
    return "\n".join(parts)


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


def helper_link(path):
    """Relative path from a module to the manual-import helper's SKILL.md.

    Computed rather than written out because the two layouts differ in depth: a flat
    module is one level under skills/, a sub-pack module is two.
    """
    target = os.path.join(ROOT, 'skills', 'notion-manual-import', 'SKILL.md')
    return Path(os.path.relpath(target, os.path.dirname(path))).as_posix()


def notion_gate(path):
    """The rule a module repeats from the shared contract. Wording stays in the contract."""
    return (
        "\n\n**Notion needs a connected workspace first.** When the user selects Notion as the\n"
        "output, emit the connection prerequisite from the\n"
        f"[shared execution contract]({contract_link(path)}) verbatim before\n"
        "the Notion mapping, then stop and wait for the reply \"Notion connected.\" If the user\n"
        "would rather not connect, emit the mapping as text, add one line saying it is\n"
        "unverified until the workspace is connected, and offer\n"
        f"[notion-manual-import]({helper_link(path)}) for the full manual path.\n"
        "Never claim a connection exists, and never ask for a Notion password or token."
    )


def router_notice():
    return (
        "\n\n**Notion is the module's step, not this one's.** If the user wants the build in\n"
        "Notion, hand off first: the module emits the connection prerequisite and waits for\n"
        "\"Notion connected.\" This router never prints the prerequisite itself."
    )


def after_first_paragraph(text, heading):
    """Insertion point just past a step heading's first paragraph.

    The paragraph is taken as a run of non-blank lines rather than as fixed wording,
    because the steps differ per skill: the accounting pack, the 360 module and the brand
    router each word the same step differently, and a fixed sentence matched none of them.
    """
    m = re.search(r"^%s\n+(.*?)(?=\n\n)" % re.escape(heading), text, re.S | re.M)
    if not m:
        raise ValueError(f"no first paragraph under {heading!r}")
    return m.end(1)


def add_notion_gate(path, text):
    if NOTION_GATE_MARKER in text or ROUTER_NOTION_MARKER in text:
        return text
    if os.fspath(path) in helpers(ROOT):
        # The manual-import helper is the unconnected path. It states that in its own
        # Step 5 and must never be given the prerequisite to emit, or it would gate a
        # build on the very connection it exists to avoid needing.
        return text
    is_router = os.fspath(path) in routers(ROOT)
    if is_router:
        step = next((h for h in ROUTER_NOTION_STEP if h in text), None)
        if step is None:
            raise ValueError(f"no hand-off step to anchor the Notion notice: {path}")
        block = router_notice()
    else:
        if MODULE_NOTION_STEP not in text:
            raise ValueError(f"no {MODULE_NOTION_STEP} to anchor the Notion gate: {path}")
        step = MODULE_NOTION_STEP
        block = notion_gate(path)
    at = after_first_paragraph(text, step)
    return text[:at] + block + text[at:]


def add_notion_pitfall(path, text):
    """A module repeats the gate as a pitfall; a router and a helper do not.

    A router has no table to get wrong, and the helper already carries the failure mode
    it exists to prevent, in its own Common Pitfalls.
    """
    if (os.fspath(path) in routers(ROOT) or os.fspath(path) in helpers(ROOT)
            or "the Notion mapping is handed over" in text):
        return text
    m = re.search(r"^## Common Pitfalls\n\n", text, re.M)
    if not m:
        raise ValueError(f"no Common Pitfalls section: {path}")
    return text[:m.end()] + NOTION_PITFALL + text[m.end():]


def routers(root):
    """Absolute paths of the root router and every sub-pack router.

    Compared against the absolute paths :func:`main` iterates, so the two sides are
    normalised the same way: a router seen as ``SKILL.md`` and a module as
    ``/repo/skills/x/SKILL.md`` would otherwise never compare equal.
    """
    return {os.path.normpath(os.path.abspath(os.fspath(p)))
            for p in skillmd.all_routers(root)}


def helpers(root):
    """Absolute paths of the skills that declare ``table: none``."""
    return {os.path.normpath(os.path.abspath(os.path.join(root, 'skills', s, 'SKILL.md')))
            for s in skillmd.all_slugs(root)
            if skillmd.is_helper(os.path.join(root, 'skills', s, 'SKILL.md'))}


def add_input_index(path, text):
    """Give a helper the full list of modules it can render, right after its Field Reference.

    Regenerated rather than appended: the section is replaced wholesale on every run, so
    adding a module refreshes all four helpers with one command instead of leaving four
    hand-maintained copies to drift. A module or router has no input index - it owns the
    field list, and the list of other modules is its catalog's job.
    """
    if os.fspath(path) not in helpers(ROOT):
        return text
    # Drop the previous block, so the section is rewritten rather than duplicated.
    text = re.sub(r"^%s\n.*?(?=^## |\Z)" % re.escape(INPUT_INDEX_HEADING), "", text,
                  flags=re.S | re.M)
    m = re.search(r"^## Field Reference\n", text, re.M)
    if not m:
        raise ValueError(f"no Field Reference to anchor the input index: {path}")
    at = re.search(r"^## ", text[m.end():], re.M)
    # The index belongs with the field list it describes, so it follows Field Reference.
    cut = m.end() + (at.start() if at else len(text) - m.end())
    return text[:cut].rstrip("\n") + "\n\n" + input_index() + "\n\n" + text[cut:]


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

    text = add_notion_gate(path, text)
    text = add_notion_pitfall(path, text)
    text = add_input_index(path, text)

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
