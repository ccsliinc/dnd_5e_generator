"""
Layout Components

Section, Column, and Page classes for building document layouts.
"""

from dataclasses import dataclass, field
from typing import Any, Optional
from .renderers import render_content


# =============================================================================
# SECTION
# =============================================================================

@dataclass
class Section:
    """A content section/box within a page."""

    content: dict
    title: Optional[str] = None
    variant: str = "default"  # "default", "lore", "highlight"
    flex_grow: bool = False
    column: int = 1
    css_class: Optional[str] = None
    style: Optional[str] = None

    def render(self, context: Optional[dict] = None) -> str:
        """Render section to HTML."""
        # Build CSS classes
        classes = ["box", "section-box"]
        if self.variant == "lore":
            classes.append("description-box")
        if self.flex_grow:
            classes.append("box--flex")
        if self.css_class:
            classes.append(self.css_class)

        class_str = " ".join(classes)

        # Build style attribute
        style_attr = f' style="{self.style}"' if self.style else ""

        # Build title HTML
        title_html = ""
        if self.title:
            title_html = f'<div class="section-title">{self.title}</div>'

        # Render content
        content_html = render_content(self.content, context)

        return f'''
                <div class="{class_str}"{style_attr}>{title_html}
                    {content_html}
                </div>'''

    @classmethod
    def from_dict(cls, data: dict) -> 'Section':
        """Create Section from dictionary."""
        return cls(
            content=data.get("content", {}),
            title=data.get("title"),
            variant=data.get("variant", "default"),
            flex_grow=data.get("flex_grow", False),
            column=data.get("column", 1),
            css_class=data.get("class"),
            style=data.get("style"),
        )


# =============================================================================
# COLUMN
# =============================================================================

@dataclass
class Column:
    """A column containing multiple sections."""

    sections: list[Section] = field(default_factory=list)
    css_class: str = "column"
    style: Optional[str] = None

    def render(self, context: Optional[dict] = None) -> str:
        """Render column to HTML."""
        sections_html = "".join([s.render(context) for s in self.sections])

        style_attr = f' style="{self.style}"' if self.style else ""

        return f'''
            <div class="{self.css_class}"{style_attr}>{sections_html}
            </div>'''

    def add_section(self, section: Section) -> None:
        """Add a section to the column."""
        self.sections.append(section)


# =============================================================================
# PAGE
# =============================================================================

@dataclass
class Page:
    """A single page in the document."""

    sections: list[Section] = field(default_factory=list)
    columns: int = 2
    gap: str = "3mm"
    header_html: str = ""
    footer_html: str = ""
    css_class: str = "page"

    def render(self, context: Optional[dict] = None) -> str:
        """Render page to HTML."""
        # Separate sections by column
        col1_sections = [s for s in self.sections if s.column == 1]
        col2_sections = [s for s in self.sections if s.column == 2]

        # Create columns
        col1 = Column(sections=col1_sections, css_class="content-column")
        col2 = Column(sections=col2_sections, css_class="content-column")

        if self.columns == 2:
            content_html = f'''
        <div class="item-content">{col1.render(context)}{col2.render(context)}
        </div>'''
        else:
            # Single column - combine all sections
            all_sections = Column(sections=self.sections, css_class="content-column")
            content_html = f'''
        <div class="item-content" style="grid-template-columns: 1fr;">{all_sections.render(context)}
        </div>'''

        return f'''
    <div class="{self.css_class}">{self.header_html}
{content_html}{self.footer_html}
    </div>'''

    def add_section(self, section: Section) -> None:
        """Add a section to the page."""
        self.sections.append(section)

    @classmethod
    def from_dict(cls, data: dict, header_html: str = "", footer_html: str = "") -> 'Page':
        """Create Page from dictionary."""
        layout = data.get("layout", {})
        sections_data = data.get("sections", [])

        sections = [Section.from_dict(s) for s in sections_data]

        return cls(
            sections=sections,
            columns=layout.get("columns", 2),
            gap=layout.get("gap", "3mm"),
            header_html=header_html,
            footer_html=footer_html,
        )
