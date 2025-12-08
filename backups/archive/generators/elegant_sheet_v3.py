#!/usr/bin/env python3
"""
Elegant D&D Character Sheet Generator v3
Professional design following "Dwarven Grimoire" philosophy
Based on expert frontend-architect recommendations
"""

import json
import os
from datetime import datetime

def generate_elegant_sheet_v3(character_data, filename="elegant_character_sheet_v3.html"):
    """Generate professionally designed character sheet - Dwarven Grimoire style"""
    
    html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{character_data['name']} - Elegant Character Sheet</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@400;600;700&family=Source+Sans+Pro:wght@300;400;600;700&family=Cormorant+Garamond:wght@300;400;600&display=swap');
        
        @page {{
            size: A4;
            margin: 0;
        }}
        
        :root {{
            /* Dwarven Forge Palette */
            --forge-iron: #2c3539;
            --forge-steel: #546a7b;
            --forge-bronze: #cd7f32;
            
            /* Arcane Energy Palette */
            --arcane-blue: #4a6fa5;
            --arcane-silver: #9da9b5;
            
            /* Parchment Base */
            --parchment: #fdfbf7;
            --ink: #2a2a2a;
            
            /* Typography Scale */
            --text-hero: 32pt;
            --text-h1: 16pt;
            --text-h2: 12pt;
            --text-h3: 10pt;
            --text-body: 9pt;
            --text-small: 7pt;
            
            /* Spacing System */
            --space-xs: 1mm;
            --space-sm: 2mm;
            --space-md: 4mm;
            --space-lg: 6mm;
            --space-xl: 8mm;
            
            /* Font Stack */
            --font-display: 'Cinzel', serif;
            --font-body: 'Source Sans Pro', sans-serif;
            --font-accent: 'Cormorant Garamond', serif;
        }}
        
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: var(--font-body);
            line-height: 1.4;
            background: var(--parchment);
            color: var(--ink);
            position: relative;
        }}
        
        /* Subtle paper texture */
        body::after {{
            content: '';
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: 
                radial-gradient(circle at 15% 85%, rgba(205,127,50,0.02) 0%, transparent 70%),
                radial-gradient(circle at 85% 15%, rgba(74,111,165,0.015) 0%, transparent 60%);
            pointer-events: none;
            z-index: -1;
        }}
        
        .page {{
            width: 210mm;
            height: 297mm;
            background: var(--parchment);
            position: relative;
            page-break-after: always;
            padding: 12mm;
        }}
        
        .page:last-child {{
            page-break-after: avoid;
        }}
        
        /* Dwarven Corner Brackets */
        .page::before,
        .page::after {{
            content: '';
            position: absolute;
            width: 15mm;
            height: 15mm;
            border: 2px solid var(--forge-bronze);
            opacity: 0.6;
        }}
        
        .page::before {{
            top: 8mm;
            left: 8mm;
            border-right: none;
            border-bottom: none;
            background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 50 50"><path d="M5,5 L15,5 M5,5 L5,15 M10,8 L12,10 M8,10 L10,12" stroke="%23cd7f32" stroke-width="0.5" fill="none" opacity="0.3"/></svg>');
        }}
        
        .page::after {{
            top: 8mm;
            right: 8mm;
            border-left: none;
            border-bottom: none;
            background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 50 50"><path d="M45,5 L35,5 M45,5 L45,15 M40,8 L38,10 M42,10 L40,12" stroke="%23cd7f32" stroke-width="0.5" fill="none" opacity="0.3"/></svg>');
        }}
        
        .content-area {{
            position: relative;
            z-index: 1;
        }}
        
        /* Character Header */
        .character-header {{
            text-align: center;
            margin-bottom: var(--space-xl);
            position: relative;
        }}
        
        .character-name {{
            font-family: var(--font-display);
            font-size: var(--text-hero);
            font-weight: 700;
            color: var(--forge-iron);
            text-shadow: 0 1px 2px rgba(205,127,50,0.2);
            margin-bottom: var(--space-sm);
            letter-spacing: 1px;
        }}
        
        .character-subtitle {{
            font-family: var(--font-accent);
            font-size: var(--text-h2);
            color: var(--forge-steel);
            font-weight: 400;
            letter-spacing: 2px;
            text-transform: uppercase;
        }}
        
        /* Dwarven Divider */
        .divider {{
            height: 1px;
            background: linear-gradient(90deg, transparent 20%, var(--forge-bronze) 50%, transparent 80%);
            margin: var(--space-lg) 0;
            position: relative;
        }}
        
        .divider::before {{
            content: '⚒';
            position: absolute;
            left: 50%;
            top: -8px;
            transform: translateX(-50%);
            background: var(--parchment);
            padding: 0 6px;
            font-size: 16px;
            color: var(--forge-bronze);
        }}
        
        /* Golden Ratio Grid System */
        .info-grid {{
            display: grid;
            grid-template-columns: repeat(8, 1fr);
            gap: var(--space-sm);
            margin-bottom: var(--space-lg);
        }}
        
        .info-box {{
            grid-column: span 2;
            background: transparent;
            border: none;
            position: relative;
            padding: var(--space-md);
            text-align: center;
        }}
        
        /* Dwarven-crafted info boxes */
        .info-box::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: 
                linear-gradient(135deg, transparent 8px, rgba(84,106,123,0.1) 8px),
                linear-gradient(225deg, transparent 8px, rgba(84,106,123,0.1) 8px),
                linear-gradient(315deg, transparent 8px, rgba(84,106,123,0.1) 8px),
                linear-gradient(45deg, transparent 8px, rgba(84,106,123,0.1) 8px);
            border: 1px solid var(--forge-steel);
            opacity: 0.7;
        }}
        
        .info-label {{
            font-family: var(--font-body);
            font-weight: 700;
            font-size: var(--text-small);
            color: var(--forge-steel);
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-bottom: var(--space-xs);
            position: relative;
            z-index: 1;
        }}
        
        .info-value {{
            font-family: var(--font-body);
            font-size: var(--text-body);
            color: var(--forge-iron);
            font-weight: 600;
            position: relative;
            z-index: 1;
        }}
        
        /* Refined Hexagonal Ability Scores */
        .abilities-container {{
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: var(--space-lg);
            margin-bottom: var(--space-xl);
            justify-items: center;
        }}
        
        .ability-hex {{
            position: relative;
            width: 28mm;
            height: 28mm;
        }}
        
        /* Carved stone effect */
        .ability-hex::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: var(--forge-bronze);
            clip-path: polygon(50% 0%, 100% 25%, 100% 75%, 50% 100%, 0% 75%, 0% 25%);
            opacity: 0.8;
        }}
        
        .ability-hex::after {{
            content: '';
            position: absolute;
            top: 2px;
            left: 2px;
            right: 2px;
            bottom: 2px;
            background: 
                radial-gradient(circle at 30% 30%, rgba(255,255,255,0.3), transparent 60%),
                var(--parchment);
            clip-path: polygon(50% 0%, 100% 25%, 100% 75%, 50% 100%, 0% 75%, 0% 25%);
            box-shadow: inset 0 0 8px rgba(44,53,57,0.2);
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
            font-family: var(--font-body);
            font-size: var(--text-small);
            font-weight: 700;
            color: var(--forge-steel);
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}
        
        .ability-score {{
            font-family: var(--font-display);
            font-size: 18pt;
            font-weight: 700;
            color: var(--forge-bronze);
            margin: var(--space-xs) 0;
            text-shadow: 0 1px 1px rgba(0,0,0,0.2);
        }}
        
        .ability-modifier {{
            font-family: var(--font-body);
            font-size: var(--text-small);
            font-weight: 600;
            color: var(--forge-iron);
            background: rgba(253,251,247,0.9);
            padding: 1px var(--space-sm);
            border-radius: 2px;
            border: 1px solid var(--forge-bronze);
        }}
        
        /* Combat Stats - Angular/Martial Design */
        .combat-grid {{
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: var(--space-md);
            margin-bottom: var(--space-xl);
        }}
        
        .combat-stat {{
            background: transparent;
            padding: var(--space-md);
            text-align: center;
            position: relative;
        }}
        
        /* Angular martial borders */
        .combat-stat::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: 
                linear-gradient(45deg, var(--forge-steel) 0%, transparent 50%),
                linear-gradient(-45deg, transparent 50%, var(--forge-steel) 100%);
            background-size: 8px 8px, 8px 8px;
            background-position: top left, top right;
            background-repeat: no-repeat;
            border: 2px solid var(--forge-steel);
            clip-path: polygon(6px 0, 100% 0, 100% calc(100% - 6px), calc(100% - 6px) 100%, 0 100%, 0 6px);
            opacity: 0.6;
        }}
        
        .combat-label {{
            font-family: var(--font-body);
            font-size: var(--text-small);
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-bottom: var(--space-sm);
            color: var(--forge-steel);
            position: relative;
            z-index: 1;
        }}
        
        .combat-value {{
            font-family: var(--font-display);
            font-size: 24pt;
            font-weight: 700;
            color: var(--forge-iron);
            position: relative;
            z-index: 1;
        }}
        
        /* Section Containers */
        .section-container {{
            margin-bottom: var(--space-xl);
            position: relative;
        }}
        
        /* Martial sections (angular) */
        .section-martial {{
            background: 
                linear-gradient(135deg, transparent 4px, rgba(84,106,123,0.04) 4px),
                linear-gradient(45deg, transparent 4px, rgba(84,106,123,0.04) 4px);
            border: 1px solid var(--forge-steel);
            border-radius: 2px;
            padding: var(--space-md);
        }}
        
        /* Magical sections (flowing) */
        .section-magical {{
            background: 
                radial-gradient(ellipse at top left, rgba(74,111,165,0.04) 0%, transparent 50%),
                radial-gradient(ellipse at bottom right, rgba(74,111,165,0.04) 0%, transparent 50%);
            border: 1px solid var(--arcane-blue);
            border-radius: 6px;
            padding: var(--space-md);
        }}
        
        /* Neutral sections (clean) */
        .section-neutral {{
            background: rgba(253,251,247,0.5);
            border: 1px solid var(--forge-steel);
            border-radius: 3px;
            padding: var(--space-md);
        }}
        
        .section-title {{
            font-family: var(--font-display);
            font-size: var(--text-h1);
            font-weight: 600;
            text-align: center;
            margin-bottom: var(--space-md);
            position: relative;
        }}
        
        .section-title.martial {{
            color: var(--forge-steel);
        }}
        
        .section-title.magical {{
            color: var(--arcane-blue);
        }}
        
        .section-title.neutral {{
            color: var(--forge-iron);
        }}
        
        /* Enhanced Skills Grid */
        .skills-grid {{
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: var(--space-sm);
        }}
        
        .skill-item {{
            background: rgba(255, 255, 255, 0.6);
            border: 1px solid rgba(84,106,123, 0.3);
            border-radius: 3px;
            padding: var(--space-sm);
            font-size: var(--text-small);
            display: flex;
            align-items: center;
            transition: background-color 0.2s ease;
        }}
        
        .skill-item:hover {{
            background: rgba(205,127,50, 0.1);
        }}
        
        .prof-circle {{
            width: 12px;
            height: 12px;
            border: 2px solid var(--forge-steel);
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            margin-right: var(--space-sm);
            font-size: 8px;
            font-weight: 700;
            color: var(--forge-steel);
            flex-shrink: 0;
        }}
        
        .prof-circle.filled {{
            background-color: var(--forge-bronze);
            color: var(--parchment);
            border-color: var(--forge-bronze);
        }}
        
        /* Enhanced Portrait Frame */
        .portrait-container {{
            width: 40mm;
            height: 50mm;
            float: right;
            margin: 0 0 var(--space-md) var(--space-md);
            position: relative;
            background: rgba(253,251,247,0.8);
        }}
        
        /* Dwarven corner brackets for portrait */
        .portrait-container::before,
        .portrait-container::after {{
            content: '';
            position: absolute;
            width: 8mm;
            height: 8mm;
            border: 2px solid var(--forge-bronze);
        }}
        
        .portrait-container::before {{
            top: -2px;
            left: -2px;
            border-right: none;
            border-bottom: none;
        }}
        
        .portrait-container::after {{
            bottom: -2px;
            right: -2px;
            border-left: none;
            border-top: none;
        }}
        
        .portrait-placeholder {{
            width: 100%;
            height: 100%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: var(--text-small);
            color: var(--forge-steel);
            text-align: center;
            padding: var(--space-sm);
            border: 1px dashed var(--forge-steel);
            background: 
                repeating-linear-gradient(
                    45deg,
                    transparent,
                    transparent 3px,
                    rgba(84,106,123,0.1) 3px,
                    rgba(84,106,123,0.1) 6px
                );
        }}
        
        /* Spell Sections with Arcane Styling */
        .spell-level-block {{
            background: rgba(255, 255, 255, 0.4);
            border: 1px solid rgba(74,111,165, 0.3);
            border-radius: 4px;
            padding: var(--space-md);
            margin-bottom: var(--space-md);
        }}
        
        .spell-level-title {{
            font-family: var(--font-accent);
            font-weight: 600;
            font-size: var(--text-h3);
            margin-bottom: var(--space-sm);
            display: flex;
            justify-content: space-between;
            align-items: center;
            color: var(--arcane-blue);
        }}
        
        .spell-slots-track {{
            display: flex;
            gap: var(--space-xs);
        }}
        
        .spell-slot {{
            width: 16px;
            height: 16px;
            border: 2px solid var(--arcane-blue);
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: 700;
            font-size: var(--text-small);
            color: var(--arcane-blue);
            background: var(--parchment);
        }}
        
        .spell-list {{
            font-family: var(--font-accent);
            font-size: var(--text-body);
            line-height: 1.5;
            color: var(--ink);
        }}
        
        /* Session Notes with Handwriting Lines */
        .notes-container {{
            border: 1px solid var(--forge-steel);
            border-radius: 4px;
            padding: var(--space-md);
            background: var(--parchment);
            height: 40mm;
            position: relative;
        }}
        
        .notes-title {{
            font-family: var(--font-display);
            font-size: var(--text-h2);
            font-weight: 600;
            text-align: center;
            margin-bottom: var(--space-md);
            color: var(--forge-bronze);
        }}
        
        .notes-lines {{
            height: calc(100% - 8mm);
            background-image: 
                repeating-linear-gradient(
                    transparent,
                    transparent 5mm,
                    var(--forge-steel) 5mm,
                    var(--forge-steel) 5.1mm
                );
            border-radius: 2px;
            padding: var(--space-sm);
        }}
        
        /* Equipment Grid */
        .equipment-grid {{
            display: grid;
            grid-template-columns: 2fr 1fr;
            gap: var(--space-md);
        }}
        
        .equipment-list,
        .currency-box {{
            background: rgba(255, 255, 255, 0.4);
            border: 1px solid var(--forge-steel);
            border-radius: 3px;
            padding: var(--space-md);
            font-size: var(--text-small);
            line-height: 1.4;
        }}
        
        .currency-box {{
            text-align: center;
        }}
        
        .coin-stack {{
            display: flex;
            flex-direction: column;
            gap: var(--space-xs);
        }}
        
        .coin-item {{
            background: rgba(205, 127, 50, 0.1);
            border: 1px solid var(--forge-bronze);
            border-radius: 2px;
            padding: var(--space-xs);
            font-size: var(--text-small);
            font-weight: 600;
        }}
        
        /* Tables */
        .elegant-table {{
            width: 100%;
            border-collapse: separate;
            border-spacing: 0;
            background: rgba(255, 255, 255, 0.6);
            border: 1px solid var(--forge-steel);
            border-radius: 4px;
            overflow: hidden;
        }}
        
        .elegant-table th,
        .elegant-table td {{
            padding: var(--space-sm);
            text-align: center;
            border-bottom: 1px solid rgba(84,106,123, 0.2);
            font-size: var(--text-small);
        }}
        
        .elegant-table th {{
            background: rgba(84,106,123, 0.1);
            font-family: var(--font-body);
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 1px;
            color: var(--forge-steel);
        }}
        
        .elegant-table tr:last-child td {{
            border-bottom: none;
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
            }}
            .no-print {{ 
                display: none; 
            }}
        }}
    </style>
