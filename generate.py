#!/usr/bin/env python3
"""
D&D 5e Character Sheet Generator
Generates HTML character sheets from JSON data files.
"""

import json
import sys
from pathlib import Path
from datetime import datetime


def calculate_modifier(score: int) -> str:
    """Calculate ability modifier from score."""
    mod = (score - 10) // 2
    return f"+{mod}" if mod >= 0 else str(mod)


def get_skill_ability(skill: str) -> tuple[str, str]:
    """Return the ability abbreviation for a skill."""
    skill_abilities = {
        "acrobatics": ("Dex", "dexterity"),
        "animal_handling": ("Wis", "wisdom"),
        "arcana": ("Int", "intelligence"),
        "athletics": ("Str", "strength"),
        "deception": ("Cha", "charisma"),
        "history": ("Int", "intelligence"),
        "insight": ("Wis", "wisdom"),
        "intimidation": ("Cha", "charisma"),
        "investigation": ("Int", "intelligence"),
        "medicine": ("Wis", "wisdom"),
        "nature": ("Int", "intelligence"),
        "perception": ("Wis", "wisdom"),
        "performance": ("Cha", "charisma"),
        "persuasion": ("Cha", "charisma"),
        "religion": ("Int", "intelligence"),
        "sleight_of_hand": ("Dex", "dexterity"),
        "stealth": ("Dex", "dexterity"),
        "survival": ("Wis", "wisdom"),
    }
    return skill_abilities.get(skill, ("???", "strength"))


def format_skill_name(skill: str) -> str:
    """Format skill name for display."""
    return skill.replace("_", " ").title()


def prepare_template_data(char_data: dict) -> dict:
    """Transform raw character data into template-ready format."""
    prof_bonus = char_data.get("proficiency_bonus", 2)
    abilities = char_data.get("abilities", {})

    # Calculate ability modifiers
    ability_mods = {}
    for ability, data in abilities.items():
        score = data.get("score", 10)
        ability_mods[ability] = (score - 10) // 2

    # Build abilities list for template
    ability_order = ["strength", "dexterity", "constitution", "intelligence", "wisdom", "charisma"]
    abilities_list = []
    for ability in ability_order:
        data = abilities.get(ability, {"score": 10})
        score = data.get("score", 10)
        abilities_list.append({
            "name": ability[:3].upper(),
            "score": score,
            "modifier": calculate_modifier(score)
        })

    # Build saving throws list
    saves = char_data.get("saving_throws", {})
    saves_list = []
    for ability in ability_order:
        save_data = saves.get(ability, {"proficient": False})
        is_prof = save_data.get("proficient", False)
        mod = ability_mods.get(ability, 0)
        if is_prof:
            mod += prof_bonus
        saves_list.append({
            "name": ability.capitalize(),
            "proficient": is_prof,
            "modifier": f"+{mod}" if mod >= 0 else str(mod)
        })

    # Build skills list
    skills_data = char_data.get("skills", {})
    skills_list = []
    skill_order = [
        "acrobatics", "animal_handling", "arcana", "athletics", "deception",
        "history", "insight", "intimidation", "investigation", "medicine",
        "nature", "perception", "performance", "persuasion", "religion",
        "sleight_of_hand", "stealth", "survival"
    ]
    for skill in skill_order:
        skill_info = skills_data.get(skill, {"proficient": False})
        is_prof = skill_info.get("proficient", False)
        ability_abbr, ability_name = get_skill_ability(skill)
        mod = ability_mods.get(ability_name, 0)
        if is_prof:
            mod += prof_bonus
        skills_list.append({
            "name": format_skill_name(skill),
            "ability": ability_abbr,
            "proficient": is_prof,
            "modifier": f"+{mod}" if mod >= 0 else str(mod)
        })

    # Calculate passive perception
    perception_skill = skills_data.get("perception", {"proficient": False})
    perception_mod = ability_mods.get("wisdom", 0)
    if perception_skill.get("proficient", False):
        perception_mod += prof_bonus
    passive_perception = 10 + perception_mod

    # Combat stats
    combat = char_data.get("combat", {})
    dex_mod = ability_mods.get("dexterity", 0)
    initiative = combat.get("initiative")
    if initiative is None:
        initiative = f"+{dex_mod}" if dex_mod >= 0 else str(dex_mod)

    # Build spell levels for template
    spellcasting = char_data.get("spellcasting", {})
    spells_data = spellcasting.get("spells", {})
    spell_levels = []
    for level in range(1, 10):
        level_str = str(level)
        level_data = spells_data.get(level_str, {"slots_total": 0, "slots_expended": 0, "known": []})
        spell_levels.append({
            "level": level,
            "slots_total": level_data.get("slots_total", 0),
            "slots_expended": level_data.get("slots_expended", 0),
            "spells": level_data.get("known", [])
        })

    # Header data
    header = char_data.get("header", {})

    return {
        # Header info
        "character_name": header.get("character_name", ""),
        "class_level": header.get("class_level", ""),
        "background": header.get("background", ""),
        "player_name": header.get("player_name", ""),
        "race": header.get("race", ""),
        "alignment": header.get("alignment", ""),
        "experience_points": header.get("experience_points", ""),

        # Abilities
        "abilities": abilities_list,

        # Core stats
        "inspiration": "" if not char_data.get("inspiration") else "X",
        "proficiency_bonus": f"+{prof_bonus}",

        # Saves & Skills
        "saving_throws": saves_list,
        "skills": skills_list,
        "passive_perception": passive_perception,

        # Combat
        "armor_class": combat.get("armor_class", ""),
        "initiative": initiative,
        "speed": combat.get("speed", ""),
        "hp_maximum": combat.get("hp_maximum", ""),
        "hp_current": combat.get("hp_current") or "",
        "hp_temporary": combat.get("hp_temporary") or "",
        "hit_dice_total": combat.get("hit_dice", {}).get("total", ""),
        "hit_dice_current": combat.get("hit_dice", {}).get("current") or "",

        # Attacks
        "attacks": char_data.get("attacks", []),

        # Personality
        "personality_traits": char_data.get("personality", {}).get("traits", ""),
        "ideals": char_data.get("personality", {}).get("ideals", ""),
        "bonds": char_data.get("personality", {}).get("bonds", ""),
        "flaws": char_data.get("personality", {}).get("flaws", ""),

        # Bottom sections
        "proficiencies_languages": char_data.get("proficiencies_languages", []),
        "equipment": char_data.get("equipment", []),
        "currency": char_data.get("currency", {}),
        "features_traits": char_data.get("features_traits", []),

        # Page 2 - Background
        "appearance": char_data.get("appearance", {}),
        "character_appearance_description": char_data.get("character_appearance_description", ""),
        "backstory": char_data.get("backstory", ""),
        "allies_organizations": char_data.get("allies_organizations", {}),
        "additional_features_traits": char_data.get("additional_features_traits", []),
        "treasure": char_data.get("treasure", []),

        # Page 3 - Spellcasting
        "spellcasting": {
            "class": spellcasting.get("class", ""),
            "ability": spellcasting.get("ability", ""),
            "spell_save_dc": spellcasting.get("spell_save_dc", ""),
            "spell_attack_bonus": spellcasting.get("spell_attack_bonus", ""),
            "cantrips": spellcasting.get("cantrips", []),
            "spell_levels": spell_levels
        },

        # Meta
        "generated_date": datetime.now().strftime("%Y-%m-%d %H:%M")
    }


