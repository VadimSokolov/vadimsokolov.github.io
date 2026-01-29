#!/bin/zsh
# quarto render index.qmd   
# quarto render cv.qmd
# quarto render index.qmd
# quarto render research.qmd
# quarto render course/568.qmd
# quarto render courses/600.qmd

# quarto publish --no-render gh-pages
# quarto render courses/caio/cursor-setup-guide.qmd
# quarto render courses/caio/final-project-guide.qmd
# quarto render courses/caio/topic-overview-caio.qmd

quarto render index.qmd
git pull
git add .
git commit -m "website update"
git push