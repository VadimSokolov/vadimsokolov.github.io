import os, glob, shutil
out = os.environ.get('QUARTO_PROJECT_OUTPUT_DIR', 'docs')
for src, page in (('_page.md', 'index'), ('_results.md', 'results')):
    for f in glob.glob('books/' + src) + glob.glob('books/*/' + src):
        dest = os.path.join(out, os.path.dirname(f))
        if os.path.isfile(os.path.join(dest, page + '.html')):
            shutil.copyfile(f, os.path.join(dest, page + '.html.md'))
