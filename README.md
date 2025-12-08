# D&D 5e Character Sheet Generator

Generate printable HTML character sheets from JSON data files.

## Usage

```bash
python3 generate.py <character>.json
```

Example:
```bash
python3 generate.py thorek.json
```

This creates `<Character_Name>.html` which you can open in a browser and print.

## Print Settings

1. Open the HTML file in your browser
2. File → Print (Ctrl/Cmd + P)
3. Enable **Background graphics**
4. Set margins to **Minimum**
5. Print all 3 pages

## JSON Structure

See `thorek.json` for a complete example. Key sections:

- `meta.portrait` - Path to character image
- `header` - Name, class, race, etc.
- `abilities` - Ability scores
- `skills` - Skill proficiencies
- `attacks` - Weapon attacks
- `spellcasting` - Spells and slots
- `backstory` - Character background (use `\n\n` for paragraphs)

## Customizing Styles

Edit `styles/sheet.css`. Key variables at the top:

```css
:root {
    --bg-page: #faf8f5;
    --border-dark: #6b4423;
    --accent-secondary: #c9a227;
    --box-radius: 0;
}
```
