#!/bin/zsh
# quarto render index.qmd   
# quarto render cv.qmd
# quarto render index.qmd
# quarto render research.qmd
# quarto render course/568.qmd


# quarto publish --no-render gh-pages

quarto render index.qmd
quarto render course/664.qmd
git pull
git add .
git commit -m "update"