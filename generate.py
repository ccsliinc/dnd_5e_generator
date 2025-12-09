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
from typing import Any

# =============================================================================
# HTML TEMPLATES - Module-level constants for reusability
# =============================================================================

TPL_ABILITY = '''
                    <div class="box ability-score">
                        <div class="box__label">{name}</div>
                        <div class="value--large">{score}</div>
                        <div class="ability-modifier">{modifier}</div>
                    </div>'''

TPL_SAVE_ROW = '''
                    <div class="save-row">
                        <div class="prof-circle {filled}"></div>
                        <div class="save-mod">{modifier}</div>
                        <div class="save-name">{name}</div>
                    </div>'''

TPL_SKILL_ROW = '''
                    <div class="skill-row">
                        <div class="prof-circle {filled}"></div>
                        <div class="skill-mod">{modifier}</div>
                        <div class="skill-name">{name} <span class="skill-ability">({ability})</span></div>
                    </div>'''

TPL_ATTACK_ROW = '''
                    <div class="attack-row">
                        <div class="attack-name">{name}</div>
                        <div class="attack-bonus">{atk_bonus}</div>
                        <div class="attack-damage">{damage_type}</div>
                    </div>'''

TPL_ATTACK_ROW_EMPTY = '''
                    <div class="attack-row">
                        <div class="attack-name"></div>
                        <div class="attack-bonus"></div>
                        <div class="attack-damage"></div>
                    </div>'''

TPL_SPELL_ITEM = '''
                    <div class="spell-item">
                        <div class="spell-prepared {filled}"></div>
                        <span>{name}</span>
                    </div>'''

TPL_SPELL_ITEM_EMPTY = '''
                    <div class="spell-item">
                        <div class="spell-prepared"></div>
                        <span></span>
                    </div>'''

TPL_GALLERY_ITEM = '''
                        <div class="gallery-item">
                            <img src="{src}" alt="Character Art" class="gallery-img">
                        </div>'''

TPL_WEAPON_CARD = '''
                    <div class="weapon-card ref-card">
                        <div class="weapon-name">{name}</div>
                        <div class="weapon-type">{type}</div>
                        <div class="weapon-stats">
                            <span class="weapon-damage">{damage}</span>
                        </div>
                        <div class="weapon-properties">{properties}</div>
                        <div class="weapon-notes">{notes}</div>
                    </div>'''

TPL_SPELL_CARD = '''
                    <div class="spell-card ref-card">
                        <div class="spell-name">{name} <span class="spell-level-tag">({level})</span></div>
                        <div class="spell-meta">
                            <span><span class="spell-meta-label">Cast:</span> {casting_time}</span>
                            <span><span class="spell-meta-label">Range:</span> {range}</span>
                            <span><span class="spell-meta-label">Duration:</span> {duration}</span>
                        </div>
                        <div class="spell-desc">{description}</div>
                    </div>'''

TPL_FEATURE_CARD = '''
                    <div class="feature-card ref-card">
                        <div class="feature-name">{name}</div>
                        <div class="feature-desc">{description}</div>
                    </div>'''

TPL_TURN_PHASE = '''
                        <div class="turn-phase">
                            <span class="turn-phase-name">{name}</span>
                            <span class="turn-phase-desc">{desc}</span>
                        </div>'''

TPL_COMBAT_ACTION = '''
                        <div class="combat-action">
                            <span class="combat-action-name">{name}</span>
                            <span class="combat-action-desc">{desc}</span>
                        </div>'''

TPL_COMBAT_CONDITION = '''
                        <div class="combat-condition">
                            <span class="combat-condition-name">{name}</span>
                            <span class="combat-condition-desc">{desc}</span>
                        </div>'''

TPL_COMBAT_COVER = '''
                        <div class="combat-cover">
                            <span class="combat-cover-type">{type}</span>
                            <span class="combat-cover-bonus">{bonus}</span>
                        </div>'''

TPL_COMPANION_ABILITY = '''
                        <div class="companion-ability">
                            <div class="companion-ability-name">{name}</div>
                            <div class="companion-ability-score">{score}</div>
                            <div class="companion-ability-mod">({mod})</div>
                        </div>'''

TPL_COMPANION_TRAIT = '''
                        <div class="companion-trait">
                            <span class="companion-trait-name">{name}.</span>
                            <span class="companion-trait-desc">{description}</span>
                        </div>'''

