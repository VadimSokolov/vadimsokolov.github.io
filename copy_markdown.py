import os, glob, shutil
out = os.environ.get('QUARTO_PROJECT_OUTPUT_DIR', 'docs')
# A render lists the files it wrote. Copy only for those pages, so that rendering one book leaves the other books alone.
done = {os.path.realpath(f) for f in os.environ.get('QUARTO_PROJECT_OUTPUT_FILES', '').split('\n') if f.strip()}
for src, page in (('_page.md', 'index'), ('_results.md', 'results')):
    for f in glob.glob('books/' + src) + glob.glob('books/*/' + src):
        dest = os.path.join(out, os.path.dirname(f))
        html = os.path.join(dest, page + '.html')
        if os.path.isfile(html) and (not done or os.path.realpath(html) in done):
            shutil.copyfile(f, os.path.join(dest, page + '.html.md'))
