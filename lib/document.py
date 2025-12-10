"""
Document Classes

Base Document class and specialized CharacterDocument and ItemDocument classes.
"""

import re
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Optional

from .components import Page, Section
from .renderers import render_content


# =============================================================================
# BASE DOCUMENT
# =============================================================================

class Document(ABC):
    """Base class for all document types."""

    def __init__(self, data: dict, base_path: str = ""):
        self.data = data
        self.base_path = base_path
        self.meta = data.get("meta", {})

    @abstractmethod
    def build_html(self) -> str:
        """Build complete HTML document."""
        pass

    def load_css(self, *css_files: str) -> str:
        """Load and combine CSS from files."""
        styles_dir = Path(__file__).parent.parent / "styles"
        css_parts = []

        for filename in css_files:
            css_path = styles_dir / filename
            if css_path.exists():
                css_parts.append(css_path.read_text())

        return "\n".join(css_parts)

    def html_wrapper(self, title: str, css: str, body: str) -> str:
        """Wrap content in complete HTML document."""
        return f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@400;500;600;700&family=Scada:wght@400;700&display=swap" rel="stylesheet">
    <style>
{css}
    </style>
</head>
<body>{body}
</body>
</html>'''


# =============================================================================
# ITEM DOCUMENT
# =============================================================================

class ItemDocument(Document):
    """Document class for magic items."""

    def __init__(self, data: dict, base_path: str = ""):
        super().__init__(data, base_path)
        self.header_data = data.get("header", {})
        self.footer_data = data.get("footer", {})
        self.pages_data = data.get("pages", [])

    def build_html(self) -> str:
        """Build complete HTML for item document."""
        css = self.load_css("sheet.css", "item.css")

        # Render header and footer
        header_html = self._render_header()
        footer_html = self._render_footer()

        # Render all pages
        pages_html = ""
        for i, page_data in enumerate(self.pages_data):
            page = Page.from_dict(
                page_data,
                header_html=header_html if i == 0 else "",
                footer_html=footer_html if i == 0 else ""
            )
            pages_html += page.render()

        title = self.header_data.get("name", "Magic Item")
        return self.html_wrapper(f"{title} - Magic Item", css, pages_html)

    def _render_header(self) -> str:
        """Render item header with image, title, and stats."""
        name = self.header_data.get("name", "")
        subtitle = self.header_data.get("subtitle", "")
        image = self.header_data.get("image", "")
        background_svg = self.header_data.get("background_svg", "")
        stats = self.header_data.get("stats", [])

        # Build image path
        if self.base_path and image:
            image_path = f"{self.base_path}/{image}"
        else:
            image_path = image

        # Build SVG background
        svg_html = self._load_svg_decoration(background_svg)

        # Build stats row
        stats_html = render_content({"type": "item_stats", "stats": stats})

        # Subtitle
        subtitle_html = f'<div class="item-subtitle">{subtitle}</div>' if subtitle else ""

        # Image section (only if image exists)
        if image_path:
            image_html = f'''
            <div class="item-image-frame">
                <img src="{image_path}" alt="{name}" class="item-image">
            </div>'''
        else:
            image_html = ""

        return f'''
        <div class="item-header">{svg_html}{image_html}
            <div class="item-title-block">
                <div class="item-title-group">
                    <div class="item-name">{name}</div>
                    {subtitle_html}
                </div>
                <div class="item-stats-row">{stats_html}
                </div>
            </div>
        </div>'''

    def _render_footer(self) -> str:
        """Render item footer."""
        left = self.footer_data.get("left", "")
        right = self.footer_data.get("right", "")

        return f'''
        <div class="item-footer">
            <div>{left}</div>
            <div class="market-value">{right}</div>
        </div>'''

    def _load_svg_decoration(self, svg_path: str) -> str:
        """Load SVG decoration from file."""
        if not svg_path:
            return ""

        full_path = Path(__file__).parent.parent / svg_path
        if not full_path.exists():
            return ""

        svg_content = full_path.read_text()
        path_match = re.search(r'<path[^>]*d="([^"]*)"', svg_content)
        if not path_match:
            return ""

        path_d = path_match.group(1)
        viewbox_match = re.search(r'viewBox="([^"]*)"', svg_content)
        viewbox = viewbox_match.group(1) if viewbox_match else "0 0 2893.32 468.16"

        return f'''
            <svg class="header-bg-decoration" viewBox="{viewbox}" preserveAspectRatio="xMidYMid slice">
                <path d="{path_d}"/>
            </svg>'''


# =============================================================================
# CHARACTER DOCUMENT
# =============================================================================

class CharacterDocument(Document):
    """Document class for character sheets."""

    # Skill to ability mapping
    SKILL_ABILITIES = {
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

    ABILITY_ORDER = ["strength", "dexterity", "constitution", "intelligence", "wisdom", "charisma"]
    SKILL_ORDER = [
        "acrobatics", "animal_handling", "arcana", "athletics", "deception",
        "history", "insight", "intimidation", "investigation", "medicine",
        "nature", "perception", "performance", "persuasion", "religion",
        "sleight_of_hand", "stealth", "survival"
    ]

    def __init__(self, data: dict, base_path: str = ""):
        super().__init__(data, base_path)
        self.header = data.get("header", {})
        self.abilities = data.get("abilities", {})
        self.prof_bonus = data.get("proficiency_bonus", 2)
        self._ability_mods = self._calculate_ability_mods()

    def _calculate_ability_mods(self) -> dict[str, int]:
        """Calculate ability modifiers from scores."""
        mods = {}
        for ability, data in self.abilities.items():
            score = data.get("score", 10)
            mods[ability] = (score - 10) // 2
        return mods

    def _format_modifier(self, value: int) -> str:
        """Format modifier with +/- sign."""
        return f"+{value}" if value >= 0 else str(value)

    def _format_skill_name(self, skill: str) -> str:
        """Format skill name for display."""
        return skill.replace("_", " ").title()

    def build_html(self) -> str:
        """Build complete HTML for character sheet."""
        css = self.load_css("sheet.css")

        pages_html = ""
        pages_html += self._build_page1()
        pages_html += self._build_page2()
        pages_html += self._build_page3()
        pages_html += self._build_page4()

        title = self.header.get("character_name", "Character")
        return self.html_wrapper(f"{title} - Character Sheet", css, pages_html)

    # =========================================================================
    # PAGE 1: Main Stats
    # =========================================================================

    def _build_page1(self) -> str:
        """Build page 1: Main stats, combat, equipment."""
        portrait = self.meta.get("portrait", "")

        # Header
        header_html = self._build_page_header(
            include_portrait=True,
            portrait=portrait,
            fields=[
                ("class_level", "Class & Level"),
                ("background", "Background"),
                ("player_name", "Player Name"),
                ("race", "Race"),
                ("alignment", "Alignment"),
                ("experience_points", "Experience Points"),
            ]
        )

        # Abilities column
        abilities_html = self._render_abilities()
        saves_html = self._render_saves()
        skills_html = self._render_skills()
        passive_perception = self._calculate_passive_perception()

        # Combat section
        combat = self.data.get("combat", {})
        dex_mod = self._ability_mods.get("dexterity", 0)
        initiative = combat.get("initiative") or self._format_modifier(dex_mod)

        # Attacks
        attacks_html = render_content({
            "type": "attacks",
            "attacks": self.data.get("attacks", []),
            "min_rows": 5
        })

        # Equipment and proficiencies
        equipment_html = render_content({
            "type": "styled_list",
            "items": self.data.get("equipment", []),
            "class": "styled-list"
        })
        prof_lang_html = render_content({
            "type": "styled_list",
            "items": self.data.get("proficiencies_languages", []),
            "class": "styled-list prof-list"
        })
        features_html = render_content({
            "type": "styled_list",
            "items": self.data.get("features_traits", []),
            "class": "styled-list"
        })

        # Currency
        currency_html = render_content({
            "type": "currency",
            "currency": self.data.get("currency", {})
        })

        # Personality
        personality = self.data.get("personality", {})

        # Gallery
        gallery_html = render_content({
            "type": "gallery",
            "images": self.meta.get("gallery", [])
        })

        # Inspiration
        inspiration = "X" if self.data.get("inspiration") else ""

        return f'''
    <!-- PAGE 1: Main Stats -->
    <div class="page">
        {header_html}

        <div class="main-content">
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
                            <div class="stat-circle">+{self.prof_bonus}</div>
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
                    <div class="passive-value">{passive_perception}</div>
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
            </div>

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
            </div>
        </div>{gallery_html}
    </div>'''

    # =========================================================================
    # PAGE 2: Background
    # =========================================================================

    def _build_page2(self) -> str:
        """Build page 2: Background, appearance, backstory."""
        appearance = self.data.get("appearance", {})
        allies = self.data.get("allies_organizations", {})

        # Header with appearance fields
        header_html = self._build_page_header(
            include_portrait=False,
            fields=[
                ("age", "Age", appearance.get("age", "")),
                ("height", "Height", appearance.get("height", "")),
                ("weight", "Weight", appearance.get("weight", "")),
                ("eyes", "Eyes", appearance.get("eyes", "")),
                ("skin", "Skin", appearance.get("skin", "")),
                ("hair", "Hair", appearance.get("hair", "")),
            ],
            name_label="Character Name"
        )

        # Text content
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
        allies_html = render_content({
            "type": "paragraphs",
            "text": allies.get("description", ""),
            "class": "text-content"
        })

        # Lists
        additional_features = render_content({
            "type": "styled_list",
            "items": self.data.get("additional_features_traits", [])
        })
        treasure = render_content({
            "type": "styled_list",
            "items": self.data.get("treasure", [])
        })

        return f'''
    <!-- PAGE 2: Background -->
    <div class="page">
        {header_html}

        <div class="page2-content">
            <div class="page2-columns">
                <div class="column">
                    <div class="box box--label-top large-box" style="min-height: 45mm;">
                        <div class="box__label">Character Appearance</div>
                        <div class="large-box-content">{appearance_html}</div>
                    </div>
                    <div class="box box--label-top large-box box--flex">
                        <div class="box__label">Character Backstory</div>
                        <div class="large-box-content">{backstory_html}</div>
                    </div>
                </div>
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
                </div>
            </div>
            <div class="page2-notes-row">
                <div class="box box--label-top large-box notes-box" style="min-height: 110mm;">
                    <div class="box__label">Notes</div>
                    <div class="notes-lines"></div>
                </div>
            </div>
        </div>
    </div>'''

    # =========================================================================
    # PAGE 3: Spellcasting
    # =========================================================================

    def _build_page3(self) -> str:
        """Build page 3: Spellcasting."""
        spellcasting = self.data.get("spellcasting", {})
        spells_data = spellcasting.get("spells", {})

        # Header
        header_html = f'''
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

        # Cantrips
        cantrips = spellcasting.get("cantrips", [])
        cantrips_html = "".join([
            f'<div class="spell-item"><span>{c}</span></div>'
            for c in cantrips
        ])

        # Spell levels
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
        {header_html}

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
    </div>'''

    # =========================================================================
    # PAGE 4: Reference / Cheat Sheet
    # =========================================================================

    def _build_page4(self) -> str:
        """Build page 4: Quick reference and companion."""
        reference = self.data.get("reference", {})
        spellcasting = self.data.get("spellcasting", {})

        # Header
        header_html = f'''
        <div class="page-header">
            <div class="header-left">
                <div class="header-brand">Dungeons & Dragons</div>
                <div class="box box--label-bottom header-name">
                    <div class="value--large">Quick Reference</div>
                    <div class="box__label">{self.header.get("character_name", "")}</div>
                </div>
            </div>
            <div class="header-right" style="grid-template-columns: repeat(3, 1fr); grid-template-rows: 1fr;">
                <div class="box box--label-bottom box--centered info-field">
                    <div class="value--medium">{self.header.get("class_level", "")}</div>
                    <div class="box__label">Class & Level</div>
                </div>
                <div class="box box--label-bottom box--centered info-field">
                    <div class="value--medium">+{self.prof_bonus}</div>
                    <div class="box__label">Proficiency Bonus</div>
                </div>
                <div class="box box--label-bottom box--centered info-field">
                    <div class="value--medium">{spellcasting.get("spell_save_dc", "")}</div>
                    <div class="box__label">Spell Save DC</div>
                </div>
            </div>
        </div>'''

        # Turn structure
        turn_html = ""
        turn_structure = reference.get("turn_structure", {})
        if turn_structure:
            turn_html = render_content({
                "type": "turn_structure",
                **turn_structure
            })

        # Combat reference
        combat_html = ""
        combat_ref = reference.get("combat_reference", {})
        if combat_ref:
            combat_html = render_content({
                "type": "combat_reference",
                **combat_ref
            })

        # Weapons
        weapons_html = render_content({
            "type": "weapon_card",
            "weapons": reference.get("weapons", [])
        })

        # Spells
        spells_html = render_content({
            "type": "spell_card",
            "spells": reference.get("spells", [])
        })

        # Companion
        companion_html = render_content({
            "type": "companion",
            "companion": self.data.get("companion", {})
        })

        return f'''
    <!-- PAGE 4: Reference / Cheat Sheet -->
    <div class="page">
        {header_html}

        <div class="page4-grid">
            <div class="column">{turn_html}{combat_html}
                <div class="box ref-box box--flex">
                    <div class="ref-section-title">Weapons</div>{weapons_html}
                </div>
            </div>
            <div class="column">
                <div class="box ref-box">
                    <div class="ref-section-title">Spells</div>{spells_html}
                </div>{companion_html}
            </div>
        </div>
    </div>'''

    # =========================================================================
    # HELPER METHODS
    # =========================================================================

    def _build_page_header(
        self,
        include_portrait: bool = False,
        portrait: str = "",
        fields: list = None,
        name_label: str = "Character Name"
    ) -> str:
        """Build page header with name and info fields."""
        fields = fields or []

        # Portrait section
        portrait_html = ""
        if include_portrait and portrait:
            portrait_html = f'''
                    <div class="portrait-frame">
                        <img src="{portrait}" alt="Character Portrait" class="portrait-img">
                    </div>'''

        # Name box
        name_html = f'''
                <div class="box box--label-bottom header-name">
                    <div class="value--large">{self.header.get("character_name", "")}</div>
                    <div class="box__label">{name_label}</div>
                </div>'''

        # Info fields
        fields_html = ""
        for field_data in fields:
            if len(field_data) == 2:
                key, label = field_data
                value = self.header.get(key, "")
            else:
                key, label, value = field_data

            fields_html += f'''
                <div class="box box--label-bottom box--centered info-field">
                    <div class="value--medium">{value}</div>
                    <div class="box__label">{label}</div>
                </div>'''

        if include_portrait:
            left_content = f'''
                <div class="header-brand">Dungeons & Dragons</div>
                <div class="header-name-row">{portrait_html}{name_html}
                </div>'''
        else:
            left_content = f'''
                <div class="header-brand">Dungeons & Dragons</div>
                {name_html}'''

        return f'''
        <div class="page-header">
            <div class="header-left">{left_content}
            </div>
            <div class="header-right">{fields_html}
            </div>
        </div>'''

    def _render_abilities(self) -> str:
        """Render ability score boxes."""
        abilities_list = []
        for ability in self.ABILITY_ORDER:
            data = self.abilities.get(ability, {"score": 10})
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

    def _render_saves(self) -> str:
        """Render saving throw rows."""
        saves_data = self.data.get("saving_throws", {})
        saves_list = []

        for ability in self.ABILITY_ORDER:
            save = saves_data.get(ability, {"proficient": False})
            is_prof = save.get("proficient", False)
            mod = self._ability_mods.get(ability, 0)
            if is_prof:
                mod += self.prof_bonus
            saves_list.append({
                "name": ability.capitalize(),
                "proficient": is_prof,
                "modifier": self._format_modifier(mod)
            })

        return render_content({
            "type": "saving_throws",
            "saves": saves_list
        })

    def _render_skills(self) -> str:
        """Render skill rows."""
        skills_data = self.data.get("skills", {})
        skills_list = []

        for skill in self.SKILL_ORDER:
            skill_info = skills_data.get(skill, {"proficient": False})
            is_prof = skill_info.get("proficient", False)
            ability_abbr, ability_name = self.SKILL_ABILITIES.get(skill, ("???", "strength"))
            mod = self._ability_mods.get(ability_name, 0)
            if is_prof:
                mod += self.prof_bonus
            skills_list.append({
                "name": self._format_skill_name(skill),
                "ability": ability_abbr,
                "proficient": is_prof,
                "modifier": self._format_modifier(mod)
            })

        return render_content({
            "type": "skills",
            "skills": skills_list
        })

    def _calculate_passive_perception(self) -> int:
        """Calculate passive perception."""
        skills_data = self.data.get("skills", {})
        perception = skills_data.get("perception", {"proficient": False})
        mod = self._ability_mods.get("wisdom", 0)
        if perception.get("proficient", False):
            mod += self.prof_bonus
        return 10 + mod
