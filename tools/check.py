#!/usr/bin/env python3
"""Per-module checker.

The Field Reference table is generated straight from the one field list, so it is
treated as the source of truth. CSV, SQL, JSON Schema and the Notion mapping must
all agree with it exactly. Usage: check.py <slug|all> [-v]
"""
import re, os, sys, io, csv, json, glob, collections, datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import skillmd

ROOT = os.environ.get('SKILL_REPO') or os.path.dirname(
    os.path.dirname(os.path.abspath(__file__)))
TYPES = {'id', 'text', 'long_text', 'select', 'checkbox', 'number', 'currency',
         'date', 'datetime', 'email', 'url', 'relation'}
SQLT = {'id': 'SERIAL PRIMARY KEY', 'text': 'VARCHAR(255)', 'long_text': 'TEXT',
        'url': 'TEXT', 'email': 'VARCHAR(255)', 'relation': 'VARCHAR(255)',
        'select': 'VARCHAR(100)', 'checkbox': 'BOOLEAN', 'number': 'NUMERIC',
        'currency': 'NUMERIC(14,2)', 'date': 'DATE', 'datetime': 'TIMESTAMP'}
JSONT = {'id': ('integer', None), 'text': ('string', None), 'long_text': ('string', None),
         'select': ('string', None), 'relation': ('string', None), 'url': ('string', 'uri'),
         'email': ('string', 'email'), 'number': ('number', None),
         'currency': ('number', None), 'date': ('string', 'date'),
         'datetime': ('string', 'date-time'), 'checkbox': ('boolean', None)}
NOTIONT = {'id': 'Text', 'text': 'Text', 'long_text': 'Text', 'select': 'Select',
           'checkbox': 'Checkbox', 'number': 'Number', 'currency': 'Number',
           'date': 'Date', 'datetime': 'Date', 'email': 'Email', 'url': 'URL',
           'relation': 'Relation'}
NOTION_OK = set(NOTIONT.values())
RESERVED = {'all', 'and', 'any', 'as', 'asc', 'both', 'case', 'cast', 'check', 'collate',
            'column', 'constraint', 'create', 'cross', 'current_date', 'current_time',
            'default', 'desc', 'distinct', 'do', 'else', 'end', 'except', 'false', 'for',
            'foreign', 'from', 'full', 'grant', 'group', 'having', 'in', 'initially',
            'inner', 'insert', 'intersect', 'into', 'is', 'join', 'leading', 'left',
            'like', 'limit', 'natural', 'not', 'null', 'offset', 'on', 'only', 'or',
            'order', 'outer', 'overlaps', 'placing', 'primary', 'references', 'returning',
            'right', 'select', 'session_user', 'similar', 'some', 'symmetric', 'table',
            'then', 'to', 'trailing', 'true', 'union', 'unique', 'user', 'using',
            'variadic', 'when', 'where', 'window', 'with'}
SECTIONS = ['Overview', 'When to Use This Skill', 'How It Works', 'Field Reference',
            'Examples', 'Best Practices', 'Limitations', 'Security & Safety Notes',
            'Common Pitfalls', 'Related Skills', 'Reusable Prompt']
STEPS = ['### Step 1 - Identify intent', '### Step 2 - Ask only what is missing',
         '### Step 3 - Hold the internal context',
         '### Step 4 - Recommend the smallest workflow',
         '### Step 5 - Build only on request']


RESERVED_COL = {'user': 'user_account', 'order': 'sort_order', 'group': 'group_name',
                'select': 'select_name', 'table': 'table_name', 'check': 'check_name',
                'references': 'reference_list', 'default': 'default_value',
                'primary': 'primary_contact', 'unique': 'unique_key', 'index': 'index_name',
                'where': 'where_clause', 'from': 'from_source', 'to': 'to_target',
                'end': 'end_value', 'start': 'start_value', 'column': 'column_name',
                'key': 'key_name', 'values': 'values_list', 'using': 'using_value'}


