#!/bin/bash
# Package the D&D Character Sheet Generator for distribution

OUTPUT="dnd-character-sheet.zip"

# Remove old package if exists
rm -f "$OUTPUT"

# Create zip with only needed files
zip -r "$OUTPUT" \
    generate.py \
    styles/sheet.css \
    thorek.json \
    images/*.png \
    README.md \
    CREATE_CHARACTER.md \
    -x "*.DS_Store"

echo "Created: $OUTPUT"
echo "Contents:"
unzip -l "$OUTPUT"
