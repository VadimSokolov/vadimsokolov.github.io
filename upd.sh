#!/bin/zsh
# quarto render index.qmd   
quarto render cv.qmd
quarto render index.qmd
quarto render research.qmd

# quarto publish --no-render gh-pages