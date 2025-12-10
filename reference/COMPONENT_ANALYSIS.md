# Component Analysis - Character Sheet vs Item Card

## Goal
Identify all UI components and map them to shared base components.

---

## BASE COMPONENTS (Shared)

### 1. `.box` - The Universal Container
Everything inherits from `.box`:
- Border with corner accents (gold fade effect)
- Paper texture background gradient
- Standard padding

**Modifiers:**
- `.box--label-top` - Label at top
- `.box--label-bottom` - Label at bottom
- `.box--flex` - Grows to fill space
- `.box--centered` - Centers content

---

## CHARACTER PAGE COMPONENTS

### PAGE 1 - Main Stats

| Component | CSS Class | Maps To |
|-----------|-----------|---------|
| Ability Score Box | `.box.ability-score` | **NEW: AbilityBox** |
| Stat Circle (Inspiration, Prof) | `.box.stat-row` | **NEW: StatCircle** |
| Saves/Skills Box | `.box.saves-skills-box` | `.box` + title |
| Passive Perception | `.box.passive-box` | **NEW: PassiveBox** |
| Proficiencies | `.box.proficiencies-box` | `.box` + list |
| Combat Stats (AC/Init/Speed) | `.box.combat-stat` | **NEW: CombatStat** |
| HP Section | `.box.hp-section` | **NEW: HPBox** |
| HP Temp | `.box.hp-temp` | `.box` |
| Hit Dice | `.box.hitdice-box` | `.box` |
| Death Saves | `.box.death-box` | **NEW: DeathSaveBox** |
| Attacks Table | `.box.attacks-box` | **= Item's table?** |
| Equipment | `.box.equipment-box` | `.box` + list |
| Trait Box | `.box.trait-box` | **= Item's section-box** |
| Notes | `.box.notes-box` | **= LINED PAPER** |

### PAGE 2 - Background

| Component | CSS Class | Maps To |
|-----------|-----------|---------|
| Large Text Box | `.large-box` | **= Item's section-box** |
| Notes (full width) | `.notes-box` | **= LINED PAPER** |

### PAGE 3 - Spellcasting

| Component | CSS Class | Maps To |
|-----------|-----------|---------|
| Spell Level Box | `.spell-level-box` | **= LINED PAPER + header** |

All 10 boxes (cantrips + levels 1-9) are identical:
- Header with level number + slots
- Lined paper area for spell names

### PAGE 4 - Reference

| Component | CSS Class | Maps To |
|-----------|-----------|---------|
| Reference Card | `.ref-card` | `.box` + sections |
| Companion Card | `.companion-box` | **= Item's section-box** |
| Feature Card | `.feature-card` | **= Item's section-box** |

---

## ITEM PAGE COMPONENTS

| Component | CSS Class | Notes |
|-----------|-----------|-------|
| Section Box | `.section-box` | Universal content box |
| Description Box | `.description-box` | Lore variant (gold tint) |
| Properties List | `.property-list` | Icon + name + desc |
| Table | `.scaling-table` | Standard table |
| Quote | `.quote-block` | Italics + attribution |

---

## SHARED PATTERNS IDENTIFIED

### Pattern 1: LINED PAPER (Notes/Spells)
Used in:
- Page 1: Notes section
- Page 2: Notes row
- Page 3: ALL spell level boxes (10 boxes)

```
┌─────────────────┐
│ TITLE           │
├─────────────────┤
│ _______________ │
│ _______________ │
│ _______________ │
│ _______________ │
└─────────────────┘
```

### Pattern 2: SECTION BOX (Text content)
Used in:
- Page 1: Trait boxes (personality, ideals, bonds, flaws, features)
- Page 2: Large boxes (appearance, backstory, allies, notes)
- Page 4: Reference cards, companion, features
- Items: ALL content sections

```
┌─────────────────┐
│ SECTION TITLE   │
├─────────────────┤
│ Content here    │
│ can be text,    │
│ lists, tables   │
└─────────────────┘
```

### Pattern 3: STAT BOX (Numbers)
Used in:
- Page 1: Ability scores, AC, Initiative, Speed, HP

