# D&D 5e Character Sheet Generator

Generate printable HTML character sheets from JSON data files.

## Quick Start

```bash
# One command does everything
./tools/build-sheet.sh

# Or specify character and DPI
./tools/build-sheet.sh example.json 150
```

This generates HTML, prints to PDF, compresses it, and opens both for review.

## How It Works

```
┌─────────────────────────────────────────────────────────────────┐
│                    build-sheet.sh                               │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  STEP 1: Generate HTML                                          │
│                                                                 │
│  characters/example.json  ──▶  generate.py  ──▶  output/*.html  │
│                                    │                            │
│                            styles/sheet.css                     │
│                            images/example/*.jpg                 │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  STEP 2: Print to PDF (Chrome Headless)                         │
│                                                                 │
│  output/*.html  ──▶  Chrome --headless  ──▶  output/*.pdf       │
│                      --print-to-pdf           (13MB vector)     │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  STEP 3: Flatten/Compress                                       │
│                                                                 │
│  output/*.pdf  ──▶  pdftoppm  ──▶  temp/*.png  ──▶  img2pdf     │
│   (13MB)           (rasterize)     (150 DPI)         │          │
│                                                      ▼          │
│                                   output/compressed/*_print.pdf │
│                                             (1.8MB raster)      │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  STEP 4: Open for Review                                        │
│                                                                 │
│  open output/*.html           (browser)                         │
│  open output/compressed/*.pdf (Preview)                         │
└─────────────────────────────────────────────────────────────────┘
```

## Project Structure

```
d_and_d/
├── characters/
│   └── example.json        # Character data (input)
├── images/
│   └── example/*.jpg       # Character images
├── styles/
│   └── sheet.css           # Stylesheet
├── tools/
│   ├── build-sheet.sh      # Full pipeline script
│   └── package.sh          # Create distribution zip
├── output/                  # Generated files (gitignored)
│   └── <CharacterName>/
│       ├── *.html
│       ├── *.pdf           # Full quality vector
│       └── *_print.pdf     # Compressed for printing
└── generate.py             # HTML generator
```

## Requirements

- Python 3
- Google Chrome (for headless PDF generation)
- poppler (`brew install poppler`) - for pdftoppm
- img2pdf (`brew install img2pdf`) - for PDF compression

## Manual Usage

If you prefer to run steps individually:

```bash
# Generate HTML only
python3 generate.py example.json

# Then print manually from browser, or use Chrome headless:
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome \
    --headless --print-to-pdf=output.pdf --print-background file.html
```

## Print Settings

When printing manually from browser:
1. File → Print (Cmd + P)
2. Enable **Background graphics**
3. Set margins to **Minimum**
4. Print all 4 pages

## Creating a New Character

See `CREATE_CHARACTER.md` for the full JSON template and guide.

Key sections in the JSON:
- `meta.portrait` - Character portrait image
- `meta.gallery` - Additional images for page 1
- `header` - Name, class, race, etc.
- `abilities` - Ability scores
- `spellcasting` - Spells and slots
- `companion` - Beast companion (optional)
- `reference` - Quick reference for page 4

## Customizing Styles

Edit `styles/sheet.css`. Key variables:

```css
:root {
    --bg-page: #ffffff;
    --border-dark: #6b4423;
    --accent-secondary: #c9a227;
    --font-display: 'Cinzel', serif;
    --font-body: 'Scada', sans-serif;
}
```

## Distribution

Create a zip package for sharing:

```bash
./tools/package.sh
# Creates output/packages/dnd-character-sheet.zip
```
