#!/usr/bin/env python3
"""Put a book on the website, or refresh it, without an agent.

Run it from the root of the site repository:

  python3 books/site.py refresh BOOK [--ref REF] [--check] [--force] [--commit] [--push]
  python3 books/site.py check

BOOK is the name of the book's repository on GitHub (VadimSokolov/BOOK) or OWNER/BOOK. The folder of its pages on the site is
the slug of its book.json, which can differ from the repository name (gbc-book has the slug gbc_book). REF is a branch, a tag
or a commit of that repository, main by default. "add" is another name of "refresh".

refresh does all of this for one book and stops at the first problem; a failed run puts every file back as it was.
  1. It fetches site/ of the book repository at REF (book.json, the page, the head, llms.txt, and the results page and its
     head when the book has results) and the cover, and checks them: no dash, local path, e-mail address or ISBN, and every
     results link has its anchor. It also checks that the release named in book.json exists (the default branch can hold the
     work toward the next version) and that the PDF, the DOI and its badge, the online edition and the repository answer.
     Everything about the book comes from its repository, nothing is written here by hand.
  2. It writes books/BOOK/index.qmd and results.qmd from books/_templates/ (the page of the Hilbert book is the template)
     and keeps the downloaded files as the copies that are not committed (_page.md, head.html, _results.md,
     results-head.html, cover.*; books/.gitignore lists them).
  3. It writes the entry of the book on the list page books/_page.md, its item in the JSON-LD of books/head.html and its
     section in llms.txt, the newest book first (a book that is already listed keeps its place).
  4. It renders the page of the book, its results page and the list page, single files only, never the whole site. Then it
     rebuilds llms-full.txt from the Markdown copies, copies llms.txt and llms-full.txt to docs/, removes the search entries
     of anchors that are gone, and keeps the lastmod of a page in docs/sitemap.xml when the page came out the same.
  A run that finds nothing to change says so and renders nothing.
  --check   only reports what would change (exit status 1 if anything would) and writes nothing.
  --force   renders the pages even when nothing differs.
  --commit  then commits exactly the files the run changed, with a pathspec, so that other uncommitted work is left alone.
            Every render writes docs/search.json and docs/sitemap.xml. When they held other changes before the run, the run
            commits only the entries of this book and of the list page into the committed text of each: the commit is made in
            a temporary index, so the other work stays in the working copy, uncommitted, and the index is not touched. --check
            names such a file when the commit lacks entries of the book, so a run also repairs what an earlier run left out.
            If any other file of the run held other changes before it, the run commits nothing, prints the commands for the
            commit and stops: a commit of the rest would be inconsistent.
  --push    also pushes (HEAD must be origin/main and the new commit the only one to push), waits for the GitHub Pages build
            and compares the live files with docs/. An agent uses --push only with the user's yes.

check runs the checks that need no network on the whole books section: the books of the list page, of the JSON-LD, of
llms.txt and of llms-full.txt are the same and newest first, the pages have the shape of the templates, the Markdown copies
and the llms files in docs/ are the ones of the sources, every results link has its anchor, and no file has a dash, a local
path or an e-mail address.

Downloads are data, never code: the script writes only the fixed names above under books/BOOK/, and reads the download
with the json module and with regular expressions.
"""
import argparse
import glob
import hashlib
import json
import os
import re
import string
import subprocess
import sys
import tempfile
import time
import urllib.error
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BOOKS = os.path.join(ROOT, 'books')
DOCS = os.path.join(ROOT, 'docs')
SITE = 'https://vsokolov.org'
OWNER = 'VadimSokolov'
SITE_REPO = 'VadimSokolov/vadimsokolov.github.io'
AMAZON_BADGE = 'available-at-amazon.png'
SHARED = ('docs/search.json', 'docs/sitemap.xml')   # every render of any page writes these two
COPIES = (('page', '_page.md'), ('head', 'head.html'), ('results', '_results.md'), ('results_head', 'results-head.html'))
SLUG = re.compile(r'[a-z0-9][a-z0-9_-]*')
GITHUB_LINK = re.compile(r'\]\(https://github\.com/([A-Za-z0-9][A-Za-z0-9-]*)/([A-Za-z0-9][A-Za-z0-9_.-]*)'
                         r'[^)\s]*\s+"Source on GitHub"\)')
DASH = re.compile('[' + chr(0x2013) + chr(0x2014) + ']')   # an en dash or an em dash
EMAIL = re.compile(r'[A-Za-z0-9._%+-]+@[A-Za-z0-9-]+(\.[A-Za-z0-9-]+)+')
PRIVATE = re.compile(r'/Users/|/home/|/scratch/|/tmp/|ghp_[A-Za-z0-9]|github_pat_|AKIA[0-9A-Z]{8}')
ISBN = re.compile(r'\bISBN\b', re.I)
EMPTY = hashlib.sha256(b'').hexdigest()


class Fail(Exception):
    """A problem that the user can read and fix; the run stops and puts the files back."""


def say(*a):
    print(*a, flush=True)


def rel(path):
    return os.path.relpath(path, ROOT)


def get_bytes(path):
    try:
        with open(path, 'rb') as f:
            return f.read()
    except FileNotFoundError:
        return None


def get_text(path):
    data = get_bytes(path)
    return None if data is None else data.decode('utf-8')


def as_bytes(data):
    return data.encode('utf-8') if isinstance(data, str) else data


def digest(path):
    return hashlib.sha256(get_bytes(path) or b'').hexdigest()


class Txn:
    """Remembers each file as it was before the first write, so that a failed run can put it back."""

    def __init__(self):
        self.before = {}

    def watch(self, path):
        if path not in self.before:
            self.before[path] = get_bytes(path)

    def write(self, path, data):
        self.watch(path)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'wb') as f:
            f.write(as_bytes(data))

    def changed(self):
        return sorted(p for p, old in self.before.items() if get_bytes(p) != old)

    def restore(self):
        for p, old in self.before.items():
            if old is None:
                if os.path.isfile(p):
                    os.remove(p)
            elif get_bytes(p) != old:
                with open(p, 'wb') as f:
                    f.write(old)


# ---------------------------------------------------------------------------------------------------- the network

