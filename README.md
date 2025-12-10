# D&D 5e Sheet Generator

Generate printable HTML character sheets and magic item cards from JSON data files.

## Quick Start

```bash
# Generate HTML only
python3 generate.py aldric

# Generate HTML + PDF
python3 generate.py aldric --pdf

# Full pipeline: HTML + PDF + compressed print version, then open
python3 generate.py aldric --compress --open

# Generate character sheet bundled with their magic items
python3 generate.py thorek --bundle --compress --open
```

## Command Line Options

```
python3 generate.py <character_name> [options]

Options:
  --pdf           Generate PDF via Chrome headless
  --compress      Compress PDF for printing (implies --pdf)
  --dpi <value>   DPI for compression (default: 150)
  --open          Open output files when done
  --output <dir>  Custom output directory
  --bundle        Include character's embedded items in output
  -h, --help      Show help message
```

## How It Works

```
┌─────────────────────────────────────────────────────────────────┐
│                      generate.py                                │
│                                                                 │
│  Input: characters/aldric.json (includes embedded items)        │
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
│   ├── aldric.json              # Character with embedded items
│   ├── thorek.json              # Character with embedded items
│   └── kazrek.json              # Character data
├── images/
│   ├── aldric/                  # Character-specific images
│   ├── thorek/                  # Including item images
│   └── kazrek/
├── lib/                         # Core library (OOP architecture)
│   ├── __init__.py              # Package exports
│   ├── renderers.py             # Content type registry & base renderer
│   ├── character_renderers.py   # Character-specific renderers
│   ├── components.py            # Layout components (Row, Col, Grid, Section, Page)
│   ├── document.py              # Document classes (CharacterDocument, ItemDocument)
│   └── pages.py                 # Page builders (StatsPage, SpellcastingPage, etc.)
├── styles/
│   ├── base.css                 # Shared variables, reset, box component, layout
│   ├── components.css           # Shared UI components (section box, tables, etc.)
│   ├── sheet.css                # Character sheet-specific styling
│   └── item.css                 # Magic item card styling
├── docs/
│   └── CHARACTER_SCHEMA.md      # JSON schema documentation
├── output/                      # Generated files (gitignored)
│   └── <CharacterName>/
│       ├── *.html
│       └── *.pdf
└── generate.py                  # Main generator CLI
```

## Architecture

### OOP Design

The generator uses an object-oriented architecture:

- **Document Classes** (`lib/document.py`)
  - `Document` - Abstract base class
  - `CharacterDocument` - 4-page character sheets
  - `ItemDocument` - Magic item cards

- **Page Builders** (`lib/pages.py`)
  - `PageBuilder` - Abstract base class
  - `StatsPage` - Page 1 (abilities, combat, equipment)
  - `BackgroundPage` - Page 2 (appearance, backstory, allies)
  - `SpellcastingPage` - Page 3 (spells and slots)
  - `ReferencePage` - Page 4 (quick reference, companion)

- **Layout Components** (`lib/components.py`)
  - `Row` - Horizontal flex container
  - `Col` - Vertical flex container
  - `Grid` - CSS Grid container
  - `Section` - Titled content box
  - `Page` - Full page container

- **Content Renderers** (`lib/renderers.py`, `lib/character_renderers.py`)
  - Registry pattern for extensible content types
  - Each renderer handles a specific content type (tables, properties, spells, etc.)

### CSS Architecture

Styles are layered for reusability:

1. `base.css` - CSS variables, reset, box component, layout utilities
2. `components.css` - Shared UI components (section boxes, tables, lists)
3. `sheet.css` / `item.css` - Document-specific styles

## Requirements

- **Python 3** - Core generator
- **Google Chrome** - PDF generation (headless mode)
- **poppler** - PDF compression (`brew install poppler`)
- **img2pdf** - PDF compression (`brew install img2pdf`)

Note: poppler and img2pdf are only required for `--compress` option.

## Documentation

| Guide | Description |
|-------|-------------|
| [docs/SCHEMA.md](docs/SCHEMA.md) | Complete JSON schema for characters and items |
| [docs/CREATE_CHARACTER.md](docs/CREATE_CHARACTER.md) | Step-by-step character creation guide |
| [docs/CREATE_ITEM.md](docs/CREATE_ITEM.md) | Magic item creation guide |

## Document Types

### Character Sheets
4-page character sheets with:
- Page 1: Stats, skills, combat, equipment
- Page 2: Background, appearance, backstory
- Page 3: Spellcasting
- Page 4: Quick reference, companion stats

### Magic Items
Items are embedded in character JSON files under the `items` array. When using `--bundle`, item pages are appended after the character sheet.

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

Edit `styles/base.css` for shared styles or `styles/sheet.css` / `styles/item.css` for document-specific styles.

Key CSS variables (in `base.css`):
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
