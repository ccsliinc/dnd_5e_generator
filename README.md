# D&D 5e Character Sheet Generator

Generate printable HTML character sheets from JSON data files.

## Project Structure

```
d_and_d/
├── characters/          # Character JSON files go here
│   └── thorek.json
├── images/              # Character artwork
├── output/              # Generated HTML (gitignored)
├── styles/
│   └── sheet.css        # Stylesheet
├── generate.py          # Main generator
└── package.sh           # Packaging script
```

## Quick Start

1. Add your character JSON to `characters/`
2. Run: `python3 generate.py`
3. Open `output/<Character_Name>.html` in your browser
4. Print!

No dependencies required - uses only Python standard library.

## Usage

```bash
# Generate first character in characters/ folder
python3 generate.py

# Generate specific character
python3 generate.py thorek.json

# Or use full path
python3 generate.py characters/thorek.json
```

Output is saved to `output/<Character_Name>.html`

## Print Settings

1. Open the HTML file in your browser
2. File → Print (Ctrl/Cmd + P)
3. Enable **Background graphics**
4. Set margins to **Minimum**
5. Print all 4 pages

## JSON Structure

See `characters/thorek.json` for a complete example. Key sections:

- `meta.portrait` - Path to character image
- `meta.gallery` - Array of additional images for page 1
- `header` - Name, class, race, etc.
- `abilities` - Ability scores
- `skills` - Skill proficiencies
- `attacks` - Weapon attacks
- `spellcasting` - Spells and slots
- `backstory` - Character background (use `\n\n` for paragraphs)
- `companion` - Beast companion stats (optional)
- `reference` - Quick reference data for page 4

## Customizing Styles

Edit `styles/sheet.css`. Key variables at the top:

```css
:root {
    --bg-page: #ffffff;
    --border-dark: #6b4423;
    --accent-secondary: #c9a227;
    --font-display: 'Cinzel', serif;
    --font-body: 'Scada', sans-serif;
}
```