def http_get(url, limit=40_000_000, nocache=False):
    headers = {'User-Agent': 'vsokolov.org site script'}
    if nocache:
        headers['Cache-Control'] = 'no-cache'
    try:
        with urllib.request.urlopen(urllib.request.Request(url, headers=headers), timeout=60) as r:
            data = r.read(limit + 1)
    except urllib.error.HTTPError as e:
        raise Fail(f'{url}: HTTP {e.code}')
    except (urllib.error.URLError, OSError) as e:
        raise Fail(f'{url}: {e}')
    if len(data) > limit:
        raise Fail(f'{url}: more than {limit} bytes')
    return data


def probe(url):
    """The status of a request for the first byte of url, or the reason it failed; a few tries for a slow server."""
    last = ''
    for _ in range(3):
        req = urllib.request.Request(url, headers={'User-Agent': 'vsokolov.org site script', 'Range': 'bytes=0-0'})
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                r.read(1)
                return r.status
        except urllib.error.HTTPError as e:
            if e.code < 500:
                return e.code
            last = e.code
        except (urllib.error.URLError, OSError) as e:
            last = str(e)
        time.sleep(2)
    return last


def check_release(owner, repo, book):
    """The release that the pages link must exist, because the default branch can hold the work toward the next version, and the
    addresses that a reader follows (the PDF, the DOI and its badge, the online edition, the repository) must answer."""
    out = []
    tag = (book.get('release') or {}).get('tag')
    if not tag:
        out.append('book.json names no release tag')
    else:
        p = subprocess.run(['git', 'ls-remote', f'https://github.com/{owner}/{repo}.git', f'refs/tags/{tag}'],
                           capture_output=True, text=True, timeout=120)
        if p.returncode or not p.stdout.strip():
            out.append(f'book.json names the release {tag}, which {owner}/{repo} does not have: the default branch holds work '
                       'toward the next version, so use --ref with the latest release tag, or wait for the release')
    links = book.get('links') or {}
    for key in ('pdf', 'doi', 'doi_badge', 'html', 'repository'):
        if links.get(key):
            code = probe(links[key])
            if code not in (200, 206):
                out.append(f'links.{key} ({links[key]}) answers {code}')
    return out


def parse_book(arg):
    owner, _, repo = arg.rpartition('/')
    owner = owner or OWNER
    if not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9-]*', owner) or not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_.-]*', repo):
        raise Fail(f'{arg}: not a repository name')
    return owner, repo


def resolve(owner, repo, ref):
    """The commit that REF names, so that every file of one run comes from the same commit."""
    if not re.fullmatch(r'[A-Za-z0-9._/-]+', ref):
        raise Fail(f'{ref}: not a branch, tag or commit')
    if re.fullmatch(r'[0-9a-f]{40}', ref):
        return ref
    names = [f'refs/heads/{ref}', f'refs/tags/{ref}^{{}}', f'refs/tags/{ref}']
    p = subprocess.run(['git', 'ls-remote', f'https://github.com/{owner}/{repo}.git', *names],
                       capture_output=True, text=True, timeout=120)
    if p.returncode:
        raise Fail(f'git ls-remote {owner}/{repo}: {p.stderr.strip()}')
    found = dict(reversed(line.split('\t')) for line in p.stdout.splitlines() if '\t' in line)
    for name in names:
        if name in found:
            return found[name]
    if re.fullmatch(r'[0-9a-f]{7,39}', ref):
        return json.loads(http_get(f'https://api.github.com/repos/{owner}/{repo}/commits/{ref}'))['sha']
    raise Fail(f'{owner}/{repo} has no branch, tag or commit {ref}')


class Bundle:
    """What a book repository publishes for the site (site/ and the cover), checked, at one commit."""

    def __init__(self, owner, repo, sha, book, files, llms, cover_name, cover):
        self.owner, self.repo, self.sha, self.book = owner, repo, sha, book
        self.files, self.llms, self.cover_name, self.cover = files, llms, cover_name, cover
        self.slug = book['slug']
        self.has_results = '_results.md' in files


def full_title(book):
    return f"{book['title']}: {book['subtitle']}" if book.get('subtitle') else book['title']


def fetch_bundle(owner, repo, ref, probes=True):
    sha = resolve(owner, repo, ref)
    raw = f'https://raw.githubusercontent.com/{owner}/{repo}/{sha}/'
    try:
        book = json.loads(http_get(raw + 'site/book.json').decode('utf-8'))
    except ValueError as e:
        raise Fail(f'site/book.json of {owner}/{repo} is not JSON: {e}')
    bundle = book.get('bundle') or {'page': 'site/index.md', 'head': 'site/head.html', 'llms': 'site/llms.txt'}
    files = {}
    for key, name in COPIES:
        path = bundle.get(key)
        if path:
            if not re.fullmatch(r'site/[A-Za-z0-9_.-]+', path):
                raise Fail(f'book.json names the file {path}, which is not under site/')
            files[name] = http_get(raw + path)
    if ('_results.md' in files) != ('results-head.html' in files):
        raise Fail('the results page and its head come as a pair, and one of them is missing')
    if not re.fullmatch(r'site/[A-Za-z0-9_.-]+', bundle.get('llms') or ''):
        raise Fail('book.json does not name site/llms.txt')
    llms = http_get(raw + bundle['llms']).decode('utf-8')
    serve = book.get('serve') or []
    if not serve:
        raise Fail('book.json lists no cover: set cover_image in book.yaml and generate again')
    if len(serve) != 1 or not re.fullmatch(r'cover\.(jpg|png)', serve[0].get('path', '')):
        names = [s.get('path', '?') for s in serve]
        raise Fail('book.json serves ' + ', '.join(names[:3]) + (f' and {len(names) - 3} more files' if len(names) > 3 else '')
                   + ', and only cover.jpg or cover.png is expected: site/ was made by an older generator, so generate it '
                   'again in the book repository')
    name, url = serve[0]['path'], serve[0].get('url', '')
    if not url.startswith(f'https://raw.githubusercontent.com/{owner}/{repo}/'):
        raise Fail(f'the cover comes from {url}, not from the repository')
    cover = http_get(url, limit=8_000_000)
    if not (cover[:3] == b'\xff\xd8\xff' or cover[:8] == b'\x89PNG\r\n\x1a\n'):
        raise Fail(f'{name} is neither a JPEG nor a PNG file')
    problems = check_bundle(book, {n: d.decode('utf-8') for n, d in files.items()}, llms)
    if probes:
        problems += check_release(owner, repo, book)
    if problems:
        raise Fail(f'{owner}/{repo} at {sha[:7]} cannot go on the site:\n  ' + '\n  '.join(problems))
    return Bundle(owner, repo, sha, book, files, llms, name, cover)


