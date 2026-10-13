import os, glob, shutil
out = os.environ.get('QUARTO_PROJECT_OUTPUT_DIR', 'docs')
for f in glob.glob('books/_page.md') + glob.glob('books/*/_page.md'):
    dest = os.path.join(out, os.path.dirname(f))
    if os.path.isdir(dest):
        shutil.copyfile(f, os.path.join(dest, 'index.html.md'))
