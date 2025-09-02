#!/usr/bin/env python3
"""
Simple D&D Character Sheet Generator
Uses built-in libraries to create printable HTML that converts to PDF
"""

import json
import os
from datetime import datetime

def generate_html_sheet(character_data, filename="character_sheet.html"):
    """Generate HTML character sheet that can be printed as PDF"""
    
    html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{character_data['name']} - D&D Character Sheet</title>
    <style>
        @page {{
            size: A4;
            margin: 0.5in;
        }}
        
        body {{
            font-family: Arial, sans-serif;
            font-size: 10pt;
            line-height: 1.2;
            margin: 0;
            padding: 0;
        }}
        
        .character-header {{
            text-align: center;
            border-bottom: 2px solid black;
            margin-bottom: 15px;
            padding-bottom: 10px;
        }}
        
        .character-name {{
            font-size: 18pt;
            font-weight: bold;
            margin-bottom: 5px;
        }}
        
        .basic-info {{
            display: flex;
            justify-content: space-between;
            margin-bottom: 15px;
        }}
        
        .info-box {{
            border: 1px solid black;
            padding: 5px;
            text-align: center;
            min-width: 120px;
        }}
        
        .info-label {{
            font-weight: bold;
            font-size: 8pt;
            margin-bottom: 2px;
        }}
        
        .main-stats {{
            display: flex;
            justify-content: space-between;
            margin-bottom: 20px;
        }}
        
        .abilities-section {{
            width: 30%;
        }}
        
        .ability-score {{
            border: 1px solid black;
            text-align: center;
            margin-bottom: 8px;
            padding: 8px;
        }}
        
        .ability-name {{
            font-weight: bold;
            font-size: 9pt;
        }}
        
        .ability-value {{
            font-size: 14pt;
            font-weight: bold;
            margin: 5px 0;
        }}
        
        .ability-modifier {{
            font-size: 12pt;
            border: 1px solid black;
            padding: 2px 8px;
            margin: 2px 0;
        }}
        
        .combat-stats {{
            width: 65%;
        }}
        
        .combat-row {{
            display: flex;
            justify-content: space-between;
            margin-bottom: 10px;
        }}
        
        .combat-box {{
            border: 1px solid black;
            padding: 8px;
            text-align: center;
            flex: 1;
            margin: 0 2px;
        }}
        
        .skills-section {{
            border: 1px solid black;
            padding: 10px;
            margin-bottom: 15px;
        }}
        
        .section-title {{
            font-weight: bold;
            font-size: 12pt;
            margin-bottom: 8px;
            text-transform: uppercase;
        }}
        
        .skills-grid {{
            display: grid;
            grid-template-columns: 1fr 1fr 1fr;
            gap: 5px;
        }}
        
        .skill-item {{
            font-size: 9pt;
        }}
        
        .prof-circle {{
            width: 12px;
            height: 12px;
            border: 1px solid black;
            border-radius: 50%;
            display: inline-block;
            text-align: center;
            line-height: 10px;
            margin-right: 5px;
        }}
        
        .prof-circle.filled {{
            background-color: black;
            color: white;
        }}
        
        .attacks-section {{
            border: 1px solid black;
            padding: 10px;
            margin-bottom: 15px;
        }}
        
        .attacks-table {{
            width: 100%;
            border-collapse: collapse;
        }}
        
        .attacks-table th,
        .attacks-table td {{
            border: 1px solid black;
            padding: 5px;
            text-align: center;
        }}
        
        .attacks-table th {{
            background-color: #f0f0f0;
            font-weight: bold;
        }}
        
        .spells-section {{
            border: 1px solid black;
            padding: 10px;
            margin-bottom: 15px;
        }}
        
        .spell-level {{
            margin-bottom: 10px;
        }}
        
        .spell-slots {{
            display: inline-block;
            margin-left: 10px;
        }}
        
        .spell-slot {{
            width: 15px;
            height: 15px;
            border: 1px solid black;
            border-radius: 50%;
            display: inline-block;
            margin-right: 3px;
        }}
        
        .equipment-section {{
            border: 1px solid black;
            padding: 10px;
            margin-bottom: 15px;
        }}
        
        .page-break {{
            page-break-before: always;
        }}
        
        @media print {{
            .no-print {{ display: none; }}
        }}
    </style>
