#!/usr/bin/env python3
"""
D&D 5e Character Sheet Generator v2
Generates HTML character sheets from JSON data files.
Uses external CSS for clean separation of concerns.
"""

import json
import sys
from pathlib import Path
from datetime import datetime


def load_css() -> str:
    """Load CSS from external file."""
    css_path = Path(__file__).parent / "styles" / "sheet.css"
    if css_path.exists():
        return css_path.read_text()
    else:
        raise FileNotFoundError(f"CSS file not found: {css_path}")


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
    meta = char_data.get("meta", {})

    return {
        # Meta
        "portrait": meta.get("portrait", ""),
        "gallery": meta.get("gallery", []),

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

        # Page 4 - Reference / Cheat Sheet
        "reference": char_data.get("reference", {}),
        "companion": char_data.get("companion", {}),

        # Meta
        "generated_date": datetime.now().strftime("%Y-%m-%d %H:%M")
    }


def build_html(data: dict) -> str:
    """Build the complete HTML document using external CSS and clean class structure."""

    # Load external CSS
    css = load_css()

    # =========================================================================
    # BUILD COMPONENT HTML
    # =========================================================================

    # Abilities
    abilities_html = ""
    for ability in data["abilities"]:
        abilities_html += f'''
                    <div class="box ability-score">
                        <div class="box__label">{ability["name"]}</div>
                        <div class="value--large">{ability["score"]}</div>
                        <div class="ability-modifier">{ability["modifier"]}</div>
                    </div>'''

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
    for _ in range(max(0, 5 - len(data["attacks"]))):
        attacks_html += '''
                    <div class="attack-row">
                        <div class="attack-name"></div>
                        <div class="attack-bonus"></div>
                        <div class="attack-damage"></div>
                    </div>'''

    # Proficiencies (as list)
    prof_items = "".join([f"<li>{item}</li>" for item in data["proficiencies_languages"]])
    prof_lang_html = f'<ul class="prof-list">{prof_items}</ul>'

    # Equipment (as list)
    equip_items = "".join([f"<li>{item}</li>" for item in data["equipment"]])
    equipment_html = f'<ul class="item-list">{equip_items}</ul>'

    # Features & Traits (as list)
    feature_items = "".join([f"<li>{item}</li>" for item in data["features_traits"]])
    features_html = f'<ul class="item-list">{feature_items}</ul>'

    # Additional Features & Traits (as list)
    add_feature_items = "".join([f"<li>{item}</li>" for item in data["additional_features_traits"]])
    additional_features_html = f'<ul class="item-list">{add_feature_items}</ul>'

    # Treasure (as list)
    treasure_items = "".join([f"<li>{item}</li>" for item in data["treasure"]])
    treasure_html = f'<ul class="item-list">{treasure_items}</ul>'

    # Convert backstory to paragraphs (split on \n\n or double newlines)
    backstory_text = data["backstory"]
    if backstory_text:
        paragraphs = [p.strip() for p in backstory_text.split('\n\n') if p.strip()]
        if not paragraphs:  # If no double newlines, try single
            paragraphs = [p.strip() for p in backstory_text.split('\n') if p.strip()]
        backstory_html = "".join([f"<p>{p}</p>" for p in paragraphs])
    else:
        backstory_html = ""

    # Character appearance as paragraphs
    appearance_text = data["character_appearance_description"]
    if appearance_text:
        app_paragraphs = [p.strip() for p in appearance_text.split('\n\n') if p.strip()]
        if not app_paragraphs:
            app_paragraphs = [p.strip() for p in appearance_text.split('\n') if p.strip()]
        if not app_paragraphs:
            app_paragraphs = [appearance_text]
        appearance_html = "".join([f"<p>{p}</p>" for p in app_paragraphs])
    else:
        appearance_html = ""

    # Allies description as paragraphs
    allies_desc = data["allies_organizations"].get("description", "")
    if allies_desc:
        allies_paragraphs = [p.strip() for p in allies_desc.split('\n\n') if p.strip()]
        if not allies_paragraphs:
            allies_paragraphs = [p.strip() for p in allies_desc.split('\n') if p.strip()]
        if not allies_paragraphs:
            allies_paragraphs = [allies_desc]
        allies_html = "".join([f"<p>{p}</p>" for p in allies_paragraphs])
    else:
        allies_html = ""

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
        for _ in range(max(0, 8 - len(level_data["spells"]))):
            spells_in_level += '''
                    <div class="spell-item">
                        <div class="spell-prepared"></div>
                        <span></span>
                    </div>'''

        spell_levels_html += f'''
            <div class="box spell-level-box">
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

    # =========================================================================
    # PAGE 1: GALLERY ROW
    # =========================================================================

    gallery_html = ""
    gallery_images = data.get("gallery", [])
    if gallery_images:
        gallery_items = ""
        for img_path in gallery_images:
            gallery_items += f'''
                        <div class="gallery-item">
                            <img src="{img_path}" alt="Character Art" class="gallery-img">
                        </div>'''
        gallery_html = f'''
                <div class="gallery-row">{gallery_items}
                </div>'''

    # =========================================================================
    # PAGE 4: REFERENCE / CHEAT SHEET
    # =========================================================================

    # Weapons reference
    weapons_html = ""
    for weapon in data.get("reference", {}).get("weapons", []):
        weapons_html += f'''
                    <div class="weapon-card">
                        <div class="weapon-name">{weapon["name"]}</div>
                        <div class="weapon-type">{weapon.get("type", "")}</div>
                        <div class="weapon-stats">
                            <span class="weapon-damage">{weapon.get("damage", "")}</span>
                        </div>
                        <div class="weapon-properties">{weapon.get("properties", "")}</div>
                        <div class="weapon-notes">{weapon.get("notes", "")}</div>
                    </div>'''

    # Spells reference
    spells_ref_html = ""
    for spell in data.get("reference", {}).get("spells", []):
        spells_ref_html += f'''
                    <div class="spell-card">
                        <div class="spell-name">{spell["name"]} <span class="spell-level-tag">({spell.get("level", "")})</span></div>
                        <div class="spell-meta">
                            <span><span class="spell-meta-label">Cast:</span> {spell.get("casting_time", "")}</span>
                            <span><span class="spell-meta-label">Range:</span> {spell.get("range", "")}</span>
                            <span><span class="spell-meta-label">Duration:</span> {spell.get("duration", "")}</span>
                        </div>
                        <div class="spell-desc">{spell.get("description", "")}</div>
                    </div>'''

    # Features reference
    features_ref_html = ""
    for feature in data.get("reference", {}).get("features", []):
        features_ref_html += f'''
                    <div class="feature-card">
                        <div class="feature-name">{feature["name"]}</div>
                        <div class="feature-desc">{feature.get("description", "")}</div>
                    </div>'''

    # Companion stat block
    companion = data.get("companion", {})
    companion_html = ""
    if companion:
        # Companion abilities
        comp_abilities = companion.get("abilities", {})
        comp_abilities_html = ""
        for ability in ["str", "dex", "con", "int", "wis", "cha"]:
            score = comp_abilities.get(ability, 10)
            mod = (score - 10) // 2
            mod_str = f"+{mod}" if mod >= 0 else str(mod)
            comp_abilities_html += f'''
                        <div class="companion-ability">
                            <div class="companion-ability-name">{ability.upper()}</div>
                            <div class="companion-ability-score">{score}</div>
                            <div class="companion-ability-mod">({mod_str})</div>
                        </div>'''

        # Companion traits
        comp_traits_html = ""
        for trait in companion.get("traits", []):
            comp_traits_html += f'''
                        <div class="companion-trait">
                            <span class="companion-trait-name">{trait["name"]}.</span>
                            <span class="companion-trait-desc">{trait.get("description", "")}</span>
                        </div>'''

        # Companion actions
        comp_actions_html = ""
        for action in companion.get("actions", []):
            comp_actions_html += f'''
                        <div class="companion-action">
                            <span class="companion-action-name">{action["name"]}.</span>
                            <span class="companion-action-desc">{action.get("description", "")}</span>
                        </div>'''

        # Companion commands
        comp_commands_html = ""
        for cmd in companion.get("commands", []):
            comp_commands_html += f"<li>{cmd}</li>"

        # Companion image
        companion_image = companion.get("image", "")
        companion_image_html = ""
        if companion_image:
            companion_image_html = f'''
                        <div class="companion-portrait">
                            <img src="{companion_image}" alt="{companion.get("name", "Companion")}" class="companion-img">
                        </div>'''

        companion_html = f'''
                <div class="box companion-block box--flex">
                    <div class="companion-header-row">
                        <div class="companion-header">
                            <div class="companion-name">{companion.get("name", "")}</div>
                            <div class="companion-type">{companion.get("size", "")} {companion.get("type", "")}</div>
                        </div>{companion_image_html}
                    </div>
                    <div class="companion-stats-row">
                        <div class="companion-stat"><span class="companion-stat-label">AC</span> {companion.get("armor_class", "")}</div>
                        <div class="companion-stat"><span class="companion-stat-label">HP</span> {companion.get("hit_points", "")} <span style="font-size: 6pt; color: #666;">({companion.get("hp_notes", "")})</span></div>
                        <div class="companion-stat"><span class="companion-stat-label">Speed</span> {companion.get("speed", "")}</div>
                    </div>
                    <div class="companion-abilities">{comp_abilities_html}
                    </div>
                    <div class="companion-stats-row">
                        <div class="companion-stat"><span class="companion-stat-label">Skills</span> {companion.get("skills", "")}</div>
                        <div class="companion-stat"><span class="companion-stat-label">Senses</span> {companion.get("senses", "")}</div>
                    </div>
                    <div class="companion-section">
                        <div class="companion-section-title">Traits</div>{comp_traits_html}
                    </div>
                    <div class="companion-section">
                        <div class="companion-section-title">Actions</div>{comp_actions_html}
                    </div>
                    <div class="companion-section">
                        <div class="companion-section-title">Beast Master Commands</div>
                        <ul class="companion-commands">{comp_commands_html}</ul>
                    </div>
                </div>'''

    # =========================================================================
    # COMPLETE HTML DOCUMENT
    # =========================================================================
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{data["character_name"]} - Character Sheet</title>
    <link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@400;500;600;700&family=Scada:wght@400;700&display=swap" rel="stylesheet">
    <style>
{css}
    </style>
</head>
<body>
    <!-- ================================================================
         PAGE 1: Main Stats
         ================================================================ -->
    <div class="page">
        <div class="page-header">
            <div class="header-left">
                <div class="header-brand">Dungeons & Dragons</div>
                <div class="header-name-row">
                    <div class="portrait-frame">
                        <img src="{data["portrait"]}" alt="Character Portrait" class="portrait-img">
                    </div>
                    <div class="box box--label-bottom header-name">
                        <div class="value--large">{data["character_name"]}</div>
                        <div class="box__label">Character Name</div>
                    </div>
                </div>
            </div>
            <div class="header-right">
                <div class="box box--label-bottom box--centered info-field">
                    <div class="value--medium">{data["class_level"]}</div>
                    <div class="box__label">Class & Level</div>
                </div>
                <div class="box box--label-bottom box--centered info-field">
                    <div class="value--medium">{data["background"]}</div>
                    <div class="box__label">Background</div>
                </div>
                <div class="box box--label-bottom box--centered info-field">
                    <div class="value--medium">{data["player_name"]}</div>
                    <div class="box__label">Player Name</div>
                </div>
                <div class="box box--label-bottom box--centered info-field">
                    <div class="value--medium">{data["race"]}</div>
                    <div class="box__label">Race</div>
                </div>
                <div class="box box--label-bottom box--centered info-field">
                    <div class="value--medium">{data["alignment"]}</div>
                    <div class="box__label">Alignment</div>
                </div>
                <div class="box box--label-bottom box--centered info-field">
                    <div class="value--medium">{data["experience_points"]}</div>
                    <div class="box__label">Experience Points</div>
                </div>
            </div>
        </div>

        <div class="main-content">
            <!-- LEFT COLUMN -->
            <div class="column">
                <div class="left-section">
                    <div class="abilities-column">
                        <div class="ability-block">{abilities_html}
                        </div>
                    </div>
                    <div class="stats-column">
                        <div class="box stat-row">
                            <div class="stat-circle">{data["inspiration"]}</div>
                            <div class="stat-label">Inspiration</div>
                        </div>
                        <div class="box stat-row">
                            <div class="stat-circle">{data["proficiency_bonus"]}</div>
                            <div class="stat-label">Proficiency Bonus</div>
                        </div>
                        <div class="box box--label-top saves-skills-box">
                            <div class="box__label">Saving Throws</div>{saves_html}
                        </div>
                        <div class="box box--label-top saves-skills-box box--flex">
                            <div class="box__label">Skills</div>{skills_html}
                        </div>
                    </div>
                </div>
                <div class="box passive-box">
                    <div class="passive-value">{data["passive_perception"]}</div>
                    <div class="passive-label">Passive Wisdom<br>(Perception)</div>
                </div>
                <div class="box box--label-bottom proficiencies-box">
                    {prof_lang_html}
                    <div class="box__label">Other Proficiencies & Languages</div>
                </div>
            </div>

            <!-- MIDDLE COLUMN -->
            <div class="column">
                <div class="combat-row">
                    <div class="box box--label-bottom combat-stat">
                        <div class="combat-value value--xlarge">{data["armor_class"]}</div>
                        <div class="box__label">Armor Class</div>
                    </div>
                    <div class="box box--label-bottom combat-stat">
                        <div class="combat-value value--xlarge">{data["initiative"]}</div>
                        <div class="box__label">Initiative</div>
                    </div>
                    <div class="box box--label-bottom combat-stat">
                        <div class="combat-value value--xlarge">{data["speed"]}</div>
                        <div class="box__label">Speed</div>
                    </div>
                </div>
                <div class="box box--label-bottom hp-section">
                    <div class="hp-max-row">
                        <div class="hp-max-label">Hit Point Maximum</div>
                        <div class="hp-max-value">{data["hp_maximum"]}</div>
                    </div>
                    <div class="hp-current">{data["hp_current"]}</div>
                    <div class="box__label">Current Hit Points</div>
                </div>
                <div class="box box--label-bottom hp-temp">
                    <div class="hp-temp-value">{data["hp_temporary"]}</div>
                    <div class="box__label">Temporary Hit Points</div>
                </div>
                <div class="hitdice-death-row">
                    <div class="box box--label-bottom hitdice-box">
                        <div class="hitdice-total">Total: {data["hit_dice_total"]}</div>
                        <div class="hitdice-value">{data["hit_dice_current"]}</div>
                        <div class="box__label">Hit Dice</div>
                    </div>
                    <div class="box box--label-bottom death-box">
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
                        <div class="box__label">Death Saves</div>
                    </div>
                </div>
                <div class="box box--label-top attacks-box">
                    <div class="box__label">Attacks & Spellcasting</div>
                    <div class="attack-header">
                        <div>Name</div>
                        <div>Atk Bonus</div>
                        <div>Damage/Type</div>
                    </div>{attacks_html}
                </div>
                <div class="box box--label-bottom equipment-box">
                    <div class="coin-row">
                        <div class="coin coin--cp"><div class="coin-icon">{data["currency"]["cp"]}</div><div class="coin-label">Copper</div></div>
                        <div class="coin coin--sp"><div class="coin-icon">{data["currency"]["sp"]}</div><div class="coin-label">Silver</div></div>
                        <div class="coin coin--ep"><div class="coin-icon">{data["currency"]["ep"]}</div><div class="coin-label">Electrum</div></div>
                        <div class="coin coin--gp"><div class="coin-icon">{data["currency"]["gp"]}</div><div class="coin-label">Gold</div></div>
                        <div class="coin coin--pp"><div class="coin-icon">{data["currency"]["pp"]}</div><div class="coin-label">Platinum</div></div>
                    </div>
                    <div class="box-content">{equipment_html}</div>
                    <div class="box__label">Equipment</div>
                </div>
            </div>

            <!-- RIGHT COLUMN - 5 Boxes -->
            <div class="column">
                <div class="box box--label-bottom trait-box">
                    <div class="trait-content">{data["personality_traits"]}</div>
                    <div class="box__label">Personality Traits</div>
                </div>
                <div class="box box--label-bottom trait-box">
                    <div class="trait-content">{data["ideals"]}</div>
                    <div class="box__label">Ideals</div>
                </div>
                <div class="box box--label-bottom trait-box">
                    <div class="trait-content">{data["bonds"]}</div>
                    <div class="box__label">Bonds</div>
                </div>
                <div class="box box--label-bottom trait-box">
                    <div class="trait-content">{data["flaws"]}</div>
                    <div class="box__label">Flaws</div>
                </div>
                <div class="box box--label-bottom trait-box box--flex">
                    <div class="trait-content">{features_html}</div>
                    <div class="box__label">Features & Traits</div>
                </div>
            </div>
        </div>{gallery_html}
    </div>

    <!-- ================================================================
         PAGE 2: Background
         ================================================================ -->
    <div class="page">
        <div class="page-header">
            <div class="header-left">
                <div class="header-brand">Dungeons & Dragons</div>
                <div class="box box--label-bottom header-name">
                    <div class="value--large">{data["character_name"]}</div>
                    <div class="box__label">Character Name</div>
                </div>
            </div>
            <div class="header-right">
                <div class="box box--label-bottom box--centered info-field">
                    <div class="value--medium">{data["appearance"]["age"]}</div>
                    <div class="box__label">Age</div>
                </div>
                <div class="box box--label-bottom box--centered info-field">
                    <div class="value--medium">{data["appearance"]["height"]}</div>
                    <div class="box__label">Height</div>
                </div>
                <div class="box box--label-bottom box--centered info-field">
                    <div class="value--medium">{data["appearance"]["weight"]}</div>
                    <div class="box__label">Weight</div>
                </div>
                <div class="box box--label-bottom box--centered info-field">
                    <div class="value--medium">{data["appearance"]["eyes"]}</div>
                    <div class="box__label">Eyes</div>
                </div>
                <div class="box box--label-bottom box--centered info-field">
                    <div class="value--medium">{data["appearance"]["skin"]}</div>
                    <div class="box__label">Skin</div>
                </div>
                <div class="box box--label-bottom box--centered info-field">
                    <div class="value--medium">{data["appearance"]["hair"]}</div>
                    <div class="box__label">Hair</div>
                </div>
            </div>
        </div>

        <div class="page2-content">
            <div class="page2-columns">
                <div class="column">
                    <div class="box box--label-top large-box" style="min-height: 45mm;">
                        <div class="box__label">Character Appearance</div>
                        <div class="large-box-content text-content">{appearance_html}</div>
                    </div>
                    <div class="box box--label-top large-box box--flex">
                        <div class="box__label">Character Backstory</div>
                        <div class="large-box-content text-content">{backstory_html}</div>
                    </div>
                </div>
                <div class="column">
                    <div class="box box--label-top large-box" style="min-height: 60mm;">
                        <div class="box__label">Allies & Organizations</div>
                        <div style="font-weight: 600; margin-bottom: 2mm;">{data["allies_organizations"]["name"]}</div>
                        <div class="large-box-content text-content">{allies_html}</div>
                    </div>
                    <div class="box box--label-top large-box">
                        <div class="box__label">Additional Features & Traits</div>
                        <div class="large-box-content">{additional_features_html}</div>
                    </div>
                    <div class="box box--label-top large-box box--flex">
                        <div class="box__label">Treasure</div>
                        <div class="large-box-content">{treasure_html}</div>
                    </div>
                </div>
            </div>
            <div class="page2-notes-row">
                <div class="box box--label-top large-box notes-box" style="min-height: 110mm;">
                    <div class="box__label">Notes</div>
                    <div class="notes-lines"></div>
                </div>
            </div>
        </div>
    </div>

    <!-- ================================================================
         PAGE 3: Spellcasting
         ================================================================ -->
    <div class="page">
        <div class="page-header">
            <div class="header-left">
                <div class="header-brand">Dungeons & Dragons</div>
                <div class="box box--label-bottom header-name">
                    <div class="value--large">{data["spellcasting"]["class"]}</div>
                    <div class="box__label">Spellcasting Class</div>
                </div>
            </div>
            <div class="header-right" style="grid-template-columns: repeat(3, 1fr); grid-template-rows: 1fr;">
                <div class="box box--label-bottom box--centered info-field">
                    <div class="value--medium">{data["spellcasting"]["ability"]}</div>
                    <div class="box__label">Spellcasting Ability</div>
                </div>
                <div class="box box--label-bottom box--centered info-field">
                    <div class="value--medium">{data["spellcasting"]["spell_save_dc"]}</div>
                    <div class="box__label">Spell Save DC</div>
                </div>
                <div class="box box--label-bottom box--centered info-field">
                    <div class="value--medium">{data["spellcasting"]["spell_attack_bonus"]}</div>
                    <div class="box__label">Spell Attack Bonus</div>
                </div>
            </div>
        </div>

        <div class="spell-grid">
            <div class="box spell-level-box cantrip-box">
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

    <!-- ================================================================
         PAGE 4: Reference / Cheat Sheet
         ================================================================ -->
    <div class="page">
        <div class="page-header">
            <div class="header-left">
                <div class="header-brand">Dungeons & Dragons</div>
                <div class="box box--label-bottom header-name">
                    <div class="value--large">Quick Reference</div>
                    <div class="box__label">{data["character_name"]}</div>
                </div>
            </div>
            <div class="header-right" style="grid-template-columns: repeat(3, 1fr); grid-template-rows: 1fr;">
                <div class="box box--label-bottom box--centered info-field">
                    <div class="value--medium">{data["class_level"]}</div>
                    <div class="box__label">Class & Level</div>
                </div>
                <div class="box box--label-bottom box--centered info-field">
                    <div class="value--medium">{data["proficiency_bonus"]}</div>
                    <div class="box__label">Proficiency Bonus</div>
                </div>
                <div class="box box--label-bottom box--centered info-field">
                    <div class="value--medium">{data["spellcasting"]["spell_save_dc"]}</div>
                    <div class="box__label">Spell Save DC</div>
                </div>
            </div>
        </div>

        <div class="page4-grid">
            <div class="column">
                <div class="box ref-box">
                    <div class="ref-section-title">Weapons</div>{weapons_html}
                </div>
                <div class="box ref-box box--flex">
                    <div class="ref-section-title">Spells</div>{spells_ref_html}
                </div>
            </div>
            <div class="column">
                <div class="box ref-box">
                    <div class="ref-section-title">Features & Abilities</div>{features_ref_html}
                </div>{companion_html}
            </div>
        </div>
    </div>
</body>
</html>'''


def main():
    """Main entry point."""
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
    html = build_html(template_data)

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
