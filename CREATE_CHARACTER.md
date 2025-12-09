# D&D 5e Character Creation Guide

You are helping create a D&D 5e character. Ask the user questions to fill out each section below, then generate a complete JSON file.

## Questions to Ask

### 1. Basic Info
- What is your character's name?
- What class and level? (e.g., "Ranger 3", "Wizard 5")
- What race? (e.g., Hill Dwarf, High Elf, Human)
- What background? (e.g., Folk Hero, Sage, Criminal)
- What alignment? (e.g., Neutral Good, Chaotic Neutral)
- Current XP?
- Player name? (optional)
- Do you have a portrait image file? (path like "images/name.png")

### 2. Ability Scores
Ask for each: Strength, Dexterity, Constitution, Intelligence, Wisdom, Charisma
(Standard array: 15, 14, 13, 12, 10, 8 or point buy or rolled)

### 3. Proficiencies
- Which saving throws are you proficient in? (usually 2, based on class)
- Which skills are you proficient in? (number varies by class/background)

Skills list: Acrobatics, Animal Handling, Arcana, Athletics, Deception, History, Insight, Intimidation, Investigation, Medicine, Nature, Perception, Performance, Persuasion, Religion, Sleight of Hand, Stealth, Survival

### 4. Combat Stats
- Armor Class?
- Speed? (usually 30ft, dwarves 25ft)
- Hit Point Maximum?
- Hit Dice? (e.g., "3d10" for level 3 ranger)

### 5. Attacks (up to 5)
For each attack ask:
- Weapon/attack name?
- Attack bonus? (e.g., "+5")
- Damage and type? (e.g., "1d8+3 slashing")

### 6. Personality
- Personality traits? (1-2 sentences)
- Ideals? (what drives them)
- Bonds? (connections to people/places)
- Flaws? (weaknesses)

### 7. Equipment
List all equipment items (armor, weapons, adventuring gear, etc.)

### 8. Currency
How much of each: CP, SP, EP, GP, PP?

### 9. Features & Traits
List racial features, class features, and background features

### 10. Proficiencies & Languages
List all: armor, weapon, tool proficiencies, and languages known

### 11. Appearance
- Age?
- Height?
- Weight?
- Eye color?
- Skin?
- Hair?
- Physical description? (1-2 sentences)

### 12. Backstory
Ask for 2-3 paragraphs of character history. Write in proper prose without dashes.

### 13. Allies & Organizations
- Organization or ally name?
- Description of relationship?

### 14. Spellcasting (if applicable)
- Spellcasting class?
- Spellcasting ability? (Int/Wis/Cha)
- Spell Save DC?
- Spell Attack Bonus?
- Cantrips known?
- For each spell level (1-9): slots total and spells known (with prepared status)

---

## JSON Template

After gathering all info, generate this JSON structure:

```json
{
  "meta": {
    "version": "1.0",
    "generated": null,
    "portrait": "images/character.png"
  },

  "header": {
    "character_name": "",
    "class_level": "",
    "background": "",
    "player_name": "",
    "race": "",
    "alignment": "",
    "experience_points": 0
  },

  "abilities": {
    "strength":     { "score": 10 },
    "dexterity":    { "score": 10 },
    "constitution": { "score": 10 },
    "intelligence": { "score": 10 },
    "wisdom":       { "score": 10 },
    "charisma":     { "score": 10 }
  },

  "proficiency_bonus": 2,
  "inspiration": false,

  "saving_throws": {
    "strength":     { "proficient": false },
    "dexterity":    { "proficient": false },
    "constitution": { "proficient": false },
    "intelligence": { "proficient": false },
    "wisdom":       { "proficient": false },
    "charisma":     { "proficient": false }
  },

  "skills": {
    "acrobatics":       { "proficient": false },
    "animal_handling":  { "proficient": false },
    "arcana":           { "proficient": false },
    "athletics":        { "proficient": false },
    "deception":        { "proficient": false },
    "history":          { "proficient": false },
    "insight":          { "proficient": false },
    "intimidation":     { "proficient": false },
    "investigation":    { "proficient": false },
    "medicine":         { "proficient": false },
    "nature":           { "proficient": false },
    "perception":       { "proficient": false },
    "performance":      { "proficient": false },
    "persuasion":       { "proficient": false },
    "religion":         { "proficient": false },
    "sleight_of_hand":  { "proficient": false },
    "stealth":          { "proficient": false },
    "survival":         { "proficient": false }
  },

  "combat": {
    "armor_class": 10,
    "initiative": null,
    "speed": 30,
    "hp_maximum": 10,
    "hp_current": null,
    "hp_temporary": null,
    "hit_dice": {
      "total": "1d8",
      "current": null
    },
    "death_saves": {
      "successes": 0,
      "failures": 0
    }
  },

  "attacks": [
    {
      "name": "Weapon",
      "atk_bonus": "+0",
      "damage_type": "1d6 type"
    }
  ],

  "personality": {
    "traits": "",
    "ideals": "",
    "bonds": "",
    "flaws": ""
  },

  "proficiencies_languages": [],

  "equipment": [],

  "currency": {
    "cp": 0,
    "sp": 0,
    "ep": 0,
    "gp": 0,
    "pp": 0
  },

  "features_traits": [],

  "appearance": {
    "age": "",
    "height": "",
    "weight": "",
    "eyes": "",
    "skin": "",
    "hair": ""
  },

  "character_appearance_description": "",

  "backstory": "",

  "allies_organizations": {
    "name": "",
    "description": ""
  },

  "additional_features_traits": [],

  "treasure": [],

  "spellcasting": {
    "class": "",
    "ability": "",
    "spell_save_dc": 0,
    "spell_attack_bonus": "+0",
    "cantrips": [],
    "spells": {
      "1": { "slots_total": 0, "slots_expended": 0, "known": [] },
      "2": { "slots_total": 0, "slots_expended": 0, "known": [] },
      "3": { "slots_total": 0, "slots_expended": 0, "known": [] },
      "4": { "slots_total": 0, "slots_expended": 0, "known": [] },
      "5": { "slots_total": 0, "slots_expended": 0, "known": [] },
      "6": { "slots_total": 0, "slots_expended": 0, "known": [] },
      "7": { "slots_total": 0, "slots_expended": 0, "known": [] },
      "8": { "slots_total": 0, "slots_expended": 0, "known": [] },
      "9": { "slots_total": 0, "slots_expended": 0, "known": [] }
    }
  }
}
```

## Notes

- For backstory, use `\n\n` between paragraphs
- Spells format: `{ "name": "Spell Name", "prepared": true }`
- Calculate proficiency bonus from level: 1-4=+2, 5-8=+3, 9-12=+4, etc.
- Initiative is calculated automatically from Dexterity if left null
- Save the file as `characters/charactername.json`
- Run `python3 generate.py` to generate the sheet in `output/`