```
┌─────────┐
│   15    │  ← Large number
│   +2    │  ← Modifier
├─────────┤
│  LABEL  │
└─────────┘
```

---

## PROPOSED UNIFIED COMPONENTS

### Layout Components

1. **Row** - Horizontal flex container
   - `.row` - display: flex, gap
   - `.row--stretch` - items stretch to fill
   - `.row--wrap` - allows wrapping

2. **Col** - Vertical flex container
   - `.col` - display: flex, flex-direction: column
   - `.col--1`, `.col--2`, `.col--3` - width fractions
   - `.col--flex` - grows to fill

3. **Grid** - CSS Grid container
   - `.grid--2col`, `.grid--3col` - column layouts

### Content Components

4. **Box** - Base container (already exists)
   - Modifiers: `--label-top`, `--label-bottom`, `--flex`, `--lore`

5. **SectionBox** - Titled content container
   - Title bar
   - Content area (accepts any content type)
   - Variant: `--lore` for description boxes

6. **LinedPaper** - Notes/spell list area
   - Optional title
   - Horizontal lines background
   - Optional header row (for spell slots)

7. **StatBox** - Numeric display
   - Large value
   - Optional modifier
   - Label

8. **Table** - Data table (already exists in items)

9. **PropertyList** - Icon + name + description list

---

## PAGE LAYOUT MAPPING

### Page 1 (Stats)
```
┌─ Row ──────────────────────────────────────┐
│ ┌─ Col ─┐ ┌─ Col ──────┐ ┌─ Col ─────────┐ │
│ │ STR   │ │ Insp/Prof  │ │ Traits       │ │
│ │ DEX   │ │ Saves      │ │ Ideals       │ │
│ │ CON   │ │ Skills     │ │ Bonds        │ │
│ │ INT   │ ├────────────┤ │ Flaws        │ │
│ │ WIS   │ │ Combat     │ │ Features     │ │
│ │ CHA   │ │ Attacks    │ │ Notes        │ │
│ └───────┘ │ Equipment  │ │ Gallery      │ │
│           └────────────┘ └──────────────┘ │
└────────────────────────────────────────────┘
```

### Page 2 (Background)
```
┌─ Row ──────────────────────────────────────┐
│ ┌─ Col ──────────┐ ┌─ Col ──────────────┐  │
│ │ Appearance     │ │ Allies             │  │
│ │ Backstory      │ │ Additional Features│  │
│ │                │ │ Treasure           │  │
│ └────────────────┘ └────────────────────┘  │
├────────────────────────────────────────────┤
│ ┌─ Notes (full width) ───────────────────┐ │
│ │ _______________________________________ │ │
│ └────────────────────────────────────────┘ │
└────────────────────────────────────────────┘
```

### Page 3 (Spellcasting)
```
┌─ Grid 3-col ───────────────────────────────┐
│ ┌─────────┐ ┌─────────┐ ┌─────────────────┐│
│ │Cantrips │ │ Level 1 │ │ Level 2         ││
│ │(lined)  │ │(lined)  │ │ (lined)         ││
│ └─────────┘ └─────────┘ └─────────────────┘│
│ ┌─────────┐ ┌─────────┐ ┌─────────────────┐│
│ │ Level 3 │ │ Level 4 │ │ Level 5         ││
│ └─────────┘ └─────────┘ └─────────────────┘│
│ ... etc                                    │
└────────────────────────────────────────────┘
```

---

## BACKUP CREATED

Reference files saved in `/reference/`:
- `Aldric_BEFORE.html` - Original character sheet
- `Thorek_BEFORE.html` - Original bundle with item

Branch backup: `backup/pre-component-refactor`

---

## NEXT STEPS

1. [ ] Create `base.css` with variables + `.box` + `.row` + `.col` + `.grid`
2. [ ] Create `components.css` with SectionBox, LinedPaper, StatBox
3. [ ] Update `sheet.css` to @import base + add character-specific only
4. [ ] Update `item.css` to @import base + add item-specific only
5. [ ] Update Python `components.py` with Row, Col, Grid classes
6. [ ] Refactor CharacterDocument to use new layout components
7. [ ] Test against BEFORE files - visual diff
8. [ ] Fix any regressions