def render_template(template_content: str, data: dict) -> str:
    """Simple template rendering without external dependencies."""
    html = template_content

    # Simple value replacements
    simple_replacements = [
        ("character_name", data["character_name"]),
        ("class_level", data["class_level"]),
        ("background", data["background"]),
        ("player_name", data["player_name"]),
        ("race", data["race"]),
        ("alignment", data["alignment"]),
        ("experience_points", str(data["experience_points"])),
        ("inspiration", data["inspiration"]),
        ("proficiency_bonus", data["proficiency_bonus"]),
        ("passive_perception", str(data["passive_perception"])),
        ("armor_class", str(data["armor_class"])),
        ("initiative", str(data["initiative"])),
        ("speed", str(data["speed"])),
        ("hp_maximum", str(data["hp_maximum"])),
        ("hp_current", str(data["hp_current"])),
        ("hp_temporary", str(data["hp_temporary"])),
        ("hit_dice_total", data["hit_dice_total"]),
        ("hit_dice_current", data["hit_dice_current"]),
        ("personality_traits", data["personality_traits"]),
        ("ideals", data["ideals"]),
        ("bonds", data["bonds"]),
        ("flaws", data["flaws"]),
        ("character_appearance_description", data["character_appearance_description"]),
        ("backstory", data["backstory"]),
    ]

    for key, value in simple_replacements:
        html = html.replace(f"{{{{{key}}}}}", str(value))

    # Nested replacements
    html = html.replace("{{appearance.age}}", data["appearance"].get("age", ""))
    html = html.replace("{{appearance.height}}", data["appearance"].get("height", ""))
    html = html.replace("{{appearance.weight}}", data["appearance"].get("weight", ""))
    html = html.replace("{{appearance.eyes}}", data["appearance"].get("eyes", ""))
    html = html.replace("{{appearance.skin}}", data["appearance"].get("skin", ""))
    html = html.replace("{{appearance.hair}}", data["appearance"].get("hair", ""))

    html = html.replace("{{allies_organizations.name}}", data["allies_organizations"].get("name", ""))
    html = html.replace("{{allies_organizations.description}}", data["allies_organizations"].get("description", ""))

    html = html.replace("{{currency.cp}}", str(data["currency"].get("cp", 0)))
    html = html.replace("{{currency.sp}}", str(data["currency"].get("sp", 0)))
    html = html.replace("{{currency.ep}}", str(data["currency"].get("ep", 0)))
    html = html.replace("{{currency.gp}}", str(data["currency"].get("gp", 0)))
    html = html.replace("{{currency.pp}}", str(data["currency"].get("pp", 0)))

    html = html.replace("{{spellcasting.class}}", data["spellcasting"]["class"])
    html = html.replace("{{spellcasting.ability}}", data["spellcasting"]["ability"])
    html = html.replace("{{spellcasting.spell_save_dc}}", str(data["spellcasting"]["spell_save_dc"]))
    html = html.replace("{{spellcasting.spell_attack_bonus}}", data["spellcasting"]["spell_attack_bonus"])

    return html