def scan(name, text):
    out = []
    for n, line in enumerate(text.splitlines(), 1):
        for pattern, what in ((DASH, 'an em or en dash'), (EMAIL, 'an e-mail address'), (PRIVATE, 'a local path or a token'),
                              (ISBN, 'an ISBN')):
            if pattern.search(line):
                out.append(f'{name}:{n}: {what}')
    return out


def results_links(text):
    return set(re.findall(r'results\.html#([A-Za-z0-9_]+)', text))


def check_bundle(book, texts, llms):
    p = []
    slug = book.get('slug', '')
    if not SLUG.fullmatch(slug):
        p.append(f'the slug {slug!r} is not lowercase letters, digits, underscores and hyphens')
    links = book.get('links') or {}
    if links.get('page') != f'{SITE}/books/{slug}/':
        p.append(f"links.page is {links.get('page')!r}, not {SITE}/books/{slug}/")
    for key in ('title', 'credit_names', 'year', 'date_released', 'short_description'):
        if not str(book.get(key) or '').strip():
            p.append(f'book.json has no {key}')
    if not re.fullmatch(r'\d{4}-\d{2}-\d{2}', str(book.get('date_released') or '')):
        p.append('date_released is not a date like 2026-10-13')
    if not book.get('authors') or not all(a.get('name') for a in book['authors']):
        p.append('book.json has no authors with names')
    for key in ('repository', 'cover'):
        if not links.get(key):
            p.append(f'book.json has no links.{key}')
    for key in ('title', 'subtitle', 'credit_names'):
        if re.search(r'["\\\n]', str(book.get(key) or '')):
            p.append(f'the {key} has a double quote, a backslash or a line break, which the page templates cannot hold')
    for name in ('_page.md', 'head.html'):
        if not texts.get(name):
            p.append(f'the bundle has no {name}')
    if ('_results.md' in texts) != bool(links.get('results')):
        p.append('links.results and the results page of the bundle disagree')
    if not llms.startswith('## ') or f'{SITE}/books/{slug}/index.html.md' not in llms:
        p.append('llms.txt does not start with a book heading or does not link the Markdown copy of the page')
    for name, text in sorted(texts.items()):
        p += scan('site/' + name, text)
    p += scan('site/llms.txt', llms)
    p += scan('site/book.json', json.dumps(book, ensure_ascii=False, indent=1))
    if '_results.md' in texts:
        ids = set(re.findall(r'<a id="([^"]+)"', texts['_results.md']))
        missing = (results_links(texts.get('_page.md', '')) | results_links(llms)) - ids
        if missing:
            p.append('links to results that are not on the results page: ' + ', '.join(sorted(missing)))
    return p


# ---------------------------------------------------------------------------------------------------- the pages

def fill(template, book, cover):
    path = os.path.join(BOOKS, '_templates', template)
    text = get_text(path)
    if text is None:
        raise Fail(f'{rel(path)} is missing')
    ft = full_title(book)
    return string.Template(text).substitute(pagetitle=f"{ft} | {book['credit_names']}", full_title=ft, cover=cover)


def join_names(xs):
    return ''.join(xs) if len(xs) <= 1 else ', '.join(xs[:-1]) + ' and ' + xs[-1]


def icon(kind):
    return f'{SITE}/books/icon-{kind}.svg'


def entry(book):
    """The four paragraphs of a book on the list page."""
    L, page = book['links'], book['links']['page']
    head = f"## [{book['title']}]({page})" + (f" <small>{book['subtitle']}</small>" if book.get('subtitle') else '')
    by = f"{join_names([a['name'] for a in book['authors']])}. {book['year']}."
    if str(book.get('edition') or '').strip():
        by += f" Edition {book['edition']}."
    cover = f"[![{full_title(book)}]({L['cover']})]({page}) {by}"
    items = []
    if L.get('pdf'):
        items.append(f'[![PDF]({icon("pdf")})]({L["pdf"]} "PDF")')
    if L.get('html'):
        items.append(f'[![Online edition]({icon("web")})]({L["html"]} "Online edition")')
    items.append(f'[![Source on GitHub]({icon("github")})]({L["repository"]} "Source on GitHub")')
    if L.get('doi_badge') and L.get('doi'):
        items.append(f'[![DOI {book["doi"]}]({L["doi_badge"]})]({L["doi"]})')
    if L.get('print'):
        items.append(f'[![Paperback, available at Amazon]({SITE}/books/{AMAZON_BADGE})]({L["print"]} "Paperback on Amazon")')
    return [head, cover, book['short_description'].strip(), ' '.join(items)]


def ld_item(book):
    people = []
    for a in book['authors']:
        person = {'@type': 'Person', 'name': a['name']}
        if a.get('orcid'):
            person['sameAs'] = a['orcid']
        people.append(person)
    return {'@type': 'Book', 'name': book['title'], 'url': book['links']['page'], 'author': people,
            'datePublished': book['date_released'], 'image': book['links']['cover']}


def slug_in(text):
    m = re.search(r'https://vsokolov\.org/books/([a-z0-9][a-z0-9_-]*)/', text)
    return m.group(1) if m else None


def parse_list(text):
    """The list page: the introduction, the entries of four paragraphs each (by slug) and the closing paragraphs."""
    paras = text.rstrip('\n').split('\n\n')
    i = next((k for k, p in enumerate(paras) if p.startswith('## [')), len(paras))
    intro, entries, order = paras[:i], {}, []
    while i < len(paras) and paras[i].startswith('## ['):
        group = paras[i:i + 4]
        slug = slug_in(group[0])
        if len(group) < 4 or any(g.startswith('## [') for g in group[1:]) or not slug:
            raise Fail('books/_page.md: an entry is not made of a heading and three paragraphs; fix it by hand or restore it')
        entries[slug] = group
        order.append(slug)
        i += 4
    return intro, entries, order, paras[i:]


def render_list(intro, entries, order, tail):
    return '\n\n'.join(intro + [p for s in order for p in entries[s]] + tail) + '\n'


