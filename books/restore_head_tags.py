"""Put back the social tags of each book page's head.html and of each results page's results-head.html after Quarto rewrites them.

Quarto sets og:title, og:description and the twitter title and description tags it finds in a
page from the page's own title and description, which are not the book's. head.html comes from
the book repository and is the source of truth, so this copies its tags into the rendered page.
Run by Quarto after every render (post-render in _quarto.yml). It changes nothing when they match.
"""
import glob, os, re

out = os.environ.get('QUARTO_PROJECT_OUTPUT_DIR', 'docs')
keys = ('og:title', 'og:description', 'og:site_name', 'twitter:title', 'twitter:description')
tag = re.compile(r'<meta\s[^>]*?(?:property|name)="(%s)"[^>]*>' % '|'.join(re.escape(k) for k in keys))

pairs = [(h, 'index.html') for h in glob.glob('books/*/head.html')] + [(h, 'results.html') for h in glob.glob('books/*/results-head.html')]
for head, name in sorted(pairs):
    page = os.path.join(out, os.path.dirname(head), name)
    if not os.path.isfile(page):
        continue
    want = {m.group(1): m.group(0) for m in tag.finditer(open(head, encoding='utf-8').read())}
    html = open(page, encoding='utf-8').read()
    fixed = tag.sub(lambda m: want.get(m.group(1), m.group(0)), html)
    if fixed != html:
        open(page, 'w', encoding='utf-8').write(fixed)