def generate_html(template_path: Path, data: dict) -> str:
    """Generate final HTML by combining template with data."""
    template_content = template_path.read_text()

    # First, render simple replacements
    html = render_template(template_content, data)

    # Now handle the complex sections by building HTML directly

    # Abilities
    abilities_html = ""
    for ability in data["abilities"]:
        abilities_html += f'''
                    <div class="ability-score">
                        <div class="ability-name">{ability["name"]}</div>
                        <div class="ability-value">{ability["score"]}</div>
                        <div class="ability-modifier">{ability["modifier"]}</div>
                    </div>'''
    html = html.replace("{{#each abilities}}", "").replace("{{/each}}", "")
    html = html.replace('''<div class="ability-name">{{name}}</div>
                        <div class="ability-value">{{score}}</div>
                        <div class="ability-modifier">{{modifier}}</div>''', "")

    # Find and replace the ability block
    ability_block_start = html.find('<div class="ability-block">')
    ability_block_end = html.find('</div>', ability_block_start + 200) + 6
    html = html[:ability_block_start] + f'<div class="ability-block">{abilities_html}\n                </div>' + html[ability_block_end:]

    # Saving throws
    saves_html = ""
    for save in data["saving_throws"]:
        filled = "filled" if save["proficient"] else ""
        saves_html += f'''
                    <div class="save-row">
                        <div class="prof-circle {filled}"></div>
                        <div class="save-mod">{save["modifier"]}</div>
                        <div class="save-name">{save["name"]}</div>
                    </div>'''

    # Skills
    skills_html = ""
    for skill in data["skills"]:
        filled = "filled" if skill["proficient"] else ""
        skills_html += f'''
                    <div class="skill-row">
                        <div class="prof-circle {filled}"></div>
                        <div class="skill-mod">{skill["modifier"]}</div>
                        <div class="skill-name">{skill["name"]} <span class="skill-ability">({skill["ability"]})</span></div>
                    </div>'''

    # Attacks
    attacks_html = ""
    for attack in data["attacks"]:
        attacks_html += f'''
                    <div class="attack-row">
                        <div class="attack-name">{attack["name"]}</div>
                        <div class="attack-bonus">{attack["atk_bonus"]}</div>
                        <div class="attack-damage">{attack["damage_type"]}</div>
                    </div>'''

    # Proficiencies & Languages
    prof_lang_html = ", ".join(data["proficiencies_languages"])

    # Equipment
    equipment_html = "<br>\n                    ".join(data["equipment"])

    # Features & Traits
    features_html = "<br>\n                    ".join(data["features_traits"])

    # Additional Features & Traits
    additional_features_html = "<br>\n                        ".join(data["additional_features_traits"])

    # Treasure
    treasure_html = "<br>\n                        ".join(data["treasure"])

    # Cantrips
    cantrips_html = ""
    for cantrip in data["spellcasting"]["cantrips"]:
        cantrips_html += f'''
                    <div class="spell-item">
                        <span>{cantrip}</span>
                    </div>'''

    # Spell levels
    spell_levels_html = ""
    for level_data in data["spellcasting"]["spell_levels"]:
        spells_in_level = ""
        for spell in level_data["spells"]:
            filled = "filled" if spell.get("prepared", False) else ""
            spells_in_level += f'''
                    <div class="spell-item">
                        <div class="spell-prepared {filled}"></div>
                        <span>{spell["name"]}</span>
                    </div>'''

        spell_levels_html += f'''
            <div class="spell-level-box">
                <div class="spell-level-header">
                    <div class="spell-level-num">{level_data["level"]}</div>
                    <div class="spell-slots">
                        <div class="spell-slots-row">
                            <span>Slots:</span>
                            <div class="spell-slot-box">{level_data["slots_total"]}</div>
                        </div>
                        <div class="spell-slots-row">
                            <span>Used:</span>
                            <div class="spell-slot-box">{level_data["slots_expended"]}</div>
                        </div>
                    </div>
                </div>
                <div class="spell-list">{spells_in_level}
                </div>
            </div>'''

    # Now do all the replacements for complex sections
    # This is a simplified approach - we'll rebuild these sections

    # Build the final HTML by reconstructing with actual data
    final_html = build_complete_html(data)

    return final_html


