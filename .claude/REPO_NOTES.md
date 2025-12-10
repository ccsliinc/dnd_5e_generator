# D&D 5e Character Sheet Generator - Project Notes

## Overview

This project generates printable D&D 5th Edition character sheets from JSON data files. It produces multi-page HTML documents that can be converted to PDF for printing or digital use.

## Repository Structure

```
d_and_d/
├── characters/           # Character JSON data files
│   ├── aldric.json       # Template/example character (Aldric the Brave)
│   ├── aldric/           # Aldric's items
│   │   └── items/
│   │       └── flamebrand_longsword.json  # Example item card
│   ├── thorek.json       # Joe's Ranger (Thorek Bearward + Ironjaw companion)
│   ├── thorek/           # Thorek's items
│   │   └── items/
│   │       └── ring_of_wild_hunt.json
│   ├── kazrek.json       # Mountain Dwarf Sorcerer (Kazrek Spellforge)
│   └── kazrek/           # Kazrek's items (empty)
│
├── images/               # Character artwork and assets
│   ├── aldric/           # Example character + item images (for public repo)
│   ├── thorek/           # Thorek's character art
│   └── kazrek/           # Kazrek's character art
│
├── lib/                  # Core library (OOP architecture)
│   ├── __init__.py       # Package initialization
│   ├── renderers.py      # Content type renderers
│   ├── character_renderers.py  # Character-specific renderers
│   ├── components.py     # Section, Column, Page dataclasses
│   └── document.py       # Document, CharacterDocument, ItemDocument
│
├── output/               # Generated sheets (gitignored except Aldric)
│   ├── Aldric_the_Brave/ # Committed example output for README
│   └── [Character_Name]/ # Timestamped outputs per character
│
├── styles/
│   ├── sheet.css         # Character sheet styling
│   └── item.css          # Magic item card styling
│
├── generate.py           # Python CLI for generating sheets
├── README.md             # Public documentation
├── CREATE_CHARACTER.md   # Guide for creating new characters
├── CREATE_ITEM.md        # Guide for creating magic items
└── SCHEMA.md             # Complete JSON schema reference
```

## Git Remotes (Dual-Push Configuration)

The repo is configured to push to **two remotes** simultaneously:

| Remote | URL | Purpose |
|--------|-----|---------|
| origin (fetch) | `git@github.com:ccsliinc/dnd_5e_generator.git` | Public GitHub repo |
| origin (push) | GitHub + Gogs | Pushes to both |
| Gogs | `http://10.0.23.71/jsugamele/dnd_5e_generator.git` | Private backup |

**Usage:** Just run `git push` - it automatically updates both repos.

## Build Pipeline

```
characters/*.json → generate.py → HTML → Chrome headless → PDF
                                              ↓
                                    pdftoppm → img2pdf (compressed)
```

**Commands:**
```bash
# Generate a character sheet
python3 generate.py characters/thorek.json --compress --open

# Generate character with bundled items
python3 generate.py characters/thorek.json --bundle --compress --open
```

## Character JSON Structure

Key sections in character JSON files:
- `meta`: version, portrait path, gallery images
- `header`: name, class/level, background, race
- `abilities`: STR, DEX, CON, INT, WIS, CHA scores
- `saving_throws` / `skills`: proficiency markers
- `combat`: AC, HP, speed, hit dice, death saves
- `attacks`: weapon/spell attacks list
- `personality`: traits, ideals, bonds, flaws
- `spellcasting`: spell slots, known spells, cantrips
- `companion`: beast companion stats (for rangers)
- `reference`: quick-reference rules for weapons, spells, features

## Image Path Convention

Images are referenced from character JSON files using relative paths:
```json
"portrait": "../../images/thorek/thorek_ironjaw_autumn.jpg"
```

Path structure: `../../images/[character_folder]/[image_name].jpg`
- Characters are in `characters/` (depth 1)
- Images are in `images/[char]/` (need to go up 2 levels)

## What's Public vs Private

**Public repo contains:**
- Generator code (generate.py, tools/, styles/)
- Documentation (README.md, CREATE_CHARACTER.md)
- Example character and output
- Empty character folders structure

**Private repo additionally contains:**
- Actual character JSON files (thorek.json, kazrek.json)
- Personal character artwork
- All generated outputs

## Characters

### Thorek Bearward (thorek.json)
- **Player:** Joe
- **Race/Class:** Hill Dwarf Ranger 3 (Beast Master)
- **Companion:** Ironjaw the Black Bear
- **Background:** Folk Hero
- **Notable:** Ring of the Wild Hunt (buffs Ironjaw)

### Kazrek Spellforge (kazrek.json)
- **Race/Class:** Mountain Dwarf Sorcerer 2 (Draconic - Brass)
- **Background:** Hermit
- **Notable:** Awakened by magical crystals, former master smith
- **Spells:** Burning Hands, Magic Missile, Shield

## Session Notes

- Created: 2025-12-09
- Last reorganization: Images moved to character subfolders
- Both character builds tested and working
