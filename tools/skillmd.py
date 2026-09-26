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


def select_options(text):
    """Map select field name -> its options, from the `## Select Options` section.

    The section looks like:

        **Leave Type**

        ```
        Annual | Sick | Casual
        ```

    A module with no select fields still has the section, just with no pairs in it.
    """
    m = re.search(r'## Select Options\n(.*?)(?=\n## )', text, re.S)
    if not m:
        return {}
    out = {}
    for field, block in re.findall(r'\*\*(.+?)\*\*\n+```\n(.*?)\n```', m.group(1), re.S):
        out[field.strip()] = [o.strip() for o in block.split('|') if o.strip()]
    return out


def slugify(s):
    return re.sub(r'[^a-z0-9]+', '-', s.lower().replace('&', ' ')).strip('-')


def read_skill(path):
    """Parse one SKILL.md. Raises KeyError if a required section is missing."""
    t = open(path).read()
    fm = re.match(r'---\n(.*?)\n---\n', t, re.S)
    d = {'path': path, 'slug': os.path.basename(os.path.dirname(path))}

    def sec(name, nxt):
        m = re.search(r'## %s\n(.*?)(?=\n## %s\n)' % (name, nxt), t, re.S)
        return m.group(1).strip() if m else ''

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
    d['csv'] = re.search(r'```csv\n(.*?)\n```', t, re.S).group(1)
    d['sql'] = re.search(r'```sql\n(.*?)\n```', t, re.S).group(1)
    d['json'] = re.search(r'```json\n(.*?)\n```', t, re.S).group(1)
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

    table = re.search(r'## Field Reference\n\n(\|.*?)\n\n', t, re.S).group(1)
    d['fields'] = []
    for line in [x for x in table.split('\n') if x.startswith('|') and '---' not in x][1:]:
        cols = [c.strip() for c in line.strip('|').split('|')]
        d['fields'].append((cols[1].strip(BT), cols[2].strip(BT)))

    if fm:
        m = re.search(r'^description: "(.*)"$', fm.group(1), re.M)
        d['desc'] = m.group(1) if m else ''
    else:
        d['desc'] = ''
    return d


def module_dir(root, slug):
    return os.path.join(root, 'skills', slug)


def read_module(root, slug):
    return read_skill(os.path.join(module_dir(root, slug), 'SKILL.md'))


def all_slugs(root):
    """Every module slug in the repository, sorted."""
    base = os.path.join(root, 'skills')
    return sorted(n for n in os.listdir(base)
                  if os.path.isfile(os.path.join(base, n, 'SKILL.md')))


if __name__ == '__main__':
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    for slug in all_slugs(root):
        d = read_module(root, slug)
        print('%-30s %2d fields  %-8s %s' % (slug, len(d['fields']),
                                              d['tier'] or '-', d['title']))