</head>
<body>
    <!-- PAGE 1: Character Overview & Core Stats -->
    <div class="page">
        <div class="content-area">
            <div class="character-header">
                <div class="character-name">{character_data['name']}</div>
                <div class="character-subtitle">{character_data['class']} • {character_data['race']} • {character_data['background']}</div>
                <div class="divider"></div>
            </div>
            
            <div class="portrait-container">
                <div class="portrait-placeholder">
                    Character<br/>Portrait<br/><br/>⚒️<br/><br/><small>Paste image or<br/>sketch here</small>
                </div>
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
            </div>
            
            <div class="info-grid" style="margin-bottom: var(--space-xl);">
                <div class="info-box" style="grid-column: span 4;">
                    <div class="info-label">Experience Points</div>
                    <div class="info-value">_____ / {character_data.get('next_level_xp', '')}</div>
                </div>
                <div class="info-box" style="grid-column: span 4;">
                    <div class="info-label">Proficiency Bonus</div>
                    <div class="info-value">+{character_data.get('proficiency_bonus', 2)}</div>
                </div>
            </div>
            
            <div class="abilities-container">
                {generate_elegant_abilities_v3(character_data)}
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
            
            <div class="section-container section-martial">
                <div class="section-title martial">⚔️ Skills & Proficiencies</div>
                {generate_elegant_skills_v3(character_data)}
            </div>
            
            <div class="notes-container">
                <div class="notes-title">📝 Session Notes</div>
                <div class="notes-lines"></div>
            </div>
        </div>
    </div>
    
    <!-- PAGE 2: Combat & Spells -->
    <div class="page">
        <div class="content-area">
            <div class="character-header">
                <div class="character-name" style="font-size: 24pt;">{character_data['name']}</div>
                <div class="character-subtitle">Combat & Arcane Arts</div>
                <div class="divider"></div>
            </div>
            
            <div class="section-container section-martial">
                <div class="section-title martial">⚔️ Attacks & Weapons</div>
                <table class="elegant-table">
                    <thead>
                        <tr>
                            <th>Weapon</th>
                            <th>Attack Bonus</th>
                            <th>Damage</th>
                            <th>Range/Properties</th>
                        </tr>
                    </thead>
                    <tbody>
                        {generate_elegant_attacks_v3(character_data)}
                    </tbody>
                </table>
            </div>
            
            <div class="section-container section-magical">
                <div class="section-title magical">✨ Spellcasting</div>
                {generate_elegant_spells_v3(character_data)}
            </div>
            
            <div class="section-container section-neutral">
                <div class="section-title neutral">🎒 Equipment & Treasure</div>
                {generate_elegant_equipment_v3(character_data)}
            </div>
            
            <div class="notes-container">
                <div class="notes-title">💰 Loot & Rewards</div>
                <div class="notes-lines"></div>
            </div>
        </div>
    </div>
    
    <!-- PAGE 3: Features & Character Details -->
    <div class="page">
        <div class="content-area">
            <div class="character-header">
                <div class="character-name" style="font-size: 24pt;">{character_data['name']}</div>
                <div class="character-subtitle">Features & Background</div>
                <div class="divider"></div>
            </div>
            
            <div class="section-container section-neutral">
                <div class="section-title neutral">🌟 Features & Traits</div>
                {generate_elegant_features_v3(character_data)}
            </div>
            
            <div class="notes-container" style="height: 30mm; margin-bottom: var(--space-lg);">
                <div class="notes-title">🎭 Roleplay & Development</div>
                <div class="notes-lines"></div>
            </div>
            
            <div class="notes-container" style="height: 30mm; margin-bottom: var(--space-lg);">
                <div class="notes-title">🗺️ Campaign & Plot Notes</div>
                <div class="notes-lines"></div>
            </div>
            
            <div class="notes-container" style="height: 25mm;">
                <div class="notes-title">🎯 Goals & Objectives</div>
                <div class="notes-lines"></div>
            </div>
            
            <div style="text-align: center; margin-top: var(--space-lg); font-size: var(--text-small); color: var(--forge-steel);">
                <span style="font-family: var(--font-display); font-weight: 600;">Kazrek's Grimoire</span> •
                <span>Generated {datetime.now().strftime('%B %d, %Y')}</span> •
                <span style="font-family: var(--font-accent);">v3.0 Dwarven Crafted</span>
            </div>
        </div>
    </div>
    
    <div class="no-print" style="position: fixed; top: 20px; right: 20px; background: rgba(44,53,57,0.9); color: white; padding: 15px; border-radius: 8px; z-index: 1000; font-family: var(--font-body);">
        <strong>🎨 Elegant Design v3:</strong><br/>
        1. Professional typography<br/>
        2. Dwarven-crafted aesthetic<br/>
        3. Print-friendly elegance<br/>
        4. Magical & martial themes<br/>
        5. Enhanced visual hierarchy<br/>
        <br/>
        <strong>📄 Print:</strong> Enable backgrounds!
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

