# Item Generator Implementation Plan

## Overview
Extend the D&D character sheet generator to support magic items and other content types using a JSON-driven component system. All HTML structure should be defined in JSON, with the Python generator acting as a pure template renderer.

---

## Phase 1: Project Restructure

### 1.1 Create Reference Folder
- [x] Create `.reference/` folder in project root
- [x] Move `ring_of_wild_hunt_stat_card.md` to `.reference/`
- [ ] Add `.reference/` to `.gitignore` (optional - keep for personal reference)

### 1.2 Create Items Folder Structure
- [x] Create `characters/<name>/items/` folder for item JSON files
- [x] Create `characters/thorek/items/ring_of_wild_hunt.json` as first item definition

### 1.3 Modular CSS Architecture
- [ ] Create `styles/base.css` - Variables, reset, page, print styles (OPTIONAL - sheet.css works)
- [ ] Create `styles/components.css` - Shared components (OPTIONAL)
- [ ] Create `styles/character.css` - Character sheet specific (OPTIONAL)
- [x] Create `styles/item.css` - Item sheet specific (header, rarity colors, synergy, lore)
- [x] Update `generate.py` to load and combine CSS files based on document type
- [x] Keep `styles/sheet.css` as base for all document types

---

## Phase 2: Define Content Type System

### 2.1 Content Types (what goes inside boxes)

| Type | JSON Structure | Renders To |
|------|----------------|------------|
| `text` | `{ "type": "text", "text": "..." }` | `<p>` paragraphs |
| `text_italic` | `{ "type": "text_italic", "text": "..." }` | `<p class="italic">` |
| `bullets` | `{ "type": "bullets", "items": ["..."] }` | `<ul class="ability-bullets">` |
| `properties` | `{ "type": "properties", "items": [{ "icon", "name", "desc" }] }` | Icon + name + desc rows |
| `table` | `{ "type": "table", "columns": [], "rows": [[]], "footer": "" }` | `<table class="scaling-table">` |
| `quote` | `{ "type": "quote", "text": "...", "attribution": "..." }` | `<div class="lore-quote">` |
| `comparison` | `{ "type": "comparison", "items": [{ "before", "after" }] }` | Before → After stat rows |
| `tales` | `{ "type": "tales", "items": [{ "title", "desc" }] }` | Title + description pairs |
| `subsections` | `{ "type": "subsections", "items": [{ "name", "bullets": [] }] }` | Named groups with bullet lists |
| `mixed` | `{ "type": "mixed", "blocks": [...] }` | Multiple content types in sequence |

### 2.2 Box/Section Options

| Option | Values | Description |
|--------|--------|-------------|
| `title` | string or null | Section title (null = no title bar) |
| `variant` | `default`, `lore`, `highlight` | Background style variant |
| `flex_grow` | boolean | Box fills remaining vertical space |
| `column` | 1 or 2 | Which column in 2-column layout |

### 2.3 Layout Options

| Option | Values | Description |
|--------|--------|-------------|
| `columns` | 1, 2 | Number of content columns |
| `gap` | CSS value | Gap between columns/sections |

---

## Phase 3: JSON Schema Definition

### 3.1 Item Document Schema
```json
{
  "type": "item",
  "meta": {
    "version": "1.0"
  },
  "header": {
    "name": "string",
    "subtitle": "string (optional)",
    "image": "path/to/image.jpg",
    "background_svg": "path/to/decoration.svg (optional)",
    "stats": [
      { "label": "string", "value": "string", "class": "optional-css-class" }
    ]
  },
  "footer": {
    "left": "string",
    "right": "string"
  },
  "pages": [
    {
      "layout": {
        "columns": 2,
        "gap": "3mm"
      },
      "sections": [
        {
          "column": 1,
          "title": "Section Title",
          "variant": "default",
          "flex_grow": false,
          "content": { /* content type object */ }
        }
      ]
    }
  ]
}
```

### 3.2 Create Ring of Wild Hunt JSON
- [x] Convert current HTML structure to JSON format
- [x] Validate all content renders correctly
- [x] Document any edge cases discovered

---

## Phase 4: Generator Implementation

### 4.1 Refactor generate.py Structure
- [x] Add document type detection (`character` vs `item`)
- [x] Create unified `generate()` function for both types
- [x] Create shared `load_css()` function that combines CSS files based on type
- [x] Add CLI with argparse: `--pdf`, `--compress`, `--dpi`, `--open`, `--output`
- [x] Integrate Chrome headless PDF generation into Python
- [x] Integrate PDF compression (pdftoppm + img2pdf) into Python

