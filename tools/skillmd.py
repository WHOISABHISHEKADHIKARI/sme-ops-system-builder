#!/usr/bin/env python3
"""Read a SKILL.md into a dict.

The field list in the Field Reference table is the single source of truth for a
module: the CSV header, the SQL columns, the JSON Schema properties and the Notion
mapping are all checked against it by ``check.py``. This module reads the same
table, so anything that needs to reason about a module (the SEO tool, for one)
sees exactly what the checker sees.

``check.py`` deliberately keeps its own stricter parsing, because it treats the table
as authoritative and reports disagreements between the table and the other three
artifacts. Sharing this module there would hide the very drift it exists to catch.

Usage:
    from skillmd import read_skill, keyword_for
    d = read_skill('skills/leave-management/SKILL.md')
    print(d['title'], len(d['fields']))
"""
import os
import re

BT = chr(96)

# Titles that do not read well as a lowercase search phrase.
KEYWORD_FIX = {
    'sop-company-wiki': ('SOP and company wiki', 'SOP & Company Wiki'),
    'esop-equity-tracker': ('ESOP equity tracker', 'ESOP Equity Tracker'),
    'okr-system': ('OKR system', 'OKR System'),
    'kpi-tracker': ('KPI tracker', 'KPI Tracker'),
    'dei-dashboard': ('DEI dashboard', 'DEI Dashboard'),
    '360-feedback-system': ('360 degree feedback', '360° Feedback'),
}


def keyword_for(slug, title):
    """Return (search phrase, display form) for a module."""
    if slug in KEYWORD_FIX:
        return KEYWORD_FIX[slug]
    t = title.replace('&', 'and').replace('°', ' degree ')
    return re.sub(r'\s+', ' ', t).strip().lower(), title


def section(text, name):
    """Body of `## <name>`, up to the next H2 or the end of the document.

    The terminator has to allow end-of-text as well as the next heading. A pattern
    that only looks ahead for another `## ` silently returns nothing when the section
    happens to be last, which loses content with no error: a trailing FAQ section
    yields no FAQPage schema, and a trailing `## Select Options` yields no dropdowns
    in the generated workbook.
    """
    m = re.search(r'## %s\n(.*?)(?=\n## |\Z)' % re.escape(name), text, re.S)
    return m.group(1) if m else ''


def select_options(text):
    """Map select field name -> its options, from the `## Select Options` section.

    The section looks like:

        **Leave Type**

        ```
        Annual | Sick | Casual
        ```

    A module with no select fields still has the section, just with no pairs in it.
    """
    out = {}
    for field, block in re.findall(r'\*\*(.+?)\*\*\n+```\n(.*?)\n```',
                                   section(text, 'Select Options'), re.S):
        out[field.strip()] = [o.strip() for o in block.split('|') if o.strip()]
    return out


def slugify(s):
    return re.sub(r'[^a-z0-9]+', '-', s.lower().replace('&', ' ')).strip('-')


def is_helper(path):
    """True when a SKILL.md declares ``table: none`` in its frontmatter.

    A helper works on another module's field list instead of owning one - the manual
    Notion import path formats a database the active module already defines, so it has
    no Field Reference table, no CSV, and no SQL of its own to keep in agreement with
    anything. The checkers exempt it from the artifact requirements for the same
    reason a router is exempt: there is no table for the artifacts to describe.

    Two conditions, because either alone lies. The key states the intent, and the
    absent Field Reference *table* is what the tools can actually verify, so a module
    that claims ``table: none`` and then ships a pipe table is not treated as a helper.
    The section heading may still be there, explaining that the list lives elsewhere.
    """
    text = open(path).read()
    m = re.match(r'---\n(.*?)\n---\n', text, re.S)
    if not m or not re.search(r'^table:\s*none\s*$', m.group(1), re.M):
        return False
    return not re.search(r'## Field Reference\n\n\|', text)


def block(text, lang):
    """The contents of the first ```<lang> fence, or None when there is none."""
    m = re.search(r'```%s\n(.*?)\n```' % lang, text, re.S)
    return m.group(1) if m else None


