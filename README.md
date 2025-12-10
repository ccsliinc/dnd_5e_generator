# D&D 5e Sheet Generator

Generate printable HTML character sheets and magic item cards from JSON data files.

![Character Sheet Preview](images/aldric/preview_page1.png)

**[View Example PDF](output/Aldric_the_Brave/Aldric_the_Brave.pdf)**

## Quick Start

```bash
# Generate HTML only
python3 generate.py aldric.json

# Generate HTML + PDF
python3 generate.py aldric.json --pdf

# Full pipeline: HTML + PDF + compressed print version, then open
python3 generate.py aldric.json --compress --open

# Generate character sheet bundled with their items
python3 generate.py thorek.json --bundle --compress --open

# Generate a magic item
python3 generate.py characters/thorek/items/ring_of_wild_hunt.json --compress --open
```

## Command Line Options

```
python3 generate.py <input.json> [options]

Options:
  --pdf           Generate PDF via Chrome headless
  --compress      Compress PDF for printing (implies --pdf)
  --dpi <value>   DPI for compression (default: 150)
  --open          Open output files when done
  --output <dir>  Custom output directory
  -h, --help      Show help message
```

## How It Works

```
┌─────────────────────────────────────────────────────────────────┐
│                      generate.py                                │
│                                                                 │
│  Input: characters/aldric.json                                   │
│         characters/<name>/items/<item>.json                     │
└─────────────────────────────────────────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        ▼                     ▼                     ▼
┌───────────────┐   ┌─────────────────┐   ┌─────────────────┐
│  HTML Output  │   │   PDF Output    │   │  Print Output   │
│               │   │  (--pdf flag)   │   │ (--compress)    │
│  *.html       │   │  *.pdf (vector) │   │  *_print.pdf    │
│               │   │  Chrome headless│   │  (rasterized)   │
└───────────────┘   └─────────────────┘   └─────────────────┘
```

## Project Structure

```
d_and_d/
├── characters/
│   ├── aldric.json               # Example character (Aldric the Brave)
│   ├── aldric/
│   │   └── items/
│   │       └── flamebrand_longsword.json  # Example item
│   └── <name>/
│       └── items/
│           └── <item>.json       # Character's magic items
├── images/
│   ├── aldric/                   # Example character images + item
│   └── <name>/                   # Character-specific images
├── lib/                          # Core library (OOP architecture)
│   ├── renderers.py              # Content type renderers
│   ├── character_renderers.py    # Character-specific renderers
│   ├── components.py             # Section, Column, Page classes
│   └── document.py               # Document classes
├── styles/
│   ├── sheet.css                 # Character sheet styling
│   └── item.css                  # Magic item card styling
├── output/                       # Generated files (gitignored)
│   └── <CharacterName>/
│       ├── *.html
│       └── *.pdf
└── generate.py                   # Main generator CLI
```

## Requirements

- **Python 3** - Core generator
- **Google Chrome** - PDF generation (headless mode)
- **poppler** - PDF compression (`brew install poppler`)
- **img2pdf** - PDF compression (`brew install img2pdf`)

Note: poppler and img2pdf are only required for `--compress` option.

## Documentation

| Guide | Description |
|-------|-------------|
| [CREATE_CHARACTER.md](CREATE_CHARACTER.md) | Character sheet creation guide with examples |
| [CREATE_ITEM.md](CREATE_ITEM.md) | Magic item card creation guide with content types |
| [SCHEMA.md](SCHEMA.md) | Complete JSON schema reference for all document types |

## Document Types

### Character Sheets
4-page character sheets with:
- Page 1: Stats, skills, combat, equipment
- Page 2: Background, appearance, backstory
- Page 3: Spellcasting
- Page 4: Quick reference, companion stats

### Magic Items
Single-page item cards with:
- Header with image, name, rarity, attunement
- Two-column layout with customizable sections
- Support for tables, properties, quotes, and more

## Print Settings

When printing manually from browser:
1. File → Print (Cmd + P)
2. Enable **Background graphics**
3. Set margins to **Minimum**
4. Print all pages

## Customizing Styles

Edit `styles/sheet.css` for characters or `styles/item.css` for items.

Key CSS variables:
```css
:root {
    --bg-page: #ffffff;
    --border-dark: #6b4423;
    --accent-primary: #8b4513;
    --accent-secondary: #c9a227;
    --font-display: 'Cinzel', serif;
    --font-body: 'Scada', sans-serif;
}
```

