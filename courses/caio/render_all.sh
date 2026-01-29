#!/bin/bash

# Render all .qmd files to HTML individually to bypass project-level constraints
echo "Rendering Quarto files individually..."

for file in *.qmd; do
    echo "Rendering $file..."
    quarto render "$file"
done

echo "Rendering complete."