LD = re.compile(r'(<script type="application/ld\+json">\n)(.*?)(\n</script>)', re.S)


def parse_head(text):
    m = LD.search(text)
    if not m:
        raise Fail('books/head.html has no JSON-LD block')
    data = json.loads(m.group(2))
    return m, data, [it['item'] for it in data['itemListElement']]


def render_head(text, m, data, items):
    data['itemListElement'] = [{'@type': 'ListItem', 'position': k, 'item': it} for k, it in enumerate(items, 1)]
    return text[:m.start(2)] + json.dumps(data, indent=1, ensure_ascii=False) + text[m.end(2):]


def parse_llms(text):
    parts = re.split(r'(?m)^(?=## )', text)
    head, books, order, optional = parts[0], {}, [], []
    for sec in parts[1:]:
        sec = sec.rstrip('\n') + '\n'
        if sec.startswith('## Optional'):
            optional.append(sec)
            continue
        slug = slug_in(sec)
        if not slug or slug in books:
            raise Fail('llms.txt: a section is not the section of one book')
        books[slug] = sec
        order.append(slug)
    return head, books, order, optional


def render_llms(head, books, order, optional):
    return head + '\n'.join([books[s] for s in order] + optional)


def new_order(order, dates, slug, date):
    """Newest first. A listed book keeps its place unless its release date changed; a new book goes in front of the first
    book that is not newer."""
    if slug in order and dates.get(slug) == date:
        return list(order)
    rest = [s for s in order if s != slug]
    i = 0
    while i < len(rest) and dates[rest[i]] > date:
        i += 1
    return rest[:i] + [slug] + rest[i:]


def llms_full(order):
    pages = []
    for slug in order:
        for url, name in ((f'{SITE}/books/{slug}/', 'index.html.md'), (f'{SITE}/books/{slug}/results.html', 'results.html.md')):
            text = get_text(os.path.join(DOCS, 'books', slug, name))
            if text is not None:
                pages.append(f'Page: {url}\n\n{text}')
    return '\n'.join(pages)


def same_books(*named):
    """All the places that list the books list the same ones."""
    for name, order in named[1:]:
        if set(order) != set(named[0][1]):
            raise Fail(f'{name} lists {sorted(order)} but {named[0][0]} lists {sorted(named[0][1])}')


def plan(b):
    """Every file that is written before rendering, as {path: content}, and the order of the books."""
    book, slug, folder = b.book, b.slug, os.path.join(BOOKS, b.slug)
    out = {os.path.join(folder, name): data for name, data in b.files.items()}
    out[os.path.join(folder, b.cover_name)] = b.cover
    out[os.path.join(folder, 'index.qmd')] = fill('book-page.qmd', book, b.cover_name)
    if b.has_results:
        out[os.path.join(folder, 'results.qmd')] = fill('book-results.qmd', book, b.cover_name)
    list_path, head_path = os.path.join(BOOKS, '_page.md'), os.path.join(BOOKS, 'head.html')
    llms_path = os.path.join(ROOT, 'llms.txt')
    intro, entries, order, tail = parse_list(get_text(list_path))
    head_text = get_text(head_path)
    m, data, items = parse_head(head_text)
    ld = {slug_in(it['url']): it for it in items}
    lhead, sections, lorder, optional = parse_llms(get_text(llms_path))
    same_books(('books/_page.md', order), ('books/head.html', list(ld)), ('llms.txt', lorder))
    final = new_order(list(ld), {s: it['datePublished'] for s, it in ld.items()}, slug, book['date_released'])
    entries[slug], ld[slug], sections[slug] = entry(book), ld_item(book), b.llms.rstrip('\n') + '\n'
    out[list_path] = render_list(intro, entries, final, tail)
    out[head_path] = render_head(head_text, m, data, [ld[s] for s in final])
    out[llms_path] = render_llms(lhead, sections, final, optional)
    return out, final


# ---------------------------------------------------------------------------------------------------- rendering

def quarto(*files):
    if not any(os.access(os.path.join(d, 'quarto'), os.X_OK) for d in os.environ.get('PATH', '').split(os.pathsep)):
        raise Fail('quarto is not installed or not on the PATH')
    for f in files:
        say(f'  quarto render {f}')
        p = subprocess.run(['quarto', 'render', f], cwd=ROOT, capture_output=True, text=True)
        if p.returncode:
            raise Fail(f'quarto render {f} failed:\n' + '\n'.join((p.stdout + p.stderr).splitlines()[-25:]))


URL = re.compile(r'(<loc>([^<]+)</loc>\s*<lastmod>)([^<]+)(</lastmod>)')


def keep_lastmod(old_text, new_text, unchanged):
    """The sitemap says when a page changed, and a page that was rendered again without a change did not."""
    old = {m.group(2): m.group(3) for m in URL.finditer(old_text)}
    return URL.sub(lambda m: m.group(1) + old[m.group(2)] + m.group(4) if m.group(2) in unchanged and m.group(2) in old
                   else m.group(0), new_text)


def prune_search(slug, txn):
    """Quarto keeps the search entry of a heading that a page no longer has."""
    path = os.path.join(DOCS, 'search.json')
    text = get_text(path)
    keep, dropped = [], 0
    for e in json.loads(text):
        page, _, frag = e['href'].lstrip('/').partition('#')
        html = get_text(os.path.join(DOCS, page)) if frag and page.startswith(f'books/{slug}/') else None
        if html is not None and f' id="{frag}"' not in html:
            dropped += 1
        else:
            keep.append(e)
    if dropped:
        txn.write(path, json.dumps(keep, indent=2, ensure_ascii=False) + ('\n' if text.endswith('\n') else ''))
        say(f'  removed {dropped} search entr{"y" if dropped == 1 else "ies"} of anchors that are gone')


SM_BLOCK = re.compile(r'[ \t]*<url>.*?</url>[ \t]*\n', re.S)
SM_LOC = re.compile(r'<loc>([^<]+)</loc>')
SM_LASTMOD = re.compile(r'<lastmod>([^<]+)</lastmod>')


def owned_page(page, slug):
    """The pages that a refresh of a book brings up to date in the shared files: its own, and the list page, whose text names it."""
    return page.startswith(f'books/{slug}/') or page == 'books/index.html'


