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
from .pages import StatsPage, BackgroundPage, SpellcastingPage, ReferencePage


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
        css = self.load_css("base.css", "components.css", "item.css")

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
        css = self.load_css("base.css", "components.css", "sheet.css")

        # Build context for page builders
        context = {
            "header": self.header,
            "abilities": self.abilities,
            "prof_bonus": self.prof_bonus,
            "ability_mods": self._ability_mods,
        }

        # Build all pages using PageBuilder classes
        pages_html = ""
        pages_html += StatsPage(self.data, context).build()
        pages_html += BackgroundPage(self.data, context).build()
        pages_html += SpellcastingPage(self.data, context).build()
        pages_html += ReferencePage(self.data, context).build()

        title = self.header.get("character_name", "Character")
        return self.html_wrapper(f"{title} - Character Sheet", css, pages_html)

    # =========================================================================
    # HELPER METHODS (kept for backward compatibility if needed)
    # =========================================================================

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
