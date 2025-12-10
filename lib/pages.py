"""
Page Builders

Specialized page builders for different page types in character sheets.
Each builder creates a complete page with its specific layout and content.
"""

from abc import ABC, abstractmethod
from typing import Optional
from .components import Row, Col, Grid
from .renderers import render_content


# =============================================================================
# BASE PAGE BUILDER
# =============================================================================

class PageBuilder(ABC):
    """Base class for page builders."""

    def __init__(self, data: dict, context: dict = None):
        self.data = data
        self.context = context or {}

    @abstractmethod
    def build(self) -> str:
        """Build and return the page HTML."""
        pass

    def _box(self, content: str, classes: str = "", label: str = "",
             label_position: str = "bottom", style: str = "") -> str:
        """Create a box element with optional label."""
        class_list = ["box"]
        if label:
            class_list.append(f"box--label-{label_position}")
        if classes:
            class_list.extend(classes.split())

        class_str = " ".join(class_list)
        style_attr = f' style="{style}"' if style else ""

        label_html = f'<div class="box__label">{label}</div>' if label else ""

        return f'<div class="{class_str}"{style_attr}>{content}{label_html}</div>'


# =============================================================================
# REFERENCE PAGE (Page 4 - Quick Reference / Cheat Sheet)
# =============================================================================

class ReferencePage(PageBuilder):
    """
    Quick Reference / Cheat Sheet page.

    Contains:
    - Turn structure reference
    - Combat actions reference
    - Weapon cards
    - Spell cards
    - Companion stat block (optional)
    """

    def build(self) -> str:
        """Build the reference page."""
        reference = self.data.get("reference", {})
        spellcasting = self.data.get("spellcasting", {})
        header = self.context.get("header", {})
        prof_bonus = self.context.get("prof_bonus", 2)

        # Build header
        header_html = self._build_header(header, spellcasting, prof_bonus)

        # Build content sections
        left_col = self._build_left_column(reference)
        right_col = self._build_right_column(reference)

        return f'''
    <!-- PAGE 4: Reference / Cheat Sheet -->
    <div class="page">
        {header_html}

        <div class="page4-grid">
            {left_col}
            {right_col}
        </div>
    </div>'''

    def _build_header(self, header: dict, spellcasting: dict, prof_bonus: int) -> str:
        """Build the reference page header."""
        return f'''
        <div class="page-header">
            <div class="header-left">
                <div class="header-brand">Dungeons & Dragons</div>
                <div class="box box--label-bottom header-name">
                    <div class="value--large">Quick Reference</div>
                    <div class="box__label">{header.get("character_name", "")}</div>
                </div>
            </div>
            <div class="header-right" style="grid-template-columns: repeat(3, 1fr); grid-template-rows: 1fr;">
                <div class="box box--label-bottom box--centered info-field">
                    <div class="value--medium">{header.get("class_level", "")}</div>
                    <div class="box__label">Class & Level</div>
                </div>
                <div class="box box--label-bottom box--centered info-field">
                    <div class="value--medium">+{prof_bonus}</div>
                    <div class="box__label">Proficiency Bonus</div>
                </div>
                <div class="box box--label-bottom box--centered info-field">
                    <div class="value--medium">{spellcasting.get("spell_save_dc", "")}</div>
                    <div class="box__label">Spell Save DC</div>
                </div>
            </div>
        </div>'''

    def _build_left_column(self, reference: dict) -> str:
        """Build the left column with turn structure, combat ref, and weapons."""
        parts = []

        # Turn structure
        turn_structure = reference.get("turn_structure", {})
        if turn_structure:
            parts.append(render_content({
                "type": "turn_structure",
                **turn_structure
            }))

        # Combat reference
        combat_ref = reference.get("combat_reference", {})
        if combat_ref:
            parts.append(render_content({
                "type": "combat_reference",
                **combat_ref
            }))

        # Weapons
        weapons_html = render_content({
            "type": "weapon_card",
            "weapons": reference.get("weapons", [])
        })
        weapons_box = f'''
                <div class="box ref-box box--flex">
                    <div class="ref-section-title">Weapons</div>{weapons_html}
                </div>'''
        parts.append(weapons_box)

        return f'''
            <div class="column">{"".join(parts)}
            </div>'''

    def _build_right_column(self, reference: dict) -> str:
        """Build the right column with spells and companion."""
        parts = []

        # Spells
        spells_html = render_content({
            "type": "spell_card",
            "spells": reference.get("spells", [])
        })
        spells_box = f'''
                <div class="box ref-box">
                    <div class="ref-section-title">Spells</div>{spells_html}
                </div>'''
        parts.append(spells_box)

        # Companion (if present)
        companion = self.data.get("companion", {})
        if companion:
            companion_html = render_content({
                "type": "companion",
                "companion": companion
            })
            parts.append(companion_html)

        return f'''
            <div class="column">{"".join(parts)}
            </div>'''