def build_complete_html(data: dict) -> str:
    """Build the complete HTML document with all data populated."""

    # Abilities HTML
    abilities_html = ""
    for ability in data["abilities"]:
        abilities_html += f'''
                    <div class="ability-score">
                        <div class="ability-name">{ability["name"]}</div>
                        <div class="ability-value">{ability["score"]}</div>
                        <div class="ability-modifier">{ability["modifier"]}</div>
                    </div>'''

    # Saving throws HTML
    saves_html = ""
    for save in data["saving_throws"]:
        filled = "filled" if save["proficient"] else ""
        saves_html += f'''
                    <div class="save-row">
                        <div class="prof-circle {filled}"></div>
                        <div class="save-mod">{save["modifier"]}</div>
                        <div class="save-name">{save["name"]}</div>
                    </div>'''

    # Skills HTML
    skills_html = ""
    for skill in data["skills"]:
        filled = "filled" if skill["proficient"] else ""
        skills_html += f'''
                    <div class="skill-row">
                        <div class="prof-circle {filled}"></div>
                        <div class="skill-mod">{skill["modifier"]}</div>
                        <div class="skill-name">{skill["name"]} <span class="skill-ability">({skill["ability"]})</span></div>
                    </div>'''

    # Attacks HTML
    attacks_html = ""
    for attack in data["attacks"]:
        attacks_html += f'''
                    <div class="attack-row">
                        <div class="attack-name">{attack["name"]}</div>
                        <div class="attack-bonus">{attack["atk_bonus"]}</div>
                        <div class="attack-damage">{attack["damage_type"]}</div>
                    </div>'''
    # Add empty rows for handwriting
    for _ in range(max(0, 5 - len(data["attacks"]))):
        attacks_html += '''
                    <div class="attack-row">
                        <div class="attack-name"></div>
                        <div class="attack-bonus"></div>
                        <div class="attack-damage"></div>
                    </div>'''

    # Proficiencies & Languages
    prof_lang_html = ", ".join(data["proficiencies_languages"])

    # Equipment
    equipment_html = "<br>".join(data["equipment"])

    # Features & Traits
    features_html = "<br>".join(data["features_traits"])

    # Additional Features & Traits
    additional_features_html = "<br>".join(data["additional_features_traits"])

    # Treasure
    treasure_html = "<br>".join(data["treasure"])

    # Cantrips
    cantrips_html = ""
    for cantrip in data["spellcasting"]["cantrips"]:
        cantrips_html += f'''
                    <div class="spell-item">
                        <span>{cantrip}</span>
                    </div>'''

    # Spell levels
    spell_levels_html = ""
    for level_data in data["spellcasting"]["spell_levels"]:
        spells_in_level = ""
        for spell in level_data["spells"]:
            filled = "filled" if spell.get("prepared", False) else ""
            spells_in_level += f'''
                    <div class="spell-item">
                        <div class="spell-prepared {filled}"></div>
                        <span>{spell["name"]}</span>
                    </div>'''
        # Add empty rows
        for _ in range(max(0, 8 - len(level_data["spells"]))):
            spells_in_level += '''
                    <div class="spell-item">
                        <div class="spell-prepared"></div>
                        <span></span>
                    </div>'''

        spell_levels_html += f'''
            <div class="spell-level-box">
                <div class="spell-level-header">
                    <div class="spell-level-num">{level_data["level"]}</div>
                    <div class="spell-slots">
                        <div class="spell-slots-row">
                            <span>Slots:</span>
                            <div class="spell-slot-box">{level_data["slots_total"]}</div>
                        </div>
                        <div class="spell-slots-row">
                            <span>Used:</span>
                            <div class="spell-slot-box">{level_data["slots_expended"]}</div>
                        </div>
                    </div>
                </div>
                <div class="spell-list">{spells_in_level}
                </div>
            </div>'''

    return f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{data["character_name"]} - Character Sheet</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@400;500;600;700&family=Scada:wght@400;700&display=swap');

        :root {{
            --bg-page: #faf8f5;
            --bg-box: #ffffff;
            --border-dark: #1a1a1a;
            --border-medium: #4a4a4a;
            --border-light: #888888;
            --text-primary: #1a1a1a;
            --text-secondary: #4a4a4a;
            --text-label: #666666;
            --accent-primary: #8b4513;
            --accent-secondary: #c9a227;
            --accent-highlight: rgba(201, 162, 39, 0.1);
            --font-display: 'Cinzel', serif;
            --font-body: 'Scada', sans-serif;
            --page-width: 210mm;
            --page-height: 297mm;
            --page-margin: 8mm;
            --box-radius: 3px;
            --border-width: 1.5px;
        }}

        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        @page {{ size: A4; margin: 0; }}
        body {{
            font-family: var(--font-body);
            font-size: 9pt;
            line-height: 1.3;
            color: var(--text-primary);
            background: #e0e0e0;
        }}

        .page {{
            width: var(--page-width);
            height: var(--page-height);
            margin: 10mm auto;
            padding: var(--page-margin);
            background: var(--bg-page);
            box-shadow: 0 2px 10px rgba(0,0,0,0.2);
            position: relative;
            overflow: hidden;
            page-break-after: always;
        }}
        .page:last-child {{ page-break-after: avoid; }}

        @media print {{
            body {{ background: none; }}
            .page {{ margin: 0; box-shadow: none; }}
        }}

        .header-banner {{
            height: 20mm;
            background: linear-gradient(135deg, var(--border-dark) 0%, #2a2a2a 50%, var(--border-dark) 100%);
            border-radius: var(--box-radius);
            margin-bottom: 3mm;
            display: flex;
            align-items: center;
            justify-content: center;
            position: relative;
        }}
        .header-title {{
            font-family: var(--font-display);
            font-size: 16pt;
            font-weight: 700;
            color: #f0f0f0;
            letter-spacing: 3px;
            text-transform: uppercase;
        }}
        .header-accent {{ color: var(--accent-secondary); }}

        .char-info-row {{
            display: grid;
            grid-template-columns: 2fr 1fr 1fr 1fr;
            gap: 2mm;
            margin-bottom: 2mm;
        }}
        .info-field {{
            border: var(--border-width) solid var(--border-dark);
            border-radius: var(--box-radius);
            padding: 1.5mm 2mm 4mm;
            background: var(--bg-box);
            position: relative;
        }}
        .info-label {{
            font-size: 6pt;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            color: var(--text-label);
            position: absolute;
            bottom: 1mm;
            left: 2mm;
        }}
        .info-value {{
            font-size: 10pt;
            font-weight: 600;
            color: var(--text-primary);
        }}
        .info-value.name {{
            font-family: var(--font-display);
            font-size: 14pt;
            font-weight: 700;
        }}

        .main-content {{
            display: grid;
            grid-template-columns: 52mm 1fr 58mm;
            gap: 3mm;
            height: calc(100% - 55mm);
        }}
        .column {{
            display: flex;
            flex-direction: column;
            gap: 1.5mm;
        }}

        .ability-block {{
            display: flex;
            flex-direction: column;
            gap: 1mm;
        }}
        .ability-score {{
            border: var(--border-width) solid var(--border-dark);
            border-radius: var(--box-radius);
            background: var(--bg-box);
            padding: 1.5mm;
            display: flex;
            flex-direction: column;
            align-items: center;
        }}
        .ability-name {{
            font-size: 6pt;
            font-weight: 700;
            text-transform: uppercase;
            color: var(--text-secondary);
        }}
        .ability-value {{
            font-family: var(--font-display);
            font-size: 18pt;
            font-weight: 700;
            line-height: 1;
        }}
        .ability-modifier {{
            width: 10mm;
            height: 6mm;
            border: var(--border-width) solid var(--border-dark);
            border-radius: 0 0 5mm 5mm;
            background: var(--bg-box);
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 9pt;
            font-weight: 700;
            margin-top: 1mm;
        }}

        .stat-row {{
            display: flex;
            align-items: center;
            gap: 2mm;
            border: var(--border-width) solid var(--border-dark);
            border-radius: var(--box-radius);
            background: var(--bg-box);
            padding: 1.5mm 2mm;
        }}
        .stat-circle {{
            width: 7mm;
            height: 7mm;
            border: var(--border-width) solid var(--border-dark);
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 9pt;
            font-weight: 700;
        }}
        .stat-label {{
            font-size: 6.5pt;
            font-weight: 700;
            text-transform: uppercase;
        }}

        .saves-skills-box {{
            border: var(--border-width) solid var(--border-dark);
            border-radius: var(--box-radius);
            background: var(--bg-box);
            padding: 1.5mm;
        }}
        .box-title {{
            font-size: 6.5pt;
            font-weight: 700;
            text-transform: uppercase;
            text-align: center;
            margin-bottom: 1mm;
            color: var(--text-secondary);
        }}
        .save-row, .skill-row {{
            display: flex;
            align-items: center;
            gap: 1mm;
            padding: 0.3mm 0;
            font-size: 7pt;
        }}
        .prof-circle {{
            width: 3mm;
            height: 3mm;
            border: 1px solid var(--border-dark);
            border-radius: 50%;
        }}
        .prof-circle.filled {{ background: var(--border-dark); }}
        .save-mod, .skill-mod {{
            width: 5mm;
            font-weight: 700;
            text-align: right;
            font-size: 7pt;
        }}
        .skill-ability {{ font-size: 5.5pt; color: var(--text-label); }}

        .passive-box {{
            border: var(--border-width) solid var(--border-dark);
            border-radius: var(--box-radius);
            background: var(--bg-box);
            padding: 1.5mm;
            display: flex;
            align-items: center;
            gap: 2mm;
        }}
        .passive-value {{
            width: 8mm;
            height: 8mm;
            border: var(--border-width) solid var(--border-dark);
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 10pt;
            font-weight: 700;
        }}
        .passive-label {{
            font-size: 6pt;
            font-weight: 700;
            text-transform: uppercase;
            line-height: 1.2;
        }}

        .combat-row {{
            display: grid;
            grid-template-columns: 1fr 1fr 1fr;
            gap: 2mm;
        }}
        .combat-stat {{
            border: var(--border-width) solid var(--border-dark);
            border-radius: var(--box-radius);
            background: var(--bg-box);
            padding: 2mm;
            text-align: center;
        }}
        .combat-value {{
            font-family: var(--font-display);
            font-size: 16pt;
            font-weight: 700;
            min-height: 10mm;
            display: flex;
            align-items: center;
            justify-content: center;
        }}
        .combat-label {{
            font-size: 5.5pt;
            font-weight: 700;
            text-transform: uppercase;
            color: var(--text-secondary);
        }}

        .hp-section {{
            border: var(--border-width) solid var(--border-dark);
            border-radius: var(--box-radius);
            background: var(--bg-box);
            padding: 2mm;
        }}
        .hp-max-row {{
            display: flex;
            align-items: center;
            gap: 2mm;
            margin-bottom: 1mm;
            padding-bottom: 1mm;
            border-bottom: 1px solid var(--border-light);
        }}
        .hp-max-label {{ font-size: 5.5pt; font-weight: 700; text-transform: uppercase; }}
        .hp-max-value {{ flex: 1; font-size: 11pt; font-weight: 700; text-align: center; }}
        .hp-current {{
            min-height: 12mm;
            display: flex;
            align-items: center;
            justify-content: center;
            font-family: var(--font-display);
            font-size: 20pt;
            font-weight: 700;
        }}
        .hp-label {{
            font-size: 6pt;
            font-weight: 700;
            text-transform: uppercase;
            text-align: center;
            color: var(--text-secondary);
        }}
        .hp-temp {{
            border: var(--border-width) solid var(--border-dark);
            border-radius: var(--box-radius);
            background: var(--bg-box);
            padding: 2mm;
        }}
        .hp-temp-value {{
            min-height: 6mm;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 12pt;
            font-weight: 700;
        }}

        .hitdice-death-row {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 2mm;
        }}
        .hitdice-box, .death-box {{
            border: var(--border-width) solid var(--border-dark);
            border-radius: var(--box-radius);
            background: var(--bg-box);
            padding: 1.5mm;
        }}
        .hitdice-total {{ font-size: 5.5pt; color: var(--text-label); }}
        .hitdice-value {{
            font-size: 10pt;
            font-weight: 700;
            text-align: center;
            min-height: 6mm;
            display: flex;
            align-items: center;
            justify-content: center;
        }}
        .death-row {{
            display: flex;
            align-items: center;
            gap: 1mm;
            font-size: 6pt;
            margin-bottom: 1mm;
        }}
        .death-label {{ width: 12mm; }}
        .death-circles {{ display: flex; gap: 1mm; }}
        .death-circle {{
            width: 3.5mm;
            height: 3.5mm;
            border: 1px solid var(--border-dark);
            border-radius: 50%;
        }}

        .attacks-box {{
            border: var(--border-width) solid var(--border-dark);
            border-radius: var(--box-radius);
            background: var(--bg-box);
            padding: 1.5mm;
            flex: 1;
        }}
        .attack-header {{
            display: grid;
            grid-template-columns: 2fr 1fr 1.5fr;
            gap: 1mm;
            font-size: 5.5pt;
            font-weight: 700;
            text-transform: uppercase;
            color: var(--text-label);
            padding-bottom: 1mm;
            border-bottom: 1px solid var(--border-light);
            margin-bottom: 1mm;
        }}
        .attack-row {{
            display: grid;
            grid-template-columns: 2fr 1fr 1.5fr;
            gap: 1mm;
            padding: 0.5mm 0;
            font-size: 7pt;
            border-bottom: 1px solid #eee;
            min-height: 5mm;
        }}
        .attack-name {{ font-weight: 600; }}
        .attack-bonus {{ text-align: center; }}

        .personality-box {{
            border: var(--border-width) solid var(--border-dark);
            border-radius: var(--box-radius);
            background: var(--bg-box);
            padding: 2mm;
            flex: 1;
        }}
        .personality-section {{
            margin-bottom: 2mm;
            padding-bottom: 2mm;
            border-bottom: 1px solid var(--border-light);
        }}
        .personality-section:last-child {{
            margin-bottom: 0;
            padding-bottom: 0;
            border-bottom: none;
        }}
        .personality-label {{
            font-size: 6pt;
            font-weight: 700;
            text-transform: uppercase;
            color: var(--text-secondary);
            margin-bottom: 1mm;
        }}
        .personality-value {{
            font-size: 7pt;
            line-height: 1.3;
        }}

        .bottom-row {{
            display: grid;
            grid-template-columns: 1fr 1.3fr 1fr;
            gap: 2mm;
            margin-top: 2mm;
        }}
        .bottom-box {{
            border: var(--border-width) solid var(--border-dark);
            border-radius: var(--box-radius);
            background: var(--bg-box);
            padding: 2mm;
        }}
        .bottom-title {{
            font-size: 6pt;
            font-weight: 700;
            text-transform: uppercase;
            text-align: center;
            color: var(--text-secondary);
            padding-bottom: 1mm;
            border-bottom: 1px solid var(--border-light);
            margin-bottom: 1mm;
        }}
        .bottom-content {{
            font-size: 6.5pt;
            line-height: 1.3;
        }}

        .coin-row {{
            display: flex;
            justify-content: space-around;
            padding: 1mm 0;
            border-bottom: 1px solid var(--border-light);
            margin-bottom: 1mm;
        }}
        .coin {{ text-align: center; }}
        .coin-value {{
            width: 7mm;
            height: 5mm;
            border: 1px solid var(--border-dark);
            border-radius: 2px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 7pt;
            font-weight: 700;
            margin-bottom: 0.5mm;
        }}
        .coin-label {{
            font-size: 5pt;
            font-weight: 700;
            color: var(--text-label);
        }}

        /* Page 2 styles */
        .page2-grid {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 3mm;
            height: calc(100% - 45mm);
        }}
        .large-box {{
            border: var(--border-width) solid var(--border-dark);
            border-radius: var(--box-radius);
            background: var(--bg-box);
            padding: 2mm;
            margin-bottom: 2mm;
        }}
        .large-box.flex-1 {{ flex: 1; }}
        .large-box-title {{
            font-size: 6.5pt;
            font-weight: 700;
            text-transform: uppercase;
            text-align: center;
            color: var(--text-secondary);
            padding-bottom: 1mm;
            border-bottom: 1px solid var(--border-light);
            margin-bottom: 1mm;
        }}
        .large-box-content {{
            font-size: 7.5pt;
            line-height: 1.4;
        }}

        /* Page 3 styles */
        .spell-header {{
            display: grid;
            grid-template-columns: 2fr 1fr 1fr 1fr;
            gap: 2mm;
            margin-bottom: 3mm;
        }}
        .spell-grid {{
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 2mm;
        }}
        .spell-level-box {{
            border: var(--border-width) solid var(--border-dark);
            border-radius: var(--box-radius);
            background: var(--bg-box);
            padding: 2mm;
        }}
        .spell-level-header {{
            display: flex;
            align-items: center;
            gap: 2mm;
            margin-bottom: 1.5mm;
            padding-bottom: 1mm;
            border-bottom: 1px solid var(--border-light);
        }}
        .spell-level-num {{
            width: 7mm;
            height: 7mm;
            background: var(--border-dark);
            color: white;
            display: flex;
            align-items: center;
            justify-content: center;
            font-family: var(--font-display);
            font-size: 10pt;
            font-weight: 700;
            border-radius: 2px;
        }}
        .spell-slots {{
            display: flex;
            flex-direction: column;
            gap: 0.5mm;
            font-size: 5.5pt;
        }}
        .spell-slots-row {{
            display: flex;
            align-items: center;
            gap: 1mm;
        }}
        .spell-slot-box {{
            width: 5mm;
            height: 4mm;
            border: 1px solid var(--border-dark);
            border-radius: 2px;
            font-size: 6pt;
            font-weight: 700;
            display: flex;
            align-items: center;
            justify-content: center;
        }}
        .spell-list {{ font-size: 7pt; line-height: 1.4; }}
        .spell-item {{
            display: flex;
            align-items: center;
            gap: 1mm;
            padding: 0.3mm 0;
            min-height: 4mm;
            border-bottom: 1px solid #eee;
        }}
        .spell-prepared {{
            width: 2.5mm;
            height: 2.5mm;
            border: 1px solid var(--border-dark);
            border-radius: 50%;
        }}
        .spell-prepared.filled {{ background: var(--border-dark); }}
        .cantrip-box .spell-level-num {{ background: var(--accent-primary); }}
    </style>
