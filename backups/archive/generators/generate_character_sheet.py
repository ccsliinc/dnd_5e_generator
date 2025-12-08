#!/usr/bin/env python3
"""
D&D 5e Character Sheet PDF Generator
Creates official-style 3-page character sheets from character data
"""

import json
from reportlab.lib.pagesizes import letter
from reportlab.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import inch, mm
from reportlab.pdfgen import canvas
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
import os

class DnDCharacterSheet:
    def __init__(self, filename="character_sheet.pdf"):
        self.filename = filename
        self.width, self.height = letter
        self.margin = 0.5 * inch
        
    def create_sheet(self, character_data):
        """Generate complete 3-page character sheet"""
        doc = SimpleDocTemplate(
            self.filename,
            pagesize=letter,
            rightMargin=self.margin,
            leftMargin=self.margin,
            topMargin=self.margin,
            bottomMargin=self.margin
        )
        
        story = []
        
        # Page 1 - Main Character Sheet
        story.extend(self.create_page_one(character_data))
        story.append(PageBreak())
        
        # Page 2 - Features & Traits, Attacks & Spellcasting
        story.extend(self.create_page_two(character_data))
        story.append(PageBreak())
        
        # Page 3 - Spells
        story.extend(self.create_page_three(character_data))
        
        doc.build(story)
        print(f"Character sheet generated: {self.filename}")
    
    def create_page_one(self, char):
        """Create main character sheet (Page 1)"""
        elements = []
        styles = getSampleStyleSheet()
        
        # Header with character name and basic info
        header_style = ParagraphStyle(
            'CharacterHeader',
            parent=styles['Heading1'],
            fontSize=16,
            spaceAfter=12,
            alignment=TA_CENTER
        )
        
        elements.append(Paragraph(f"<b>{char['name']}</b>", header_style))
        
        # Basic info row
        basic_info_data = [
            ["Class & Level", "Background", "Race", "Alignment", "Experience Points"],
            [f"{char['class']} {char['level']}", char['background'], char['race'], char['alignment'], f"{char.get('current_xp', '')} / {char.get('next_level_xp', '')}"]
        ]
        
        basic_info_table = Table(basic_info_data, colWidths=[1.4*inch, 1.4*inch, 1.0*inch, 1.0*inch, 1.4*inch])
        basic_info_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))
        elements.append(basic_info_table)
        elements.append(Spacer(1, 12))
        
        # Main stats section
        main_stats_data = [
            # Headers
            ["", "Ability\nScore", "Ability\nModifier", "Prof", "Saving Throws", "", "Skills"],
            # Abilities with saves and skills
            ["Strength", str(char['abilities']['strength']), 
             self.format_modifier(char['abilities']['strength']), 
             "●" if 'strength' in char.get('saving_throw_profs', []) else "○",
             self.format_modifier(char['abilities']['strength']) + (" ●" if 'strength' in char.get('saving_throw_profs', []) else ""),
             "", ""],
            ["Dexterity", str(char['abilities']['dexterity']), 
             self.format_modifier(char['abilities']['dexterity']), 
             "●" if 'dexterity' in char.get('saving_throw_profs', []) else "○",
             self.format_modifier(char['abilities']['dexterity']) + (" ●" if 'dexterity' in char.get('saving_throw_profs', []) else ""),
             "", ""],
            ["Constitution", str(char['abilities']['constitution']), 
             self.format_modifier(char['abilities']['constitution']), 
             "●" if 'constitution' in char.get('saving_throw_profs', []) else "○",
             self.format_modifier(char['abilities']['constitution']) + (" ●" if 'constitution' in char.get('saving_throw_profs', []) else ""),
             "", ""],
            ["Intelligence", str(char['abilities']['intelligence']), 
             self.format_modifier(char['abilities']['intelligence']), 
             "●" if 'intelligence' in char.get('saving_throw_profs', []) else "○",
             self.format_modifier(char['abilities']['intelligence']) + (" ●" if 'intelligence' in char.get('saving_throw_profs', []) else ""),
             "", ""],
            ["Wisdom", str(char['abilities']['wisdom']), 
             self.format_modifier(char['abilities']['wisdom']), 
             "●" if 'wisdom' in char.get('saving_throw_profs', []) else "○",
             self.format_modifier(char['abilities']['wisdom']) + (" ●" if 'wisdom' in char.get('saving_throw_profs', []) else ""),
             "", ""],
            ["Charisma", str(char['abilities']['charisma']), 
             self.format_modifier(char['abilities']['charisma']), 
             "●" if 'charisma' in char.get('saving_throw_profs', []) else "○",
             self.format_modifier(char['abilities']['charisma']) + (" ●" if 'charisma' in char.get('saving_throw_profs', []) else ""),
             "", ""],
        ]
        
        # Combat stats section
        combat_data = [
            ["Armor Class", "Initiative", "Speed", "Hit Point Maximum", "Current Hit Points"],
            [str(char.get('ac', '')), self.format_modifier(char['abilities']['dexterity']), 
             f"{char.get('speed', '')} ft", str(char.get('hp_max', '')), ""]
        ]
        
        combat_table = Table(combat_data, colWidths=[1.0*inch, 1.0*inch, 1.0*inch, 1.4*inch, 1.4*inch])
        combat_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))
        elements.append(combat_table)
        elements.append(Spacer(1, 12))
        
        # Hit dice and death saves
        other_combat_data = [
            ["Temporary Hit Points", "Hit Dice", "Death Saves"],
            ["", f"{char.get('level', 1)}d{char.get('hit_die', 6)}", "Successes: ○ ○ ○\nFailures: ○ ○ ○"]
        ]
        
        other_combat_table = Table(other_combat_data, colWidths=[2.0*inch, 2.0*inch, 2.0*inch])
        other_combat_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))
        elements.append(other_combat_table)
        elements.append(Spacer(1, 12))
        
        # Skills section
        skills_text = self.format_skills(char)
        skills_style = ParagraphStyle(
            'Skills',
            parent=styles['Normal'],
            fontSize=8,
            leading=10
        )
        elements.append(Paragraph(f"<b>SKILLS</b><br/>{skills_text}", skills_style))
        elements.append(Spacer(1, 12))
        
        # Proficiencies and languages
        prof_data = [
            ["Other Proficiencies & Languages"],
            [self.format_proficiencies(char)]
        ]
        
        prof_table = Table(prof_data, colWidths=[7*inch])
        prof_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 8),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ]))
        elements.append(prof_table)
        
        return elements
    
    def create_page_two(self, char):
        """Create features, traits and attacks page (Page 2)"""
        elements = []
        styles = getSampleStyleSheet()
        
        # Attacks & Spellcasting
        elements.append(Paragraph("<b>ATTACKS & SPELLCASTING</b>", styles['Heading2']))
        
        attacks_data = [
            ["Name", "Atk Bonus", "Damage/Type", "Range"],
        ]
        
        for attack in char.get('attacks', []):
            attacks_data.append([
                attack['name'],
                attack['attack_bonus'],
                attack['damage'],
                attack.get('range', '')
            ])
        
        # Fill empty rows if needed
        while len(attacks_data) < 6:
            attacks_data.append(["", "", "", ""])
            
        attacks_table = Table(attacks_data, colWidths=[2.0*inch, 1.0*inch, 2.0*inch, 1.0*inch])
        attacks_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))
        elements.append(attacks_table)
        elements.append(Spacer(1, 12))
        
        # Equipment
        elements.append(Paragraph("<b>EQUIPMENT</b>", styles['Heading2']))
        equipment_text = self.format_equipment(char)
        elements.append(Paragraph(equipment_text, styles['Normal']))
        elements.append(Spacer(1, 12))
        
        # Features & Traits
        elements.append(Paragraph("<b>FEATURES & TRAITS</b>", styles['Heading2']))
        features_text = self.format_features(char)
        elements.append(Paragraph(features_text, styles['Normal']))
        
        return elements
    
    def create_page_three(self, char):
        """Create spells page (Page 3)"""
        elements = []
        styles = getSampleStyleSheet()
        
        elements.append(Paragraph("<b>SPELLCASTING</b>", styles['Heading1']))
        elements.append(Spacer(1, 12))
        
        # Spellcasting ability
        spell_data = [
            ["Spellcasting Class", "Spellcasting Ability", "Spell Save DC", "Spell Attack Bonus"],
            [char.get('class', ''), char.get('spellcasting_ability', 'Charisma'), 
             str(char.get('spell_save_dc', '')), char.get('spell_attack_bonus', '')]
        ]
        
        spell_table = Table(spell_data, colWidths=[1.5*inch, 1.5*inch, 1.5*inch, 1.5*inch])
        spell_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))
        elements.append(spell_table)
        elements.append(Spacer(1, 12))
        
        # Cantrips
        elements.append(Paragraph("<b>CANTRIPS (0 LEVEL)</b>", styles['Heading2']))
        cantrips_text = " • ".join(char.get('cantrips', []))
        elements.append(Paragraph(cantrips_text, styles['Normal']))
        elements.append(Spacer(1, 12))
        
        # Spell slots
        spell_slots = char.get('spell_slots', {})
        for level in sorted(spell_slots.keys()):
            if spell_slots[level] > 0:
                elements.append(Paragraph(f"<b>{level.upper()} LEVEL SPELLS</b> (Slots: {spell_slots[level]})", styles['Heading3']))
                level_spells = char.get('spells', {}).get(level, [])
                if level_spells:
                    spells_text = " • ".join(level_spells)
                    elements.append(Paragraph(spells_text, styles['Normal']))
                else:
                    elements.append(Paragraph("○ ○ ○ ○ ○", styles['Normal']))
                elements.append(Spacer(1, 8))
        
        # Sorcery Points (if applicable)
        if char.get('class') == 'Sorcerer':
            elements.append(Paragraph(f"<b>SORCERY POINTS:</b> {char.get('sorcery_points', 0)}", styles['Heading3']))
            if char.get('level', 1) >= 3:
                elements.append(Paragraph("<b>METAMAGIC:</b> " + " • ".join(char.get('metamagic', [])), styles['Normal']))
        
        return elements
    
    def format_modifier(self, ability_score):
        """Convert ability score to modifier string"""
        modifier = (ability_score - 10) // 2
        return f"+{modifier}" if modifier >= 0 else str(modifier)
    
    def format_skills(self, char):
        """Format skills list"""
        skills = char.get('skills', {})
        skill_list = []
        
        standard_skills = [
            ('Acrobatics', 'dexterity'),
            ('Animal Handling', 'wisdom'),
            ('Arcana', 'intelligence'),
            ('Athletics', 'strength'),
            ('Deception', 'charisma'),
            ('History', 'intelligence'),
            ('Insight', 'wisdom'),
            ('Intimidation', 'charisma'),
            ('Investigation', 'intelligence'),
            ('Medicine', 'wisdom'),
            ('Nature', 'intelligence'),
            ('Perception', 'wisdom'),
            ('Performance', 'charisma'),
            ('Persuasion', 'charisma'),
            ('Religion', 'intelligence'),
            ('Sleight of Hand', 'dexterity'),
            ('Stealth', 'dexterity'),
            ('Survival', 'wisdom')
        ]
        
        for skill, ability in standard_skills:
            prof_bonus = char.get('proficiency_bonus', 2) if skill.lower() in [s.lower() for s in skills] else 0
            ability_mod = (char['abilities'][ability] - 10) // 2
            total = ability_mod + prof_bonus
            prof_marker = "●" if prof_bonus > 0 else "○"
            skill_list.append(f"{prof_marker} {total:+d} {skill}")
        
        return "<br/>".join(skill_list)
    
    def format_proficiencies(self, char):
        """Format proficiencies and languages"""
        prof_text = []
        
        if char.get('languages'):
            prof_text.append(f"<b>Languages:</b> {', '.join(char['languages'])}")
        
        if char.get('weapon_proficiencies'):
            prof_text.append(f"<b>Weapons:</b> {', '.join(char['weapon_proficiencies'])}")
            
        if char.get('tool_proficiencies'):
            prof_text.append(f"<b>Tools:</b> {', '.join(char['tool_proficiencies'])}")
        
        return "<br/>".join(prof_text)
    
    def format_equipment(self, char):
        """Format equipment list"""
        equipment = char.get('equipment', [])
        currency = char.get('currency', {})
        
        equip_text = []
        if equipment:
            equip_text.append("<b>Equipment:</b><br/>" + "<br/>".join([f"• {item}" for item in equipment]))
        
        if currency:
            coins = []
            for coin_type, amount in currency.items():
                if amount > 0:
                    coins.append(f"{amount} {coin_type}")
            if coins:
                equip_text.append(f"<b>Currency:</b> {', '.join(coins)}")
        
        return "<br/><br/>".join(equip_text)
    
    def format_features(self, char):
        """Format racial and class features"""
        features = []
        
        # Racial features
        if char.get('racial_features'):
            features.append("<b>Racial Features:</b>")
            for feature in char['racial_features']:
                features.append(f"• <b>{feature['name']}:</b> {feature['description']}")
        
        # Class features  
        if char.get('class_features'):
            features.append("<b>Class Features:</b>")
            for feature in char['class_features']:
                features.append(f"• <b>{feature['name']}:</b> {feature['description']}")
                
        return "<br/>".join(features)


def load_kazrek_data():
    """Load Kazrek's character data"""
    return {
        "name": "Kazrek Spellforge",
        "class": "Sorcerer",
        "level": 2,
        "background": "Hermit",
        "race": "Mountain Dwarf",
        "alignment": "Chaotic Good",
        "current_xp": "",
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
        "weapon_proficiencies": [
            "Daggers", "Darts", "Slings", "Quarterstaffs", "Light crossbows",
            "Battleaxe", "Handaxe", "Light hammer", "Warhammer"
        ],
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
    sheet = DnDCharacterSheet("Kazrek_Spellforge_Official.pdf")
    sheet.create_sheet(character_data)
    
    print("✅ Official D&D 5e character sheet generated!")
    print("📄 File: Kazrek_Spellforge_Official.pdf")
    print("🖨️  Ready to print!")