def merge_sitemap(base, work, slug):
    """`base`, the committed docs/sitemap.xml, with the URLs of the book as `work`, the file as it is now, has them: a URL that is
    there is replaced where it stands, a new one goes to the end (Quarto adds a page at the end), one that `work` no longer has
    goes; a page is never taken back to an older lastmod than the committed one. Every other URL stays as committed, so the
    changes of other work in `work` are not taken along."""
    def loc(block):
        m = SM_LOC.search(block)
        return m.group(1) if m else ''

    def mine(url):
        return url.startswith(SITE + '/') and owned_page(url[len(SITE) + 1:], slug)
    new = {loc(m.group(0)): m.group(0) for m in SM_BLOCK.finditer(work) if mine(loc(m.group(0)))}
    seen = set()

    def swap(m):
        url = loc(m.group(0))
        if not mine(url):
            return m.group(0)
        seen.add(url)
        mine_now = new.get(url, '')
        old, cur = SM_LASTMOD.search(m.group(0)), SM_LASTMOD.search(mine_now)
        return m.group(0) if old and cur and old.group(1) > cur.group(1) else mine_now
    out = SM_BLOCK.sub(swap, base)
    added = ''.join(b for url, b in new.items() if url not in seen)
    return out.replace('</urlset>', added + '</urlset>', 1) if added else out


def merge_search(base, work, slug):
    """The same for docs/search.json: the entries of the pages of the book as `work` has them, where the committed ones stand
    (the entries of a new page go to the end), and the file written the way Quarto writes it."""
    def page(e):
        return e['href'].lstrip('/').partition('#')[0]
    new = {}
    for e in json.loads(work):
        if owned_page(page(e), slug):
            new.setdefault(page(e), []).append(e)
    out, seen = [], set()
    for e in json.loads(base):
        p = page(e)
        if not owned_page(p, slug):
            out.append(e)
        elif p not in seen:
            seen.add(p)
            out.extend(new.get(p, []))
    for p, es in new.items():
        if p not in seen:
            out.extend(es)
    return json.dumps(out, indent=2, ensure_ascii=False) + ('\n' if base.endswith('\n') else '')


def repo_of(slug):
    """The repository that a listed book comes from: the GitHub link of its entry on the list page (the repository can have
    another name than the slug), or OWNER/slug when the entry has none."""
    try:
        entries = parse_list(get_text(os.path.join(BOOKS, '_page.md')))[1]
    except Fail:
        entries = {}
    m = GITHUB_LINK.search(' '.join(entries.get(slug, [])))
    return (m.group(1), m.group(2)) if m else (OWNER, slug)


def ensure_copies(slug):
    """Quarto reads the include files of every book at every render, so a book whose copies are missing is fetched first."""
    for d in sorted(glob.glob(os.path.join(BOOKS, '*', 'index.qmd'))):
        folder = os.path.dirname(d)
        other = os.path.basename(folder)
        if other == slug:
            continue
        cover = re.search(r'^  - (cover\.(?:jpg|png))$', get_text(d), re.M)
        needed = ['_page.md', 'head.html'] + ([cover.group(1)] if cover else [])
        if os.path.isfile(os.path.join(folder, 'results.qmd')):
            needed += ['_results.md', 'results-head.html']
        if all(os.path.isfile(os.path.join(folder, n)) for n in needed):
            continue
        say(f'  fetching the copies of {other}, which the render needs')
        b = fetch_bundle(*repo_of(other), 'main', probes=False)
        for name, data in list(b.files.items()) + [(b.cover_name, b.cover)]:
            with open(os.path.join(folder, name), 'wb') as f:
                f.write(data)


def verify_outputs(slug, has_results):
    pairs = [(os.path.join(BOOKS, slug, '_page.md'), os.path.join(DOCS, 'books', slug, 'index.html.md')),
             (os.path.join(BOOKS, '_page.md'), os.path.join(DOCS, 'books', 'index.html.md'))]
    if has_results:
        pairs.append((os.path.join(BOOKS, slug, '_results.md'), os.path.join(DOCS, 'books', slug, 'results.html.md')))
    for src, out in pairs:
        if get_bytes(src) is None or get_bytes(src) != get_bytes(out):
            raise Fail(f'{rel(out)} is not the Markdown copy of {rel(src)}: the post-render step copy_markdown.py did not run')
    for name in ('index.html', 'results.html') if has_results else ('index.html',):
        if not os.path.isfile(os.path.join(DOCS, 'books', slug, name)):
            raise Fail(f'docs/books/{slug}/{name} was not rendered')
    page = get_text(os.path.join(DOCS, 'books', slug, 'index.html'))
    for tag in ('og:description', 'application/ld+json', 'rel="canonical"'):
        if tag not in page:
            raise Fail(f'docs/books/{slug}/index.html has lost {tag}: the head of the book did not apply')


def refresh_site(b, final, txn):
    """Render the pages of the book and the list page, and bring the files that depend on the rendering up to date. A page
    that comes out the same keeps its bytes and its lastmod, so rendering a page whose source did not change is harmless."""
    slug = b.slug
    pages = [f'books/{slug}/index.qmd'] + ([f'books/{slug}/results.qmd'] if b.has_results else []) + ['books/index.qmd']
    outs = {p: os.path.join(DOCS, os.path.splitext(p)[0] + '.html') for p in pages}
    for o in outs.values():
        txn.watch(o)
        txn.watch(o + '.md')
    for name in (f'books/{slug}/cover.jpg', f'books/{slug}/cover.png', 'sitemap.xml', 'search.json', 'llms.txt', 'llms-full.txt'):
        txn.watch(os.path.join(DOCS, name))
    before = {p: digest(o) for p, o in outs.items()}
    sitemap_before = get_text(os.path.join(DOCS, 'sitemap.xml'))
    ensure_copies(slug)
    quarto(*pages)
    unchanged = {f'{SITE}/{os.path.relpath(o, DOCS)}' for p, o in outs.items() if before[p] != EMPTY and digest(o) == before[p]}
    sitemap = os.path.join(DOCS, 'sitemap.xml')
    if sitemap_before is not None and get_text(sitemap) is not None:
        txn.write(sitemap, keep_lastmod(sitemap_before, get_text(sitemap), unchanged))
    prune_search(slug, txn)
    verify_outputs(slug, b.has_results)
    full = llms_full(final)
    txn.write(os.path.join(ROOT, 'llms-full.txt'), full)
    txn.write(os.path.join(DOCS, 'llms-full.txt'), full)
    txn.write(os.path.join(DOCS, 'llms.txt'), get_bytes(os.path.join(ROOT, 'llms.txt')))


