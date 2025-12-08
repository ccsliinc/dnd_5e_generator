#!/usr/bin/env python3
"""
Modern D&D Character Sheet Generator
Creates stunning, modern character sheets with graphics and fixed page layouts
"""

import json
import os
from datetime import datetime

def generate_modern_sheet(character_data, filename="modern_character_sheet.html"):
    """Generate modern, graphics-rich character sheet with fixed pages"""
    
    html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{character_data['name']} - Epic D&D Character Sheet</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@400;600;700&family=Roboto:wght@300;400;500;700&display=swap');
        
        @page {{
            size: A4;
            margin: 0;
        }}
        
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Roboto', sans-serif;
            line-height: 1.3;
            background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
            color: #333;
        }}
        
        .page {{
            width: 210mm;
            height: 297mm;
            background: #ffffff;
            position: relative;
            page-break-after: always;
            overflow: hidden;
            border: 3mm solid transparent;
            background-clip: padding-box;
        }}
        
        .page:last-child {{
            page-break-after: avoid;
        }}
        
        /* Decorative Borders */
        .page::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: 
                linear-gradient(45deg, #d4af37 0%, #ffd700 25%, #d4af37 50%, #b8860b 75%, #d4af37 100%);
            z-index: -2;
        }}
        
        .page::after {{
            content: '';
            position: absolute;
            top: 3mm;
            left: 3mm;
            right: 3mm;
            bottom: 3mm;
            background: #ffffff;
            border-radius: 2mm;
            box-shadow: 
                inset 0 0 20px rgba(212, 175, 55, 0.3),
                0 0 30px rgba(0, 0, 0, 0.1);
            z-index: -1;
        }}
        
        /* Celtic Border Pattern */
        .celtic-border {{
            position: absolute;
            top: 8mm;
            left: 8mm;
            right: 8mm;
            bottom: 8mm;
            border: 2px solid #d4af37;
            border-radius: 3mm;
            background: 
                repeating-linear-gradient(
                    0deg,
                    transparent,
                    transparent 5mm,
                    rgba(212, 175, 55, 0.1) 5mm,
                    rgba(212, 175, 55, 0.1) 5.2mm
                ),
                repeating-linear-gradient(
                    90deg,
                    transparent,
                    transparent 5mm,
                    rgba(212, 175, 55, 0.1) 5mm,
                    rgba(212, 175, 55, 0.1) 5.2mm
                );
        }}
        
        .content-area {{
            position: absolute;
            top: 12mm;
            left: 12mm;
            right: 12mm;
            bottom: 12mm;
            z-index: 1;
        }}
        
        /* Header Styling */
        .character-header {{
            text-align: center;
            margin-bottom: 8mm;
            position: relative;
        }}
        
        .character-name {{
            font-family: 'Cinzel', serif;
            font-size: 28pt;
            font-weight: 700;
            color: #2c3e50;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
            background: linear-gradient(135deg, #d4af37, #ffd700, #d4af37);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin-bottom: 3mm;
        }}
        
        .character-title {{
            font-family: 'Cinzel', serif;
            font-size: 14pt;
            color: #34495e;
            font-weight: 400;
            letter-spacing: 2px;
            text-transform: uppercase;
        }}
        
        /* Decorative Divider */
        .divider {{
            height: 2px;
            background: linear-gradient(90deg, transparent, #d4af37, transparent);
            margin: 5mm 0;
            position: relative;
        }}
        
        .divider::before {{
            content: '⚔️';
            position: absolute;
            left: 50%;
            top: -8px;
            transform: translateX(-50%);
            background: white;
            padding: 0 5px;
            font-size: 16px;
        }}
        
        /* Info Boxes */
        .info-grid {{
            display: grid;
            grid-template-columns: repeat(5, 1fr);
            gap: 2mm;
            margin-bottom: 6mm;
        }}
        
        .info-box {{
            background: linear-gradient(135deg, #f8f9fa, #e9ecef);
            border: 1px solid #d4af37;
            border-radius: 3mm;
            padding: 3mm;
            text-align: center;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            position: relative;
            overflow: hidden;
        }}
        
        .info-box::before {{
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(212, 175, 55, 0.2), transparent);
            animation: shimmer 3s infinite;
        }}
        
        @keyframes shimmer {{
            0% {{ left: -100%; }}
            100% {{ left: 100%; }}
        }}
        
        .info-label {{
            font-weight: 700;
            font-size: 7pt;
            color: #2c3e50;
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-bottom: 1mm;
        }}
        
        .info-value {{
            font-size: 10pt;
            color: #34495e;
            font-weight: 500;
        }}
        
        /* Ability Scores - Hexagonal Design */
        .abilities-container {{
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 4mm;
            margin-bottom: 8mm;
        }}
        
        .ability-hex {{
            position: relative;
            width: 25mm;
            height: 25mm;
            margin: 0 auto;
        }}
        
        .ability-hex::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: linear-gradient(135deg, #d4af37, #ffd700);
            clip-path: polygon(50% 0%, 100% 25%, 100% 75%, 50% 100%, 0% 75%, 0% 25%);
            z-index: 1;
        }}
        
        .ability-content {{
            position: absolute;
            top: 1px;
            left: 1px;
            right: 1px;
            bottom: 1px;
            background: linear-gradient(135deg, #f8f9fa, #ffffff);
            clip-path: polygon(50% 0%, 100% 25%, 100% 75%, 50% 100%, 0% 75%, 0% 25%);
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            z-index: 2;
        }}
        
        .ability-name {{
            font-size: 6pt;
            font-weight: 700;
            color: #2c3e50;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}
        
        .ability-score {{
            font-size: 14pt;
            font-weight: 700;
            color: #d4af37;
            margin: 1mm 0;
        }}
        
        .ability-modifier {{
            font-size: 8pt;
            font-weight: 600;
            color: #34495e;
            background: #ecf0f1;
            padding: 1mm 2mm;
            border-radius: 2mm;
        }}
        
        /* Combat Stats */
        .combat-grid {{
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 3mm;
            margin-bottom: 8mm;
        }}
        
        .combat-stat {{
            background: linear-gradient(135deg, #e74c3c, #c0392b);
            color: white;
            border-radius: 5mm;
            padding: 4mm;
            text-align: center;
            box-shadow: 0 4px 8px rgba(0,0,0,0.2);
            position: relative;
            overflow: hidden;
        }}
        
        .combat-stat::before {{
            content: '';
            position: absolute;
            top: -50%;
            left: -50%;
            width: 200%;
            height: 200%;
            background: radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%);
            animation: pulse 2s ease-in-out infinite;
        }}
        
        @keyframes pulse {{
            0%, 100% {{ opacity: 0.3; }}
            50% {{ opacity: 0.7; }}
        }}
        
        .combat-label {{
            font-size: 7pt;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-bottom: 2mm;
        }}
        
        .combat-value {{
            font-size: 20pt;
            font-weight: 700;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }}
        
        /* Skills Section */
        .skills-section {{
            background: linear-gradient(135deg, #3498db, #2980b9);
            border-radius: 5mm;
            padding: 4mm;
            margin-bottom: 6mm;
            color: white;
            box-shadow: 0 4px 8px rgba(0,0,0,0.2);
        }}
        
        .section-title {{
            font-family: 'Cinzel', serif;
            font-size: 14pt;
            font-weight: 600;
            text-align: center;
            margin-bottom: 3mm;
            text-shadow: 1px 1px 2px rgba(0,0,0,0.3);
        }}
        
        .skills-grid {{
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 2mm;
        }}
        
        .skill-item {{
            background: rgba(255, 255, 255, 0.1);
            border-radius: 2mm;
            padding: 2mm;
            font-size: 8pt;
            display: flex;
            align-items: center;
        }}
        
        .prof-circle {{
            width: 4mm;
            height: 4mm;
            border: 1px solid white;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            margin-right: 2mm;
            font-size: 6pt;
            font-weight: 700;
        }}
        
        .prof-circle.filled {{
            background-color: #ffd700;
            color: #2c3e50;
            border-color: #ffd700;
        }}
        
        /* Spells Section */
        .spells-section {{
            background: linear-gradient(135deg, #9b59b6, #8e44ad);
            border-radius: 5mm;
            padding: 4mm;
            color: white;
            box-shadow: 0 4px 8px rgba(0,0,0,0.2);
            margin-bottom: 6mm;
        }}
        
        .spell-level-block {{
            background: rgba(255, 255, 255, 0.1);
            border-radius: 3mm;
            padding: 3mm;
            margin-bottom: 3mm;
        }}
        
        .spell-level-title {{
            font-weight: 700;
            font-size: 10pt;
            margin-bottom: 2mm;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}
        
        .spell-slots-track {{
            display: flex;
            gap: 1mm;
        }}
        
        .spell-slot {{
            width: 6mm;
            height: 6mm;
            border: 2px solid white;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: 700;
            font-size: 8pt;
        }}
        
        .spell-list {{
            font-size: 9pt;
            line-height: 1.4;
        }}
        
        /* Session Notes */
        .notes-section {{
            background: linear-gradient(135deg, #f39c12, #e67e22);
            border-radius: 5mm;
            padding: 4mm;
            color: white;
            box-shadow: 0 4px 8px rgba(0,0,0,0.2);
            height: 40mm;
        }}
        
        .notes-title {{
            font-family: 'Cinzel', serif;
            font-size: 12pt;
            font-weight: 600;
            text-align: center;
            margin-bottom: 3mm;
            text-shadow: 1px 1px 2px rgba(0,0,0,0.3);
        }}
        
        .notes-lines {{
            height: calc(100% - 8mm);
            background-image: 
                repeating-linear-gradient(
                    transparent,
                    transparent 4mm,
                    rgba(255, 255, 255, 0.3) 4mm,
                    rgba(255, 255, 255, 0.3) 4.2mm
                );
            border-radius: 2mm;
            padding: 2mm;
        }}
        
        /* Equipment Section */
        .equipment-section {{
            background: linear-gradient(135deg, #27ae60, #229954);
            border-radius: 5mm;
            padding: 4mm;
            color: white;
            box-shadow: 0 4px 8px rgba(0,0,0,0.2);
        }}
        
        .equipment-grid {{
            display: grid;
            grid-template-columns: 2fr 1fr;
            gap: 3mm;
        }}
        
        .equipment-list {{
            background: rgba(255, 255, 255, 0.1);
            border-radius: 3mm;
            padding: 3mm;
            font-size: 8pt;
            line-height: 1.4;
        }}
        
        .currency-box {{
            background: rgba(255, 255, 255, 0.1);
            border-radius: 3mm;
            padding: 3mm;
            text-align: center;
        }}
        
        .coin-stack {{
            display: flex;
            flex-direction: column;
            gap: 1mm;
        }}
        
        .coin-item {{
            background: rgba(255, 215, 0, 0.2);
            border: 1px solid #ffd700;
            border-radius: 2mm;
            padding: 1mm;
            font-size: 8pt;
            font-weight: 600;
        }}
        
        /* Attacks Table */
        .attacks-section {{
            background: linear-gradient(135deg, #e67e22, #d68910);
            border-radius: 5mm;
            padding: 4mm;
            color: white;
            box-shadow: 0 4px 8px rgba(0,0,0,0.2);
            margin-bottom: 6mm;
        }}
        
        .attacks-table {{
            width: 100%;
            border-collapse: collapse;
            background: rgba(255, 255, 255, 0.1);
            border-radius: 3mm;
            overflow: hidden;
        }}
        
        .attacks-table th,
        .attacks-table td {{
            padding: 2mm;
            text-align: center;
            border-bottom: 1px solid rgba(255, 255, 255, 0.2);
            font-size: 8pt;
        }}
        
        .attacks-table th {{
            background: rgba(0, 0, 0, 0.2);
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 1px;
        }}
        
        /* Features Section */
        .features-section {{
            background: linear-gradient(135deg, #34495e, #2c3e50);
            border-radius: 5mm;
            padding: 4mm;
            color: white;
            box-shadow: 0 4px 8px rgba(0,0,0,0.2);
        }}
        
        .feature-item {{
            background: rgba(255, 255, 255, 0.1);
            border-radius: 3mm;
            padding: 2mm;
            margin-bottom: 2mm;
            font-size: 8pt;
            line-height: 1.4;
        }}
        
        .feature-name {{
            font-weight: 700;
            color: #ffd700;
            margin-bottom: 1mm;
        }}
        
        /* Print Optimizations */
        @media print {{
            body {{ 
                background: none;
                -webkit-print-color-adjust: exact;
                color-adjust: exact;
            }}
            .page {{ box-shadow: none; }}
            .no-print {{ display: none; }}
        }}
    </style>
</head>
<body>
    <!-- PAGE 1: Character Overview & Core Stats -->
    <div class="page">
        <div class="celtic-border"></div>
        <div class="content-area">
            <div class="character-header">
                <div class="character-name">{character_data['name']}</div>
                <div class="character-title">{character_data['class']} • {character_data['race']} • {character_data['background']}</div>
                <div class="divider"></div>
            </div>
            
            <div class="info-grid">
                <div class="info-box">
                    <div class="info-label">Class & Level</div>
                    <div class="info-value">{character_data['class']} {character_data['level']}</div>
                </div>
                <div class="info-box">
                    <div class="info-label">Background</div>
                    <div class="info-value">{character_data['background']}</div>
                </div>
                <div class="info-box">
                    <div class="info-label">Race</div>
                    <div class="info-value">{character_data['race']}</div>
                </div>
                <div class="info-box">
                    <div class="info-label">Alignment</div>
                    <div class="info-value">{character_data['alignment']}</div>
                </div>
                <div class="info-box">
                    <div class="info-label">Experience</div>
                    <div class="info-value">____ / {character_data.get('next_level_xp', '')}</div>
                </div>
            </div>
            
            <div class="abilities-container">
                {generate_ability_hexagons(character_data)}
            </div>
            
            <div class="combat-grid">
                <div class="combat-stat">
                    <div class="combat-label">Armor Class</div>
                    <div class="combat-value">{character_data.get('ac', '')}</div>
                </div>
                <div class="combat-stat">
                    <div class="combat-label">Initiative</div>
                    <div class="combat-value">{format_modifier(character_data['abilities']['dexterity'])}</div>
                </div>
                <div class="combat-stat">
                    <div class="combat-label">Speed</div>
                    <div class="combat-value">{character_data.get('speed', '')} ft</div>
                </div>
            </div>
            
            <div class="combat-grid">
                <div class="combat-stat">
                    <div class="combat-label">Hit Point Max</div>
                    <div class="combat-value">{character_data.get('hp_max', '')}</div>
                </div>
                <div class="combat-stat">
                    <div class="combat-label">Current HP</div>
                    <div class="combat-value" style="background: linear-gradient(135deg, #2ecc71, #27ae60);">____</div>
                </div>
                <div class="combat-stat">
                    <div class="combat-label">Temp HP</div>
                    <div class="combat-value" style="background: linear-gradient(135deg, #f39c12, #e67e22);">____</div>
                </div>
            </div>
            
            <div class="skills-section">
                <div class="section-title">⚔️ Skills & Proficiencies ⚔️</div>
                {generate_modern_skills(character_data)}
            </div>
            
            <div class="notes-section">
                <div class="notes-title">📝 This Session's Notes</div>
                <div class="notes-lines"></div>
            </div>
        </div>
    </div>
    
    <!-- PAGE 2: Combat & Spells -->
    <div class="page">
        <div class="celtic-border"></div>
        <div class="content-area">
            <div class="character-header">
                <div class="character-name" style="font-size: 20pt;">{character_data['name']}</div>
                <div class="character-title">Combat & Magic Arsenal</div>
                <div class="divider"></div>
            </div>
            
            <div class="attacks-section">
                <div class="section-title">⚔️ Attacks & Weapons ⚔️</div>
                <table class="attacks-table">
                    <thead>
                        <tr>
                            <th>Weapon</th>
                            <th>Attack Bonus</th>
                            <th>Damage</th>
                            <th>Range</th>
                        </tr>
                    </thead>
                    <tbody>
                        {generate_modern_attacks(character_data)}
                    </tbody>
                </table>
            </div>
            
            <div class="spells-section">
                <div class="section-title">✨ Spellcasting Magic ✨</div>
                {generate_modern_spells(character_data)}
            </div>
            
            <div class="equipment-section">
                <div class="section-title">🎒 Equipment & Treasure 🎒</div>
                {generate_modern_equipment(character_data)}
            </div>
            
            <div class="notes-section">
                <div class="notes-title">💰 Loot & Rewards This Session</div>
                <div class="notes-lines"></div>
            </div>
        </div>
    </div>
    
    <!-- PAGE 3: Features & Character Details -->
    <div class="page">
        <div class="celtic-border"></div>
        <div class="content-area">
            <div class="character-header">
                <div class="character-name" style="font-size: 20pt;">{character_data['name']}</div>
                <div class="character-title">Features, Traits & Background</div>
                <div class="divider"></div>
            </div>
            
            <div class="features-section">
                <div class="section-title">🌟 Racial & Class Features 🌟</div>
                {generate_modern_features(character_data)}
            </div>
            
            <div class="notes-section" style="height: 30mm; margin-bottom: 6mm;">
                <div class="notes-title">🎭 Roleplay Notes & Character Development</div>
                <div class="notes-lines"></div>
            </div>
            
            <div class="notes-section" style="height: 30mm; margin-bottom: 6mm;">
                <div class="notes-title">🗺️ Campaign Notes & Plot Threads</div>
                <div class="notes-lines"></div>
            </div>
            
            <div class="notes-section" style="height: 25mm;">
                <div class="notes-title">🎯 Goals & Objectives</div>
                <div class="notes-lines"></div>
            </div>
            
            <div style="text-align: center; margin-top: 8mm; font-size: 8pt; color: #666;">
                <span style="font-family: 'Cinzel', serif; font-weight: 600;">Generated on {datetime.now().strftime('%B %d, %Y')}</span><br/>
                <span>Session Ready • Print-Optimized • Epic Adventures Await! 🐉</span>
            </div>
        </div>
    </div>
    
    <div class="no-print" style="position: fixed; top: 20px; right: 20px; background: rgba(0,0,0,0.8); color: white; padding: 15px; border-radius: 10px; z-index: 1000;">
        <strong>🖨️ Print Instructions:</strong><br/>
        1. File → Print (Ctrl/Cmd + P)<br/>
        2. Select "More settings"<br/>
        3. Check "Background graphics"<br/>
        4. Set margins to "Minimum"<br/>
        5. Print or Save as PDF<br/>
        <br/>
        <strong>✨ Features:</strong><br/>
        • 3 Fixed pages, no orphaned headers<br/>
        • Session note areas on each page<br/>
        • Modern graphics & animations<br/>
        • Print-optimized colors<br/>
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

def generate_ability_hexagons(char):
    """Generate hexagonal ability score displays"""
    abilities = [
        ('strength', 'STR'), ('dexterity', 'DEX'), ('constitution', 'CON'),
        ('intelligence', 'INT'), ('wisdom', 'WIS'), ('charisma', 'CHA')
    ]
    
    html = ""
    for ability, short_name in abilities:
        score = char['abilities'][ability]
        modifier = format_modifier(score)
        
        html += f'''
        <div class="ability-hex">
            <div class="ability-content">
                <div class="ability-name">{short_name}</div>
                <div class="ability-score">{score}</div>
                <div class="ability-modifier">{modifier}</div>
            </div>
        </div>
        '''
    
    return html

def generate_modern_skills(char):
    """Generate modern skills display"""
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
            <div class="prof-circle {circle_class}">{circle_content}</div>
            <strong>{total:+d}</strong> {skill}
        </div>
        '''
    
    html += '</div>'
    return html

def generate_modern_attacks(char):
    """Generate modern attacks table"""
    attacks = char.get('attacks', [])
    html = ""
    
    for attack in attacks:
        html += f'''
        <tr>
            <td><strong>{attack['name']}</strong></td>
            <td>{attack['attack_bonus']}</td>
            <td>{attack['damage']}</td>
            <td>{attack.get('range', '')}</td>
        </tr>
        '''
    
    # Fill empty rows
    for i in range(max(0, 4 - len(attacks))):
        html += '<tr><td>____________________</td><td>____</td><td>____________________</td><td>________</td></tr>'
    
    return html

def generate_modern_spells(char):
    """Generate modern spells display"""
    html = f'''
    <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 3mm; margin-bottom: 4mm; text-align: center;">
        <div><strong>Class:</strong> {char.get('class', '')}</div>
        <div><strong>Ability:</strong> {char.get('spellcasting_ability', 'Charisma')}</div>
        <div><strong>Save DC:</strong> {char.get('spell_save_dc', '')}</div>
        <div><strong>Attack:</strong> {char.get('spell_attack_bonus', '')}</div>
    </div>
    '''
    
    # Cantrips
    html += '''
    <div class="spell-level-block">
        <div class="spell-level-title">
            <span>✨ CANTRIPS (0 Level) ✨</span>
        </div>
        <div class="spell-list">
    '''
    cantrips = char.get('cantrips', [])
    html += ' • '.join(cantrips) if cantrips else '○ ○ ○ ○'
    html += '</div></div>'
    
    # Spell levels
    spell_slots = char.get('spell_slots', {})
    spells = char.get('spells', {})
    
    level_icons = {'1st': '🔥', '2nd': '❄️', '3rd': '⚡', '4th': '🌪️', '5th': '💫'}
    
    for level in sorted(spell_slots.keys()):
        if spell_slots[level] > 0:
            icon = level_icons.get(level, '✨')
            html += f'''
            <div class="spell-level-block">
                <div class="spell-level-title">
                    <span>{icon} {level.upper()} LEVEL SPELLS {icon}</span>
                    <div class="spell-slots-track">
            '''
            
            for i in range(spell_slots[level]):
                html += '<div class="spell-slot">○</div>'
            html += '</div></div><div class="spell-list">'
            
            level_spells = spells.get(level, [])
            if level_spells:
                html += ' • '.join(level_spells)
            else:
                html += '____________________     ____________________     ____________________'
            html += '</div></div>'
    
    # Sorcery Points
    if char.get('class') == 'Sorcerer':
        html += f'''
        <div class="spell-level-block">
            <div class="spell-level-title">
                <span>🔮 SORCERY POINTS 🔮</span>
                <div style="font-size: 14pt; font-weight: 700;">{char.get('sorcery_points', 0)} Points</div>
            </div>
        </div>
        '''
        
        if char.get('level', 1) >= 3 and char.get('metamagic'):
            html += f'''
            <div class="spell-level-block">
                <div class="spell-level-title">
                    <span>🌟 METAMAGIC 🌟</span>
                </div>
                <div class="spell-list">
                    {' • '.join(char.get('metamagic', []))}
                </div>
            </div>
            '''
    
    return html

def generate_modern_equipment(char):
    """Generate modern equipment display"""
    equipment = char.get('equipment', [])
    currency = char.get('currency', {})
    
    html = '<div class="equipment-grid">'
    html += '<div class="equipment-list">'
    
    # Split equipment into categories
    armor_weapons = [item for item in equipment if any(word in item.lower() for word in ['armor', 'shield', 'sword', 'crossbow', 'dagger', 'axe'])]
    gear_supplies = [item for item in equipment if item not in armor_weapons]
    
    if armor_weapons:
        html += '<div style="margin-bottom: 3mm;"><strong>⚔️ Weapons & Armor:</strong><br/>'
        for item in armor_weapons[:6]:  # Limit to prevent overflow
            html += f'• {item}<br/>'
        html += '</div>'
    
    if gear_supplies:
        html += '<div><strong>🎒 Gear & Supplies:</strong><br/>'
        for item in gear_supplies[:8]:  # Limit to prevent overflow
            html += f'• {item}<br/>'
        html += '</div>'
    
    html += '</div>'
    
    # Currency
    html += '<div class="currency-box">'
    html += '<div style="font-weight: 700; margin-bottom: 2mm; font-size: 10pt;">💰 CURRENCY 💰</div>'
    html += '<div class="coin-stack">'
    
    coin_symbols = {'cp': '🥉', 'sp': '🥈', 'gp': '🥇', 'pp': '💎'}
    for coin_type, amount in currency.items():
        if coin_type != 'special' and amount > 0:
            symbol = coin_symbols.get(coin_type, '💰')
            html += f'<div class="coin-item">{symbol} {amount} {coin_type.upper()}</div>'
    
    if currency.get('special'):
        html += f'<div class="coin-item">✨ {currency["special"]}</div>'
    
    html += '</div></div></div>'
    
    return html

def generate_modern_features(char):
    """Generate modern features display"""
    html = ""
    
    # Racial features
    racial_features = char.get('racial_features', [])
    if racial_features:
        for feature in racial_features:
            html += f'''
            <div class="feature-item">
                <div class="feature-name">🧬 {feature["name"]} (Racial)</div>
                <div>{feature["description"]}</div>
            </div>
            '''
    
    # Class features
    class_features = char.get('class_features', [])
    if class_features:
        for feature in class_features:
            html += f'''
            <div class="feature-item">
                <div class="feature-name">⚡ {feature["name"]} (Class)</div>
                <div>{feature["description"]}</div>
            </div>
            '''
    
    # Background & Languages
    html += f'''
    <div class="feature-item">
        <div class="feature-name">📚 Background: {char.get("background", "")}</div>
        <div><strong>Languages:</strong> {", ".join(char.get("languages", []))}</div>
        <div><strong>Tool Proficiencies:</strong> {", ".join(char.get("tool_proficiencies", []))}</div>
    </div>
    '''
    
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
                "description": "60 feet darkvision in dim light"
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
                "description": "Charisma-based spellcasting with known spells"
            },
            {
                "name": "Font of Magic",
                "description": "2 sorcery points, can convert to spell slots or use for metamagic"
            }
        ]
    }

if __name__ == "__main__":
    # Generate Kazrek's epic character sheet
    character_data = load_kazrek_data()
    html_file = generate_modern_sheet(character_data, "Kazrek_Epic_Sheet.html")
    
    print("🎨 ✅ EPIC CHARACTER SHEET GENERATED!")
    print(f"📄 File: {html_file}")
    print("🖨️  Open in browser and print (enable background graphics)")
    print("✨ Features:")
    print("   • 3 fixed pages with no orphaned headers")
    print("   • Session note areas on every page")
    print("   • Modern graphics with gold borders")
    print("   • Hexagonal ability scores")
    print("   • Animated elements (shimmer effects)")
    print("   • Color-coded sections")
    print("   • Celtic border patterns")
    print("   • Professional typography")
    print("🐉 Ready for epic adventures!")