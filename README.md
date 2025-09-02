# 🐉 D&D Character Sheet Manager

An epic character sheet management system for D&D 5e with modern graphics, automated updates, and professional printing.

## ✨ Features

- **🎨 Epic Modern Character Sheets** - Beautiful graphics with Celtic borders, hexagonal ability scores, and color-coded sections
- **📄 3-Page Fixed Layout** - No orphaned headers, optimized for printing
- **📝 Session Note Areas** - Dedicated spaces for notes on every page
- **🔄 Weekly Updates** - Interactive scripts to update XP, loot, and character progression
- **📈 Automatic Level-ups** - Handles Sorcerer advancement with metamagic and spell choices
- **🖨️ Print-Optimized** - Professional PDF-ready output

## 🗂️ Project Structure

```
📁 d_and_d/
├── 📁 generators/          # Character sheet generators
│   ├── modern_sheet_generator.py    # Epic modern sheets
│   ├── simple_sheet_generator.py    # Basic HTML sheets  
│   └── generate_character_sheet.py  # ReportLab PDF version
├── 📁 scripts/             # Update and maintenance scripts
│   ├── epic_weekly_update.py        # Interactive weekly updater
│   └── weekly_update.py             # Basic updater
├── 📁 sheets/              # Generated character sheets
│   ├── Kazrek_Epic_Sheet.html       # Current epic sheet
│   └── Kazrek_Official_Sheet.html   # Basic sheet
├── 📁 docs/                # Documentation and templates
│   ├── Kazrek_Session_Tracker.md    # Session tracking template
│   ├── Kazrek_Spellforge_Level2.md  # Character data template
│   └── update_system.md             # Update workflow guide
├── 📁 data/                # Character data and saves
├── 📁 backups/             # Backup files and session summaries
└── 📁 venv/                # Python virtual environment
```

## 🚀 Quick Start

### Generate Epic Character Sheet

```bash
python3 generators/modern_sheet_generator.py
```

This creates `sheets/Kazrek_Epic_Sheet.html` - open in browser and print!

### Weekly Session Updates

```bash
python3 scripts/epic_weekly_update.py
```

Interactive prompts for:
- XP gained
- New equipment
- Currency changes
- HP updates
- Automatic level-up handling

## 🖨️ Printing Instructions

1. Open `sheets/Kazrek_Epic_Sheet.html` in any browser
2. **File → Print** (Ctrl/Cmd + P)
3. Click **"More settings"**
4. ✅ Check **"Background graphics"** (essential for borders/colors)
5. Set margins to **"Minimum"**
6. Print 3 epic pages!

## 📋 Character: Kazrek Spellforge

- **Race:** Mountain Dwarf
- **Class:** Sorcerer (Level 2)
- **Background:** Hermit
- **Alignment:** Chaotic Good

**Current Stats:**
- HP: 20
- AC: 11
- Spells: 4 cantrips, 3 first-level spells
- Sorcery Points: 2

## 🎯 Weekly Workflow

1. **Before Session:** Print current sheet from `sheets/`
2. **During Session:** Fill in note areas, track resources
3. **After Session:** Run `scripts/epic_weekly_update.py`
4. **Next Session:** Fresh updated sheet ready!

## 🛠️ Development

### Setup Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\\Scripts\\activate
pip install reportlab     # Only needed for PDF generator
```

### File Dependencies

- **Epic sheets require:** Modern browser with CSS3 support
- **PDF generator requires:** `reportlab` library
- **Updates work with:** Python 3.7+

## 📝 Session Tracking

Each update creates:
- Updated character sheet
- Session summary file
- Character data backup (JSON)

## 🎨 Visual Features

- **Celtic gold borders** with decorative patterns
- **Hexagonal ability scores** for visual impact  
- **Color-coded sections:** Red (combat), Blue (skills), Purple (spells), Green (equipment)
- **Shimmer animations** on interactive elements
- **Professional typography** with fantasy fonts
- **Session note areas** with lined backgrounds

## 🔮 Level-Up Support

Automated handling for:
- HP increases (roll or average)
- New spell slots
- Sorcerer metamagic choices
- Additional known spells
- Sorcery point progression

## 📜 License

Personal use for D&D campaigns. Feel free to adapt for your own characters!

---

*Ready for epic adventures! 🗡️⚔️🐉*