TPL_COMPANION_ACTION = '''
                        <div class="companion-action">
                            <span class="companion-action-name">{name}.</span>
                            <span class="companion-action-desc">{description}</span>
                        </div>'''


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def render_items(items: list[dict], template: str, empty_template: str = "",
                 min_rows: int = 0, **field_defaults) -> str:
    """
    Generic HTML list renderer with optional empty row padding.

    Args:
        items: List of dicts to render
        template: Template string with {field} placeholders
        empty_template: Template for empty rows (if different from template)
        min_rows: Minimum number of rows to render (pads with empty rows)
        **field_defaults: Default values for missing fields
    """
    html = ""
    for item in items:
        # Merge defaults with item data
        data = {**field_defaults, **item}
        html += template.format(**data)

    # Add empty rows if needed
    empty_count = max(0, min_rows - len(items))
    if empty_count > 0:
        tpl = empty_template or template
        for _ in range(empty_count):
            html += tpl.format(**field_defaults)

    return html


def render_list(items: list[str], css_class: str = "styled-list") -> str:
    """Convert list of strings to HTML unordered list."""
    if not items:
        return f'<ul class="{css_class}"></ul>'
    list_items = "".join([f"<li>{item}</li>" for item in items])
    return f'<ul class="{css_class}">{list_items}</ul>'


def text_to_paragraphs(text: str) -> str:
    """Convert text with newlines into HTML paragraphs."""
    if not text:
        return ""

    # Try double newlines first
    paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]

    # Fall back to single newlines
    if not paragraphs:
        paragraphs = [p.strip() for p in text.split('\n') if p.strip()]

    # Fall back to entire text as single paragraph
    if not paragraphs:
        paragraphs = [text.strip()]

    return "".join([f"<p>{p}</p>" for p in paragraphs])


