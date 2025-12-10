# Character Creation Guide

Create custom D&D 5e character sheets from JSON data files.

## Quick Start

1. Create a JSON file: `characters/<name>.json`
2. Add character images: `images/<name>/`
3. Generate: `python3 generate.py <name> --compress --open`

## File Structure

```
d_and_d/
├── characters/
│   └── aldric.json           # Character data + embedded items
├── images/
│   └── aldric/
│       ├── portrait.jpg      # Main portrait
│       ├── scene1.jpg        # Gallery images
│       └── companion.jpg     # Companion image
└── output/
    └── Aldric_the_Brave/     # Generated files
        ├── *.html
        └── *.pdf
```

## JSON Structure

```json
{
  "meta": {
    "version": "1.0",
    "portrait": "../../images/aldric/portrait.jpg",
    "gallery": [
      "../../images/aldric/image1.jpg",
      "../../images/aldric/image2.jpg"
    ]
  },
  "header": {
    "character_name": "Character Name",
    "class_level": "Ranger 3",
    "background": "Folk Hero",
    "player_name": "Player",
    "race": "Hill Dwarf",
    "alignment": "Neutral Good",
    "experience_points": 900
  },
  "abilities": { ... },
  "saving_throws": { ... },
  "skills": { ... },
  "combat": { ... },
  "attacks": [ ... ],
  "personality": { ... },
  "equipment": [ ... ],
  "spellcasting": { ... },
  "companion": { ... },
  "items": [ ... ]
}
```

See [SCHEMA.md](SCHEMA.md) for complete field documentation.

## Information to Gather

### 1. Basic Info
- Character name, class, level, race, background
- Alignment, XP, player name
- Portrait image file

### 2. Ability Scores
Six scores: Strength, Dexterity, Constitution, Intelligence, Wisdom, Charisma
(Standard array: 15, 14, 13, 12, 10, 8)

### 3. Proficiencies
- Saving throws (usually 2 based on class)
- Skills (varies by class/background)

### 4. Combat Stats
- Armor Class, Speed, Hit Points, Hit Dice

### 5. Attacks
- Weapon name, attack bonus, damage/type

### 6. Personality
- Traits, Ideals, Bonds, Flaws

### 7. Equipment & Currency
- All items and coin amounts

### 8. Features & Traits
- Racial, class, and background features

### 9. Appearance & Backstory
- Physical description, character history

### 10. Spellcasting (if applicable)
- Spellcasting ability, DC, attack bonus
- Cantrips and spells by level

### 11. Companion (optional)
- Beast Master companion, familiar, etc.

### 12. Magic Items (optional)
- Items embedded in the `items` array

## JSON Sections

### meta

```json
"meta": {
  "version": "1.0",
  "portrait": "../../images/aldric/portrait.jpg",
  "gallery": [
    "../../images/aldric/forest.jpg",
    "../../images/aldric/combat.jpg"
  ]
}
```

### header

```json
"header": {
  "character_name": "Aldric the Brave",
  "class_level": "Ranger 3",
  "background": "Folk Hero",
  "player_name": "Joe",
  "race": "Hill Dwarf",
  "alignment": "Neutral Good",
  "experience_points": 900
}
```

### abilities

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

### saving_throws

```json
"saving_throws": {
  "strength":     { "proficient": true },
  "dexterity":    { "proficient": true },
  "constitution": { "proficient": false },
  "intelligence": { "proficient": false },
  "wisdom":       { "proficient": false },
  "charisma":     { "proficient": false }
}
```

### skills

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

### combat

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

### attacks

```json
"attacks": [
  {
    "name": "Battleaxe",
    "atk_bonus": "+5",
    "damage_type": "1d8+3 slashing"
  },
  {
    "name": "Longbow",
    "atk_bonus": "+4",
    "damage_type": "1d8+2 piercing"
  }
]
```

### personality

```json
"personality": {
  "traits": "I watch over my friends as if they were a litter of newborn pups.",
  "ideals": "Nature. The natural world is more important than all constructs of civilization.",
  "bonds": "I will bring terrible wrath upon those who harm nature.",
  "flaws": "I am slow to trust the words of any civilized folk."
}
```

### equipment

```json
"proficiencies_languages": [
  "Light armor", "Medium armor", "Shields",
  "Simple weapons", "Martial weapons",
  "Common", "Dwarvish", "Sylvan"
],

"equipment": [
  "Scale mail",
  "Battleaxe",
  "Handaxe (2)",
  "Longbow",
  "Quiver with 20 arrows",
  "Explorer's pack"
],

"currency": {
  "cp": 0, "sp": 5, "ep": 0, "gp": 45, "pp": 0
}
```

### spellcasting

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
        { "name": "Hunter's Mark", "prepared": true }
      ]
    }
  }
}
```

### companion (optional)

```json
"companion": {
  "name": "Ironjaw",
  "size": "Medium",
  "type": "Beast (Black Bear)",
  "armor_class": 12,
  "hit_points": 25,
  "speed": "40 ft, climb 30 ft",
  "image": "../../images/aldric/ironjaw.jpg",
  "abilities": {
    "str": 16, "dex": 12, "con": 14,
    "int": 2, "wis": 13, "cha": 7
  },
  "traits": [
    { "name": "Keen Smell", "description": "Advantage on Perception checks using smell." }
  ],
  "actions": [
    { "name": "Bite", "description": "+5 to hit, 1d6+3 piercing." }
  ]
}
```

Set to `null` if no companion.

### items (optional)

Magic items are embedded directly in the character file. See [SCHEMA.md](SCHEMA.md) for item structure.

```json
"items": [
  {
    "type": "item",
    "meta": { "version": "1.0" },
    "header": { ... },
    "footer": { ... },
    "pages": [ ... ]
  }
]
```

Set to `[]` if no items.

## Tips

- Image paths use `../../images/<name>/` (relative from output folder)
- Use `\n\n` for paragraph breaks in backstory
- Spell format: `{ "name": "Spell Name", "prepared": true/false }`
- Proficiency bonus: 1-4=+2, 5-8=+3, 9-12=+4, 13-16=+5, 17-20=+6
- Initiative is calculated from DEX if left null

## Generation Commands

```bash
# HTML only
python3 generate.py aldric

# With PDF
python3 generate.py aldric --pdf

# Full pipeline with compressed PDF
python3 generate.py aldric --compress --open

# Include magic items in output
python3 generate.py aldric --bundle --compress --open
```
