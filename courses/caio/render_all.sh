#!/bin/bash

# Render all .qmd files to HTML
echo "Rendering Quarto files..."
quarto render *.qmd

echo "Rendering complete. Files are ready for publishing."