</head>
<body>
    <!-- PAGE 1: Main Stats -->
    <div class="page">
        <div class="header-banner">
            <div class="header-title">Dungeons <span class="header-accent">&</span> Dragons</div>
        </div>

        <div class="char-info-row">
            <div class="info-field">
                <div class="info-value name">{data["character_name"]}</div>
                <div class="info-label">Character Name</div>
            </div>
            <div class="info-field">
                <div class="info-value">{data["class_level"]}</div>
                <div class="info-label">Class & Level</div>
            </div>
            <div class="info-field">
                <div class="info-value">{data["background"]}</div>
                <div class="info-label">Background</div>
            </div>
            <div class="info-field">
                <div class="info-value">{data["player_name"]}</div>
                <div class="info-label">Player Name</div>
            </div>
        </div>
        <div class="char-info-row">
            <div class="info-field">
                <div class="info-value">{data["race"]}</div>
                <div class="info-label">Race</div>
            </div>
            <div class="info-field">
                <div class="info-value">{data["alignment"]}</div>
                <div class="info-label">Alignment</div>
            </div>
            <div class="info-field">
                <div class="info-value">{data["experience_points"]}</div>
                <div class="info-label">Experience Points</div>
            </div>
            <div class="info-field"></div>
        </div>

        <div class="main-content">
            <div class="column">
                <div class="ability-block">{abilities_html}
                </div>
                <div class="stat-row">
                    <div class="stat-circle">{data["inspiration"]}</div>
                    <div class="stat-label">Inspiration</div>
                </div>
                <div class="stat-row">
                    <div class="stat-circle">{data["proficiency_bonus"]}</div>
                    <div class="stat-label">Proficiency Bonus</div>
                </div>
                <div class="saves-skills-box">
                    <div class="box-title">Saving Throws</div>{saves_html}
                </div>
                <div class="saves-skills-box" style="flex: 1;">
                    <div class="box-title">Skills</div>{skills_html}
                </div>
                <div class="passive-box">
                    <div class="passive-value">{data["passive_perception"]}</div>
                    <div class="passive-label">Passive Wisdom<br>(Perception)</div>
                </div>
            </div>

            <div class="column">
                <div class="combat-row">
                    <div class="combat-stat">
                        <div class="combat-value">{data["armor_class"]}</div>
                        <div class="combat-label">Armor Class</div>
                    </div>
                    <div class="combat-stat">
                        <div class="combat-value">{data["initiative"]}</div>
                        <div class="combat-label">Initiative</div>
                    </div>
                    <div class="combat-stat">
                        <div class="combat-value">{data["speed"]}</div>
                        <div class="combat-label">Speed</div>
                    </div>
                </div>
                <div class="hp-section">
                    <div class="hp-max-row">
                        <div class="hp-max-label">Hit Point Maximum</div>
                        <div class="hp-max-value">{data["hp_maximum"]}</div>
                    </div>
                    <div class="hp-current">{data["hp_current"]}</div>
                    <div class="hp-label">Current Hit Points</div>
                </div>
                <div class="hp-temp">
                    <div class="hp-temp-value">{data["hp_temporary"]}</div>
                    <div class="hp-label">Temporary Hit Points</div>
                </div>
                <div class="hitdice-death-row">
                    <div class="hitdice-box">
                        <div class="hitdice-total">Total: {data["hit_dice_total"]}</div>
                        <div class="hitdice-value">{data["hit_dice_current"]}</div>
                        <div class="box-title">Hit Dice</div>
                    </div>
                    <div class="death-box">
                        <div class="death-row">
                            <div class="death-label">Successes</div>
                            <div class="death-circles">
                                <div class="death-circle"></div>
                                <div class="death-circle"></div>
                                <div class="death-circle"></div>
                            </div>
                        </div>
                        <div class="death-row">
                            <div class="death-label">Failures</div>
                            <div class="death-circles">
                                <div class="death-circle"></div>
                                <div class="death-circle"></div>
                                <div class="death-circle"></div>
                            </div>
                        </div>
                        <div class="box-title">Death Saves</div>
                    </div>
                </div>
                <div class="attacks-box">
                    <div class="box-title">Attacks & Spellcasting</div>
                    <div class="attack-header">
                        <div>Name</div>
                        <div>Atk Bonus</div>
                        <div>Damage/Type</div>
                    </div>{attacks_html}
                </div>
            </div>

            <div class="column">
                <div class="personality-box">
                    <div class="personality-section">
                        <div class="personality-label">Personality Traits</div>
                        <div class="personality-value">{data["personality_traits"]}</div>
                    </div>
                    <div class="personality-section">
                        <div class="personality-label">Ideals</div>
                        <div class="personality-value">{data["ideals"]}</div>
                    </div>
                    <div class="personality-section">
                        <div class="personality-label">Bonds</div>
                        <div class="personality-value">{data["bonds"]}</div>
                    </div>
                    <div class="personality-section">
                        <div class="personality-label">Flaws</div>
                        <div class="personality-value">{data["flaws"]}</div>
                    </div>
                </div>
            </div>
        </div>

        <div class="bottom-row">
            <div class="bottom-box">
                <div class="bottom-title">Other Proficiencies & Languages</div>
                <div class="bottom-content">{prof_lang_html}</div>
            </div>
            <div class="bottom-box">
                <div class="bottom-title">Equipment</div>
                <div class="coin-row">
                    <div class="coin"><div class="coin-value">{data["currency"]["cp"]}</div><div class="coin-label">CP</div></div>
                    <div class="coin"><div class="coin-value">{data["currency"]["sp"]}</div><div class="coin-label">SP</div></div>
                    <div class="coin"><div class="coin-value">{data["currency"]["ep"]}</div><div class="coin-label">EP</div></div>
                    <div class="coin"><div class="coin-value">{data["currency"]["gp"]}</div><div class="coin-label">GP</div></div>
                    <div class="coin"><div class="coin-value">{data["currency"]["pp"]}</div><div class="coin-label">PP</div></div>
                </div>
                <div class="bottom-content">{equipment_html}</div>
            </div>
            <div class="bottom-box">
                <div class="bottom-title">Features & Traits</div>
                <div class="bottom-content">{features_html}</div>
            </div>
        </div>
    </div>

    <!-- PAGE 2: Background -->
    <div class="page">
        <div class="header-banner">
            <div class="header-title">Dungeons <span class="header-accent">&</span> Dragons</div>
        </div>

        <div class="char-info-row">
            <div class="info-field">
                <div class="info-value name">{data["character_name"]}</div>
                <div class="info-label">Character Name</div>
            </div>
            <div class="info-field">
                <div class="info-value">{data["appearance"]["age"]}</div>
                <div class="info-label">Age</div>
            </div>
            <div class="info-field">
                <div class="info-value">{data["appearance"]["height"]}</div>
                <div class="info-label">Height</div>
            </div>
            <div class="info-field">
                <div class="info-value">{data["appearance"]["weight"]}</div>
                <div class="info-label">Weight</div>
            </div>
        </div>
        <div class="char-info-row">
            <div class="info-field">
                <div class="info-value">{data["appearance"]["eyes"]}</div>
                <div class="info-label">Eyes</div>
            </div>
            <div class="info-field">
                <div class="info-value">{data["appearance"]["skin"]}</div>
                <div class="info-label">Skin</div>
            </div>
            <div class="info-field">
                <div class="info-value">{data["appearance"]["hair"]}</div>
                <div class="info-label">Hair</div>
            </div>
            <div class="info-field"></div>
        </div>

        <div class="page2-grid">
            <div class="column">
                <div class="large-box" style="min-height: 45mm;">
                    <div class="large-box-title">Character Appearance</div>
                    <div class="large-box-content">{data["character_appearance_description"]}</div>
                </div>
                <div class="large-box flex-1">
                    <div class="large-box-title">Character Backstory</div>
                    <div class="large-box-content">{data["backstory"]}</div>
                </div>
            </div>
            <div class="column">
                <div class="large-box" style="min-height: 60mm;">
                    <div class="large-box-title">Allies & Organizations</div>
                    <div style="font-weight: 600; margin-bottom: 2mm;">{data["allies_organizations"]["name"]}</div>
                    <div class="large-box-content">{data["allies_organizations"]["description"]}</div>
                </div>
                <div class="large-box">
                    <div class="large-box-title">Additional Features & Traits</div>
                    <div class="large-box-content">{additional_features_html}</div>
                </div>
                <div class="large-box flex-1">
                    <div class="large-box-title">Treasure</div>
                    <div class="large-box-content">{treasure_html}</div>
                </div>
            </div>
        </div>
    </div>

    <!-- PAGE 3: Spellcasting -->
    <div class="page">
        <div class="header-banner">
            <div class="header-title">Dungeons <span class="header-accent">&</span> Dragons</div>
        </div>

        <div class="spell-header">
            <div class="info-field">
                <div class="info-value">{data["spellcasting"]["class"]}</div>
                <div class="info-label">Spellcasting Class</div>
            </div>
            <div class="info-field">
                <div class="info-value">{data["spellcasting"]["ability"]}</div>
                <div class="info-label">Spellcasting Ability</div>
            </div>
            <div class="info-field">
                <div class="info-value">{data["spellcasting"]["spell_save_dc"]}</div>
                <div class="info-label">Spell Save DC</div>
            </div>
            <div class="info-field">
                <div class="info-value">{data["spellcasting"]["spell_attack_bonus"]}</div>
                <div class="info-label">Spell Attack Bonus</div>
            </div>
        </div>

        <div class="spell-grid">
            <div class="spell-level-box cantrip-box">
                <div class="spell-level-header">
                    <div class="spell-level-num">0</div>
                    <div style="font-size: 6.5pt; font-weight: 700; text-transform: uppercase;">Cantrips</div>
                </div>
                <div class="spell-list">{cantrips_html}
                </div>
            </div>
            {spell_levels_html}
        </div>
    </div>
</body>
</html>'''


def main():
    """Main entry point."""
    # Default to kazrek.json if no argument provided
    if len(sys.argv) > 1:
        json_path = Path(sys.argv[1])
    else:
        json_path = Path(__file__).parent / "kazrek.json"

    if not json_path.exists():
        print(f"Error: {json_path} not found")
        sys.exit(1)

    # Load character data
    with open(json_path, 'r', encoding='utf-8') as f:
        char_data = json.load(f)

    # Prepare template data
    template_data = prepare_template_data(char_data)

    # Generate HTML
    html = build_complete_html(template_data)

    # Output filename
    char_name = char_data.get("header", {}).get("character_name", "character")
    safe_name = char_name.replace(" ", "_")
    output_path = Path(__file__).parent / f"{safe_name}.html"

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)

    print(f"Generated: {output_path}")
    return output_path


if __name__ == "__main__":
    main()
