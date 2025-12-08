#!/usr/bin/env python3
"""
Modern D&D Character Sheet Generator v2
Print-friendly design with subtle graphics and no solid color blocks
"""

import json
import os
from datetime import datetime

def generate_modern_sheet_v2(character_data, filename="modern_character_sheet_v2.html"):
    """Generate print-friendly modern character sheet with subtle graphics"""
    
    html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{character_data['name']} - D&D Character Sheet v2</title>
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
            background: #ffffff;
            color: #333;
        }}
        
        .page {{
            width: 210mm;
            height: 297mm;
            background: #ffffff;
            position: relative;
            page-break-after: always;
            overflow: hidden;
            padding: 8mm;
        }}
        
        .page:last-child {{
            page-break-after: avoid;
        }}
        
        /* Decorative Corner Graphics */
        .page::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 30mm;
            height: 30mm;
            background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><path d="M0,0 Q25,0 50,25 Q75,50 100,0 L100,100 Q75,75 50,50 Q25,25 0,100 Z" fill="%23d4af37" opacity="0.1"/></svg>');
            background-size: contain;
        }}
        
        .page::after {{
            content: '';
            position: absolute;
            top: 0;
            right: 0;
            width: 30mm;
            height: 30mm;
            background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><path d="M100,0 Q75,0 50,25 Q25,50 0,0 L0,100 Q25,75 50,50 Q75,25 100,100 Z" fill="%23d4af37" opacity="0.1"/></svg>');
            background-size: contain;
        }}
        
        /* Ornate Border */
        .ornate-border {{
            position: absolute;
            top: 6mm;
            left: 6mm;
            right: 6mm;
            bottom: 6mm;
            border: 2px solid #d4af37;
            border-radius: 3mm;
            background: 
                repeating-linear-gradient(
                    0deg,
                    transparent,
                    transparent 10mm,
                    rgba(212, 175, 55, 0.05) 10mm,
                    rgba(212, 175, 55, 0.05) 10.5mm
                ),
                repeating-linear-gradient(
                    90deg,
                    transparent,
                    transparent 10mm,
                    rgba(212, 175, 55, 0.05) 10mm,
                    rgba(212, 175, 55, 0.05) 10.5mm
                );
        }}
        
        .content-area {{
            position: relative;
            z-index: 1;
            padding: 4mm;
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
            text-shadow: 1px 1px 2px rgba(212, 175, 55, 0.3);
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
            height: 1px;
            background: linear-gradient(90deg, transparent, #d4af37, transparent);
            margin: 5mm 0;
            position: relative;
        }}
        
        .divider::before {{
            content: '⚔';
            position: absolute;
            left: 50%;
            top: -8px;
            transform: translateX(-50%);
            background: white;
            padding: 0 5px;
            font-size: 16px;
            color: #d4af37;
        }}
        
        /* Print-Friendly Info Boxes */
        .info-grid {{
            display: grid;
            grid-template-columns: repeat(5, 1fr);
            gap: 2mm;
            margin-bottom: 6mm;
        }}
        
        .info-box {{
            background: transparent;
            border: 2px solid #d4af37;
            border-radius: 3mm;
            padding: 3mm;
            text-align: center;
            position: relative;
        }}
        
        .info-box::before {{
            content: '';
            position: absolute;
            top: -1px;
            left: -1px;
            right: -1px;
            bottom: -1px;
            border: 1px solid rgba(212, 175, 55, 0.3);
            border-radius: 3mm;
            z-index: -1;
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
        
        /* Hexagonal Ability Scores - Outline Only */
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
            border: 2px solid #d4af37;
            clip-path: polygon(50% 0%, 100% 25%, 100% 75%, 50% 100%, 0% 75%, 0% 25%);
            z-index: 1;
        }}
        
        .ability-hex::after {{
            content: '';
            position: absolute;
            top: 1px;
            left: 1px;
            right: 1px;
            bottom: 1px;
            background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 50 50"><defs><pattern id="dots" x="0" y="0" width="10" height="10" patternUnits="userSpaceOnUse"><circle cx="5" cy="5" r="0.5" fill="%23d4af37" opacity="0.1"/></pattern></defs><rect width="50" height="50" fill="url(%23dots)"/></svg>');
            clip-path: polygon(50% 0%, 100% 25%, 100% 75%, 50% 100%, 0% 75%, 0% 25%);
            z-index: 1;
        }}
        
        .ability-content {{
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
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
            border: 1px solid #d4af37;
            padding: 1mm 2mm;
            border-radius: 2mm;
            background: rgba(212, 175, 55, 0.05);
        }}
        
        /* Combat Stats - Outline Style */
        .combat-grid {{
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 3mm;
            margin-bottom: 8mm;
        }}
        
        .combat-stat {{
            background: transparent;
            border: 2px solid #e74c3c;
            border-radius: 5mm;
            padding: 4mm;
            text-align: center;
            position: relative;
        }}
        
        .combat-stat::before {{
            content: '';
            position: absolute;
            top: 2px;
            left: 2px;
            right: 2px;
            bottom: 2px;
            border: 1px solid rgba(231, 76, 60, 0.2);
            border-radius: 4mm;
            background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20"><path d="M10,2 L12,8 L18,8 L13,12 L15,18 L10,14 L5,18 L7,12 L2,8 L8,8 Z" fill="%23e74c3c" opacity="0.03"/></svg>');
            background-repeat: repeat;
            background-size: 10mm 10mm;
        }}
        
        .combat-label {{
            font-size: 7pt;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-bottom: 2mm;
            color: #e74c3c;
        }}
        
        .combat-value {{
            font-size: 20pt;
            font-weight: 700;
            color: #2c3e50;
        }}
        
        /* Section Headers */
        .section-container {{
            border: 2px solid #3498db;
            border-radius: 5mm;
            padding: 4mm;
            margin-bottom: 6mm;
            background: rgba(52, 152, 219, 0.02);
            position: relative;
        }}
        
        .section-container::before {{
            content: '';
            position: absolute;
            top: 3px;
            left: 3px;
            right: 3px;
            bottom: 3px;
            border: 1px solid rgba(52, 152, 219, 0.1);
            border-radius: 4mm;
        }}
        
        .section-title {{
            font-family: 'Cinzel', serif;
            font-size: 14pt;
            font-weight: 600;
            text-align: center;
            margin-bottom: 3mm;
            color: #3498db;
            text-shadow: 1px 1px 1px rgba(0,0,0,0.1);
        }}
        
        /* Skills Grid */
        .skills-grid {{
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 2mm;
        }}
        
        .skill-item {{
            background: rgba(255, 255, 255, 0.8);
            border: 1px solid rgba(52, 152, 219, 0.3);
            border-radius: 2mm;
            padding: 2mm;
            font-size: 8pt;
            display: flex;
            align-items: center;
        }}
        
        .prof-circle {{
            width: 4mm;
            height: 4mm;
            border: 1px solid #3498db;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            margin-right: 2mm;
            font-size: 6pt;
            font-weight: 700;
            color: #3498db;
        }}
        
        .prof-circle.filled {{
            background-color: #3498db;
            color: white;
        }}
        
        /* Spells Section */
        .spells-container {{
            border: 2px solid #9b59b6;
            border-radius: 5mm;
            padding: 4mm;
            background: rgba(155, 89, 182, 0.02);
            margin-bottom: 6mm;
            position: relative;
        }}
        
        .spell-level-block {{
            background: rgba(255, 255, 255, 0.5);
            border: 1px solid rgba(155, 89, 182, 0.3);
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
            color: #9b59b6;
        }}
        
        .spell-slots-track {{
            display: flex;
            gap: 1mm;
        }}
        
        .spell-slot {{
            width: 6mm;
            height: 6mm;
            border: 2px solid #9b59b6;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: 700;
            font-size: 8pt;
            color: #9b59b6;
        }}
        
        .spell-list {{
            font-size: 9pt;
            line-height: 1.4;
            color: #34495e;
        }}
        
        /* Session Notes */
        .notes-container {{
            border: 2px solid #f39c12;
            border-radius: 5mm;
            padding: 4mm;
            background: rgba(243, 156, 18, 0.02);
            height: 40mm;
            position: relative;
        }}
        
        .notes-title {{
            font-family: 'Cinzel', serif;
            font-size: 12pt;
            font-weight: 600;
            text-align: center;
            margin-bottom: 3mm;
            color: #f39c12;
        }}
        
        .notes-lines {{
            height: calc(100% - 8mm);
            background-image: 
                repeating-linear-gradient(
                    transparent,
                    transparent 4mm,
                    rgba(243, 156, 18, 0.2) 4mm,
                    rgba(243, 156, 18, 0.2) 4.1mm
                );
            border-radius: 2mm;
            padding: 2mm;
        }}
        
        /* Equipment Section */
        .equipment-container {{
            border: 2px solid #27ae60;
            border-radius: 5mm;
            padding: 4mm;
            background: rgba(39, 174, 96, 0.02);
        }}
        
        .equipment-grid {{
            display: grid;
            grid-template-columns: 2fr 1fr;
            gap: 3mm;
        }}
        
        .equipment-list {{
            background: rgba(255, 255, 255, 0.5);
            border: 1px solid rgba(39, 174, 96, 0.3);
            border-radius: 3mm;
            padding: 3mm;
            font-size: 8pt;
            line-height: 1.4;
        }}
        
        .currency-box {{
            background: rgba(255, 255, 255, 0.5);
            border: 1px solid rgba(39, 174, 96, 0.3);
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
            background: rgba(255, 215, 0, 0.1);
            border: 1px solid #d4af37;
            border-radius: 2mm;
            padding: 1mm;
            font-size: 8pt;
            font-weight: 600;
        }}
        
        /* Attacks Table */
        .attacks-container {{
            border: 2px solid #e67e22;
            border-radius: 5mm;
            padding: 4mm;
            background: rgba(230, 126, 34, 0.02);
            margin-bottom: 6mm;
        }}
        
        .attacks-table {{
            width: 100%;
            border-collapse: collapse;
            background: rgba(255, 255, 255, 0.5);
            border-radius: 3mm;
            overflow: hidden;
        }}
        
        .attacks-table th,
        .attacks-table td {{
            padding: 2mm;
            text-align: center;
            border-bottom: 1px solid rgba(230, 126, 34, 0.2);
            font-size: 8pt;
        }}
        
        .attacks-table th {{
            background: rgba(230, 126, 34, 0.1);
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 1px;
            color: #e67e22;
        }}
        
        /* Features Section */
        .features-container {{
            border: 2px solid #34495e;
            border-radius: 5mm;
            padding: 4mm;
            background: rgba(52, 73, 94, 0.02);
        }}
        
        .feature-item {{
            background: rgba(255, 255, 255, 0.5);
            border: 1px solid rgba(52, 73, 94, 0.2);
            border-radius: 3mm;
            padding: 2mm;
            margin-bottom: 2mm;
            font-size: 8pt;
            line-height: 1.4;
        }}
        
        .feature-name {{
            font-weight: 700;
            color: #d4af37;
            margin-bottom: 1mm;
        }}
        
        /* Character Portrait Area */
        .portrait-container {{
            width: 35mm;
            height: 45mm;
            border: 2px solid #d4af37;
            border-radius: 5mm;
            background: rgba(212, 175, 55, 0.05);
            float: right;
            margin: 0 0 3mm 3mm;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 8pt;
            color: #666;
            text-align: center;
        }}
        
        /* Subtle Background Pattern */
        .page {{
            background-image: 
                radial-gradient(circle at 25% 25%, rgba(212, 175, 55, 0.03) 0%, transparent 50%),
                radial-gradient(circle at 75% 75%, rgba(212, 175, 55, 0.03) 0%, transparent 50%);
        }}
        
        /* Print Optimizations */
        @media print {{
            body {{ 
                background: none;
                -webkit-print-color-adjust: exact;
                color-adjust: exact;
            }}
            .page {{ 
                box-shadow: none;
                background-image: none;
            }}
            .no-print {{ display: none; }}
        }}
    </style>
</head>
<body>
    <!-- PAGE 1: Character Overview & Core Stats -->
    <div class="page">
        <div class="ornate-border"></div>
        <div class="content-area">
            <div class="character-header">
                <div class="character-name">{character_data['name']}</div>
                <div class="character-title">{character_data['class']} • {character_data['race']} • {character_data['background']}</div>
                <div class="divider"></div>
            </div>
            
            <div class="portrait-container">
                <div>Character<br/>Portrait<br/><br/>📸<br/><br/><small>Paste photo or<br/>sketch here</small></div>
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
                {generate_ability_hexagons_v2(character_data)}
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
                    <div class="combat-value">____</div>
                </div>
                <div class="combat-stat">
                    <div class="combat-label">Temp HP</div>
                    <div class="combat-value">____</div>
                </div>
            </div>
            
            <div class="section-container">
                <div class="section-title">⚔️ Skills & Proficiencies ⚔️</div>
                {generate_modern_skills_v2(character_data)}
            </div>
            
            <div class="notes-container">
                <div class="notes-title">📝 This Session's Notes</div>
                <div class="notes-lines"></div>
            </div>
        </div>
    </div>
    
    <!-- PAGE 2: Combat & Spells -->
    <div class="page">
        <div class="ornate-border"></div>
        <div class="content-area">
            <div class="character-header">
                <div class="character-name" style="font-size: 20pt;">{character_data['name']}</div>
                <div class="character-title">Combat & Magic Arsenal</div>
                <div class="divider"></div>
            </div>
            
            <div class="attacks-container">
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
                        {generate_modern_attacks_v2(character_data)}
                    </tbody>
                </table>
            </div>
            
            <div class="spells-container">
                <div class="section-title">✨ Spellcasting Magic ✨</div>
                {generate_modern_spells_v2(character_data)}
            </div>
            
            <div class="equipment-container">
                <div class="section-title">🎒 Equipment & Treasure 🎒</div>
                {generate_modern_equipment_v2(character_data)}
            </div>
            
            <div class="notes-container">
                <div class="notes-title">💰 Loot & Rewards This Session</div>
                <div class="notes-lines"></div>
            </div>
        </div>
    </div>
    
    <!-- PAGE 3: Features & Character Details -->
    <div class="page">
        <div class="ornate-border"></div>
        <div class="content-area">
            <div class="character-header">
                <div class="character-name" style="font-size: 20pt;">{character_data['name']}</div>
                <div class="character-title">Features, Traits & Background</div>
                <div class="divider"></div>
            </div>
            
            <div class="features-container">
                <div class="section-title">🌟 Racial & Class Features 🌟</div>
                {generate_modern_features_v2(character_data)}
            </div>
            
            <div class="notes-container" style="height: 30mm; margin-bottom: 6mm;">
                <div class="notes-title">🎭 Roleplay Notes & Character Development</div>
                <div class="notes-lines"></div>
            </div>
            
            <div class="notes-container" style="height: 30mm; margin-bottom: 6mm;">
                <div class="notes-title">🗺️ Campaign Notes & Plot Threads</div>
                <div class="notes-lines"></div>
            </div>
            
            <div class="notes-container" style="height: 25mm;">
                <div class="notes-title">🎯 Goals & Objectives</div>
                <div class="notes-lines"></div>
            </div>
            
            <div style="text-align: center; margin-top: 8mm; font-size: 8pt; color: #666;">
                <span style="font-family: 'Cinzel', serif; font-weight: 600;">Generated on {datetime.now().strftime('%B %d, %Y')}</span><br/>
                <span>v2.0 Print-Friendly • Epic Adventures Await! 🐉</span>
            </div>
        </div>
    </div>
    
    <div class="no-print" style="position: fixed; top: 20px; right: 20px; background: rgba(0,0,0,0.8); color: white; padding: 15px; border-radius: 10px; z-index: 1000;">
        <strong>🖨️ Print Instructions v2:</strong><br/>
        1. File → Print (Ctrl/Cmd + P)<br/>
        2. Select "More settings"<br/>
        3. Check "Background graphics"<br/>
        4. Set margins to "Minimum"<br/>
        5. Print 3 pages!<br/>
        <br/>
        <strong>✨ v2 Features:</strong><br/>
        • Print-friendly (no solid colors)<br/>
        • Subtle patterns & borders<br/>
        • Character portrait area<br/>
        • Ornate corner graphics<br/>
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

def generate_ability_hexagons_v2(char):
    """Generate hexagonal ability score displays v2"""
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

def generate_modern_skills_v2(char):
    """Generate modern skills display v2"""
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

def generate_modern_attacks_v2(char):
    """Generate modern attacks table v2"""
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

def generate_modern_spells_v2(char):
    """Generate modern spells display v2"""
    html = f'''
    <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 3mm; margin-bottom: 4mm; text-align: center; font-weight: 600;">
        <div>Class: {char.get('class', '')}</div>
        <div>Ability: {char.get('spellcasting_ability', 'Charisma')}</div>
        <div>Save DC: {char.get('spell_save_dc', '')}</div>
        <div>Attack: {char.get('spell_attack_bonus', '')}</div>
    </div>
    '''
    
    # Cantrips
    html += '''
    <div class="spell-level-block">
        <div class="spell-level-title">
            <span>✨ CANTRIPS (0 Level)</span>
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
                    <span>{icon} {level.upper()} LEVEL SPELLS</span>
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
                <span>🔮 SORCERY POINTS: {char.get('sorcery_points', 0)}</span>
            </div>
        '''
        
        if char.get('level', 1) >= 3 and char.get('metamagic'):
            html += f'''
            <div class="spell-list">
                <strong>Metamagic:</strong> {' • '.join(char.get('metamagic', []))}
            </div>
            '''
        html += '</div>'
    
    return html

def generate_modern_equipment_v2(char):
    """Generate modern equipment display v2"""
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
    html += '<div style="font-weight: 700; margin-bottom: 2mm; font-size: 10pt;">💰 CURRENCY</div>'
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

def generate_modern_features_v2(char):
    """Generate modern features display v2"""
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
    # Generate Kazrek's v2 character sheet
    character_data = load_kazrek_data()
    html_file = generate_modern_sheet_v2(character_data, "Kazrek_Epic_Sheet_v2.html")
    
    print("🎨 ✅ CHARACTER SHEET v2 GENERATED!")
    print(f"📄 File: {html_file}")
    print("🖨️  Print-friendly design features:")
    print("   • No solid color blocks - ink-friendly!")
    print("   • Subtle patterns and borders")
    print("   • Character portrait area")
    print("   • Ornate corner graphics")
    print("   • Professional outline styling")
    print("   • 3 fixed pages with session notes")
    print("🐉 Ready for epic adventures - printer friendly!")