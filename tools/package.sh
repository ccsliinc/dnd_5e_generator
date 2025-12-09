#!/bin/bash
# Package the D&D Character Sheet Generator for distribution
# Run from project root: ./tools/package.sh

# Get project root (one level up from tools/)
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"

PACKAGES_DIR="$PROJECT_DIR/output/packages"
OUTPUT="$PACKAGES_DIR/dnd-character-sheet.zip"

# Ensure packages directory exists
mkdir -p "$PACKAGES_DIR"

# Remove old package if exists
rm -f "$OUTPUT"

# Change to project root for relative paths in zip
cd "$PROJECT_DIR"

# Create zip with only needed files for public distribution
zip -r "$OUTPUT" \
    generate.py \
    tools/build-sheet.sh \
    tools/package.sh \
    styles/sheet.css \
    characters/example.json \
    images/example/*.jpg \
    README.md \
    CREATE_CHARACTER.md \
    -x "*.DS_Store"

echo "Created: $OUTPUT"
echo "Contents:"
unzip -l "$OUTPUT"