def generate_elegant_abilities_v3(char):
    """Generate elegant hexagonal ability scores"""
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

def generate_elegant_skills_v3(char):
    """Generate elegant skills display"""
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

def generate_elegant_attacks_v3(char):
    """Generate elegant attacks table"""
    attacks = char.get('attacks', [])
    html = ""
    
    for attack in attacks:
        html += f'''
        <tr>
            <td style="font-weight: 600;">{attack['name']}</td>
            <td>{attack['attack_bonus']}</td>
            <td>{attack['damage']}</td>
            <td style="font-size: 7pt;">{attack.get('range', '')}</td>
        </tr>
        '''
    
    # Fill empty rows for consistency
    for i in range(max(0, 3 - len(attacks))):
        html += '<tr><td>_________________</td><td>___</td><td>_________________</td><td>_______</td></tr>'
    
    return html

def generate_elegant_spells_v3(char):
    """Generate elegant spells display"""
    html = f'''
    <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: var(--space-md); margin-bottom: var(--space-md); text-align: center; font-weight: 600; font-size: var(--text-small);">
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
            <span>✨ Cantrips (0 Level)</span>
            <span style="font-size: var(--text-small);">At Will</span>
        </div>
        <div class="spell-list">
    '''
    cantrips = char.get('cantrips', [])
    html += ' • '.join(cantrips) if cantrips else 'None known'
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
                    <span>{icon} {level.upper()} Level Spells</span>
                    <div class="spell-slots-track">
            '''
            
            for i in range(spell_slots[level]):
                html += '<div class="spell-slot">○</div>'
            html += '</div></div><div class="spell-list">'
            
            level_spells = spells.get(level, [])
            if level_spells:
                html += ' • '.join(level_spells)
            else:
                html += '_________________     _________________     _________________'
            html += '</div></div>'
    
    # Sorcery Points
    if char.get('class') == 'Sorcerer':
        html += f'''
        <div class="spell-level-block">
            <div class="spell-level-title">
                <span>🔮 Sorcery Points</span>
                <span style="font-size: 14pt; color: var(--forge-bronze);">{char.get('sorcery_points', 0)}</span>
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