</head>
<body>
    <!-- PAGE 1: Main Character Sheet -->
    <div class="character-header">
        <div class="character-name">{character_data['name']}</div>
        <div class="basic-info">
            <div class="info-box">
                <div class="info-label">CLASS & LEVEL</div>
                <div>{character_data['class']} {character_data['level']}</div>
            </div>
            <div class="info-box">
                <div class="info-label">BACKGROUND</div>
                <div>{character_data['background']}</div>
            </div>
            <div class="info-box">
                <div class="info-label">RACE</div>
                <div>{character_data['race']}</div>
            </div>
            <div class="info-box">
                <div class="info-label">ALIGNMENT</div>
                <div>{character_data['alignment']}</div>
            </div>
            <div class="info-box">
                <div class="info-label">EXPERIENCE POINTS</div>
                <div>____ / {character_data.get('next_level_xp', '')}</div>
            </div>
        </div>
    </div>
    
    <div class="main-stats">
        <div class="abilities-section">
            {generate_abilities_html(character_data)}
        </div>
        
        <div class="combat-stats">
            <div class="combat-row">
                <div class="combat-box">
                    <div class="info-label">ARMOR CLASS</div>
                    <div style="font-size: 24pt; font-weight: bold;">{character_data.get('ac', '')}</div>
                </div>
                <div class="combat-box">
                    <div class="info-label">INITIATIVE</div>
                    <div style="font-size: 18pt; font-weight: bold;">{format_modifier(character_data['abilities']['dexterity'])}</div>
                </div>
                <div class="combat-box">
                    <div class="info-label">SPEED</div>
                    <div style="font-size: 18pt; font-weight: bold;">{character_data.get('speed', '')} ft</div>
                </div>
            </div>
            
            <div class="combat-row">
                <div class="combat-box" style="flex: 2;">
                    <div class="info-label">HIT POINT MAXIMUM</div>
                    <div style="font-size: 24pt; font-weight: bold;">{character_data.get('hp_max', '')}</div>
                </div>
                <div class="combat-box" style="flex: 2;">
                    <div class="info-label">CURRENT HIT POINTS</div>
                    <div style="font-size: 18pt; height: 30px; border-bottom: 1px solid black; margin: 5px;"></div>
                </div>
            </div>
            
            <div class="combat-row">
                <div class="combat-box">
                    <div class="info-label">TEMPORARY HIT POINTS</div>
                    <div style="height: 25px; border-bottom: 1px solid black; margin: 5px;"></div>
                </div>
                <div class="combat-box">
                    <div class="info-label">HIT DICE</div>
                    <div>{character_data.get('level', 1)}d{character_data.get('hit_die', 6)}</div>
                </div>
                <div class="combat-box">
                    <div class="info-label">DEATH SAVES</div>
                    <div>
                        <div>Successes: ○ ○ ○</div>
                        <div>Failures: ○ ○ ○</div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    
    <div class="skills-section">
        <div class="section-title">Skills</div>
        {generate_skills_html(character_data)}
    </div>
    
    <div class="attacks-section">
        <div class="section-title">Attacks & Spellcasting</div>
        <table class="attacks-table">
            <thead>
                <tr>
                    <th>NAME</th>
                    <th>ATK BONUS</th>
                    <th>DAMAGE/TYPE</th>
                    <th>RANGE</th>
                </tr>
            </thead>
            <tbody>
                {generate_attacks_html(character_data)}
            </tbody>
        </table>
    </div>
    
    <div class="equipment-section">
        <div class="section-title">Equipment</div>
        {generate_equipment_html(character_data)}
    </div>
    
    <!-- PAGE 2: Spells -->
    <div class="page-break">
        <div class="spells-section">
            <div class="section-title">Spellcasting</div>
            {generate_spells_html(character_data)}
        </div>
        
        <div class="equipment-section">
            <div class="section-title">Features & Traits</div>
            {generate_features_html(character_data)}
        </div>
    </div>
    
    <div class="no-print" style="position: fixed; bottom: 10px; right: 10px; background: yellow; padding: 10px; border-radius: 5px;">
        <strong>Print Instructions:</strong><br/>
        1. File → Print (Ctrl/Cmd + P)<br/>
        2. Select "Save as PDF" or print directly<br/>
        3. Make sure margins are set to minimum<br/>
        4. Enable "Print backgrounds" for borders
    </div>
    
    <div style="text-align: center; margin-top: 30px; font-size: 8pt; color: #666;">
        Generated on {datetime.now().strftime('%B %d, %Y at %I:%M %p')} • Ready for Session {character_data.get('session', '_____')}
    </div>