# =============================================================================
# STATS PAGE (Page 1 - Main Stats)
# =============================================================================

class StatsPage(PageBuilder):
    """
    Main Stats page (Page 1).

    Contains:
    - Character header with portrait
    - Ability scores
    - Saving throws and skills
    - Combat stats (AC, Initiative, Speed)
    - HP and death saves
    - Attacks and equipment
    - Personality traits
    - Gallery
    """

    def build(self) -> str:
        """Build the stats page."""
        # Get context values
        header = self.context.get("header", {})
        abilities = self.context.get("abilities", {})
        prof_bonus = self.context.get("prof_bonus", 2)
        ability_mods = self.context.get("ability_mods", {})
        meta = self.data.get("meta", {})
        combat = self.data.get("combat", {})
        personality = self.data.get("personality", {})

        # Build page header
        page_header = self._build_page_header(header, meta.get("portrait", ""))

        # Build sections
        left_section = self._build_left_section(abilities, ability_mods, prof_bonus)
        middle_section = self._build_middle_section(combat, ability_mods)
        right_section = self._build_right_section(personality)

        # Gallery
        gallery_html = render_content({
            "type": "gallery",
            "images": meta.get("gallery", [])
        })

        return f'''
    <!-- PAGE 1: Main Stats -->
    <div class="page">
        {page_header}

        <div class="main-content">
            {left_section}
            {middle_section}
            {right_section}
        </div>{gallery_html}
    </div>'''

    def _build_page_header(self, header: dict, portrait: str) -> str:
        """Build the page 1 header with portrait and info fields."""
        portrait_html = ""
        if portrait:
            portrait_html = f'''
                    <div class="portrait-frame">
                        <img src="{portrait}" alt="Character Portrait" class="portrait-img">
                    </div>'''

        return f'''
        <div class="page-header">
            <div class="header-left">
                <div class="header-brand">Dungeons & Dragons</div>
                <div class="header-name-row">{portrait_html}
                <div class="box box--label-bottom header-name">
                    <div class="value--large">{header.get("character_name", "")}</div>
                    <div class="box__label">Character Name</div>
                </div>
                </div>
            </div>
            <div class="header-right">
                <div class="box box--label-bottom box--centered info-field">
                    <div class="value--medium">{header.get("class_level", "")}</div>
                    <div class="box__label">Class & Level</div>
                </div>
                <div class="box box--label-bottom box--centered info-field">
                    <div class="value--medium">{header.get("background", "")}</div>
                    <div class="box__label">Background</div>
                </div>
                <div class="box box--label-bottom box--centered info-field">
                    <div class="value--medium">{header.get("player_name", "")}</div>
                    <div class="box__label">Player Name</div>
                </div>
                <div class="box box--label-bottom box--centered info-field">
                    <div class="value--medium">{header.get("race", "")}</div>
                    <div class="box__label">Race</div>
                </div>
                <div class="box box--label-bottom box--centered info-field">
                    <div class="value--medium">{header.get("alignment", "")}</div>
                    <div class="box__label">Alignment</div>
                </div>
                <div class="box box--label-bottom box--centered info-field">
                    <div class="value--medium">{header.get("experience_points", "")}</div>
                    <div class="box__label">Experience Points</div>
                </div>
            </div>
        </div>'''

    def _build_left_section(self, abilities: dict, ability_mods: dict, prof_bonus: int) -> str:
        """Build left column with abilities, saves, skills, proficiencies."""
        # Ability scores
        abilities_html = self._render_abilities(abilities, ability_mods)

        # Saves and Skills
        saves_html = self._render_saves(ability_mods, prof_bonus)
        skills_html = self._render_skills(ability_mods, prof_bonus)

        # Passive perception
        passive = self._calculate_passive_perception(ability_mods, prof_bonus)

        # Proficiencies
        prof_lang_html = render_content({
            "type": "styled_list",
            "items": self.data.get("proficiencies_languages", []),
            "class": "styled-list prof-list"
        })

        # Inspiration
        inspiration = "X" if self.data.get("inspiration") else ""

        return f'''
            <!-- LEFT COLUMN -->
            <div class="column">
                <div class="left-section">
                    <div class="abilities-column">
                        {abilities_html}
                    </div>
                    <div class="stats-column">
                        <div class="box stat-row">
                            <div class="stat-circle">{inspiration}</div>
                            <div class="stat-label">Inspiration</div>
                        </div>
                        <div class="box stat-row">
                            <div class="stat-circle">+{prof_bonus}</div>
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
                    <div class="passive-value">{passive}</div>
                    <div class="passive-label">Passive Wisdom<br>(Perception)</div>
                </div>
                <div class="box box--label-bottom proficiencies-box">
                    {prof_lang_html}
                    <div class="box__label">Other Proficiencies & Languages</div>
                </div>
            </div>'''

    def _build_middle_section(self, combat: dict, ability_mods: dict) -> str:
        """Build middle column with combat stats, HP, attacks, equipment."""
        dex_mod = ability_mods.get("dexterity", 0)
        initiative = combat.get("initiative") or self._format_modifier(dex_mod)

        # Attacks
        attacks_html = render_content({
            "type": "attacks",
            "attacks": self.data.get("attacks", []),
            "min_rows": 5
        })

        # Equipment
        equipment_html = render_content({
            "type": "styled_list",
            "items": self.data.get("equipment", []),
            "class": "styled-list"
        })

        # Currency
        currency_html = render_content({
            "type": "currency",
            "currency": self.data.get("currency", {})
        })

        return f'''
            <!-- MIDDLE COLUMN -->
            <div class="column">
                <div class="combat-row">
                    <div class="box box--label-bottom combat-stat">
                        <div class="combat-value value--xlarge">{combat.get("armor_class", "")}</div>
                        <div class="box__label">Armor Class</div>
                    </div>
                    <div class="box box--label-bottom combat-stat">
                        <div class="combat-value value--xlarge">{initiative}</div>
                        <div class="box__label">Initiative</div>
                    </div>
                    <div class="box box--label-bottom combat-stat">
                        <div class="combat-value value--xlarge">{combat.get("speed", "")}</div>
                        <div class="box__label">Speed</div>
                    </div>
                </div>
                <div class="box box--label-bottom hp-section">
                    <div class="hp-max-row">
                        <div class="hp-max-label">Hit Point Maximum</div>
                        <div class="hp-max-value">{combat.get("hp_maximum", "")}</div>
                    </div>
                    <div class="hp-current">{combat.get("hp_current") or ""}</div>
                    <div class="box__label">Current Hit Points</div>
                </div>
                <div class="box box--label-bottom hp-temp">
                    <div class="hp-temp-value">{combat.get("hp_temporary") or ""}</div>
                    <div class="box__label">Temporary Hit Points</div>
                </div>
                <div class="hitdice-death-row">
                    <div class="box box--label-bottom hitdice-box">
                        <div class="hitdice-total">Total: {combat.get("hit_dice", {}).get("total", "")}</div>
                        <div class="hitdice-value">{combat.get("hit_dice", {}).get("current") or ""}</div>
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
                    {currency_html}
                    <div class="box-content">{equipment_html}</div>
                    <div class="box__label">Equipment</div>
                </div>
            </div>'''

    def _build_right_section(self, personality: dict) -> str:
        """Build right column with personality traits, features, notes."""
        features_html = render_content({
            "type": "styled_list",
            "items": self.data.get("features_traits", []),
            "class": "styled-list"
        })

        return f'''
            <!-- RIGHT COLUMN -->
            <div class="column">
                <div class="box box--label-bottom trait-box">
                    <div class="trait-content">{personality.get("traits", "")}</div>
                    <div class="box__label">Personality Traits</div>
                </div>
                <div class="box box--label-bottom trait-box">
                    <div class="trait-content">{personality.get("ideals", "")}</div>
                    <div class="box__label">Ideals</div>
                </div>
                <div class="box box--label-bottom trait-box">
                    <div class="trait-content">{personality.get("bonds", "")}</div>
                    <div class="box__label">Bonds</div>
                </div>
                <div class="box box--label-bottom trait-box">
                    <div class="trait-content">{personality.get("flaws", "")}</div>
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
            </div>'''

    def _render_abilities(self, abilities: dict, ability_mods: dict) -> str:
        """Render ability score boxes."""
        ability_order = ["strength", "dexterity", "constitution", "intelligence", "wisdom", "charisma"]
        abilities_list = []
        for ability in ability_order:
            data = abilities.get(ability, {"score": 10})
            score = data.get("score", 10)
            mod = (score - 10) // 2
            abilities_list.append({
                "name": ability[:3].upper(),
                "score": score,
                "modifier": self._format_modifier(mod)
            })

        return render_content({
            "type": "ability_scores",
            "abilities": abilities_list
        })

    def _render_saves(self, ability_mods: dict, prof_bonus: int) -> str:
        """Render saving throw rows."""
        saves_data = self.data.get("saving_throws", {})
        ability_order = ["strength", "dexterity", "constitution", "intelligence", "wisdom", "charisma"]
        saves_list = []

        for ability in ability_order:
            save = saves_data.get(ability, {"proficient": False})
            is_prof = save.get("proficient", False)
            mod = ability_mods.get(ability, 0)
            if is_prof:
                mod += prof_bonus
            saves_list.append({
                "name": ability.capitalize(),
                "proficient": is_prof,
                "modifier": self._format_modifier(mod)
            })

        return render_content({
            "type": "saving_throws",
            "saves": saves_list
        })

    def _render_skills(self, ability_mods: dict, prof_bonus: int) -> str:
        """Render skill rows."""
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
        skill_order = [
            "acrobatics", "animal_handling", "arcana", "athletics", "deception",
            "history", "insight", "intimidation", "investigation", "medicine",
            "nature", "perception", "performance", "persuasion", "religion",
            "sleight_of_hand", "stealth", "survival"
        ]

        skills_data = self.data.get("skills", {})
        skills_list = []

        for skill in skill_order:
            skill_info = skills_data.get(skill, {"proficient": False})
            is_prof = skill_info.get("proficient", False)
            ability_abbr, ability_name = skill_abilities.get(skill, ("???", "strength"))
            mod = ability_mods.get(ability_name, 0)
            if is_prof:
                mod += prof_bonus
            skills_list.append({
                "name": skill.replace("_", " ").title(),
                "ability": ability_abbr,
                "proficient": is_prof,
                "modifier": self._format_modifier(mod)
            })

        return render_content({
            "type": "skills",
            "skills": skills_list
        })

    def _calculate_passive_perception(self, ability_mods: dict, prof_bonus: int) -> int:
        """Calculate passive perception."""
        skills_data = self.data.get("skills", {})
        perception = skills_data.get("perception", {"proficient": False})
        mod = ability_mods.get("wisdom", 0)
        if perception.get("proficient", False):
            mod += prof_bonus
        return 10 + mod

    def _format_modifier(self, value: int) -> str:
        """Format modifier with +/- sign."""
        return f"+{value}" if value >= 0 else str(value)


