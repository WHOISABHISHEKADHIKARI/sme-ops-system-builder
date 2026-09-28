#!/usr/bin/env python3
"""Generate a SpreadsheetML workbook for every module.

A module ships the same field list as five artifacts. Four of them are inline in
SKILL.md: CSV, SQL DDL, JSON Schema and the Notion mapping. The fifth, this
workbook, is a separate file per module because a real spreadsheet is far too
long to inline.

Why SpreadsheetML and not .xlsx: a .xlsx is a ZIP of binary parts, so a skill
cannot hand one to a user in a chat reply. SpreadsheetML 2003 is a single plain
XML file that Excel, LibreOffice and Numbers all open natively, and it survives
being pasted into a message. It also carries the things CSV throws away, which
is the whole reason to ask for an Excel template in the first place:

  - a real dropdown on every select field, sourced from the Options sheet
  - date, datetime, currency and number formats, so Excel stops guessing
  - a Field Reference sheet, so the columns are self-documenting

The header row and the example row are taken from the CSV artifact rather than
rebuilt here, so the workbook cannot drift from the other four.

Usage:
    python3 tools/excel.py            # write every module's workbook
    python3 tools/excel.py --check    # verify, write nothing
    python3 tools/excel.py leave-management
"""
import html
import os
import re
import sys
import xml.etree.ElementTree as ET

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from skillmd import all_slugs, read_module, table_slugs  # noqa: E402

ROOT = os.environ.get('SKILL_REPO') or os.path.dirname(
    os.path.dirname(os.path.abspath(__file__)))

FILENAME = 'excel.xml'
DATA_ROWS = 500          # how many rows the dropdowns are offered for
SHEET_MAX = 31           # Excel's own limit on sheet-name length

# SpreadsheetML Data types, and the number format each one needs.
TYPE_XML = {
    'id': 'String', 'text': 'String', 'long_text': 'String', 'select': 'String',
    'email': 'String', 'url': 'String', 'relation': 'String',
    'checkbox': 'Boolean',
    'number': 'Number', 'currency': 'Number',
    'date': 'Date', 'datetime': 'DateTime',
}
FORMAT = {
    'date': 'yyyy\\-mm\\-dd',
    'datetime': 'yyyy\\-mm\\-dd\\ hh:mm',
    'currency': '#,##0.00',
    'number': '#,##0.##',
}
# A checkbox reads better as a plain Yes/No in a template a human will fill in.
BOOL_WORDS = {'true': 'Yes', 'false': 'No', '1': 'Yes', '0': 'No'}

ILLEGAL_XML = re.compile(
    '[\x00-\x08\x0b\x0c\x0e-\x1f\ud800-\udfff￾￿]')


def esc(value):
    """XML-escape a value and drop characters XML 1.0 cannot represent."""
    return html.escape(ILLEGAL_XML.sub('', str(value)), quote=False)


def col_letter(index):
    """1 -> A, 27 -> AA."""
    out = ''
    while index > 0:
        index, rem = divmod(index - 1, 26)
        out = chr(65 + rem) + out
    return out


def sheet_name(title, fallback):
    """Excel sheet names: 31 characters, and none of [ ] : * ? / \\."""
    name = re.sub(r'[\[\]:*?/\\]', '-', title).strip() or fallback
    return name[:SHEET_MAX]


def load_config():
    import json
    path = os.path.join(ROOT, 'site.json')
    if not os.path.exists(path):
        return {'author_name': '', 'date_reviewed': ''}
    with open(path) as fh:
        return json.load(fh)


def cell(value, style=None, ctype='String'):
    """One <Cell>. An empty value still emits a cell so the column keeps its type."""
    a = ' ss:StyleID="%s"' % style if style else ''
    return '<Cell%s><Data ss:Type="%s">%s</Data></Cell>' % (a, ctype, esc(value))


def row(cells, height=None):
    a = ' ss:Height="%s"' % height if height else ''
    return '<Row%s>%s</Row>' % (a, ''.join(cells))


