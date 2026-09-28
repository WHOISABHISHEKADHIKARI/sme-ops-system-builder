#!/usr/bin/env python3
"""Check that the published indexes agree with the modules they index.

Every index in this repository is hand-maintained prose, and each one went wrong the same
way: 158fc1e flattened 16 accounting modules out of their sub-pack into skills/, and the
module files moved while the indexes kept their old numbers. The root README lost the 16
rows outright, the catalog claimed 71 when there were 100, five rows carried field counts
that no longer matched their module, and the brand pack's 13 links pointed at
skills/<slug>/ where no such directory exists.

None of that is visible from checking a single module, which is what check.py does, so it
is checked here instead: for each index, every module that belongs in it is present
exactly once, every row's link resolves, and every tier and field count is the one the
module itself declares. The module is the source of truth throughout - a catalog that
disagrees with a SKILL.md is the thing that is wrong.

Usage: check_indexes.py
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import skillmd

ROOT = os.environ.get('SKILL_REPO') or os.path.dirname(
    os.path.dirname(os.path.abspath(__file__)))

# | Title | Code | Fits | Fields | `path` |      - the catalogs and the root README
CATALOG_ROW = re.compile(
    r"^\| (?P<title>[^|]+?) \| (?P<code>[^|]*) \| (?P<tier>\w+) \| (?P<fields>\d+) \| "
    r"`(?P<path>[^`]+)` \|\s*$", re.M)
# | [Title](./skills/slug/README.md) | Fits | Fields | One row is |   - the root index
README_ROW = re.compile(
    r"^\| \[[^\]]+\]\(\./skills/(?P<slug>[^/]+)/README\.md\) \| (?P<tier>\w+) \| "
    r"(?P<fields>\d+) \| [^|]+\|\s*$", re.M)

# The flat indexes list the flat modules; each pack's own catalog lists its pack.
INDEXES = (
    ('references/catalog.md', CATALOG_ROW, 'flat'),
    ('README.md', README_ROW, 'flat'),
    ('skills/accounting-audit-system-builder/catalog.md', CATALOG_ROW, 'promoted'),
    ('skills/brand-growth-system-builder/catalog.md', CATALOG_ROW, 'pack'),
)


def expected_slugs(kind):
    """The module names an index is supposed to carry, given what kind of index it is.

    Names, not slugs: a row is identified by the directory it links to, so a pack module
    arrives here as `logo-image-design` and is resolved back to its pack by
    :func:`skillmd.resolve_slug`. Comparing qualified and bare forms would report every
    pack module as missing from its own catalog.
    """
    tables = skillmd.table_slugs(ROOT)
    if kind == 'pack':
        pack = 'brand-growth-system-builder'
        return {s.split('/', 1)[1] for s in tables if s.startswith(pack + '/')}
    # 'promoted' is the accounting cycle catalog: its modules now live flat, so it is a
    # second view of names the flat index already carries. Its rows are still checked for
    # links, tiers and field counts, but completeness is not asserted for it.
    return {s for s in tables if '/' not in s}


def read(path):
    with open(os.path.join(ROOT, path), encoding='utf-8') as fh:
        return fh.read()


def row_target(row):
    """The repo-relative SKILL.md a row points at, whichever index shape it came from.

    The catalogs link to the skill itself; the root README links to the module's page. Both
    name the module by the directory they point into, so the module is read from that
    directory either way.
    """
    if 'path' in row:
        return row['path']
    return 'skills/%s/SKILL.md' % row['slug']


def check_index(path, row_re, kind):
    issues = []
    bad = lambda tag, detail: issues.append((tag, detail))
    text = read(path)
    rows = [m.groupdict() for m in row_re.finditer(text)]

    names = []
    for row in rows:
        target = row_target(row)
        if not os.path.isfile(os.path.join(ROOT, target)):
            bad('broken link', '%s -> %s' % (row.get('title') or row.get('slug'), target))
            continue
        name = os.path.basename(os.path.dirname(target))
        names.append(name)
        slug = skillmd.resolve_slug(ROOT, name) or name
        module = skillmd.read_module(ROOT, slug)
        if module['tier'] and module['tier'] != row['tier']:
            bad('tier', '%s: index says %s, module says %s'
                % (name, row['tier'], module['tier']))
        if module['fields'] and len(module['fields']) != int(row['fields']):
            bad('field count', '%s: index says %s, module has %d'
                % (name, row['fields'], len(module['fields'])))

    for name in sorted(set(names)):
        if names.count(name) > 1:
            bad('duplicate row', '%s listed %d times' % (name, names.count(name)))

    listed = set(names)
    if kind != 'promoted':
        want = expected_slugs(kind)
        for name in sorted(want - listed):
            bad('missing module', name)
        for name in sorted(listed - want):
            bad('unknown module', name)
    return issues


def main():
    failures = 0
    for path, row_re, kind in INDEXES:
        if not os.path.exists(os.path.join(ROOT, path)):
            print('MISSING  %s' % path)
            failures += 1
            continue
        issues = check_index(path, row_re, kind)
        if issues:
            failures += len(issues)
            print('FAIL  %s' % path)
            for tag, detail in issues:
                print('   %-14s %s' % (tag, detail))
        else:
            print('ok    %s' % path)

    if failures:
        print('\nindex check: %d problem(s)' % failures)
        return 1
    print('\nindex check: OK - every module is listed once, and every row matches its module')
    return 0


if __name__ == '__main__':
    sys.exit(main())
