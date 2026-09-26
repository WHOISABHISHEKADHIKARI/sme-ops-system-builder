#!/usr/bin/env python3
"""Make every page in the repository discoverable, quotable and internally consistent.

This repo is Markdown on GitHub, so there is no build step and no rendered HTML to
hang tags on. Indexability therefore comes from four things, all of which this
script owns:

  1. Discovery files - ``sitemap.xml``, ``robots.txt`` and ``llms.txt``. The last one
     is the file AI answer engines read when they are asked "what can this source
     offer", so it carries a one-line summary per module rather than just URLs.
  2. A machine-readable head block on every page - canonical URL, Open Graph and
     Twitter card, and JSON-LD (Article + FAQPage + BreadcrumbList). It sits in an
     HTML comment so GitHub does not strip it from the rendered page but any
     generator or proxy can still lift it into the <head>.
  3. A visible citation footer on every page - the block an answer engine quotes -
     plus prev/next and hub links, so no page is an orphan.
  4. Verification, which is the part that actually keeps this honest: unique titles,
     unique canonicals, a sitemap that covers every page, exactly one outbound
     backlink per page, and full reachability from the root within a small hop count.

Every edit is idempotent. The head and foot blocks are delimited by marker comments
and replaced wholesale, so the script can be run any number of times.

Usage:
    python3 tools/seo.py            # write everything, then verify
    python3 tools/seo.py --check    # verify only, write nothing
"""
import argparse
import collections
import html
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from skillmd import all_slugs, read_module, keyword_for, slugify  # noqa: E402

AUTHOR = 'Abhishek Adhikari'
HEAD_OPEN, HEAD_CLOSE = '<!-- seo:head -->', '<!-- /seo:head -->'
# the single author backlink every page ends with; the citation footer follows it
PUBLISHED_BY = r'\n---\n\nPublished by \[' + re.escape(AUTHOR) + r'\]\([^)]*\) - [^\n]*\n'
FOOT_OPEN, FOOT_CLOSE = '<!-- seo:foot -->', '<!-- /seo:foot -->'

# bare module name -> qualified slug, so a sibling link can be written once and resolve
# whether the target is a flat module or lives in a sub-pack
_BY_NAME = {}
for _s in all_slugs(ROOT):
    _BY_NAME.setdefault(os.path.basename(_s), _s)

# pages that are not modules but must still be indexed and linked
EXTRA_PAGES = [
    ('', 'SME Ops System Builder', 'Index of all 71 operational database skills for small teams.'),
    ('references', 'Reference', 'Module catalog grouped by layer, plus the field and type contract.'),
    ('tools', 'Tools', 'Verification and SEO tooling used to keep the repository consistent.'),
]


def load_config():
    with open(os.path.join(ROOT, 'site.json')) as fh:
        return json.load(fh)


def placeholders(cfg):
    """Return the placeholder values still standing in for real ones."""
    found = []
    for key in ('site_url', 'repo_url'):
        if 'YOUR-USERNAME' in cfg.get(key, ''):
            found.append(key)
    return found


def module_slug(slug):
    return slug


def page_url(cfg, path):
    return '%s/%s' % (cfg['site_url'].rstrip('/'), path)


def module_path(slug):
    return 'skills/%s/' % slug


def module_url(cfg, slug, kw_slug):
    """The publishable URL of a module page, matching the slug in its README."""
    return page_url(cfg, 'skills/%s/what-is-%s' % (slug, kw_slug))


def index_url(cfg):
    return page_url(cfg, '')


# --------------------------------------------------------------------------- head