def columns(widths):
    out = []
    for i, w in enumerate(widths, 1):
        out.append('<Column ss:Index="%d" ss:Width="%d"/>' % (i, w))
    return ''.join(out)


def styles():
    """Header, plain, and one style per formatted type."""
    out = [
        '<Style ss:ID="hdr"><Font ss:Bold="1" ss:Color="#FFFFFF"/>'
        '<Interior ss:Color="#1F3864" ss:Pattern="Solid"/>'
        '<Alignment ss:Vertical="Bottom" ss:WrapText="1"/></Style>',
        '<Style ss:ID="lbl"><Font ss:Bold="1"/></Style>',
        '<Style ss:ID="wrap"><Alignment ss:WrapText="1" ss:Vertical="Top"/></Style>',
    ]
    for name, fmt in FORMAT.items():
        out.append('<Style ss:ID="f_%s"><NumberFormat ss:Format="%s"/></Style>'
                   % (name, fmt))
    return '<Styles>%s</Styles>' % ''.join(out)


def data_sheet(name, fields, example, options_cols):
    """The sheet a person fills in: header row, one example row, live dropdowns."""
    widths = []
    for f, ty in fields:
        widths.append(min(46, max(12, len(f) + 4)))

    out = [row([cell(f, 'hdr') for f, _ in fields], height='30')]
    cells = []
    for i, (f, ty) in enumerate(fields):
        raw = example[i] if i < len(example) else ''
        if ty == 'checkbox':
            cells.append(cell(BOOL_WORDS.get(raw.strip().lower(), raw), 'lbl'))
        else:
            cells.append(cell(raw, 'f_%s' % ty if ty in FORMAT else None,
                              TYPE_XML[ty]))
    out.append(row(cells))

    validations = []
    for col, field in options_cols:
        validations.append(
            '<DataValidation ss:Type="List" ss:AllowBlank="1" '
            'ss:ShowInputMessage="1" ss:ShowErrorMessage="1" '
            'ss:Sqref="%s2:%s%d"><Formula1>=Options!$%s$2:$%s$%d</Formula1>'
            '</DataValidation>'
            % (col, col, DATA_ROWS + 1, col, col, DATA_ROWS + 1))

    return (
        '<Worksheet ss:Name="%s"><Table>%s%s</Table>%s'
        '<WorksheetOptions xmlns="urn:schemas-microsoft-com:office:excel">'
        '<FreezePanes/><FrozenNoSplit/><SplitHorizontal>1</SplitHorizontal>'
        '<TopRowBottomPane>1</TopRowBottomPane><ActivePane>2</ActivePane>'
        '</WorksheetOptions></Worksheet>'
        % (esc(name), columns(widths), ''.join(out), ''.join(validations))
    )


def reference_sheet(name, rows):
    """The field dictionary, so the columns explain themselves."""
    head = ['#', 'Field', 'Type', 'SQL', 'Notion', 'Example']
    body = [row([cell(h, 'hdr') for h in head], height='24')]
    for r in rows:
        cells = [cell('#', 'lbl', 'Number'),
                 cell(r['name'], 'wrap'),
                 cell(r['type'], None),
                 cell(r['sql'], 'wrap'),
                 cell(r['notion'], 'wrap'),
                 cell(r['example'], 'wrap')]
        body.append(row(cells))
    return ('<Worksheet ss:Name="Field Reference"><Table>%s%s</Table>'
            '<WorksheetOptions xmlns="urn:schemas-microsoft-com:office:excel">'
            '<FreezePanes/><FrozenNoSplit/><SplitHorizontal>1</SplitHorizontal>'
            '<TopRowBottomPane>1</TopRowBottomPane><ActivePane>2</ActivePane>'
            '</WorksheetOptions></Worksheet>'
            % (columns([5, 28, 12, 22, 14, 34]), ''.join(body)))


def options_sheet(option_fields):
    """One column per select field. The data validations point at these ranges."""
    if not option_fields:
        return ''
    n = max(len(v) for v in option_fields.values())
    body = [row([cell(f, 'hdr') for f in option_fields], height='24')]
    for i in range(n):
        body.append(row([cell(vals[i] if i < len(vals) else '')
                         for vals in option_fields.values()]))
    return ('<Worksheet ss:Name="Options"><Table>%s%s</Table></Worksheet>'
            % (columns([20] * len(option_fields)), ''.join(body)))