def snake(n):
    # '%' is a unit suffix, not a word break: 'TDS Rate %' -> 'tds_rate_pct', the
    # name the SQL/JSON/Notion artifacts already carry. Dropping it here made
    # check.py disagree with itself and report clean modules as drifted.
    n = n.replace('%', ' Pct')
    s = re.sub(r'_+', '_', re.sub(r'[^a-z0-9]+', '_', n.lower()).strip('_')) or 'field'
    return RESERVED_COL.get(s, s)


def v_conf(row, names, name):
    return row[names.index(name)] if name in names else ''


def is_pack_dir(path):
    """True when path is a sub-pack: it holds module directories, not just files.

    A module directory has no child directory carrying its own SKILL.md. A sub-pack
    has at least one, which is how the two layouts are told apart without a
    hardcoded list.
    """
    if not os.path.isdir(path):
        return False
    for current, dirs, files in os.walk(path):
        if current != path and 'SKILL.md' in files:
            return True
    return False


def is_router(path):
    """A router routes between modules; it owns no table, so it has no artifacts."""
    if os.path.dirname(path) == ROOT:
        return True
    return is_pack_dir(os.path.dirname(path))


def owns_no_table(path):
    """A router routes; a helper renders another module's table. Neither owns one.

    Both are exempt from the artifact requirements below, for the same reason: there is
    no Field Reference for a CSV, a schema or a mapping to agree with. A helper is
    identified by ``table: none`` in its own frontmatter rather than by a hardcoded
    slug, so declaring one is what opts a file out.
    """
    return is_router(path) or skillmd.is_helper(path)