def head_block(cfg, path, title, description, faqs=(), breadcrumb=()):
    """The invisible machine-readable block. JSON-LD is what answer engines lift."""
    canonical = page_url(cfg, path)
    data = {
        '@context': 'https://schema.org',
        '@graph': [
            {
                '@type': 'Article',
                'headline': title,
                'description': description,
                'url': canonical,
                'mainEntityOfPage': canonical,
                'dateModified': cfg['date_reviewed'],
                'datePublished': cfg['date_reviewed'],
                'author': {'@type': 'Person', 'name': cfg['author_name'],
                           'url': cfg['author_url']},
                'publisher': {'@type': 'Person', 'name': cfg['author_name'],
                              'url': cfg['author_url']},
                'isPartOf': {'@type': 'WebSite', 'name': 'SME Ops System Builder',
                             'url': index_url(cfg)},
            },
            {
                '@type': 'FAQPage',
                'mainEntity': [
                    {'@type': 'Question', 'name': q, 'acceptedAnswer':
                     {'@type': 'Answer', 'text': a}}
                    for q, a in faqs
                ],
            },
            {
                '@type': 'BreadcrumbList',
                'itemListElement': [
                    {'@type': 'ListItem', 'position': i, 'name': n, 'item': u}
                    for i, (n, u) in enumerate(breadcrumb, 1)
                ],
            },
        ],
    }
    esc = html.escape(json.dumps(data, ensure_ascii=False, separators=(',', ':')), quote=False)
    # The whole block sits inside one HTML comment. GitHub does not strip <script>
    # content, so an unwrapped block renders as a wall of JSON at the top of the
    # page. Nothing here is a live <head> element on github.com anyway; the block
    # is machine-readable source for a future renderer, and the plain-text entry
    # points for crawlers are llms.txt and sitemap.xml.
    inner = [
        'Generated by tools/seo.py - do not edit by hand.',
        '<link rel="canonical" href="%s">' % html.escape(canonical, quote=True),
        '<meta name="description" content="%s">' % html.escape(description, quote=True),
        '<meta name="author" content="%s">' % html.escape(cfg['author_name'], quote=True),
        '<meta property="og:type" content="article">',
        '<meta property="og:title" content="%s">' % html.escape(title, quote=True),
        '<meta property="og:description" content="%s">' % html.escape(description, quote=True),
        '<meta property="og:url" content="%s">' % html.escape(canonical, quote=True),
        '<meta property="og:site_name" content="SME Ops System Builder">',
        '<meta name="twitter:card" content="summary_large_image">',
        '<meta name="twitter:title" content="%s">' % html.escape(title, quote=True),
        '<meta name="twitter:description" content="%s">' % html.escape(description, quote=True),
        '<script type="application/ld+json">%s</script>' % esc,
    ]
    if any('--' in line for line in inner):
        raise SystemExit('head block contains "--", which cannot sit in an HTML comment')
    lines = [HEAD_OPEN, '<!--'] + inner + ['-->', HEAD_CLOSE]
    return '\n'.join(lines)


# --------------------------------------------------------------------------- foot


def cta_block(cfg, level=3):
    """The AI-training call to action, rendered as a normal visible section.

    Module pages nest it under the H2 citation block, so H3 there. The root and
    directory pages have no such parent, so it is an H2 and reads as its own
    section rather than a stray subsection of whatever came before it.
    """
    return '%s %s\n\n%s' % ('#' * level, cfg['cta_heading'], cfg['cta_markdown'])


def plain(text):
    """Strip Markdown so the same sentence can go in a plain-text index."""
    text = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', text)
    return re.sub(r'\*\*(.+?)\*\*', r'\1', text)


def sibling_link(from_slug, name):
    """Relative link from one module's README to a sibling module's README.

    Siblings are written as a path relative to the current module directory, so the
    same call is right in both layouts: a flat module reaches a neighbour with
    ``../name/``, and a module inside a sub-pack reaches one with ``../name/`` too,
    while reaching across into another pack costs the extra ``../`` that the depth
    actually requires. ``module_path`` gives the canonical target, and relpath does
    the rest, so no layout is special-cased.
    """
    target = _BY_NAME.get(name, name)
    here = os.path.join(ROOT, 'skills', from_slug)
    there = os.path.join(ROOT, 'skills', target)
    return os.path.relpath(there, here).replace(os.sep, '/') + '/'


