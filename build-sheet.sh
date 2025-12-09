#!/bin/bash
# Complete character sheet pipeline
# Usage: ./build-sheet.sh [character.json] [dpi]
#
# Steps:
#   1. Generate HTML from JSON
#   2. Print to PDF via Chrome headless
#   3. Flatten/compress PDF for smaller size

set -e

# Configuration
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
OUTPUT_DIR="$SCRIPT_DIR/output"
COMPRESSED_DIR="$OUTPUT_DIR/compressed"
DPI="${2:-150}"

# Input file (default to first JSON in characters/)
if [ -n "$1" ]; then
    INPUT="$1"
else
    INPUT=$(ls "$SCRIPT_DIR/characters/"*.json 2>/dev/null | head -1)
fi

if [ -z "$INPUT" ] || [ ! -f "$INPUT" ] && [ ! -f "$SCRIPT_DIR/characters/$INPUT" ]; then
    echo "Usage: $0 [character.json] [dpi]"
    echo "Example: $0 thorek.json 150"
    exit 1
fi

# Ensure directories exist
mkdir -p "$OUTPUT_DIR" "$COMPRESSED_DIR"

echo "=== D&D Character Sheet Builder ==="
echo ""

# Step 1: Generate HTML
echo "[1/3] Generating HTML..."
cd "$SCRIPT_DIR"
python3 generate.py "$INPUT"

# Get character name from the generated file
HTML_FILE=$(ls -t "$OUTPUT_DIR"/*.html 2>/dev/null | head -1)
if [ -z "$HTML_FILE" ]; then
    echo "Error: No HTML file generated"
    exit 1
fi

BASENAME=$(basename "$HTML_FILE" .html)
PDF_FILE="$OUTPUT_DIR/${BASENAME}.pdf"
COMPRESSED_FILE="$COMPRESSED_DIR/${BASENAME}_print.pdf"

echo "   Generated: $HTML_FILE"

# Step 2: Print to PDF via Chrome headless
echo "[2/3] Printing to PDF via Chrome..."
"$CHROME" \
    --headless \
    --disable-gpu \
    --no-pdf-header-footer \
    --print-to-pdf="$PDF_FILE" \
    --print-background \
    "file://$HTML_FILE" \
    2>/dev/null

if [ ! -f "$PDF_FILE" ]; then
    echo "Error: PDF generation failed"
    exit 1
fi

PDF_SIZE=$(ls -lh "$PDF_FILE" | awk '{print $5}')
echo "   Generated: $PDF_FILE ($PDF_SIZE)"

# Step 3: Flatten/compress PDF
echo "[3/3] Compressing PDF at ${DPI} DPI..."
TEMP_DIR=$(mktemp -d)

# Convert to images
pdftoppm -png -r "$DPI" "$PDF_FILE" "$TEMP_DIR/page"

# Recombine
img2pdf "$TEMP_DIR"/page*.png -o "$COMPRESSED_FILE" 2>/dev/null

# Cleanup
rm -rf "$TEMP_DIR"

COMPRESSED_SIZE=$(ls -lh "$COMPRESSED_FILE" | awk '{print $5}')
echo "   Generated: $COMPRESSED_FILE ($COMPRESSED_SIZE)"

echo ""
echo "=== Done! ==="
echo "   HTML:         $HTML_FILE"
echo "   Full quality: $PDF_FILE ($PDF_SIZE)"
echo "   Print-ready:  $COMPRESSED_FILE ($COMPRESSED_SIZE)"
echo ""

# Open both HTML and compressed PDF
echo "Opening files..."
open "$HTML_FILE"
open "$COMPRESSED_FILE"
