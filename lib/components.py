"""
Layout Components

Row, Col, Grid, Section, and Page classes for building document layouts.

Layout Hierarchy:
- Page: Full A4 page container
- Row: Horizontal flex container
- Col: Vertical flex container / flex child
- Grid: CSS Grid container
- Section: Titled content box
"""

from dataclasses import dataclass, field
from typing import Any, Optional, Union
from .renderers import render_content


# =============================================================================
# ROW - Horizontal flex container
# =============================================================================

@dataclass
class Row:
    """Horizontal flex container for layout."""

    children: list = field(default_factory=list)
    gap: str = "md"  # "xs", "sm", "md", "lg" or custom value
    stretch: bool = False
    center: bool = False
    wrap: bool = False
    css_class: Optional[str] = None
    style: Optional[str] = None

    def render(self, context: Optional[dict] = None) -> str:
        """Render row to HTML."""
        classes = ["row"]

        # Gap modifier
        if self.gap in ("xs", "sm", "lg"):
            classes.append(f"row--gap-{self.gap}")
        elif self.gap == "none":
            classes.append("row--no-gap")
        # "md" is default, no class needed

        if self.stretch:
            classes.append("row--stretch")
        if self.center:
            classes.append("row--center")
        if self.wrap:
            classes.append("row--wrap")
        if self.css_class:
            classes.append(self.css_class)

        class_str = " ".join(classes)
        style_attr = f' style="{self.style}"' if self.style else ""

        # Render children
        children_html = ""
        for child in self.children:
            if hasattr(child, 'render'):
                children_html += child.render(context)
            elif isinstance(child, str):
                children_html += child
            elif isinstance(child, dict):
                children_html += render_content(child, context)

        return f'<div class="{class_str}"{style_attr}>{children_html}</div>'

    def add(self, child) -> 'Row':
        """Add a child element. Returns self for chaining."""
        self.children.append(child)
        return self


# =============================================================================
# COL - Vertical flex container
# =============================================================================

@dataclass
class Col:
    """Vertical flex container / flex child for layout."""

    children: list = field(default_factory=list)
    flex: int = 0  # 0=auto, 1-3=flex ratio
    gap: str = "sm"  # "xs", "sm", "md", "lg" or "none"
    css_class: Optional[str] = None
    style: Optional[str] = None

    def render(self, context: Optional[dict] = None) -> str:
        """Render column to HTML."""
        classes = ["col"]

        # Flex modifier
        if self.flex in (1, 2, 3):
            classes.append(f"col--{self.flex}")

        # Gap modifier
        if self.gap == "xs":
            classes.append("col--gap-xs")
        elif self.gap == "md":
            classes.append("col--gap-md")
        elif self.gap == "none":
            classes.append("col--no-gap")
        # "sm" is default, no class needed

        if self.css_class:
            classes.append(self.css_class)

        class_str = " ".join(classes)
        style_attr = f' style="{self.style}"' if self.style else ""

        # Render children
        children_html = ""
        for child in self.children:
            if hasattr(child, 'render'):
                children_html += child.render(context)
            elif isinstance(child, str):
                children_html += child
            elif isinstance(child, dict):
                children_html += render_content(child, context)

        return f'<div class="{class_str}"{style_attr}>{children_html}</div>'

    def add(self, child) -> 'Col':
        """Add a child element. Returns self for chaining."""
        self.children.append(child)
        return self


# =============================================================================
# GRID - CSS Grid container
# =============================================================================

@dataclass
class Grid:
    """CSS Grid container for layout."""

    children: list = field(default_factory=list)
    columns: int = 2  # 2, 3, or 4
    gap: str = "md"  # "sm", "md", "lg"
    css_class: Optional[str] = None
    style: Optional[str] = None

    def render(self, context: Optional[dict] = None) -> str:
        """Render grid to HTML."""
        classes = ["grid", f"grid--{self.columns}col"]

        # Gap modifier
        if self.gap == "sm":
            classes.append("grid--gap-sm")
        elif self.gap == "lg":
            classes.append("grid--gap-lg")
        # "md" is default, no class needed

        if self.css_class:
            classes.append(self.css_class)

        class_str = " ".join(classes)
        style_attr = f' style="{self.style}"' if self.style else ""

        # Render children
        children_html = ""
        for child in self.children:
            if hasattr(child, 'render'):
                children_html += child.render(context)
            elif isinstance(child, str):
                children_html += child
            elif isinstance(child, dict):
                children_html += render_content(child, context)

        return f'<div class="{class_str}"{style_attr}>{children_html}</div>'

    def add(self, child) -> 'Grid':
        """Add a child element. Returns self for chaining."""
        self.children.append(child)
        return self


# =============================================================================
# SECTION - Titled content box
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