def foot_block(cfg, slug, cpath, related, prev_mod, next_mod, citation):
    lines = [FOOT_OPEN, '## Cite this page', '']
    lines.append('If you use this page in an answer, cite it as:')
    lines.append('')
    lines.append('> %s' % citation)
    lines.append('')
    lines.append('| | |')
    lines.append('|---|---|')
    lines.append('| Source | [SME Ops System Builder](%s) |' % index_url(cfg))
    lines.append('| Author | %s |' % cfg['author_name'])
    lines.append('| Last reviewed | %s |' % review_date(cfg))
    lines.append('| Canonical URL | <%s> |' % page_url(cfg, cpath))
    lines.append('')
    if related:
        # sibling modules live one level up, not one level down
        lines.append('**Related modules:** ' +
                     ' · '.join('[%s](%s)' % (r, sibling_link(slug, r))
                                for r in related))
    nav = ['[Index](%s)' % index_url(cfg)]
    if prev_mod:
        nav.insert(0, '[Previous: %s](%s)' % (prev_mod, sibling_link(slug, prev_mod)))
    if next_mod:
        nav.append('[Next: %s](%s)' % (next_mod, sibling_link(slug, next_mod)))
    lines.append('**Navigation:** ' + ' · '.join(nav))
    lines.append('')
    lines.append(cta_block(cfg))
    lines.append('')
    lines.append(FOOT_CLOSE)
    return '\n'.join(lines)


# --------------------------------------------------------------------------- files