def check(path, verbose=False):
    slug = os.path.basename(os.path.dirname(path))
    t = open(path).read()
    iss = []
    bad = lambda tag, d='': iss.append((tag, d))

    # ---------------------------------------------------------- frontmatter
    m = re.match(r'^---\n(.*?)\n---\n', t, re.S)
    if not m:
        return slug, [('no frontmatter', '')]
    fm = m.group(1)
    for k in ['name', 'description', 'category', 'risk', 'source', 'source_type',
              'date_added', 'author', 'tags', 'tools']:
        if not re.search(r'^%s:' % k, fm, re.M):
            bad('fm missing ' + k)
    dm = re.search(r'^description:\s*"(.*)"\s*$', fm, re.M)
    if not dm:
        bad('fm description not a quoted string')
    else:
        if len(dm.group(1)) > 200:
            bad('fm description %d chars' % len(dm.group(1)))
        if not re.search(r'[Uu]se (for|when)', dm.group(1)):
            bad('fm description has no trigger clause')
    if not re.search(r'^name:\s*%s\s*$' % re.escape(slug), fm, re.M):
        bad('fm name != folder')
    body = t[m.end():]

    # ---------------------------------------------------------- sections
    heads = re.findall(r'^## (.+)$', body, re.M)
    no_table = owns_no_table(path)
    for s in SECTIONS:
        # a router and a helper have no field list, so they carry no Field Reference
        if s == 'Field Reference' and no_table:
            continue
        if s not in set(heads):
            bad('missing section ' + s)
    if heads and heads[-1] != 'Reusable Prompt':
        bad('Reusable Prompt not last (last=%r)' % heads[-1])
    if not t.rstrip().endswith('```'):
        bad('does not end with the prompt fence')
    for st in STEPS:
        if st not in body:
            bad('missing ' + st)

    # A router routes between modules and a helper renders another module's table, so
    # neither defines a table of its own and the artifact requirements below do not
    # apply. The frontmatter, section and step checks above still ran.
    if no_table:
        return slug, iss

    # ---------------------------------------------------------- blocks
    cb = re.search(r'```csv\n(.*?)\n```', body, re.S)
    sb = re.search(r'```sql\n(.*?)\n```', body, re.S)
    jb = re.search(r'```json\n(.*?)\n```', body, re.S)
    nb = re.search(r'```markdown\n(.*?)\n```', body, re.S)
    for nm, b in [('csv', cb), ('sql', sb), ('json', jb), ('notion', nb)]:
        if not b:
            bad('no %s block' % nm)
    fr = re.search(r'## Field Reference\n\n(\|.*?)\n\n', body, re.S)
    if not fr:
        bad('no field reference table')
    if not all([cb, sb, jb, nb, fr]):
        return slug, iss

    # ------------------------------------------------- field reference = truth
    frows = [l for l in fr.group(1).split('\n') if l.startswith('|') and '---' not in l][1:]
    ref = []
    for l in frows:
        c = [x.strip() for x in l.strip('|').split('|')]
        if len(c) != 7:
            bad('field reference row has %d cells' % len(c))
            continue
        name = c[1].strip('`')
        typ = c[2].strip('`')
        if typ not in TYPES:
            bad('field reference unknown type %r for %s' % (typ, name))
        ref.append(dict(name=name, type=typ, sql=c[3].strip('`'), js=c[4].strip('`'),
                        nt=c[5].strip('`'), ex=c[6].strip('`')))
    if not ref:
        return slug, iss
    names = [r['name'] for r in ref]
    if len(set(names)) != len(names):
        bad('field reference duplicate names %s'
            % [k for k, v in collections.Counter(names).items() if v > 1])
    for r in ref:
        if r['sql'].replace(' NOT NULL', '') != SQLT.get(r['type']):
            bad('field reference SQL for %s is %s, want %s' % (r['name'], r['sql'], SQLT.get(r['type'])))
        want_js = JSONT[r['type']]
        want_js = ('string, format: %s' % want_js[1]) if want_js[1] else want_js[0]
        if r['js'] != want_js:
            bad('field reference JSON for %s is %s, want %s' % (r['name'], r['js'], want_js))
        if r['nt'].split(' (')[0] != NOTIONT[r['type']]:
            bad('field reference Notion for %s is %s, want %s' % (r['name'], r['nt'], NOTIONT[r['type']]))

    # ---------------------------------------------------------- CSV
    rows = list(csv.reader(io.StringIO(cb.group(1))))
    if len(rows) != 2:
        bad('csv has %d rows, want header + 1' % len(rows))
        return slug, iss
    hdr, row = rows
    if hdr != names:
        bad('csv header != field reference order')
    if len(hdr) != len(row):
        bad('csv row width %d vs header %d' % (len(row), len(hdr)))
    blanks = [h for h, v in zip(hdr, row) if v == '']
    nonblank_wanted = [r['name'] for r in ref if r['type'] != 'id']
    if blanks and blanks != [r['name'] for r in ref if r['type'] == 'id']:
        bad('csv blank example cells: %s' % blanks)
    for r in ref:
        v = row[names.index(r['name'])]
        if r['ex'] != (v if v else '(blank)'):
            bad('csv example for %s differs from field reference' % r['name'])
    for r in ref:
        v = row[names.index(r['name'])]
        if r['type'] == 'date' and v and not re.match(r'^\d{4}-\d{2}-\d{2}$', v):
            bad('date example not ISO: %s = %r' % (r['name'], v))
        if r['type'] == 'datetime' and v and not re.match(r'^\d{4}-\d{2}-\d{2}[T ]\d{2}:\d{2}', v):
            bad('datetime example not ISO: %s = %r' % (r['name'], v))
        if r['type'] in ('number', 'currency') and v and not re.match(r'^-?[\d,]+(\.\d+)?$', v):
            bad('numeric example not numeric: %s = %r' % (r['name'], v))
        if r['type'] == 'email' and v and '@' not in v:
            bad('email example has no @: %s = %r' % (r['name'], v))
        if r['type'] == 'checkbox' and v not in ('', 'TRUE', 'FALSE'):
            bad('checkbox example not TRUE/FALSE: %s = %r' % (r['name'], v))
        if r['type'] == 'select' and not v:
            bad('select example empty: %s' % r['name'])
        if v and re.search(r'(?i)\b(n/?a|todo|tbd|lorem ipsum|xxx+|foo|bar)\b', v):
            bad('filler example for %s = %r' % (r['name'], v))
        if v and re.search(r'(?i)replace with|goes here|short description|one line summary', v):
            bad('instructional placeholder for %s = %r' % (r['name'], v))
        if v and re.search(r'@(?!(example|linkedin|meet\.|northwind)[.\w])', v):
            bad('non-example email domain in %s = %r' % (r['name'], v))
    if re.search(r'\b\d{12,}\b', cb.group(1)):
        bad('long digit run, possible real id')
    for r in ref:
        if re.search(r'(?i)passport|ssn|aadhaar|pan number', r['name']):
            v = row[names.index(r['name'])]
            if v not in ('', 'FALSE', 'No', 'None'):
                bad('sensitive field %s filled with %r' % (r['name'], v))
        if re.search(r'(?i)bank account', r['name']):
            v = row[names.index(r['name'])]
            if v and '*' not in v:
                bad('bank account example is not masked: %r' % v)
        if re.match(r'(?i)^confidential(ity)?$', r['name']) and v_conf(row, names, r['name']) \
                not in ('', 'Internal', 'No', 'FALSE'):
            bad('example row marked %r in %s' % (v_conf(row, names, r['name']), r['name']))

    # ---------------------------------------------------------- SQL
    sql = sb.group(1)
    if not sql.rstrip().endswith(');') and ');' not in sql:
        bad('sql does not end with );')
    tb = re.search(r'CREATE TABLE ("\w+"|\w+)', sql)
    if not tb:
        bad('sql has no CREATE TABLE')
        return slug, iss
    tname = tb.group(1).strip('"')
    if tname in RESERVED:
        bad('table name is reserved: %s' % tname)
    cols = []
    for line in sql.split('\n'):
        mm = re.match(r'^  ("\w+"|\w+) (SERIAL PRIMARY KEY|[A-Z]+(?:\(\d+(?:,\d+)?\))?(?: NOT NULL)?|TIMESTAMP DEFAULT NOW\(\))(?:,|  --|$)', line)
        if mm:
            cols.append((mm.group(1).strip('"'), mm.group(2).strip()))
    body_cols = [c for c in cols if c[0] not in ('created_at', 'updated_at')]
    if [c[0] for c in body_cols] != [snake(n) for n in names]:
        bad('sql columns != field reference order (%d vs %d)'
            % (len(body_cols), len(names)))
    dupe = [k for k, v in collections.Counter(c[0] for c in cols).items() if v > 1]
    if dupe:
        bad('DUPLICATE sql columns %s - invalid DDL' % dupe)
    for c, ty in body_cols:
        if c in RESERVED:
            bad('sql column is a reserved word: %s' % c)
    for r, (c, ty) in zip(ref, body_cols):
        if ty.replace(' NOT NULL', '') != SQLT[r['type']]:
            bad('sql type for %s is %r want %r' % (r['name'], ty, SQLT[r['type']]))
    if 'created_at' not in [c[0] for c in cols] or 'updated_at' not in [c[0] for c in cols]:
        bad('sql missing created_at/updated_at')
    has_status = any(snake(n) == 'status' for n in names)
    if has_status and 'CREATE INDEX' not in sql:
        bad('status field but no CREATE INDEX emitted')
    if 'CREATE INDEX' in sql:
        ix = re.search(r'CREATE INDEX (\w+) ON ("\w+"|\w+) \((\w+)\);', sql)
        if not ix:
            bad('malformed CREATE INDEX')
        else:
            if ix.group(2).strip('"') != tname:
                bad('index on wrong table %s' % ix.group(2))
            if ix.group(3) not in [c[0] for c in cols]:
                bad('index on unknown column %s' % ix.group(3))
            if ix.group(1) in RESERVED:
                bad('index name is reserved: %s' % ix.group(1))
    if not has_status and 'CREATE INDEX' in sql:
        bad('CREATE INDEX emitted but no status field')

    # ---------------------------------------------------------- JSON Schema
    try:
        o = json.loads(jb.group(1))
    except Exception as e:
        return slug, iss + [('json invalid: %s' % str(e)[:50], '')]
    if o.get('additionalProperties') is not False:
        bad('json additionalProperties not false')
    if o.get('type') != 'object':
        bad('json type not object')
    props = o.get('properties', {})
    if list(props) != names:
        bad('json properties != field reference order')
    for r in ref:
        p = props.get(r['name'])
        if p is None:
            continue
        wt, wf = JSONT[r['type']]
        if p.get('type') != wt:
            bad('json type for %s is %s want %s' % (r['name'], p.get('type'), wt))
        if wf and p.get('format') != wf:
            bad('json format for %s is %s want %s' % (r['name'], p.get('format'), wf))
    req = o.get('required', [])
    for rq in req:
        if rq not in names:
            bad('json required unknown field %r' % rq)
    hard = [r['name'] for r in ref if r['type'] in ('select', 'date', 'datetime', 'currency')]
    for h in ('email', 'url', 'checkbox', 'id', 'text', 'long_text', 'relation'):
        for r in ref:
            if r['type'] == h and r['name'] in req:
                bad('json required includes optional %s (%s)' % (r['name'], h))

    # ---------------------------------------------------------- Notion mapping
    nrows = [l for l in nb.group(1).split('\n') if l.startswith('|') and '---' not in l]
    nhead = [c.strip() for c in nrows[0].strip('|').split('|')]
    if nhead[:2] != ['CSV column', 'Notion property']:
        bad('notion header %s' % nhead)
    nmap = []
    for l in nrows[1:]:
        c = [x.strip() for x in l.strip('|').split('|')]
        nmap.append(c)
    if [c[0] for c in nmap] != names:
        bad('notion rows != field reference order')
    for r, c in zip(ref, nmap):
        base = c[1].split(' (')[0]
        if base not in NOTION_OK:
            bad('notion property %r is not a real Notion type' % c[1])
        if base != NOTIONT[r['type']]:
            bad('notion type for %s is %s want %s' % (r['name'], base, NOTIONT[r['type']]))
        if r['type'] == 'select' and 'add options:' in c[2]:
            listed = re.findall(r'"([^"]+)"', c[2])
            if len(listed) < 2:
                bad('notion mapping lists %d options for %s' % (len(listed), r['name']))

    # ---------------------------------------------------------- select options
    sels = [r['name'] for r in ref if r['type'] == 'select']
    so = re.search(r'## Select Options\n\n(.*?)\n\n## ', body, re.S)
    blocks = {}
    if so:
        blocks = dict(re.findall(r'\*\*(.+?)\*\*\n\n```\n(.*?)\n```', so.group(1), re.S))
    if not sels:
        if so and '_No Select fields._' not in so.group(1):
            bad('select block present but module has no select fields')
    else:
        for s in sels:
            if s not in blocks:
                bad('select field %s has no options block' % s)
                continue
            opts = [o.strip() for o in blocks[s].split('|') if o.strip()]
            if len(opts) < 2:
                bad('select field %s has %d options' % (s, len(opts)))
            if len(set(opts)) != len(opts):
                bad('select field %s has duplicate options' % s)
            v = row[names.index(s)]
            if v not in opts:
                bad('csv value %r not among options for %s' % (v, s))
        for b in blocks:
            if b not in sels:
                bad('options block for non-select field %r' % b)
        for r, c in zip(ref, nmap):
            if r['type'] == 'select' and r['name'] in blocks:
                listed = re.findall(r'"([^"]+)"', c[2])
                real = [o.strip() for o in blocks[r['name']].split('|') if o.strip()]
                if listed != real:
                    bad('notion options for %s differ from the options block (%s vs %s)'
                        % (r['name'], listed, real))

    # ---------------------------------------------------------- relations
    rels = [r['name'] for r in ref if r['type'] == 'relation']
    rsec = re.search(r'## Relations\n\n(.*?)\n\n## ', body, re.S)
    if rels:
        if not rsec:
            bad('has relation fields but no Relations section')
        else:
            txt = rsec.group(1)
            for r in rels:
                if r not in txt:
                    bad('relation field %s not listed in Relations' % r)
    else:
        if rsec and 'No relation fields' not in rsec.group(1) and 'Link fields: none' not in rsec.group(1):
            bad('Relations section says relations exist but none do')

    # ---------------------------------------------------------- context block
    ym = re.search(r'```yaml\n(.*?)\n```', body, re.S)
    if not ym:
        bad('no yaml context block')
    else:
        y = ym.group(1)
        if 'module: %s' % slug not in y:
            bad('yaml module slug mismatch')
        for k in ['intent:', 'scale:', 'areas:', 'requested_outputs:',
                  'confirmed_facts:', 'open_questions:']:
            if k not in y:
                bad('yaml missing %s' % k)
        areas = re.findall(r'^  "([^"]+)": null$', y, re.M)
        if len(areas) != 5:
            bad('yaml has %d areas, want 5' % len(areas))
    qs = re.findall(r'> \*\*Q:\*\* (.+)', body)
    if len(qs) < 2:
        bad('fewer than 2 example questions')
    if re.search(r'\bDescribe |Here is |I will |Sure,|Certainly', body):
        bad('assistant prose filler')

    # ------------------------------------------------- identifiers and example sanity
    ddl = re.search(r'```sql\n(.*?)\n```', body, re.S)
    if ddl:
        d = ddl.group(1)
        try:
            import sqlglot
            if not [s for s in sqlglot.parse(d, dialect='postgres') if s]:
                bad('DDL parsed to nothing')
        except ImportError:
            pass
        except Exception as e:
            bad('DDL is not valid PostgreSQL: %s' % str(e)[:60])
        tbl = re.search(r'CREATE TABLE (\S+)', d)
        for ident in re.findall(r'^  "?([a-z0-9_]+)"?\s', d, re.M):
            if ident[:1].isdigit() and '"%s"' % ident not in d:
                bad('unquoted identifier starts with a digit: %s' % ident)
            if ident in RESERVED:
                bad('column name is a reserved word: %s' % ident)
        if tbl and tbl.group(1)[:1].isdigit() and '"%s"' % tbl.group(1) not in d:
            bad('unquoted table name starts with a digit: %s' % tbl.group(1))

    for r in ref:
        name, ty, ex = r['name'], r['type'], r['ex']
        if ty in ('number', 'currency') and ex in ('0', '0.00'):
            bad('numeric example is a zero placeholder: %s' % name)
        if ty == 'id' and ex != '(blank)':
            bad('id column must not be pre-filled: %s' % name)
        if ty in ('text', 'long_text') and re.match(r'^\d{4}-\d{2}-\d{2}$', ex):
            bad('date value in a text column: %s' % name)

    # ------------------------------------------- example row internal coherence
    if cb:
        rows = list(csv.reader(io.StringIO(cb.group(1))))
        if len(rows) == 2 and len(rows[0]) == len(rows[1]):
            v = dict(zip(rows[0], rows[1]))
            started = re.search(r'(?i)\b(not started|draft|new|open|pending)\b',
                                ' '.join(v.get(k, '') for k in
                                         ('Status', 'Payment Status')))
            for f in ('Days Overdue', 'Sent Date', 'Acknowledged Date',
                      'Amount Paid', 'Actual', 'Resolution Date'):
                if started and v.get(f):
                    bad('row claims %s=%r but status is %r'
                        % (f, v[f], v.get('Status', '')))
            issue_dt = next((v[k] for k in ('Issue Date', 'Request Date', 'Order Date',
                                            'Start Date') if v.get(k)), None)
            due, terms = v.get('Due Date'), v.get('Payment Terms (Days)')
            if issue_dt and due and terms and terms.isdigit():
                want = (datetime.date.fromisoformat(issue_dt)
                        + datetime.timedelta(days=int(terms)))
                if want.isoformat() != due:
                    bad('due date mismatch',
                        'due %s != issue %s + %s days (%s)'
                        % (due, issue_dt, terms, want))
            try:
                money = {k: float(x.replace(',', '')) for k, x in v.items()
                         if re.match(r'^-?[\d,]+\.\d{2}$', x or '')}
                if {'Subtotal', 'Tax Amount', 'Total'} <= set(money):
                    calc = (money['Subtotal'] - money.get('Discount', 0)
                            + money['Tax Amount'])
                    if abs(calc - money['Total']) > 0.01:
                        bad('total does not reconcile',
                            'total %.2f != subtotal - discount + tax (%.2f)'
                            % (money['Total'], calc))
                if {'Total', 'Amount Paid', 'Balance'} <= set(money):
                    if abs(money['Total'] - money['Amount Paid']
                           - money['Balance']) > 0.01:
                        bad('balance does not reconcile',
                            'balance %.2f != total - amount paid' % money['Balance'])
            except ValueError:
                pass
    return slug, iss