# ---------------------------------------------------------------------------------------------------- git

def git(*args, check=True):
    p = subprocess.run(['git', *args], cwd=ROOT, capture_output=True, text=True)
    if check and p.returncode:
        raise Fail('git ' + ' '.join(args) + ': ' + (p.stderr or p.stdout).strip())
    return p.stdout


def dirty():
    """The paths that differ from HEAD (modified, deleted, staged or untracked), one per file."""
    fields = git('status', '--porcelain=v1', '-uall', '-z').split('\0')
    paths, i = set(), 0
    while i < len(fields):
        if fields[i]:
            paths.add(fields[i][3:])
            i += 1 if fields[i][0] not in 'RC' else 2
        else:
            i += 1
    return paths


def guard_push():
    if git('branch', '--show-current').strip() != 'main':
        raise Fail('--push needs the branch main')
    git('fetch', '-q', 'origin', 'main')
    if git('rev-parse', 'HEAD').strip() != git('rev-parse', 'origin/main').strip():
        raise Fail('HEAD is not origin/main: run git pull first, or push what is unpushed before you refresh a book')


def subject(b, new_book, entries=False):
    title = b.book['title']
    if entries:
        return f'Add the entries of {title} to the sitemap and the search index'
    return f'Add {title} to the books section' if new_book else f'Refresh the pages of {title} from its repository'


def tracked_files(written):
    """The files of the run that git tracks; the downloaded copies are ignored."""
    changed = [rel(p) for p in written]
    ignored = set(git('check-ignore', *changed, check=False).split('\n')) if changed else set()
    return [c for c in changed if c not in ignored]


def commit_commands(b, files, new_book):
    say('  To commit exactly these files and nothing else:')
    say(f'    git add -- {" ".join(files)}')
    say(f'    git commit -m "{subject(b, new_book)}" -- {" ".join(files)}')


def head_text(path):
    """The text of a file in HEAD, None when HEAD does not have it."""
    p = subprocess.run(['git', 'show', f'HEAD:{path}'], cwd=ROOT, capture_output=True)
    return p.stdout.decode('utf-8') if p.returncode == 0 else None


def own_entries(slug, held):
    """For each of the shared files in `held` (they hold other uncommitted work): its committed text with the entries of the book
    put in, when that is a change. A commit may take that much of such a file and no more."""
    out = {}
    for path in held:
        base, work = head_text(path), get_text(os.path.join(ROOT, path))
        if base is None or work is None:
            continue
        try:
            merged = (merge_sitemap if path.endswith('.xml') else merge_search)(base, work, slug)
        except (ValueError, KeyError, TypeError) as e:
            raise Fail(f'{path} is not in the form that the script expects ({e}); nothing is committed of it')
        if merged != base:
            out[path] = merged
    return out


def commit_tree(message, files, blobs):
    """One commit with `files` as they are in the working copy and `blobs` (path: text) as given, made in a temporary index, so
    that the index and the working copy of other work stay as they are. Afterwards the index entries of these paths are set to
    the new HEAD (git reset leaves the working copy alone): a file that holds more than the commit shows as modified again."""
    head = git('rev-parse', 'HEAD').strip()
    with tempfile.TemporaryDirectory() as tmp:
        env = dict(os.environ, GIT_INDEX_FILE=os.path.join(tmp, 'index'))

        def g(*args, data=None):
            p = subprocess.run(['git', *args], cwd=ROOT, env=env, capture_output=True, input=data)
            if p.returncode:
                raise Fail('git ' + ' '.join(args) + ': ' + (p.stderr or p.stdout).decode('utf-8', 'replace').strip())
            return p.stdout.decode('utf-8')
        g('read-tree', head)
        if files:
            g('add', '--', *files)
        for path, text in blobs.items():
            mode = (g('ls-tree', head, '--', path).split() or ['100644'])[0]
            sha = g('hash-object', '-w', '--stdin', data=text.encode('utf-8')).strip()
            g('update-index', '--add', '--cacheinfo', f'{mode},{sha},{path}')
        g('commit', '-q', '-F', message)
    r = subprocess.run(['git', 'reset', '-q', '--', *files, *blobs], cwd=ROOT, capture_output=True, text=True)
    if r.returncode:   # the commit is made; only the index entries of these paths still show the old state
        say(f'  note: the commit is made, but git reset failed ({(r.stderr or r.stdout).strip()}); run: '
            f'git reset -q -- {" ".join([*files, *blobs])}')


def commit(b, written, dirty_before, new_book):
    """Commit what the run changed. Returns the files committed and, for a shared file that holds other work, the text that was
    committed of it (the push compares the live file with that, not with the working copy)."""
    files = tracked_files(written)
    held = [c for c in files if c in dirty_before]
    blocking = [c for c in held if c not in SHARED]
    if blocking:
        commit_commands(b, files, new_book)
        raise Fail(f'nothing committed: {", ".join(blocking)} held other uncommitted changes before this run and this run '
                   'changed them too, so a commit of the rest would leave the site inconsistent. Commit or discard those '
                   'changes first, then commit the files of this run with the commands above.')
    own = own_entries(b.slug, [c for c in SHARED if c in dirty_before])
    for c in held:
        if c not in own:
            say(f'  not committed: {c} held other uncommitted changes before this run, so it is yours to commit')
    files = [c for c in files if c not in held]
    if not files and not own:
        say('  nothing to commit')
        return [], {}
    first = subject(b, new_book, entries=not files)
    body = f'The pages follow {b.owner}/{b.repo} at {b.sha[:7]}.\n'
    if own:
        body += (f'\n{" and ".join(sorted(own))}: only the entries of {b.slug} and of the list page; the files hold other '
                 'uncommitted work, which this commit leaves alone.\n')
    with tempfile.NamedTemporaryFile('w', suffix='.txt', delete=False, encoding='utf-8') as f:
        f.write(f'{first}\n\n{body}')
    try:
        if own:
            commit_tree(f.name, files, own)
        else:
            git('add', '--', *files)
            git('commit', '-q', '-F', f.name, '--', *files)
    finally:
        os.remove(f.name)
    for c in sorted(own):
        say(f'  {c} holds other uncommitted work: committed only the entries of the book, the rest stays in your working copy')
    done = files + sorted(own)
    say(f'  committed {len(done)} files as {git("rev-parse", "--short", "HEAD").strip()}: {first}')
    return done, own