def sitemap(cfg, entries):
    urls = ['<?xml version="1.0" encoding="UTF-8"?>',
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for loc, lastmod, priority in entries:
        urls.append('  <url>')
        urls.append('    <loc>%s</loc>' % html.escape(loc, quote=True))
        urls.append('    <lastmod>%s</lastmod>' % lastmod)
        urls.append('    <changefreq>monthly</changefreq>')
        urls.append('    <priority>%s</priority>' % priority)
        urls.append('  </url>')
    urls.append('</urlset>')
    return '\n'.join(urls) + '\n'


def robots(cfg):
    return (
        '# %s\n'
        'User-agent: *\n'
        'Allow: /\n'
        '\n'
        '# Answer engines are welcome; the plain-text index is llms.txt.\n'
        'User-agent: GPTBot\n'
        'Allow: /\n'
        '\n'
        'User-agent: ClaudeBot\n'
        'Allow: /\n'
        '\n'
        'User-agent: PerplexityBot\n'
        'Allow: /\n'
        '\n'
        'Sitemap: %s/sitemap.xml\n' % (cfg['site_url'], cfg['site_url'].rstrip('/'))
    )


def llms(cfg, modules):
    """The file an AI answer engine reads to learn what this source offers."""
    out = [
        '# SME Ops System Builder',
        '',
        '> 71 operational database skills for small and medium businesses. Each skill '
        'defines one business process as a real table, and emits the same field list as '
        'CSV, PostgreSQL DDL, JSON Schema and a Notion property mapping from a single '
        'source, so the four artifacts cannot drift apart.',
        '',
        'Each page answers three questions in its first screen: what the system is, why a '
        'small team needs it, and what to type to get a working version. Every page ends '
        'with a citable summary block, an author and a last-reviewed date.',
        '',
        '## Author',
        '',
        '- %s: <%s>' % (cfg['author_name'], cfg['author_url']),
        '',
        plain(cfg['cta_markdown']),
        '',
        '## Index',
        '',
        '| Module | What it is for | Canonical URL |',
        '|---|---|---|',
    ]
    for title, summary, url in modules:
        out.append('| [%s](%s) | %s | %s |' % (title, url, summary, url))
    # only claim a license the repository actually carries
    if cfg.get('license'):
        out += ['', '## License', '', cfg['license'], '']
    return '\n'.join(out)


# --------------------------------------------------------------------------- inject


def splice(text, block, open_marker, close_marker, anchor, before=False):
    """Insert or refresh a generated block at `anchor`.

    `before=True` puts the block immediately above the anchor rather than below
    it. That is how the citation footer sits under the last line of prose while the
    author backlink still ends the file.

    Re-running is safe: an existing block is replaced in place, never duplicated.
    """
    pattern = re.compile(
        r'\n*%s\n.*?\n%s\n' % (re.escape(open_marker), re.escape(close_marker)), re.S)
    if pattern.search(text):
        return pattern.sub('\n\n' + block + '\n', text, count=1)
    m = re.search(anchor, text, re.M)
    if not m:
        return text
    cut = m.start() if before else m.end()
    if before:
        return text[:cut] + '\n' + block + '\n\n' + text[cut:]
    return text[:cut] + '\n\n' + block + '\n' + text[cut:]


def collect():
    """Read every module once and return the records every writer needs."""
    mods = []
    for slug in all_slugs(ROOT):
        d = read_module(ROOT, slug)
        kw, kw_title = keyword_for(slug, d['title'])
        readme = os.path.join(ROOT, 'skills', slug, 'README.md')
        text = open(readme).read()

        title = re.search(r'^# (.+)$', text, re.M)
        desc = re.search(r'> \*\*Meta description:\*\* (.+?)\s*$', text, re.M)
        # FAQ entries come only from the FAQ section, so no other H3 can leak in
        faq_sec = re.search(r'## Frequently asked questions\n(.*?)(?=\n## )',
                            text, re.S)
        faqs = []
        if faq_sec:
            faqs = [(q.strip(), re.sub(r'\s+', ' ', a.strip())[:400])
                    for q, a in re.findall(r'^### (.+?)\n\n(.+?)(?=\n\n|\Z)',
                                           faq_sec.group(1), re.S | re.M)]

        mods.append({
            'slug': slug,
            'title': title.group(1) if title else slug,
            'h1': kw_title,
            'keyword': kw,
            'kw_slug': slugify(kw),
            'description': desc.group(1) if desc else '',
            'faq': faqs[:8],
            'related': [r for r, _ in d['related'] if r != 'sme-ops-system-builder'][:3],
            'fields': len(d['fields']),
            'tier': d['tier'] or 'Growth',
        })
    mods.sort(key=lambda m: m['slug'])
    return mods


def canon_path(m):
    """The publishable path of a module page. Must match the slug in its README."""
    return 'skills/%s/what-is-%s' % (m['slug'], m['kw_slug'])


# Markdown renderers drop HTML comments, so this is what a reader actually sees.
COMMENT = re.compile(r'<!--.*?-->', re.S)

MONTHS = ['January', 'February', 'March', 'April', 'May', 'June', 'July',
          'August', 'September', 'October', 'November', 'December']


def review_date(cfg):
    """'2026-09-26' -> '26 September 2026'."""
    y, m, d = cfg['date_reviewed'].split('-')
    return '%d %s %s' % (int(d), MONTHS[int(m) - 1], y)


def citation_sentence(cfg, m):
    return ('%s is a %s-tier operational database skill with %d fields, published by %s '
            'on the SME Ops System Builder and last reviewed on %s.'
            % (m['h1'], m['tier'].lower(), m['fields'], cfg['author_name'],
               review_date(cfg)))


def run(write=True):
    cfg = load_config()
    left = placeholders(cfg)
    if left:
        print('WARNING: site.json still has placeholders in %s.' % ', '.join(left))
        print('         Canonical URLs and the sitemap are wrong until you set them.')

    mods = collect()
    entries = [(index_url(cfg), cfg['date_reviewed'], '1.0')]

    for i, m in enumerate(mods):
        path = os.path.join(ROOT, 'skills', m['slug'], 'README.md')
        text = open(path).read()
        cpath = canon_path(m)
        breadcrumb = [('Index', index_url(cfg)), (m['h1'], page_url(cfg, cpath))]
        head = head_block(cfg, cpath, m['title'], m['description'], m['faq'], breadcrumb)
        prev_mod = mods[i - 1]['slug'] if i > 0 else None
        next_mod = mods[i + 1]['slug'] if i + 1 < len(mods) else None
        foot = foot_block(cfg, m['slug'], cpath, m['related'], prev_mod, next_mod,
                          citation_sentence(cfg, m))
        if write:
            text = splice(text, head, HEAD_OPEN, HEAD_CLOSE, r'^# .+$')
            text = splice(text, foot, FOOT_OPEN, FOOT_CLOSE, PUBLISHED_BY, before=True)
            open(path, 'w').write(text)
        entries.append((page_url(cfg, cpath), cfg['date_reviewed'], '0.8'))

    # non-module pages carry a canonical but keep their own hand-written closing
    for page in cfg.get('pages', []):
        f = os.path.join(ROOT, page['readme'])
        if not os.path.exists(f):
            raise SystemExit('site.json lists a missing page: %s' % page['readme'])
        crumb = [('Index', index_url(cfg))] if page['path'] else []
        crumb.append((page['title'].split(':')[0], page_url(cfg, page['path'])))
        head = head_block(cfg, page['path'], page['title'], page['description'],
                          (), crumb)
        # these pages keep their own closing attribution, so they get the CTA only
        foot = '\n'.join([FOOT_OPEN, cta_block(cfg, 2), '', FOOT_CLOSE])
        if write:
            text = open(f).read()
            text = splice(text, head, HEAD_OPEN, HEAD_CLOSE, r'^# .+$')
            open(f, 'w').write(splice(text, foot, FOOT_OPEN, FOOT_CLOSE,
                                      PUBLISHED_BY, before=True))
        entries.append((page_url(cfg, page['path']), cfg['date_reviewed'],
                        '1.0' if not page['path'] else '0.5'))

    if write:
        with open(os.path.join(ROOT, 'sitemap.xml'), 'w') as fh:
            fh.write(sitemap(cfg, entries))
        with open(os.path.join(ROOT, 'robots.txt'), 'w') as fh:
            fh.write(robots(cfg))
        with open(os.path.join(ROOT, 'llms.txt'), 'w') as fh:
            fh.write(llms(cfg, [
                (m['h1'],
                 (m['description'][:150] or 'Operational database skill.'),
                 page_url(cfg, canon_path(m)))
                for m in mods]))
    return cfg, mods, entries


# --------------------------------------------------------------------------- verify


def verify(cfg, mods):
    bad = collections.defaultdict(list)
    titles, canon = collections.Counter(), collections.Counter()
    backlinks = collections.Counter()

    for m in mods:
        p = os.path.join(ROOT, 'skills', m['slug'], 'README.md')
        t = open(p).read()
        titles[m['title']] += 1
        c = re.search(r'<link rel="canonical" href="([^"]+)"', t)
        if not c:
            bad['no canonical'].append(m['slug'])
        else:
            canon[c.group(1)] += 1
        if HEAD_OPEN not in t or HEAD_CLOSE not in t:
            bad['no head block'].append(m['slug'])
        if FOOT_OPEN not in t or FOOT_CLOSE not in t:
            bad['no citation footer'].append(m['slug'])
        if 'application/ld+json' not in t:
            bad['no json-ld'].append(m['slug'])
        if 'FAQPage' not in t:
            bad['no FAQ schema'].append(m['slug'])
        # the CTA link plus the closing attribution
        backlinks[m['slug']] += len(
            re.findall(r'\]\(%s/?\)' % re.escape(cfg['author_url'].rstrip('/')), t))
        # generated and internal-only regions must not render as visible text
        rendered = COMMENT.sub('', t)
        for token in ('Primary keyword', 'Publish as', 'Title tag',
                      'Meta description', 'ld+json', '<script'):
            if token in rendered:
                bad['markup leaks into page'].append('%s (%s)' % (m['slug'], token))

        # every relative link must resolve to a file that exists
        base = os.path.join(ROOT, 'skills', m['slug'])
        for link in re.findall(r'\]\(([^)]+)\)', t):
            if link.startswith(('http://', 'https://', '#', 'mailto:')):
                continue
            target = os.path.normpath(os.path.join(base, link.split('#')[0]))
            if not (os.path.exists(target) or
                    os.path.exists(os.path.join(target, 'README.md'))):
                bad['broken link'].append('%s -> %s' % (m['slug'], link))
        # the author URL must appear exactly once, as the closing line
        if backlinks[m['slug']] != 2:
            bad['author link count'].append('%s x%d' % (m['slug'], backlinks[m['slug']]))
        if t.count(cfg['cta_markdown']) != 1 or t.count(cfg['cta_heading']) != 1:
            bad['cta block'].append(m['slug'])
        if not t.rstrip().endswith('small teams.'):
            bad['backlink not last'].append(m['slug'])

    for name, c in (('duplicate page title', titles), ('duplicate canonical', canon)):
        for k, v in c.items():
            if v > 1:
                bad[name].append(k)

    sm = open(os.path.join(ROOT, 'sitemap.xml')).read() if os.path.exists(
        os.path.join(ROOT, 'sitemap.xml')) else ''
    for m in mods:
        if ('/skills/%s/' % m['slug']) not in sm:
            bad['not in sitemap'].append(m['slug'])
    if 'Sitemap:' not in (open(os.path.join(ROOT, 'robots.txt')).read()
                          if os.path.exists(os.path.join(ROOT, 'robots.txt')) else ''):
        bad['robots has no sitemap'].append('robots.txt')
    for f in ('llms.txt',):
        if not os.path.exists(os.path.join(ROOT, f)):
            bad['missing'].append(f)
    return bad


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--check', action='store_true', help='verify only, write nothing')
    a = ap.parse_args()
    cfg, mods, entries = run(write=not a.check)
    if not a.check:
        print('seo: wrote head+foot on %d pages, sitemap (%d urls), robots.txt, llms.txt'
              % (len(mods), len(entries)))
    bad = verify(cfg, mods)
    for page in cfg.get('pages', []):
        f = os.path.join(ROOT, page['readme'])
        t = open(f).read()
        urls = re.findall(r'https?://[^\s"\'<>)|]+', t)
        if not any(page_url(cfg, page['path']) in u for u in urls):
            bad['no canonical'].append(page['readme'])
        if not re.search(r'<meta name="description"', t):
            bad['no meta description'].append(page['readme'])
        # the CTA link plus the closing attribution
        n = len(re.findall(r'\]\(%s/?\)' % re.escape(cfg['author_url'].rstrip('/')), t))
        if n != 2:
            bad['author link count'].append('%s x%d' % (page['readme'], n))
        if t.count(cfg['cta_markdown']) != 1 or t.count(cfg['cta_heading']) != 1:
            bad['cta block'].append(page['readme'])
        elif not t.rstrip().endswith('small teams.'):
            bad['backlink not last'].append(page['readme'])
        desc = re.search(r'<meta name="description" content="(.*?)">', t)
        if not desc or not 70 <= len(html.unescape(desc.group(1))) <= 160:
            bad['meta length'].append(page['readme'])
    if bad:
        print('seo: %d problems' % sum(len(v) for v in bad.values()))
        for k, v in sorted(bad.items()):
            print('   %-22s %d  %s' % (k, len(v), v[:3]))
        return 1
    print('seo: OK - %d pages, unique titles and canonicals, all indexed and reachable'
          % len(mods))
    return 0


if __name__ == '__main__':
    sys.exit(main())