if __name__ == '__main__':
    arg = sys.argv[1] if len(sys.argv) > 1 else 'all'
    verbose = '-v' in sys.argv
    files = sorted(glob.glob(ROOT + '/skills/*/SKILL.md')
                   + glob.glob(ROOT + '/skills/*/*/SKILL.md'))
    if arg != 'all':
        # Accept a bare slug, a pack/slug, or a suffix match, so a nested module can
        # be named on the command line without repeating its pack.
        files = [f for f in files
                 if arg in (os.path.basename(os.path.dirname(f)),
                            os.path.relpath(os.path.dirname(f),
                                            os.path.join(ROOT, 'skills')))]
    freq = collections.Counter()
    nbad = 0
    nmod = 0
    nhelp = 0
    nhbad = 0
    for f in files:
        # Sub-pack modules use the newer artifact contract checked by qa_verify.py
        # (including portable percentage names, custom SQL widths and booleans).
        if any(os.path.join('skills', pack) in f for pack in (
                'accounting-audit-system-builder',
                'brand-growth-system-builder')):
            continue
        if is_router(f):
            continue
        if skillmd.is_helper(f):
            # A helper has no artifacts to disagree with, but its frontmatter, sections
            # and intake steps are still checked, and it is reported on its own line
            # rather than folded into the module count it does not belong in.
            slug, iss = check(f, verbose)
            nhelp += 1
            if iss:
                nhbad += 1
                print('\n=== %s  (helper, %d)' % (slug, len(iss)))
                for tag, d in iss:
                    freq[tag.split(' (')[0][:52]] += 1
                    print('    %-52s %s' % (tag, d))
            elif verbose:
                print('=== %s  OK  (helper, no table of its own)' % slug)
            continue
        nmod += 1
        slug, iss = check(f, verbose)
        if iss:
            nbad += 1
            print('\n=== %s  (%d)' % (slug, len(iss)))
            for tag, d in iss:
                freq[tag.split(' (')[0][:52]] += 1
                print('    %-52s %s' % (tag, d))
        elif verbose:
            print('=== %s  OK  (%d fields)' % (slug, len(open(f).read())))
    print('\n%d/%d modules clean' % (nmod - nbad, nmod))
    if nhelp:
        # counted apart from the modules: a helper has no table, so its failures are
        # structure failures and folding them into the module ratio reads as -1/0
        print('%d/%d helper skills clean (no table of their own)'
              % (nhelp - nhbad, nhelp))
    if freq:
        print('\nissue frequency:')
        for tag, n in freq.most_common(30):
            print('  %3d  %s' % (n, tag))