# =============================================================================
# BACKGROUND PAGE (Page 2)
# =============================================================================

class BackgroundPage(PageBuilder):
    """
    Background page (Page 2).

    Contains:
    - Character appearance details
    - Character backstory
    - Allies and organizations
    - Additional features and traits
    - Treasure
    - Notes section
    """

    def build(self) -> str:
        """Build the background page."""
        header = self.context.get("header", {})
        appearance = self.data.get("appearance", {})
        allies = self.data.get("allies_organizations", {})

        # Build page header
        page_header = self._build_page_header(header, appearance)

        # Build content
        left_col = self._build_left_column(appearance)
        right_col = self._build_right_column(allies)

        return f'''
    <!-- PAGE 2: Background -->
    <div class="page">
        {page_header}

        <div class="page2-content">
            <div class="page2-columns">
                {left_col}
                {right_col}
            </div>
            <div class="page2-notes-row">
                <div class="box box--label-top large-box notes-box" style="min-height: 110mm;">
                    <div class="box__label">Notes</div>
                    <div class="notes-lines"></div>
                </div>
            </div>
        </div>
    </div>'''

    def _build_page_header(self, header: dict, appearance: dict) -> str:
        """Build the page 2 header with appearance fields."""
        return f'''
        <div class="page-header">
            <div class="header-left">
                <div class="header-brand">Dungeons & Dragons</div>
                <div class="box box--label-bottom header-name">
                    <div class="value--large">{header.get("character_name", "")}</div>
                    <div class="box__label">Character Name</div>
                </div>
            </div>
            <div class="header-right">
                <div class="box box--label-bottom box--centered info-field">
                    <div class="value--medium">{appearance.get("age", "")}</div>
                    <div class="box__label">Age</div>
                </div>
                <div class="box box--label-bottom box--centered info-field">
                    <div class="value--medium">{appearance.get("height", "")}</div>
                    <div class="box__label">Height</div>
                </div>
                <div class="box box--label-bottom box--centered info-field">
                    <div class="value--medium">{appearance.get("weight", "")}</div>
                    <div class="box__label">Weight</div>
                </div>
                <div class="box box--label-bottom box--centered info-field">
                    <div class="value--medium">{appearance.get("eyes", "")}</div>
                    <div class="box__label">Eyes</div>
                </div>
                <div class="box box--label-bottom box--centered info-field">
                    <div class="value--medium">{appearance.get("skin", "")}</div>
                    <div class="box__label">Skin</div>
                </div>
                <div class="box box--label-bottom box--centered info-field">
                    <div class="value--medium">{appearance.get("hair", "")}</div>
                    <div class="box__label">Hair</div>
                </div>
            </div>
        </div>'''

    def _build_left_column(self, appearance: dict) -> str:
        """Build left column with appearance and backstory."""
        appearance_html = render_content({
            "type": "paragraphs",
            "text": self.data.get("character_appearance_description", ""),
            "class": "text-content"
        })
        backstory_html = render_content({
            "type": "paragraphs",
            "text": self.data.get("backstory", ""),
            "class": "text-content"
        })

        return f'''
                <div class="column">
                    <div class="box box--label-top large-box" style="min-height: 45mm;">
                        <div class="box__label">Character Appearance</div>
                        <div class="large-box-content">{appearance_html}</div>
                    </div>
                    <div class="box box--label-top large-box box--flex">
                        <div class="box__label">Character Backstory</div>
                        <div class="large-box-content">{backstory_html}</div>
                    </div>
                </div>'''

    def _build_right_column(self, allies: dict) -> str:
        """Build right column with allies, features, treasure."""
        allies_html = render_content({
            "type": "paragraphs",
            "text": allies.get("description", ""),
            "class": "text-content"
        })
        additional_features = render_content({
            "type": "styled_list",
            "items": self.data.get("additional_features_traits", [])
        })
        treasure = render_content({
            "type": "styled_list",
            "items": self.data.get("treasure", [])
        })

        return f'''
                <div class="column">
                    <div class="box box--label-top large-box" style="min-height: 60mm;">
                        <div class="box__label">Allies & Organizations</div>
                        <div style="font-weight: 600; margin-bottom: 2mm;">{allies.get("name", "")}</div>
                        <div class="large-box-content">{allies_html}</div>
                    </div>
                    <div class="box box--label-top large-box">
                        <div class="box__label">Additional Features & Traits</div>
                        <div class="large-box-content">{additional_features}</div>
                    </div>
                    <div class="box box--label-top large-box box--flex">
                        <div class="box__label">Treasure</div>
                        <div class="large-box-content">{treasure}</div>
                    </div>
                </div>'''