def build(d, cfg):
    fields = d['fields']
    example = next(iter([l for l in d['csv'].split('\n')[1:] if l.strip()]), '').split(',')
    rows = d.get('rows') or [
        {'name': f, 'type': ty, 'sql': '', 'notion': '', 'example': ''}
        for f, ty in fields
    ]

    # a select field's dropdown is sourced from the Options sheet, so the two
    # must agree on which column holds which field
    option_fields = {}
    for i, (f, ty) in enumerate(fields):
        if ty == 'select' and f in d['options']:
            option_fields[f] = d['options'][f]
    options_cols = [(col_letter(i + 1), f)
                    for i, f in enumerate(option_fields)]

    title = d['title']
    parts = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<?mso-application progid="Excel.Sheet"?>',
        '<Workbook xmlns="urn:schemas-microsoft-com:office:spreadsheet"'
        ' xmlns:o="urn:schemas-microsoft-com:office:office"'
        ' xmlns:x="urn:schemas-microsoft-com:office:excel"'
        ' xmlns:ss="urn:schemas-microsoft-com:office:spreadsheet"'
        ' xmlns:html="http://www.w3.org/TR/REC-html40">',
        '<DocumentProperties xmlns="urn:schemas-microsoft-com:office:office">'
        '<Title>%s</Title><Author>%s</Author>'
        '<Company>SME Ops System Builder</Company>'
        '<Comments>Generated by tools/excel.py from the module field reference. '
        'Edit the SKILL.md, not this file.</Comments>'
        '</DocumentProperties>' % (esc(title), esc(cfg.get('author_name', ''))),
        styles(),
        data_sheet(sheet_name(title, d['slug']), fields, example, options_cols),
        reference_sheet(title, rows),
        options_sheet(option_fields),
        '</Workbook>',
        '',
    ]
    return '\n'.join(parts)


def path_for(slug):
    return os.path.join(ROOT, 'skills', slug, FILENAME)


def generate(slugs, cfg, write=True):
    made, problems = [], []
    for slug in slugs:
        d = read_module(ROOT, slug)
        xml = build(d, cfg)
        target = path_for(slug)
        try:
            ET.fromstring(xml)
        except ET.ParseError as exc:
            problems.append('%s: not well-formed XML (%s)' % (slug, exc))
            continue
        if write:
            with open(target, 'w', encoding='utf-8') as fh:
                fh.write(xml)
        made.append(slug)
    return made, problems


def verify(slugs):
    """Re-derive each workbook and confirm the committed file matches."""
    import io
    cfg = load_config()
    bad = []
    for slug in slugs:
        target = path_for(slug)
        if not os.path.exists(target):
            bad.append('%s: no %s' % (slug, FILENAME))
            continue
        stored = open(target, encoding='utf-8').read()
        try:
            ET.fromstring(stored)
        except ET.ParseError as exc:
            bad.append('%s: not well-formed XML (%s)' % (slug, exc))
            continue
        if stored != build(read_module(ROOT, slug), cfg):
            bad.append('%s: out of date, re-run tools/excel.py' % slug)
    return bad


def main():
    args = [a for a in sys.argv[1:]]
    check = '--check' in args
    args = [a for a in args if a != '--check']

    if args:
        slugs = args
    else:
        slugs = table_slugs(ROOT)

    if check:
        bad = verify(slugs)
        if bad:
            print('excel: %d problems' % len(bad))
            for b in bad[:10]:
                print('   %s' % b)
            return 1
        print('excel: OK - %d workbooks well-formed and up to date' % len(slugs))
        return 0

    made, problems = generate(slugs, load_config())
    if problems:
        print('excel: %d problems' % len(problems))
        for p in problems[:10]:
            print('   %s' % p)
        return 1
    print('excel: wrote %d workbooks' % len(made))
    return 0


if __name__ == '__main__':
    sys.exit(main())