### 4.2 Content Type Renderers
Create one function per content type:
- [x] `render_text(content)` → paragraphs
- [x] `render_text_italic(content)` → italic paragraphs
- [x] `render_bullets(content)` → ability-bullets list
- [x] `render_properties(content)` → icon/name/desc property list
- [x] `render_table(content)` → scaling table with optional footer
- [x] `render_quote(content)` → lore quote with attribution
- [x] `render_comparison(content)` → before/after stat rows
- [x] `render_tales(content)` → title/description pairs
- [x] `render_subsections(content)` → named groups with bullets
- [x] `render_mixed(content)` → dispatch to multiple renderers
- [x] `render_synergy(content)` → special composite type
- [x] `render_content(content)` → dispatcher that routes to correct renderer
- [x] `render_markdown_bold(text)` → **bold** → <strong>

### 4.3 Layout Engine
- [x] `render_item_section(section)` → box with title and content
- [x] `render_item_page(page)` → page with column layout
- [x] `render_item_header(header)` → item header with image, title, stats
- [x] `render_item_footer(footer)` → page footer

### 4.4 Main Item Generator
- [x] `build_item_html(data)` → complete HTML document
- [x] Integrate with existing CLI interface
- [x] `build-sheet.sh` no longer needed - all in `generate.py`

---

## Phase 5: Testing & Validation

### 5.1 Test Ring of Wild Hunt
- [x] Generate HTML from new JSON
- [x] Compare visual output to current hand-crafted HTML
- [x] Fix any rendering differences
- [x] Test PDF generation pipeline

### 5.2 Create Additional Test Items
- [ ] Create a simple item (weapon or potion) to test basic features
- [ ] Create a multi-page item to test pagination
- [ ] Document any limitations discovered

---

## Phase 6: Documentation

### 6.1 Update Project Documentation
- [x] Update README.md with new CLI usage
- [x] Create `CREATE_ITEM.md` guide (parallel to CREATE_CHARACTER.md)
- [x] Document all content types with examples
- [x] Document CSS customization options
- [x] Update CREATE_CHARACTER.md with new generation command

### 6.2 Schema Documentation
- [x] Full JSON schema documented in CREATE_ITEM.md
- [x] Examples for each content type included
- [x] Variant options documented

---

## Content Type Templates (Reference)

### text
```json
{
  "type": "text",
  "text": "Paragraph content here. Supports **markdown bold**."
}
```

### bullets
```json
{
  "type": "bullets",
  "items": [
    "First bullet point",
    "Second bullet with **bold**"
  ]
}
```

### properties
```json
{
  "type": "properties",
  "items": [
    { "icon": "⚔", "name": "Property Name", "desc": "Property description" }
  ]
}
```

### table
```json
{
  "type": "table",
  "columns": ["Column 1", "Column 2", "Column 3"],
  "rows": [
    ["Row 1 Col 1", "Row 1 Col 2", "Row 1 Col 3"],
    ["Row 2 Col 1", "Row 2 Col 2", "Row 2 Col 3"]
  ],
  "footer": "Optional footnote text"
}
```

### quote
```json
{
  "type": "quote",
  "text": "Quote text in italics...",
  "attribution": "— Source Name"
}
```

### comparison
```json
{
  "type": "comparison",
  "items": [
    { "before": "HP: 19", "after": "HP: 25 (+31%)" }
  ]
}
```

### subsections
```json
{
  "type": "subsections",
  "items": [
    {
      "name": "Subsection Name",
      "bullets": ["Bullet 1", "Bullet 2"]
    }
  ]
}
```

### synergy (special composite type)
```json
{
  "type": "synergy",
  "header": {
    "icon": "🐻",
    "title": "Synergy with Ironjaw",
    "subtitle": "Thorek Bearward's Companion"
  },
  "comparisons": [
    { "before": "HP: 19", "after": "HP: 25 (+31%)" }
  ],
  "subsections": [
    { "name": "Tactical Combinations", "bullets": ["..."] }
  ]
}
```

---

## Priority Order

1. **Phase 1.1** - Move reference file (quick win)
2. **Phase 3.2** - Create Ring JSON (defines the target)
3. **Phase 2** - Finalize content type definitions
4. **Phase 4.2** - Build content renderers (core work)
5. **Phase 4.3-4.4** - Layout engine and main generator
6. **Phase 1.3** - Modular CSS (can be done in parallel)
7. **Phase 5** - Testing
8. **Phase 6** - Documentation

---

## Open Questions

1. Should items support multiple pages? (e.g., artifact with extensive lore)
2. Should we support card-sized output for quick reference cards?
3. How to handle SVG background decorations - embed or reference?
4. Should markdown parsing be added for bold/italic in text content?

---

## Files to Create/Modify

### New Files
- `.reference/ring_of_wild_hunt_stat_card.md` (moved)
- `items/ring_of_wild_hunt.json`
- `styles/base.css`
- `styles/components.css`
- `styles/item.css`
- `docs/CREATE_ITEM.md`
- `docs/SCHEMA_ITEMS.md`

### Modified Files
- `generate.py` - Add item generation support
- `tools/build-sheet.sh` - Handle item type detection
- `README.md` - Add item documentation
- `.gitignore` - Add `.reference/` if desired