# =============================================================================
# SPELLCASTING PAGE (Page 3)
# =============================================================================

class SpellcastingPage(PageBuilder):
    """
    Spellcasting page (Page 3).

    Contains:
    - Spellcasting class and ability
    - Spell save DC and attack bonus
    - Cantrips
    - Spell levels 1-9 with slots and known spells
    - Notes sections
    """

    def build(self) -> str:
        """Build the spellcasting page."""
        spellcasting = self.data.get("spellcasting", {})
        spells_data = spellcasting.get("spells", {})

        # Build header
        page_header = self._build_page_header(spellcasting)

        # Build cantrips
        cantrips_html = self._build_cantrips(spellcasting.get("cantrips", []))

        # Build spell levels
        spell_levels_html = ""
        for level in range(1, 10):
            level_str = str(level)
            level_data = spells_data.get(level_str, {"slots_total": 0, "slots_expended": 0, "known": []})
            spell_levels_html += render_content({
                "type": "spell_level",
                "level": level,
                "slots_total": level_data.get("slots_total", 0),
                "slots_expended": level_data.get("slots_expended", 0),
                "spells": level_data.get("known", []),
                "min_rows": 8
            })

        return f'''
    <!-- PAGE 3: Spellcasting -->
    <div class="page">
        {page_header}

        <div class="spell-grid">
            {cantrips_html}
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
    </div>'''

    def _build_page_header(self, spellcasting: dict) -> str:
        """Build the spellcasting page header."""
        return f'''
        <div class="page-header">
            <div class="header-left">
                <div class="header-brand">Dungeons & Dragons</div>
                <div class="box box--label-bottom header-name">
                    <div class="value--large">{spellcasting.get("class", "")}</div>
                    <div class="box__label">Spellcasting Class</div>
                </div>
            </div>
            <div class="header-right" style="grid-template-columns: repeat(3, 1fr); grid-template-rows: 1fr;">
                <div class="box box--label-bottom box--centered info-field">
                    <div class="value--medium">{spellcasting.get("ability", "")}</div>
                    <div class="box__label">Spellcasting Ability</div>
                </div>
                <div class="box box--label-bottom box--centered info-field">
                    <div class="value--medium">{spellcasting.get("spell_save_dc", "")}</div>
                    <div class="box__label">Spell Save DC</div>
                </div>
                <div class="box box--label-bottom box--centered info-field">
                    <div class="value--medium">{spellcasting.get("spell_attack_bonus", "")}</div>
                    <div class="box__label">Spell Attack Bonus</div>
                </div>
            </div>
        </div>'''

    def _build_cantrips(self, cantrips: list) -> str:
        """Build the cantrips box."""
        cantrips_html = "".join([
            f'<div class="spell-item"><span>{c}</span></div>'
            for c in cantrips
        ])

        return f'''
            <div class="box spell-level-box cantrip-box">
                <div class="spell-level-header">
                    <div class="spell-level-num">0</div>
                    <div style="font-size: 6.5pt; font-weight: 700; text-transform: uppercase;">Cantrips</div>
                </div>
                <div class="spell-list">{cantrips_html}
                </div>
            </div>'''