def generate_elegant_equipment_v3(char):
    """Generate elegant equipment display"""
    equipment = char.get('equipment', [])
    currency = char.get('currency', {})
    
    html = '<div class="equipment-grid">'
    html += '<div class="equipment-list">'
    
    # Categorize equipment
    armor_weapons = [item for item in equipment if any(word in item.lower() for word in ['armor', 'shield', 'sword', 'crossbow', 'dagger', 'axe', 'hammer'])]
    gear_supplies = [item for item in equipment if item not in armor_weapons]
    
    if armor_weapons:
        html += '<div style="margin-bottom: var(--space-md);"><strong>⚔️ Weapons & Armor:</strong><br/>'
        for item in armor_weapons[:6]:
            html += f'• {item}<br/>'
        html += '</div>'
    
    if gear_supplies:
        html += '<div><strong>🎒 Gear & Supplies:</strong><br/>'
        for item in gear_supplies[:8]:
            html += f'• {item}<br/>'
        html += '</div>'
    
    html += '</div>'
    
    # Currency
    html += '<div class="currency-box">'
    html += '<div style="font-weight: 700; margin-bottom: var(--space-sm); font-size: var(--text-h3);">💰 Currency</div>'
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

def generate_elegant_features_v3(char):
    """Generate elegant features display"""
    html = ""
    
    # Racial features
    racial_features = char.get('racial_features', [])
    if racial_features:
        for feature in racial_features:
            html += f'''
            <div style="background: rgba(205,127,50,0.05); border-left: 3px solid var(--forge-bronze); padding: var(--space-md); margin-bottom: var(--space-sm); border-radius: 0 3px 3px 0;">
                <div style="font-family: var(--font-body); font-weight: 700; color: var(--forge-bronze); margin-bottom: var(--space-xs);">
                    🧬 {feature["name"]} <span style="font-size: var(--text-small); color: var(--forge-steel); font-weight: 400;">(Racial)</span>
                </div>
                <div style="font-size: var(--text-small); line-height: 1.4;">{feature["description"]}</div>
            </div>
            '''
    
    # Class features
    class_features = char.get('class_features', [])
    if class_features:
        for feature in class_features:
            html += f'''
            <div style="background: rgba(74,111,165,0.05); border-left: 3px solid var(--arcane-blue); padding: var(--space-md); margin-bottom: var(--space-sm); border-radius: 0 3px 3px 0;">
                <div style="font-family: var(--font-body); font-weight: 700; color: var(--arcane-blue); margin-bottom: var(--space-xs);">
                    ⚡ {feature["name"]} <span style="font-size: var(--text-small); color: var(--forge-steel); font-weight: 400;">(Class)</span>
                </div>
                <div style="font-size: var(--text-small); line-height: 1.4;">{feature["description"]}</div>
            </div>
            '''
    
    # Background info
    html += f'''
    <div style="background: rgba(84,106,123,0.05); border-left: 3px solid var(--forge-steel); padding: var(--space-md); margin-bottom: var(--space-sm); border-radius: 0 3px 3px 0;">
        <div style="font-family: var(--font-body); font-weight: 700; color: var(--forge-steel); margin-bottom: var(--space-xs);">
            📚 {char.get("background", "")} <span style="font-size: var(--text-small); font-weight: 400;">(Background)</span>
        </div>
        <div style="font-size: var(--text-small); line-height: 1.4;">
            <strong>Languages:</strong> {", ".join(char.get("languages", []))}<br/>
            <strong>Tool Proficiencies:</strong> {", ".join(char.get("tool_proficiencies", []))}
        </div>
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
                "description": "Can see in dim light within 60 feet as if it were bright light"
            },
            {
                "name": "Dwarven Resilience",
                "description": "Advantage on saving throws against poison, resistance to poison damage"
            },
            {
                "name": "Stonecunning",
                "description": "Double proficiency bonus on History checks related to stonework"
            }
        ],
        "class_features": [
            {
                "name": "Spellcasting",
                "description": "Cast spells using Charisma as spellcasting ability"
            },
            {
                "name": "Font of Magic",
                "description": "2 sorcery points. Can convert to spell slots or use for metamagic (level 3+)"
            }
        ]
    }

if __name__ == "__main__":
    # Generate Kazrek's elegant v3 character sheet
    character_data = load_kazrek_data()
    html_file = generate_elegant_sheet_v3(character_data, "Kazrek_Elegant_Sheet_v3.html")
    
    print("🎨 ✅ ELEGANT CHARACTER SHEET v3 CREATED!")
    print(f"📄 File: {html_file}")
    print("✨ Design Features:")
    print("   • Professional 'Dwarven Grimoire' aesthetic")
    print("   • Advanced typography hierarchy") 
    print("   • Themed sections (martial/magical/neutral)")
    print("   • Elegant hexagonal ability scores")
    print("   • Print-friendly with sophisticated styling")
    print("   • Enhanced visual hierarchy and spacing")
    print("   • Character portrait with dwarven brackets")
    print("   • Refined color palette and textures")
    print("🏰 Crafted with dwarven precision and arcane elegance!")