</body>
</html>
"""
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    return filename

def format_modifier(ability_score):
    """Convert ability score to modifier string"""
    modifier = (ability_score - 10) // 2
    return f"+{modifier}" if modifier >= 0 else str(modifier)

def generate_abilities_html(char):
    """Generate HTML for ability scores"""
    abilities = ['strength', 'dexterity', 'constitution', 'intelligence', 'wisdom', 'charisma']
    html = ""
    
    for ability in abilities:
        score = char['abilities'][ability]
        modifier = format_modifier(score)
        is_save_prof = ability in char.get('saving_throw_profs', [])
        save_bonus = (score - 10) // 2 + (char.get('proficiency_bonus', 2) if is_save_prof else 0)
        
        html += f'''
        <div class="ability-score">
            <div class="ability-name">{ability.upper()}</div>
            <div class="ability-value">{score}</div>
            <div class="ability-modifier">{modifier}</div>
            <div style="font-size: 8pt; margin-top: 5px;">
                Save: {'+' if save_bonus >= 0 else ''}{save_bonus}
            </div>
        </div>
        '''
    
    return html

def generate_skills_html(char):
    """Generate HTML for skills"""
    skills_data = [
        ('Acrobatics', 'dexterity'), ('Animal Handling', 'wisdom'), ('Arcana', 'intelligence'),
        ('Athletics', 'strength'), ('Deception', 'charisma'), ('History', 'intelligence'),
        ('Insight', 'wisdom'), ('Intimidation', 'charisma'), ('Investigation', 'intelligence'),
        ('Medicine', 'wisdom'), ('Nature', 'intelligence'), ('Perception', 'wisdom'),
        ('Performance', 'charisma'), ('Persuasion', 'charisma'), ('Religion', 'intelligence'),
        ('Sleight of Hand', 'dexterity'), ('Stealth', 'dexterity'), ('Survival', 'wisdom')
    ]
    
    html = '<div class="skills-grid">'
    
    for skill, ability in skills_data:
        is_proficient = skill.lower() in [s.lower() for s in char.get('skills', [])]
        ability_mod = (char['abilities'][ability] - 10) // 2
        prof_bonus = char.get('proficiency_bonus', 2) if is_proficient else 0
        total = ability_mod + prof_bonus
        
        circle_class = "filled" if is_proficient else ""
        circle_content = "●" if is_proficient else "○"
        
        html += f'''
        <div class="skill-item">
            <span class="prof-circle {circle_class}">{circle_content}</span>
            {total:+d} {skill}
        </div>
        '''
    
    html += '</div>'
    return html

def generate_attacks_html(char):
    """Generate HTML for attacks table"""
    attacks = char.get('attacks', [])
    html = ""
    
    for attack in attacks:
        html += f'''
        <tr>
            <td>{attack['name']}</td>
            <td>{attack['attack_bonus']}</td>
            <td>{attack['damage']}</td>
            <td>{attack.get('range', '')}</td>
        </tr>
        '''
    
    # Fill empty rows
    for i in range(max(0, 5 - len(attacks))):
        html += '<tr><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td></tr>'
    
    return html

def generate_equipment_html(char):
    """Generate HTML for equipment"""
    equipment = char.get('equipment', [])
    currency = char.get('currency', {})
    
    html = '<div style="display: flex; justify-content: space-between;">'
    html += '<div style="width: 70%;">'
    html += '<strong>Equipment:</strong><br/>'
    for item in equipment[:12]:  # Limit to prevent overflow
        html += f'• {item}<br/>'
    html += '</div>'
    
    html += '<div style="width: 25%;">'
    html += '<strong>Currency:</strong><br/>'
    for coin_type, amount in currency.items():
        if coin_type != 'special' and amount > 0:
            html += f'{amount} {coin_type}<br/>'
    if currency.get('special'):
        html += f'{currency["special"]}<br/>'
    html += '</div>'
    html += '</div>'
    
    return html

def generate_spells_html(char):
    """Generate HTML for spells"""
    html = f'''
    <div style="display: flex; justify-content: space-between; margin-bottom: 15px;">
        <div><strong>Spellcasting Class:</strong> {char.get('class', '')}</div>
        <div><strong>Spellcasting Ability:</strong> {char.get('spellcasting_ability', 'Charisma')}</div>
        <div><strong>Spell Save DC:</strong> {char.get('spell_save_dc', '')}</div>
        <div><strong>Spell Attack Bonus:</strong> {char.get('spell_attack_bonus', '')}</div>
    </div>
    '''
    
    # Cantrips
    html += '<div class="spell-level">'
    html += '<strong>CANTRIPS (0 Level)</strong><br/>'
    cantrips = char.get('cantrips', [])
    html += ' • '.join(cantrips) if cantrips else '○ ○ ○ ○'
    html += '</div>'
    
    # Spell levels
    spell_slots = char.get('spell_slots', {})
    spells = char.get('spells', {})
    
    for level in sorted(spell_slots.keys()):
        if spell_slots[level] > 0:
            html += f'<div class="spell-level">'
            html += f'<strong>{level.upper()} LEVEL SPELLS</strong>'
            html += f'<span class="spell-slots">Slots: '
            for i in range(spell_slots[level]):
                html += '<span class="spell-slot">○</span>'
            html += '</span><br/>'
            
            level_spells = spells.get(level, [])
            if level_spells:
                html += ' • '.join(level_spells)
            else:
                html += '○ ○ ○ ○'
            html += '</div>'
    
    # Sorcery Points
    if char.get('class') == 'Sorcerer':
        html += f'<div style="margin-top: 15px;"><strong>Sorcery Points:</strong> {char.get("sorcery_points", 0)}</div>'
    
    return html

def generate_features_html(char):
    """Generate HTML for features and traits"""
    html = ""
    
    # Racial features
    racial_features = char.get('racial_features', [])
    if racial_features:
        html += '<div style="margin-bottom: 15px;"><strong>Racial Features:</strong><br/>'
        for feature in racial_features:
            html += f'<strong>{feature["name"]}:</strong> {feature["description"]}<br/>'
        html += '</div>'
    
    # Class features
    class_features = char.get('class_features', [])
    if class_features:
        html += '<div style="margin-bottom: 15px;"><strong>Class Features:</strong><br/>'
        for feature in class_features:
            html += f'<strong>{feature["name"]}:</strong> {feature["description"]}<br/>'
        html += '</div>'
    
    # Background
    html += f'<div style="margin-bottom: 15px;"><strong>Background:</strong> {char.get("background", "")}<br/>'
    html += f'<strong>Languages:</strong> {", ".join(char.get("languages", []))}<br/>'
    html += f'<strong>Tool Proficiencies:</strong> {", ".join(char.get("tool_proficiencies", []))}</div>'
    
    return html

def load_kazrek_data():
    """Load Kazrek's character data"""
    return {
        "name": "Kazrek Spellforge",
        "class": "Sorcerer",
        "level": 2,
        "background": "Hermit",
        "race": "Mountain Dwarf",
        "alignment": "Chaotic Good",
        "next_level_xp": "900",
        "abilities": {
            "strength": 12,
            "dexterity": 12,
            "constitution": 18,
            "intelligence": 13,
            "wisdom": 10,
            "charisma": 15
        },
        "saving_throw_profs": ["constitution", "charisma"],
        "proficiency_bonus": 2,
        "ac": 11,
        "hp_max": 20,
        "speed": 25,
        "hit_die": 6,
        "skills": ["Arcana", "Persuasion", "Medicine"],
        "languages": ["Common", "Dwarvish", "Draconic"],
        "tool_proficiencies": ["Herbalism Kit", "Smith's Tools"],
        "attacks": [
            {
                "name": "Dagger",
                "attack_bonus": "+3",
                "damage": "1d4+1 piercing",
                "range": "Thrown 20/60"
            },
            {
                "name": "Light Crossbow",
                "attack_bonus": "+3",
                "damage": "1d8+1 piercing",
                "range": "80/320"
            }
        ],
        "equipment": [
            "Explorer's Pack", "2 Daggers", "Light Crossbow with 20 bolts",
            "Arcane Focus (Crystal)", "Scroll case with notes", "Winter blanket",
            "Common clothes", "Herbalism Kit", "1 lb white mushrooms",
            "½ lb snake meat"
        ],
        "currency": {
            "cp": 1,
            "sp": 1,
            "gp": 16,
            "special": "1 commemorative platinum coin"
        },
        "spellcasting_ability": "Charisma",
        "spell_save_dc": 12,
        "spell_attack_bonus": "+4",
        "sorcery_points": 2,
        "cantrips": ["Light", "Prestidigitation", "Ray of Frost", "Shocking Grasp"],
        "spell_slots": {
            "1st": 3
        },
        "spells": {
            "1st": ["Burning Hands", "Magic Missile", "Shield"]
        },
        "racial_features": [
            {
                "name": "Darkvision",
                "description": "60 feet"
            },
            {
                "name": "Dwarven Resilience",
                "description": "Advantage on saves vs poison, resistance to poison damage"
            },
            {
                "name": "Stonecunning",
                "description": "Double proficiency on History checks about stonework"
            }
        ],
        "class_features": [
            {
                "name": "Spellcasting",
                "description": "Charisma-based spellcasting"
            },
            {
                "name": "Font of Magic",
                "description": "2 sorcery points, can convert to spell slots"
            }
        ]
    }

if __name__ == "__main__":
    # Generate Kazrek's character sheet
    character_data = load_kazrek_data()
    html_file = generate_html_sheet(character_data, "Kazrek_Official_Sheet.html")
    
    print("✅ Official-style D&D character sheet generated!")
    print(f"📄 File: {html_file}")
    print("🖨️  Open in browser and print to PDF or directly to printer")
    print("💡 Pro tip: In browser, go to File → Print → Save as PDF")