def read_skill(path):
    """Parse one SKILL.md. Raises KeyError if a required section is missing."""
    t = open(path).read()
    fm = re.match(r'---\n(.*?)\n---\n', t, re.S)
    d = {'path': path, 'slug': os.path.basename(os.path.dirname(path)),
         'helper': is_helper(path)}

    def sec(name, nxt=None):
        return section(t, name).strip()

    d['title'] = re.search(r'^# (.+)$', t, re.M).group(1).strip()
    d['what_is'] = sec('Overview', 'When to Use This Skill')
    d['triggers'] = [re.sub(r'^[-*] ', '', l).strip()
                     for l in sec('When to Use This Skill', 'How It Works').split('\n')
                     if l.strip().startswith('- ')][:4]
    d['limits'] = sec('Limitations', 'Security & Safety Notes')
    d['safety'] = sec('Security & Safety Notes', 'Common Pitfalls')
    d['related'] = re.findall(r'^- `([a-z0-9-]+)` - (.+)$',
                              sec('Related Skills', 'Reusable Prompt'), re.M)
    d['options'] = select_options(t)
    d['csv'] = block(t, 'csv')
    d['sql'] = block(t, 'sql')
    d['json'] = block(t, 'json')
    d['prompt'] = re.search(r'## Reusable Prompt\n\n```\n(.*?)\n```', t, re.S).group(1).strip()
    d['first_q'] = re.search(r'> \*\*Q:\*\* (.+)', t).group(1).strip()

    for key, pat in (('approach', r'\*\*Recommended approach:\*\* (.+)'),
                     ('why', r'\*\*Why this one:\*\* (.+)'),
                     ('flow', r'\*\*Workflow:\*\* (.+)')):
        m = re.search(pat, t)
        d[key] = m.group(1).strip() if m else ''

    # the layer line runs on: "Layer 4: Manage. Fits: Growth stage. Table code: n/a."
    m = re.search(r'Layer (\d+): ([^.|]+?)\.', t)
    d['layer'] = 'Layer %s: %s' % (m.group(1), m.group(2).strip()) if m else ''
    m = re.search(r'Fits: (\w+) stage', t)
    d['tier'] = m.group(1) if m else ''

    # A helper has no field list of its own: it renders whatever the active module
    # defines, so the table is optional for it and its absence is not a parse failure.
    d['fields'] = []
    table = re.search(r'## Field Reference\n\n(\|.*?)\n\n', t, re.S)
    if table:
        for line in [x for x in table.group(1).split('\n')
                     if x.startswith('|') and '---' not in x][1:]:
            cols = [c.strip() for c in line.strip('|').split('|')]
            d['fields'].append((cols[1].strip(BT), cols[2].strip(BT)))

    if fm:
        m = re.search(r'^description: "(.*)"$', fm.group(1), re.M)
        d['desc'] = m.group(1) if m else ''
    else:
        d['desc'] = ''
    return d


def module_dir(root, slug):
    """Directory holding a module's files.

    A slug may be qualified as ``pack/slug`` for a module inside a sub-pack, so one
    path join serves both the flat layout and the nested one.
    """
    return os.path.join(root, 'skills', slug)


def read_module(root, slug):
    return read_skill(os.path.join(module_dir(root, slug), 'SKILL.md'))


def _is_pack(path):
    """A sub-pack holds its own router plus its own catalog.

    Two signals, because both occur in the repository: a pack normally holds child
    module directories, but a pack whose modules were promoted to the flat layout
    is left holding only its router and its catalog. A flat module has neither, so
    testing for a sibling ``catalog.md`` keeps a pack router from being read as a
    module once its modules have moved.
    """
    if not os.path.isdir(path):
        return False
    if os.path.isfile(os.path.join(path, 'catalog.md')):
        return True
    for current, dirs, files in os.walk(path):
        if current != path and 'SKILL.md' in files:
            return True
    return False


def all_packs(root):
    """Sub-pack names: directories under skills/ that hold module directories.

    A sub-pack is a second router plus its own modules, kept in one folder so the
    flat module surface stays flat. Its router is not a module and is not returned
    by :func:`all_slugs`.
    """
    base = os.path.join(root, 'skills')
    return sorted(n for n in os.listdir(base) if _is_pack(os.path.join(base, n)))


def all_slugs(root):
    """Every module slug in the repository, sorted.

    Modules in a sub-pack come back qualified as ``pack/slug``; flat modules come
    back bare. Callers that build a path with :func:`module_dir` need no change.
    """
    base = os.path.join(root, 'skills')
    out = []
    for n in sorted(os.listdir(base)):
        d = os.path.join(base, n)
        if not os.path.isdir(d):
            continue
        if _is_pack(d):
            out.extend('%s/%s' % (n, m) for m in sorted(os.listdir(d))
                       if os.path.isfile(os.path.join(d, m, 'SKILL.md')))
        elif os.path.isfile(os.path.join(d, 'SKILL.md')):
            out.append(n)
    return out


def all_routers(root):
    """Every router SKILL.md path: the root router plus one per sub-pack."""
    out = [os.path.join(root, 'SKILL.md')]
    out.extend(os.path.join(root, 'skills', p, 'SKILL.md') for p in all_packs(root))
    return out


def table_slugs(root):
    """The slugs that own a field list, i.e. every slug except the helpers.

    The generators that emit a CSV, a workbook or a Google Sheet need a Field Reference
    to emit anything from. A helper has none, so it is dropped here rather than being
    discovered as a crash deep inside a writer.
    """
    return [s for s in all_slugs(root)
            if not is_helper(os.path.join(module_dir(root, s), 'SKILL.md'))]


def all_skill_files(root):
    """Every SKILL.md that :func:`all_slugs` and :func:`all_routers` cover."""
    return ([os.path.join(module_dir(root, s), 'SKILL.md') for s in all_slugs(root)]
            + all_routers(root))


if __name__ == '__main__':
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    for slug in all_slugs(root):
        d = read_module(root, slug)
        print('%-30s %2d fields  %-8s %s' % (slug, len(d['fields']),
                                              d['tier'] or '-', d['title']))
