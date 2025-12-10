# D&D 5e Sheet JSON Schema

Complete reference for all available fields in character and item JSON files.

---

## Document Types

This generator supports two document types:
- **Character Sheets** - 4-page character sheets (default)
- **Magic Items** - Single-page item cards

The document type is determined by the `"type"` field in the JSON root:
- `"type": "item"` - Magic item
- No type field or any other value - Character sheet

---

## Table of Contents

### Character Schema
- [meta](#meta) - File metadata and images
- [header](#header) - Basic character info
- [abilities](#abilities) - Ability scores (STR, DEX, etc.)
- [saving_throws](#saving_throws) - Save proficiencies
- [skills](#skills) - Skill proficiencies
- [combat](#combat) - AC, HP, speed, hit dice
- [attacks](#attacks) - Weapon/spell attacks list
- [personality](#personality) - Traits, ideals, bonds, flaws
- [equipment](#equipment) - Inventory and currency
- [features_traits](#features_traits) - Class/race features
- [appearance](#appearance) - Physical description
- [backstory](#backstory) - Character history
- [allies_organizations](#allies_organizations) - Connections
- [spellcasting](#spellcasting) - Spells and slots
- [companion](#companion) - Beast companion (optional)
- [reference](#reference) - Quick reference cards (Page 4)

### Item Schema
- [item-header](#item-header) - Item name, image, stats
- [item-footer](#item-footer) - Identifier and value
- [item-pages](#item-pages) - Page layout and sections
- [content-types](#content-types) - Available content blocks

---

# Character Schema

## meta

File metadata and character images.

```json
"meta": {
  "version": "1.0",
  "generated": null,
  "portrait": "../../images/[character]/portrait.jpg",
  "gallery": [
    "../../images/[character]/image1.jpg",
    "../../images/[character]/image2.jpg",
    "../../images/[character]/image3.jpg",
    "../../images/[character]/image4.jpg"
  ]
}
```

| Field | Type | Description |
|-------|------|-------------|
| `version` | string | Schema version for compatibility |
| `generated` | string/null | Auto-filled with generation timestamp |
| `portrait` | string | Path to main portrait image (Page 1 header) |
| `gallery` | array | Additional images shown at bottom of Page 1 (max 4 recommended) |

**Image paths**: Use `../../images/[character]/` prefix since JSON files are in `characters/` folder.

---

## header

Basic character identification shown in the header area.

```json
"header": {
  "character_name": "Thorek Bearward",
  "class_level": "Ranger 3",
  "background": "Folk Hero",
  "player_name": "Joe",
  "race": "Hill Dwarf",
  "alignment": "Neutral Good",
  "experience_points": "900"
}
```

| Field | Type | Description |
|-------|------|-------------|
| `character_name` | string | Character's full name |
| `class_level` | string | Class and level (e.g., "Ranger 3", "Fighter 2 / Wizard 1") |
| `background` | string | D&D background (Soldier, Sage, Criminal, etc.) |
| `player_name` | string | Player's name (optional) |
| `race` | string | Character's race (Human, Hill Dwarf, High Elf, etc.) |
| `alignment` | string | Two-axis alignment (Lawful Good, Chaotic Neutral, etc.) |
| `experience_points` | string/int | Current XP total |

---

## Core Stats

```json
"inspiration": false,
"proficiency_bonus": 2
```

| Field | Type | Description |
|-------|------|-------------|
| `inspiration` | boolean | Whether character has inspiration (shows "X" if true) |
| `proficiency_bonus` | integer | Proficiency bonus based on level (2-6) |

**Proficiency by level**: 1-4=+2, 5-8=+3, 9-12=+4, 13-16=+5, 17-20=+6

---

## abilities

The six ability scores. Modifiers are calculated automatically.

```json
"abilities": {
  "strength":     { "score": 16 },
  "dexterity":    { "score": 14 },
  "constitution": { "score": 15 },
  "intelligence": { "score": 10 },
  "wisdom":       { "score": 12 },
  "charisma":     { "score": 8 }
}
```

**Modifier calculation**: `(score - 10) / 2` rounded down

| Score | Modifier | Score | Modifier |
|-------|----------|-------|----------|
| 1 | -5 | 12-13 | +1 |
| 2-3 | -4 | 14-15 | +2 |
| 4-5 | -3 | 16-17 | +3 |
| 6-7 | -2 | 18-19 | +4 |
| 8-9 | -1 | 20-21 | +5 |
| 10-11 | +0 | 22+ | +6 |

---

## saving_throws

Saving throw proficiencies. Modifiers are calculated from ability + proficiency.

```json
"saving_throws": {
  "strength":     { "proficient": true },
  "dexterity":    { "proficient": false },
  "constitution": { "proficient": true },
  "intelligence": { "proficient": false },
  "wisdom":       { "proficient": false },
  "charisma":     { "proficient": false }
}
```

**Common class saves**:
- Fighter/Ranger: STR, CON
- Rogue/Bard: DEX, CHA
- Wizard: INT, WIS
- Cleric/Druid: WIS, CHA
- Sorcerer/Warlock: CON, CHA
- Paladin: WIS, CHA

---

## skills

Skill proficiencies. Each skill links to an ability (shown automatically).

```json
"skills": {
  "acrobatics":       { "proficient": false },
  "animal_handling":  { "proficient": true },
  "arcana":           { "proficient": false },
  "athletics":        { "proficient": true },
  "deception":        { "proficient": false },
  "history":          { "proficient": false },
  "insight":          { "proficient": false },
  "intimidation":     { "proficient": false },
  "investigation":    { "proficient": false },
  "medicine":         { "proficient": false },
  "nature":           { "proficient": true },
  "perception":       { "proficient": true },
  "performance":      { "proficient": false },
  "persuasion":       { "proficient": false },
  "religion":         { "proficient": false },
  "sleight_of_hand":  { "proficient": false },
  "stealth":          { "proficient": true },
  "survival":         { "proficient": true }
}
```

**Skill → Ability mapping**:
- **STR**: Athletics
- **DEX**: Acrobatics, Sleight of Hand, Stealth
- **INT**: Arcana, History, Investigation, Nature, Religion
- **WIS**: Animal Handling, Insight, Medicine, Perception, Survival
- **CHA**: Deception, Intimidation, Performance, Persuasion

---

## combat

Combat statistics and hit points.

```json
"combat": {
  "armor_class": 16,
  "initiative": null,
  "speed": "25 ft",
  "hp_maximum": 30,
  "hp_current": null,
  "hp_temporary": null,
  "hit_dice": {
    "total": "3d10",
    "current": null
  },
  "death_saves": {
    "successes": 0,
    "failures": 0
  }
}
```

| Field | Type | Description |
|-------|------|-------------|
| `armor_class` | integer | Total AC from armor + DEX + shield + other |
| `initiative` | string/null | Override initiative; null = use DEX modifier |
| `speed` | string | Movement speed (usually "30 ft", dwarves "25 ft") |
| `hp_maximum` | integer | Maximum hit points |
| `hp_current` | integer/null | Current HP (null = leave blank for tracking) |
| `hp_temporary` | integer/null | Temporary HP |
| `hit_dice.total` | string | Total hit dice (e.g., "3d10" for level 3 fighter) |
| `hit_dice.current` | string/null | Remaining hit dice |
| `death_saves` | object | Track death save successes/failures |

---

## attacks

Weapon and spell attacks (up to 5 shown on sheet).

```json
"attacks": [
  {
    "name": "Battleaxe",
    "atk_bonus": "+5",
    "damage_type": "1d8+3 slashing"
  },
  {
    "name": "Handaxe",
    "atk_bonus": "+5",
    "damage_type": "1d6+3 slashing"
  },
  {
    "name": "Longbow",
    "atk_bonus": "+4",
    "damage_type": "1d8+2 piercing"
  }
]
```

| Field | Type | Description |
|-------|------|-------------|
| `name` | string | Weapon or spell name |
| `atk_bonus` | string | Attack roll modifier (include + sign) |
| `damage_type` | string | Damage dice + modifier + damage type |

---

## personality

Character personality displayed on Page 1 right column.

```json
"personality": {
  "traits": "I watch over my friends as if they were a litter of newborn pups.",
  "ideals": "Nature. The natural world is more important than all the constructs of civilization.",
  "bonds": "I will bring terrible wrath upon those who harm nature.",
  "flaws": "I am slow to trust the words of any civilized folk."
}
```

---

## equipment

Inventory list and currency.

```json
"proficiencies_languages": [
  "Light armor",
  "Medium armor",
  "Shields",
  "Simple weapons",
  "Martial weapons",
  "Common",
  "Dwarvish",
  "Sylvan"
],

"equipment": [
  "Scale mail",
  "Battleaxe",
  "Handaxe (2)",
  "Longbow",
  "Quiver with 20 arrows",
  "Explorer's pack",
  "Herbalism kit"
],

"currency": {
  "cp": 0,
  "sp": 5,
  "ep": 0,
  "gp": 45,
  "pp": 0
}
```

---

## features_traits

Class features, racial traits, and background features (Page 1).

```json
"features_traits": [
  "Darkvision (60 ft)",
  "Dwarven Resilience",
  "Favored Enemy: Beasts",
  "Natural Explorer: Forest",
  "Fighting Style: Archery (+2)",
  "Ranger Archetype: Beast Master",
  "Rustic Hospitality"
]
```

---

## appearance

Physical description shown in Page 2 header.

```json
"appearance": {
  "age": "85",
  "height": "4'5\"",
  "weight": "165 lbs",
  "eyes": "Amber",
  "skin": "Tan",
  "hair": "Black with gray streaks"
}
```

---

## backstory

Character history (Page 2). Use `\n\n` for paragraph breaks.

```json
"character_appearance_description": "Thorek is a stocky dwarf with...",

"backstory": "Born in the mountain halls of Kazak-Thurn...\n\nAfter witnessing the destruction...\n\nNow he wanders the forests..."
```

---

## allies_organizations

Allies and organizational affiliations (Page 2).

```json
"allies_organizations": {
  "name": "The Emerald Enclave",
  "description": "A far-reaching network of druids and rangers who protect the natural world.\n\nThorek serves as a scout and beast handler."
}
```

---

## additional_features_traits

Additional features that overflow from Page 1 (Page 2).

```json
"additional_features_traits": [
  "Primeval Awareness",
  "Beast Master: Exceptional Training"
]
```

---

## treasure

Notable treasure and magic items (Page 2).

```json
"treasure": [
  "Ring of the Wild Hunt",
  "Potion of Healing (2)",
  "50 gp ruby"
]
```

---

## spellcasting

Full spellcasting information (Page 3).

```json
"spellcasting": {
  "class": "Ranger",
  "ability": "WIS",
  "spell_save_dc": 13,
  "spell_attack_bonus": "+5",
  "cantrips": [],
  "spells": {
    "1": {
      "slots_total": 3,
      "slots_expended": 0,
      "known": [
        { "name": "Cure Wounds", "prepared": true },
        { "name": "Hunter's Mark", "prepared": true },
        { "name": "Speak with Animals", "prepared": false }
      ]
    },
    "2": {
      "slots_total": 0,
      "slots_expended": 0,
      "known": []
    }
  }
}
```

| Field | Type | Description |
|-------|------|-------------|
| `class` | string | Spellcasting class |
| `ability` | string | Spellcasting ability (INT/WIS/CHA) |
| `spell_save_dc` | integer | 8 + proficiency + ability mod |
| `spell_attack_bonus` | string | proficiency + ability mod |
| `cantrips` | array | List of cantrip names (strings) |
| `spells.[level].slots_total` | integer | Total spell slots at this level |
| `spells.[level].slots_expended` | integer | Used slots (for tracking) |
| `spells.[level].known` | array | Spells known/prepared at this level |

**Spell format**: `{ "name": "Spell Name", "prepared": true/false }`

---

## companion

Beast companion for Beast Master Rangers, familiars, etc. (Page 4).

**Set to `null` if no companion.**

```json
"companion": {
  "name": "Ironjaw",
  "size": "Medium",
  "type": "Beast (Black Bear)",
  "armor_class": 12,
  "hit_points": 25,
  "hp_notes": "4d8+8",
  "speed": "40 ft, climb 30 ft",
  "image": "../../images/thorek/ironjaw_portrait.jpg",

  "abilities": {
    "str": 16,
    "dex": 12,
    "con": 14,
    "int": 2,
    "wis": 13,
    "cha": 7
  },

  "skills": "Perception +3",
  "senses": "Passive Perception 13",

  "traits": [
    {
      "name": "Keen Smell",
      "description": "Advantage on Perception checks that rely on smell."
    }
  ],

  "actions": [
    {
      "name": "Multiattack",
      "description": "Makes two attacks: one bite and one claw."
    },
    {
      "name": "Bite",
      "description": "+5 to hit, 1d6+3 piercing damage."
    },
    {
      "name": "Claw",
      "description": "+5 to hit, 2d4+3 slashing damage."
    }
  ],

  "commands": [
    "Attack (bonus action)",
    "Dash, Disengage, or Help (bonus action)",
    "Defend: Advantage on saves vs. fear"
  ]
}
```

---

## reference

Quick reference cards for Page 4. All subsections are optional.

### Weapons Reference

```json
"reference": {
  "weapons": [
    {
      "name": "Battleaxe",
      "type": "Martial Melee",
      "damage": "1d8 slashing",
      "properties": "Versatile (1d10)",
      "notes": "+5 to hit, +3 damage"
    }
  ]
}
```

### Spells Reference

```json
"reference": {
  "spells": [
    {
      "name": "Hunter's Mark",
      "level": "1st",
      "casting_time": "1 bonus action",
      "range": "90 feet",
      "duration": "Concentration, 1 hour",
      "description": "Extra 1d6 damage on hits. Advantage on Perception/Survival to find target."
    }
  ]
}
```

### Features Reference

```json
"reference": {
  "features": [
    {
      "name": "Favored Enemy: Beasts",
      "description": "Advantage on Survival to track and INT checks to recall info about beasts."
    }
  ]
}
```

### Turn Structure

```json
"reference": {
  "turn_structure": {
    "title": "Your Turn",
    "phases": [
      { "name": "Movement", "desc": "Move up to 25 ft (can split)" },
      { "name": "Action", "desc": "Attack, Cast Spell, Dash, etc." },
      { "name": "Bonus Action", "desc": "Hunter's Mark, off-hand attack" },
      { "name": "Free Action", "desc": "Interact with object, speak" }
    ],
    "reaction": "Opportunity Attack when enemy leaves reach"
  }
}
```

### Combat Reference

```json
"reference": {
  "combat_reference": {
    "actions": [
      { "name": "Attack", "desc": "Weapon attack (extra at level 5)" },
      { "name": "Dash", "desc": "Double movement" },
      { "name": "Dodge", "desc": "Attacks have disadvantage" },
      { "name": "Help", "desc": "Give ally advantage" },
      { "name": "Ready", "desc": "Prepare action with trigger" }
    ],
    "conditions_quick": [
      { "name": "Prone", "desc": "Melee adv, ranged disadv" },
      { "name": "Grappled", "desc": "Speed 0" },
      { "name": "Restrained", "desc": "Speed 0, attacks disadv" },
      { "name": "Stunned", "desc": "Incapacitated, auto-fail saves" }
    ],
    "cover": [
      { "type": "Half", "bonus": "+2 AC" },
      { "type": "3/4", "bonus": "+5 AC" },
      { "type": "Full", "bonus": "Can't target" }
    ]
  }
}
```

---

## Complete Minimal Example

A bare-minimum character with only required fields:

```json
{
  "meta": { "version": "1.0" },
  "header": {
    "character_name": "Test Character",
    "class_level": "Fighter 1",
    "race": "Human"
  },
  "abilities": {
    "strength": { "score": 10 },
    "dexterity": { "score": 10 },
    "constitution": { "score": 10 },
    "intelligence": { "score": 10 },
    "wisdom": { "score": 10 },
    "charisma": { "score": 10 }
  },
  "proficiency_bonus": 2,
  "combat": {
    "armor_class": 10,
    "speed": "30 ft",
    "hp_maximum": 10,
    "hit_dice": { "total": "1d10" }
  }
}
```

All other fields will use sensible defaults (empty arrays, blank strings, etc.).

---

# Item Schema

Magic items use a different structure with `"type": "item"` at the root.

## Item Structure Overview

```json
{
  "type": "item",
  "meta": { "version": "1.0" },
  "header": { ... },
  "footer": { ... },
  "pages": [ ... ]
}
```

---

## item-header

Item identification and display information.

```json
"header": {
  "name": "Ring of the Wild Hunt",
  "subtitle": "Forged in the Moonwell of Eternal Spring",
  "image": "images/character/item.jpg",
  "background_svg": "images/character/decoration.svg",
  "stats": [
    { "label": "Rarity", "value": "Rare", "class": "rarity-rare" },
    { "label": "Attunement", "value": "Beast Master Ranger" },
    { "label": "Weight", "value": "0.1 lbs" }
  ]
}
```

| Field | Type | Description |
|-------|------|-------------|
| `name` | string | Item name (displayed large) |
| `subtitle` | string | Flavor text or origin (optional) |
| `image` | string | Path to item image |
| `background_svg` | string | Path to SVG decoration (optional) |
| `stats` | array | Stat badges displayed below title |

**Rarity CSS classes**: `rarity-common`, `rarity-uncommon`, `rarity-rare`, `rarity-very-rare`, `rarity-legendary`

---

## item-footer

Footer information.

```json
"footer": {
  "left": "Item identifier or maker info",
  "right": "Market Value: 5,000 gp"
}
```

---

## item-pages

Array of page definitions. Each page contains layout and sections.

```json
"pages": [
  {
    "layout": {
      "columns": 2,
      "gap": "3mm"
    },
    "sections": [ ... ]
  }
]
```

| Field | Type | Description |
|-------|------|-------------|
| `layout.columns` | integer | Number of columns (1 or 2) |
| `layout.gap` | string | Gap between columns (CSS value) |
| `sections` | array | Section definitions |

---

## Section Definition

Each section in a page:

```json
{
  "column": 1,
  "title": "Section Title",
  "variant": "default",
  "flex_grow": false,
  "content": { ... }
}
```

| Field | Type | Description |
|-------|------|-------------|
| `column` | integer | Which column (1 or 2) |
| `title` | string/null | Section title (null = no title bar) |
| `variant` | string | `"default"` or `"lore"` (special background) |
| `flex_grow` | boolean | Fill remaining vertical space |
| `content` | object | Content type object |

---

## content-types

### text

Plain paragraph text.

```json
{ "type": "text", "text": "Content with **bold** support." }
```

### text_italic

Italic paragraph for descriptions.

```json
{ "type": "text_italic", "text": "This ancient ring glows..." }
```

### bullets

Bullet point list.

```json
{
  "type": "bullets",
  "items": ["First point", "Second with **bold**"]
}
```

### properties

Icon + name + description rows.

```json
{
  "type": "properties",
  "items": [
    { "icon": "⚔", "name": "Enhanced Damage", "desc": "+2 to damage" }
  ]
}
```

### table

Data table with optional footer.

```json
{
  "type": "table",
  "columns": ["Level", "Bonus"],
  "rows": [["3", "+1"], ["5", "+2"]],
  "footer": "* Optional footnote"
}
```

### quote

Lore quote with attribution.

```json
{
  "type": "quote",
  "text": "The ring was forged...",
  "attribution": "— From the Archives"
}
```

### comparison

Before/after stat rows.

```json
{
  "type": "comparison",
  "items": [
    { "before": "HP: 19", "after": "HP: 25 (+31%)" }
  ]
}
```

### tales

Title + description pairs.

```json
{
  "type": "tales",
  "items": [
    { "title": "Battle of X", "desc": "The item saved a kingdom" }
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
      "bullets": ["Point 1", "Point 2"]
    }
  ]
}
```

### synergy

Special composite for companion effects.

```json
{
  "type": "synergy",
  "header": {
    "icon": "🐻",
    "title": "Synergy with Companion",
    "subtitle": "Character's Animal"
  },
  "comparisons": [
    { "before": "HP: 19", "after": "HP: 25" }
  ],
  "subsections": [
    { "name": "Tactics", "bullets": ["Point 1"] }
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

---

## Complete Item Example

```json
{
  "type": "item",
  "meta": { "version": "1.0" },
  "header": {
    "name": "Sword of Flames",
    "subtitle": "Forged in dragon fire",
    "image": "images/hero/sword.jpg",
    "stats": [
      { "label": "Rarity", "value": "Rare", "class": "rarity-rare" },
      { "label": "Type", "value": "Longsword" }
    ]
  },
  "footer": {
    "left": "Crafted by Smith",
    "right": "Value: 5,000 gp"
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
          "column": 2,
          "title": "Properties",
          "content": {
            "type": "properties",
            "items": [
              { "icon": "🔥", "name": "Flame", "desc": "+1d6 fire" }
            ]
          }
        }
      ]
    }
  ]
}
```
