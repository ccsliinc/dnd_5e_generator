# D&D 5e Magic Item Creation Guide

Create custom magic item cards from JSON data files.

## Quick Start

1. Create a JSON file in `characters/<character_name>/items/`
2. Run: `python3 generate.py characters/<name>/items/<item>.json --compress --open`

## JSON Structure

```json
{
  "type": "item",
  "meta": {
    "version": "1.0"
  },
  "header": {
    "name": "Item Name",
    "subtitle": "Flavor text or origin",
    "image": "images/<character>/item_image.jpg",
    "background_svg": "images/<character>/decoration.svg",
    "stats": [
      { "label": "Rarity", "value": "Rare", "class": "rarity-rare" },
      { "label": "Attunement", "value": "Required by..." },
      { "label": "Weight", "value": "1 lb" }
    ]
  },
  "footer": {
    "left": "Item identifier or maker",
    "right": "Market Value: X gp"
  },
  "pages": [
    {
      "layout": {
        "columns": 2,
        "gap": "3mm"
      },
      "sections": [
        // Section definitions go here
      ]
    }
  ]
}
```

## Rarity Classes

Use these CSS classes for the rarity stat value:
- `rarity-common` - Gray
- `rarity-uncommon` - Green
- `rarity-rare` - Blue
- `rarity-very-rare` - Purple
- `rarity-legendary` - Orange

## Section Definition

Each section in a page has:

```json
{
  "column": 1,           // 1 or 2 (which column)
  "title": "Section Title",  // null for no title bar
  "variant": "default",  // "default" or "lore"
  "flex_grow": false,    // true to fill remaining space
  "content": { }         // Content type object
}
```

## Content Types

### text
Plain paragraph text.
```json
{
  "type": "text",
  "text": "Paragraph content. Supports **bold** markdown."
}
```

### text_italic
Italic paragraph (for descriptions/flavor text).
```json
{
  "type": "text_italic",
  "text": "This ancient ring glows with emerald light..."
}
```

### bullets
Bullet point list.
```json
{
  "type": "bullets",
  "items": [
    "First bullet point",
    "Second with **bold** text"
  ]
}
```

### properties
Icon + name + description rows (for item abilities).
```json
{
  "type": "properties",
  "items": [
    { "icon": "⚔", "name": "Enhanced Damage", "desc": "+2 to damage rolls" },
    { "icon": "🛡", "name": "Protection", "desc": "Advantage on saves" }
  ]
}
```

### table
Data table with optional footer note.
```json
{
  "type": "table",
  "columns": ["Level", "Bonus", "Effect"],
  "rows": [
    ["3", "+1", "Minor effect"],
    ["5", "+2", "Major effect"]
  ],
  "footer": "* Requires attunement"
}
```

### quote
Lore quote with attribution.
```json
{
  "type": "quote",
  "text": "The ring was forged in the ancient times...",
  "attribution": "— From the Archives of the Enclave"
}
```

### comparison
Before/after stat comparison rows.
```json
{
  "type": "comparison",
  "items": [
    { "before": "HP: 19", "after": "HP: 25 (+31%)" },
    { "before": "AC: 10", "after": "AC: 12" }
  ]
}
```

### tales
Title + description pairs (for legendary tales).
```json
{
  "type": "tales",
  "items": [
    { "title": "Battle of X", "desc": "The item saved a kingdom" },
    { "title": "Siege of Y", "desc": "It broke through wards" }
  ]
}
```

### subsections
Named groups with bullet lists.
```json
{
  "type": "subsections",
  "items": [
    {
      "name": "Subsection Name",
      "bullets": [
        "**Bold intro:** explanation text",
        "Another point here"
      ]
    }
  ]
}
```

### synergy
Special composite for companion/synergy effects.
```json
{
  "type": "synergy",
  "header": {
    "icon": "🐻",
    "title": "Synergy with Companion",
    "subtitle": "Character's Animal Companion"
  },
  "comparisons": [
    { "before": "HP: 19", "after": "HP: 25" }
  ],
  "subsections": [
    {
      "name": "Tactical Combinations",
      "bullets": ["Point 1", "Point 2"]
    }
  ]
}
```

### mixed
Multiple content blocks in sequence.
```json
{
  "type": "mixed",
  "blocks": [
    { "type": "quote", "text": "...", "attribution": "..." },
    { "type": "tales", "items": [...] }
  ]
}
```

## Complete Example

```json
{
  "type": "item",
  "meta": { "version": "1.0" },
  "header": {
    "name": "Sword of Flames",
    "subtitle": "Forged in dragon fire",
    "image": "images/character/sword.jpg",
    "stats": [
      { "label": "Rarity", "value": "Very Rare", "class": "rarity-very-rare" },
      { "label": "Attunement", "value": "Any" },
      { "label": "Type", "value": "Longsword" }
    ]
  },
  "footer": {
    "left": "Crafted by Master Smith",
    "right": "Value: 15,000 gp"
  },
  "pages": [
    {
      "layout": { "columns": 2 },
      "sections": [
        {
          "column": 1,
          "title": "Description",
          "variant": "lore",
          "content": {
            "type": "text_italic",
            "text": "The blade glows with inner fire..."
          }
        },
        {
          "column": 1,
          "title": "Properties",
          "content": {
            "type": "properties",
            "items": [
              { "icon": "🔥", "name": "Flame Blade", "desc": "+1d6 fire damage" }
            ]
          }
        },
        {
          "column": 2,
          "title": "Abilities",
          "content": {
            "type": "subsections",
            "items": [
              {
                "name": "Ignite",
                "bullets": [
                  "**Action:** Ignite the blade",
                  "Lasts 1 minute"
                ]
              }
            ]
          }
        }
      ]
    }
  ]
}
```

## Tips

- Use `variant: "lore"` for description sections to get the special background
- Use `flex_grow: true` on the last section in a column to fill remaining space
- Image paths are relative to the project root (e.g., `images/character/item.jpg`)
- SVG decorations are optional - leave `background_svg` empty if not needed
- Support for **bold** text in all text content via markdown

## Generation

```bash
# HTML only
python3 generate.py characters/name/items/item.json

# With PDF
python3 generate.py characters/name/items/item.json --pdf

# Full pipeline with compressed PDF
python3 generate.py characters/name/items/item.json --compress --open
```