def pages_latest():
    try:
        p = subprocess.run(['gh', 'api', f'repos/{SITE_REPO}/pages/builds/latest'], capture_output=True, text=True, timeout=60)
        if p.returncode == 0:
            return json.loads(p.stdout)
    except (FileNotFoundError, subprocess.TimeoutExpired):
        pass
    return json.loads(http_get(f'https://api.github.com/repos/{SITE_REPO}/pages/builds/latest'))


def push(files, expect=None):
    sha = git('rev-parse', 'HEAD').strip()
    git('push', 'origin', 'main')
    say(f'  pushed {sha[:7]}; waiting for the GitHub Pages build')
    deadline = time.time() + 900
    while True:
        latest = pages_latest()
        if latest.get('commit') == sha and latest.get('status') == 'built':
            break
        if latest.get('commit') == sha and latest.get('status') == 'errored':
            raise Fail('the GitHub Pages build failed')
        if time.time() > deadline:
            raise Fail('the GitHub Pages build did not finish in 15 minutes')
        time.sleep(15)
    bad = []
    for f in (f for f in files if f.startswith('docs/')):
        want = expect[f].encode('utf-8') if expect and f in expect else get_bytes(os.path.join(ROOT, f))
        for attempt in range(6):
            if http_get(f'{SITE}/{f[len("docs/"):]}?v={int(time.time())}', nocache=True) == want:
                break
            time.sleep(10)
        else:
            bad.append(f)
    if bad:
        raise Fail('the live files differ from docs/: ' + ', '.join(bad))
    say(f'  built and live: {len([f for f in files if f.startswith("docs/")])} files match docs/')


# ---------------------------------------------------------------------------------------------------- the commands

def allowed(path, slug):
    return (path.startswith((f'books/{slug}/', f'docs/books/{slug}/')) or
            path in ('books/_page.md', 'books/head.html', 'docs/books/index.html', 'docs/books/index.html.md', 'llms.txt',
                     'llms-full.txt', 'docs/llms.txt', 'docs/llms-full.txt', 'docs/search.json', 'docs/sitemap.xml'))


def stale_docs(b):
    """What in docs/ was not rendered from the page that the repository has now, for example after the rendered pages were
    discarded with git while the downloaded copies stayed."""
    out = []
    for name, src in [('index.html', '_page.md')] + ([('results.html', '_results.md')] if b.has_results else []):
        html = os.path.join(DOCS, 'books', b.slug, name)
        if not os.path.isfile(html):
            out.append(f'docs/books/{b.slug}/{name} is missing')
        elif get_bytes(html + '.md') != b.files[src]:
            out.append(f'docs/books/{b.slug}/{name}.md is not the copy of the page in the repository')
    return out


def refresh(args):
    owner, repo = parse_book(args.book)
    if args.push:
        args.commit = True
        guard_push()
    b = fetch_bundle(owner, repo, args.ref)
    say(f'{b.slug}: {owner}/{repo} at {b.sha[:7]}')
    files, final = plan(b)
    differing = {p: d for p, d in files.items() if get_bytes(p) != as_bytes(d)}
    stale = stale_docs(b)
    todo = bool(differing or stale or args.force)
    new_book = not os.path.isfile(os.path.join(BOOKS, b.slug, 'index.qmd'))
    dirty_now = dirty()
    pending = own_entries(b.slug, [c for c in SHARED if c in dirty_now])   # entries that HEAD lacks in files of other work
    if args.check:
        for p in sorted(differing):
            say('  would change', rel(p))
        for s in stale:
            say('  would render again:', s)
        for p in sorted(pending):
            say('  would change', p, '(only the entries of the book: the file holds other uncommitted work)')
        say('  would render the pages' if todo else '  would commit the entries of the book' if pending else '  up to date')
        return 1 if todo or pending else 0
    if not b.has_results and os.path.isfile(os.path.join(BOOKS, b.slug, 'results.qmd')):
        say(f'  WARNING: the book has no results page any more. Remove by hand: books/{b.slug}/results.qmd, _results.md and '
            f'results-head.html, and docs/books/{b.slug}/results.html and results.html.md')
    if not todo and not pending:
        say('  already up to date')
        return 0
    before = dirty()
    if not todo:   # nothing to render: only the entries of the book that the files of other work keep from HEAD are left
        if not args.commit:
            say(f'  not committed: {", ".join(sorted(pending))} lack entries of the book that the working copy has (run with --commit)')
            return 0
        committed, expect = commit(b, [], before, False)
        if args.push and committed:
            push(committed, expect)
        return 0
    txn = Txn()
    try:
        for p, d in differing.items():
            txn.write(p, d)
        refresh_site(b, final, txn)
    except BaseException:
        txn.restore()
        raise
    written = txn.changed()
    if not written and not pending:
        say('  rendered again, nothing changed')
        return 0
    if written:
        say(f'  changed {len(written)} files:')
    for p in written:
        say(f'    {rel(p)}')
    extra = sorted(p for p in dirty() - before if not allowed(p, b.slug))
    if extra:
        say('  WARNING: these other files changed too, look at them with git diff: ' + ', '.join(extra))
    if args.commit:
        committed, expect = commit(b, written, before, new_book)
        if args.push and committed:
            push(committed, expect)
    else:
        tracked = tracked_files(written)
        if tracked:
            say('  not committed.')
            commit_commands(b, tracked, new_book)
            held = [c for c in SHARED if c in before and (c in tracked or c in pending)]
            if held:
                say(f'  {", ".join(held)} hold other uncommitted work, which the commands above would take along: '
                    '--commit commits only the entries of the book')
        else:
            say('  nothing to commit: only the copies that are not committed changed')
    return 0


def parse_qmd(qmd, results):
    pt = re.search(r'^pagetitle: "(.*)"$', qmd, re.M)
    if not pt:
        return None
    pagetitle = pt.group(1)[len('Results by chapter | '):] if results else pt.group(1)
    cover = re.search(r'^  - (cover\.(?:jpg|png))$', qmd, re.M)
    alt = re.search(r'fig-alt="Cover of (.*)"\}', qmd)
    return dict(pagetitle=pagetitle, cover=cover.group(1) if cover else 'cover.jpg', full_title=alt.group(1) if alt else '')