def format_modifier(value: int) -> str:
    """Format a modifier value with +/- sign."""
    return f"+{value}" if value >= 0 else str(value)


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
    # BUILD COMPONENT HTML - Using helper functions and templates
    # =========================================================================

    # Abilities - using template
    abilities_html = render_items(data["abilities"], TPL_ABILITY)

    # Saving throws - add 'filled' field
    saves_with_filled = [
        {**s, "filled": "filled" if s["proficient"] else ""}
        for s in data["saving_throws"]
    ]
    saves_html = render_items(saves_with_filled, TPL_SAVE_ROW)

    # Skills - add 'filled' field
    skills_with_filled = [
        {**s, "filled": "filled" if s["proficient"] else ""}
        for s in data["skills"]
    ]
    skills_html = render_items(skills_with_filled, TPL_SKILL_ROW)

    # Attacks - with empty row padding
    attacks_html = render_items(
        data["attacks"], TPL_ATTACK_ROW,
        empty_template=TPL_ATTACK_ROW_EMPTY,
        min_rows=5,
        name="", atk_bonus="", damage_type=""
    )

    # Lists using render_list helper
    prof_lang_html = render_list(data["proficiencies_languages"], "styled-list prof-list")
    equipment_html = render_list(data["equipment"], "styled-list")
    features_html = render_list(data["features_traits"], "styled-list")
    additional_features_html = render_list(data["additional_features_traits"], "styled-list")
    treasure_html = render_list(data["treasure"], "styled-list")

    # Text content using text_to_paragraphs helper
    backstory_html = text_to_paragraphs(data["backstory"])
    appearance_html = text_to_paragraphs(data["character_appearance_description"])
    allies_html = text_to_paragraphs(data["allies_organizations"].get("description", ""))

    # Cantrips - simple list without prepared checkbox
    cantrips_html = "".join([
        f'<div class="spell-item"><span>{c}</span></div>'
        for c in data["spellcasting"]["cantrips"]
    ])

    # Spell levels - using templates
    spell_levels_html = ""
    for level_data in data["spellcasting"]["spell_levels"]:
        spells_with_filled = [
            {"name": s["name"], "filled": "filled" if s.get("prepared") else ""}
            for s in level_data["spells"]
        ]
        spells_in_level = render_items(
            spells_with_filled, TPL_SPELL_ITEM,
            empty_template=TPL_SPELL_ITEM_EMPTY,
            min_rows=8,
            name="", filled=""
        )
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

    gallery_images = data.get("gallery", [])
    if gallery_images:
        gallery_items = render_items(
            [{"src": img} for img in gallery_images],
            TPL_GALLERY_ITEM
        )
        gallery_html = f'''
                <div class="gallery-row">{gallery_items}
                </div>'''
    else:
        gallery_html = ""

    # =========================================================================
    # PAGE 4: REFERENCE / CHEAT SHEET - Using templates
    # =========================================================================

    reference = data.get("reference", {})

    # Weapons reference
    weapons_html = render_items(
        reference.get("weapons", []),
        TPL_WEAPON_CARD,
        type="", damage="", properties="", notes=""
    )

    # Spells reference
    spells_ref_html = render_items(
        reference.get("spells", []),
        TPL_SPELL_CARD,
        level="", casting_time="", range="", duration="", description=""
    )

    # Features reference
    features_ref_html = render_items(
        reference.get("features", []),
        TPL_FEATURE_CARD,
        description=""
    )

    # Companion stat block - using templates
    companion = data.get("companion", {})
    companion_html = ""
    if companion:
        # Companion abilities
        comp_abilities = companion.get("abilities", {})
        ability_items = []
        for ability in ["str", "dex", "con", "int", "wis", "cha"]:
            score = comp_abilities.get(ability, 10)
            mod = (score - 10) // 2
            ability_items.append({
                "name": ability.upper(),
                "score": score,
                "mod": format_modifier(mod)
            })
        comp_abilities_html = render_items(ability_items, TPL_COMPANION_ABILITY)

        # Companion traits and actions - using templates
        comp_traits_html = render_items(
            companion.get("traits", []), TPL_COMPANION_TRAIT, description=""
        )
        comp_actions_html = render_items(
            companion.get("actions", []), TPL_COMPANION_ACTION, description=""
        )

        # Companion commands - simple list
        comp_commands_html = "".join([f"<li>{cmd}</li>" for cmd in companion.get("commands", [])])

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
    # TURN STRUCTURE & COMBAT REFERENCE - Using templates
    # =========================================================================

    # Turn structure
    turn_structure = reference.get("turn_structure", {})
    turn_html = ""
    if turn_structure:
        phases_html = render_items(turn_structure.get("phases", []), TPL_TURN_PHASE)
        turn_html = f'''
                <div class="box ref-box turn-box">
                    <div class="ref-section-title">{turn_structure.get("title", "Your Turn")}</div>{phases_html}
                    <div class="turn-reaction">
                        <span class="turn-phase-name">Reaction</span>
                        <span class="turn-phase-desc">{turn_structure.get("reaction", "")}</span>
                    </div>
                </div>'''

    # Combat reference (actions, conditions, cover)
    combat_ref = reference.get("combat_reference", {})
    combat_html = ""
    if combat_ref:
        actions_html = render_items(combat_ref.get("actions", []), TPL_COMBAT_ACTION)
        conditions_html = render_items(combat_ref.get("conditions_quick", []), TPL_COMBAT_CONDITION)
        cover_html = render_items(combat_ref.get("cover", []), TPL_COMBAT_COVER)

        combat_html = f'''
                <div class="box ref-box combat-ref-box">
                    <div class="ref-section-title">Actions</div>{actions_html}
                    <div class="ref-section-title" style="margin-top: 2mm;">Conditions</div>{conditions_html}
                    <div class="ref-section-title" style="margin-top: 2mm;">Cover</div>{cover_html}
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

            <!-- RIGHT COLUMN - 6 Boxes -->
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
                <div class="box box--label-bottom trait-box">
                    <div class="trait-content">{features_html}</div>
                    <div class="box__label">Features & Traits</div>
                </div>
                <div class="box box--label-top notes-box box--flex">
                    <div class="box__label">Notes</div>
                    <div class="notes-lines"></div>
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
            <div class="box spell-level-box notes-box">
                <div class="box__label" style="font-size: 6.5pt; font-weight: 700; text-transform: uppercase; color: var(--accent-primary);">Notes</div>
                <div class="notes-lines"></div>
            </div>
            <div class="box spell-level-box notes-box">
                <div class="box__label" style="font-size: 6.5pt; font-weight: 700; text-transform: uppercase; color: var(--accent-primary);">Notes</div>
                <div class="notes-lines"></div>
            </div>
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
            <div class="column">{turn_html}{combat_html}
                <div class="box ref-box box--flex">
                    <div class="ref-section-title">Weapons</div>{weapons_html}
                </div>
            </div>
            <div class="column">
                <div class="box ref-box">
                    <div class="ref-section-title">Spells</div>{spells_ref_html}
                </div>{companion_html}
            </div>
        </div>
    </div>
</body>
</html>'''


def main():
    """Main entry point."""
    base_dir = Path(__file__).parent
    characters_dir = base_dir / "characters"
    output_dir = base_dir / "output"

    # Ensure output directory exists
    output_dir.mkdir(exist_ok=True)

    if len(sys.argv) > 1:
        # Allow full path or just filename
        arg = sys.argv[1]
        json_path = Path(arg)
        if not json_path.exists():
            # Try in characters folder
            json_path = characters_dir / arg
    else:
        # Default to first JSON in characters folder
        json_files = list(characters_dir.glob("*.json"))
        if json_files:
            json_path = json_files[0]
        else:
            print("Error: No character files found in characters/")
            sys.exit(1)

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

    # Output to output/ folder
    char_name = char_data.get("header", {}).get("character_name", "character")
    safe_name = char_name.replace(" ", "_")
    output_path = output_dir / f"{safe_name}.html"

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)

    print(f"Generated: {output_path}")
    return output_path


if __name__ == "__main__":
    main()
