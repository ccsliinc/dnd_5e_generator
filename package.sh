#!/bin/bash
# Package the D&D Character Sheet Generator for distribution

PACKAGES_DIR="output/packages"
OUTPUT="$PACKAGES_DIR/dnd-character-sheet.zip"

# Ensure packages directory exists
mkdir -p "$PACKAGES_DIR"

# Remove old package if exists
rm -f "$OUTPUT"

# Create zip with only needed files
zip -r "$OUTPUT" \
    generate.py \
    build-sheet.sh \
    styles/sheet.css \
    characters/*.json \
    images/web/*.jpg \
    README.md \
    CREATE_CHARACTER.md \
    -x "*.DS_Store"

echo "Created: $OUTPUT"
echo "Contents:"
unzip -l "$OUTPUT"