def check_all():
    problems = []
    slugs = sorted(os.path.basename(os.path.dirname(p)) for p in glob.glob(os.path.join(BOOKS, '*', 'index.qmd')))
    try:
        intro, entries, order, tail = parse_list(get_text(os.path.join(BOOKS, '_page.md')))
        m, data, items = parse_head(get_text(os.path.join(BOOKS, 'head.html')))
        lhead, sections, lorder, optional = parse_llms(get_text(os.path.join(ROOT, 'llms.txt')))
    except (Fail, TypeError, ValueError, KeyError) as e:
        raise Fail(f'cannot read the lists: {e}')
    jorder = [slug_in(it['url']) for it in items]
    full = get_text(os.path.join(ROOT, 'llms-full.txt')) or ''
    forder = []
    for s in re.findall(r'(?m)^Page: https://vsokolov\.org/books/([a-z0-9_-]+)/', full):
        if s not in forder:
            forder.append(s)
    for name, o in (('books/_page.md', order), ('books/head.html', jorder), ('llms.txt', lorder), ('llms-full.txt', forder)):
        if o != jorder:
            problems.append(f'{name} lists the books as {o}, books/head.html as {jorder}')
    if sorted(jorder) != slugs:
        problems.append(f'the folders with an index.qmd are {slugs}, the books listed are {sorted(jorder)}')
    dates = [it['datePublished'] for it in items]
    if dates != sorted(dates, reverse=True):
        problems.append(f'the books are not newest first: {dict(zip(jorder, dates))}')
    if render_head(get_text(os.path.join(BOOKS, 'head.html')), m, data, items) != get_text(os.path.join(BOOKS, 'head.html')):
        problems.append('books/head.html is not written the way the script writes it')
    if render_list(intro, entries, order, tail) != get_text(os.path.join(BOOKS, '_page.md')):
        problems.append('books/_page.md is not written the way the script writes it')
    if render_llms(lhead, sections, lorder, optional) != get_text(os.path.join(ROOT, 'llms.txt')):
        problems.append('llms.txt is not written the way the script writes it')
    for slug in slugs:
        folder = os.path.join(BOOKS, slug)
        has_results = os.path.isfile(os.path.join(DOCS, 'books', slug, 'results.html'))
        if has_results != os.path.isfile(os.path.join(folder, 'results.qmd')):
            problems.append(f'books/{slug}: results.qmd and docs/books/{slug}/results.html do not go together')
        for template, name, results in (('book-page.qmd', 'index.qmd', False), ('book-results.qmd', 'results.qmd', True)):
            qmd = get_text(os.path.join(folder, name))
            if qmd is None:
                continue
            v = parse_qmd(qmd, results)
            if v is None or string.Template(get_text(os.path.join(BOOKS, '_templates', template))).substitute(**v) != qmd:
                problems.append(f'books/{slug}/{name} is not made from books/_templates/{template}')
        for src, out in (('_page.md', 'index.html.md'), ('_results.md', 'results.html.md')):
            a, o = get_bytes(os.path.join(folder, src)), get_bytes(os.path.join(DOCS, 'books', slug, out))
            if a is not None and a != o:
                problems.append(f'docs/books/{slug}/{out} is not the Markdown copy of books/{slug}/{src}')
        if has_results:
            ids = set(re.findall(r' id="([^"]+)"', get_text(os.path.join(DOCS, 'books', slug, 'results.html'))))
            page_md = get_text(os.path.join(DOCS, 'books', slug, 'index.html.md')) or ''
            linked = results_links(page_md) | results_links(sections.get(slug, ''))
            missing = {i for i in linked if i not in ids}
            if missing:
                problems.append(f'books/{slug}: links to results that are not on the results page: {sorted(missing)}')
        sitemap = get_text(os.path.join(DOCS, 'sitemap.xml')) or ''
        for name in ('index.html', 'results.html') if has_results else ('index.html',):
            if f'<loc>{SITE}/books/{slug}/{name}</loc>' not in sitemap:
                problems.append(f'docs/sitemap.xml does not list books/{slug}/{name}')
        for f in glob.glob(os.path.join(DOCS, 'books', slug, '*.md')):
            problems += scan(rel(f), get_text(f))
    for name in ('llms.txt', 'llms-full.txt'):
        if get_bytes(os.path.join(ROOT, name)) != get_bytes(os.path.join(DOCS, name)):
            problems.append(f'docs/{name} is not a copy of {name}')
        problems += scan(name, get_text(os.path.join(ROOT, name)) or '')
    if full != llms_full(jorder):
        problems.append('llms-full.txt is not the pages of the books in the order of the list')
    for f in (os.path.join(BOOKS, '_page.md'), os.path.join(BOOKS, 'head.html')):
        problems += scan(rel(f), get_text(f))
    for p in problems:
        say(f'problem: {p}')
    say(f'{len(slugs)} books checked: ' + (f'{len(problems)} problems' if problems else 'no problem'))
    return 1 if problems else 0


def main(argv=None):
    ap = argparse.ArgumentParser(description='Put a book on the website, or refresh it, without an agent.')
    sub = ap.add_subparsers(dest='cmd', required=True)
    r = sub.add_parser('refresh', aliases=['add'], help='put a book on the site or refresh it from its repository')
    r.add_argument('book', help='the repository of the book, VadimSokolov/BOOK or just BOOK')
    r.add_argument('--ref', default='main', help='branch, tag or commit of the repository (default main)')
    r.add_argument('--check', action='store_true', help='only say what would change')
    r.add_argument('--force', action='store_true', help='render the pages again although nothing differs')
    r.add_argument('--commit', action='store_true', help='commit exactly the files this run changed')
    r.add_argument('--push', action='store_true', help='commit, push, wait for the Pages build and compare the live files')
    sub.add_parser('check', help='offline checks of the whole books section')
    args = ap.parse_args(argv)
    os.chdir(ROOT)
    try:
        return refresh(args) if args.cmd in ('refresh', 'add') else check_all()
    except Fail as e:
        say(f'error: {e}')
        return 2


if __name__ == '__main__':
    sys.exit(main())
