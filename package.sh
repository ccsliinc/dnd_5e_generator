#!/bin/bash
# Package the D&D Character Sheet Generator for distribution

OUTPUT="output/dnd-character-sheet.zip"

# Ensure output directory exists
mkdir -p output

# Remove old package if exists
rm -f "$OUTPUT"

# Create zip with only needed files
zip -r "$OUTPUT" \
    generate.py \
    styles/sheet.css \
    characters/*.json \
    images/*.png \
    README.md \
    CREATE_CHARACTER.md \
    -x "*.DS_Store"

echo "Created: $OUTPUT"
echo "Contents:"
unzip -l "$OUTPUT"
