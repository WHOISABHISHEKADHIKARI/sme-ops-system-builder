import os, re, glob, json, csv, io, collections, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import skillmd
ROOT = os.environ.get('SKILL_REPO') or os.path.dirname(
    os.path.dirname(os.path.abspath(__file__)))
REQUIRED_KEYS = ['name', 'description', 'category', 'risk', 'source', 'source_type',
                 'date_added', 'author', 'tags', 'tools']
REQUIRED_SECTIONS = ['Overview', 'When to Use This Skill', 'How It Works', 'Examples',
                     'Best Practices', 'Limitations', 'Security & Safety Notes',
                     'Common Pitfalls', 'Related Skills']
BT = chr(96)
# Every module plus every router: flat modules, sub-pack modules, the root router and
# each sub-pack router. skillmd owns discovery so the tools cannot drift apart.
files = skillmd.all_skill_files(ROOT)
routers = set(skillmd.all_routers(ROOT))
errs = collections.defaultdict(list)
rows = []
for f in files:
    # A nested module's own name is its folder name; the pack prefix is a path detail.
    slug = os.path.basename(os.path.dirname(f))
    t = open(f).read()
    m = re.match(r'^---\n(.*?)\n---\n', t, re.S)
    if not m:
        errs['no frontmatter'].append(slug); continue
    fm = m.group(1)
    keys = re.findall(r'^([a-z_]+):', fm, re.M)
    for k in REQUIRED_KEYS:
        if k not in keys: errs['missing key ' + k].append(slug)
    dm = re.search(r'^description:\s*"(.*)"\s*$', fm, re.M)
    if not dm:
        errs['description not quoted string'].append(slug)
    else:
        d = dm.group(1)
        if len(d) > 200: errs['description >200 (%d)' % len(d)].append(slug)
        if not re.search(r'[Uu]se (for|when)', d): errs['no trigger clause'].append(slug)
    nm = re.search(r'^name:\s*(\S+)', fm, re.M)
    if nm and nm.group(1) != slug: errs['name != folder'].append(slug)
    heads = set(x.strip() for x in re.findall(r'^## (.+)$', t, re.M))
    for s in REQUIRED_SECTIONS:
        if s not in heads: errs['missing section ' + s].append(slug)
    if 'Reusable Prompt' not in heads: errs['no Reusable Prompt'].append(slug)
    if not t.rstrip().endswith('```'): errs['does not end with prompt block'].append(slug)
    # A router routes between modules; it owns no table of its own, so the
    # per-module artifact requirements below do not apply to it.
    if f in routers:
        rows.append((slug, len(t), 0))
        continue
    if '```csv' not in t or '```sql' not in t or '```json' not in t:
        errs['missing an artifact block'].append(slug)
    # CSV parses, 2 rows
    csvblk = re.search(r'```csv\n(.*?)\n```', t, re.S)
    ncol = 0
    if csvblk:
        r = list(csv.reader(io.StringIO(csvblk.group(1))))
        if len(r) != 2: errs['csv not header+1 example row'].append(slug)
        elif len(r[0]) != len(r[1]): errs['csv row width mismatch'].append(slug)
        else: ncol = len(r[0])
    else:
        errs['no csv block'].append(slug)
    # SQL/JSON valid
    sqlb = re.search(r'```sql\n(.*?)\n```', t, re.S)
    if sqlb and 'CREATE TABLE' not in sqlb.group(1): errs['sql has no CREATE TABLE'].append(slug)
    jsb = re.search(r'```json\n(.*?)\n```', t, re.S)
    if jsb:
        try: json.loads(jsb.group(1))
        except Exception as e: errs['json invalid: %s' % str(e)[:30]].append(slug)
    else: errs['no json block'].append(slug)
    if re.search(r'\bDescribe |Here is |I will |Sure,', t): errs['prose filler'].append(slug)
    rows.append((slug, len(t), ncol))

print('files checked:', len(files))
if not errs:
    print('ALL CHECKS PASS')
for k, v in errs.items():
    print('%-34s %3d  %s' % (k, len(v), v[:4]))
sizes = [r[1] for r in rows]
print('SKILL.md size: min %d max %d mean %d' % (min(sizes), max(sizes), sum(sizes) // len(sizes)))
readmes = ([os.path.join(skillmd.module_dir(ROOT, s), 'README.md')
            for s in skillmd.all_slugs(ROOT)]
           + [os.path.join(os.path.dirname(f), 'README.md') for f in routers])
readmes = [f for f in readmes if os.path.isfile(f)]
rs = [os.path.getsize(f) for f in readmes]
print('README files: %d, total %d KB' % (len(readmes), sum(rs) // 1024))
repo_files = [f for f in glob.glob(ROOT + '/**/*', recursive=True) if os.path.isfile(f)]
print('repo total: %d KB across %d files' % (
    sum(os.path.getsize(f) for f in repo_files) // 1024, len(repo_files)))
