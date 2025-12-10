"""
Content Type Renderers

Each renderer handles a specific content type from JSON and produces HTML.
Uses a registry pattern for extensibility and clean dispatch.
"""

import re
from abc import ABC, abstractmethod
from typing import Any, Optional


# =============================================================================
# BASE RENDERER
# =============================================================================

class ContentRenderer(ABC):
    """Base class for all content renderers."""

    content_type: str = "base"

    @abstractmethod
    def render(self, content: dict, context: Optional[dict] = None) -> str:
        """Render content dict to HTML string."""
        pass

    @staticmethod
    def markdown_bold(text: str) -> str:
        """Convert **bold** markdown to <strong> tags."""
        return re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', text)

    @staticmethod
    def markdown_italic(text: str) -> str:
        """Convert *italic* markdown to <em> tags."""
        return re.sub(r'\*([^*]+)\*', r'<em>\1</em>', text)

    @staticmethod
    def format_modifier(value: int) -> str:
        """Format a modifier value with +/- sign."""
        return f"+{value}" if value >= 0 else str(value)


# =============================================================================
# TEXT RENDERERS
# =============================================================================

class TextRenderer(ContentRenderer):
    """Render plain text paragraphs."""

    content_type = "text"

    def render(self, content: dict, context: Optional[dict] = None) -> str:
        text = content.get("text", "")
        text = self.markdown_bold(text)
        css_class = content.get("class", "section-content")
        return f'<div class="{css_class}">{text}</div>'


class TextItalicRenderer(ContentRenderer):
    """Render italic/flavor text."""

    content_type = "text_italic"

    def render(self, content: dict, context: Optional[dict] = None) -> str:
        text = content.get("text", "")
        text = self.markdown_bold(text)
        return f'<div class="section-content description-text">{text}</div>'


class ParagraphsRenderer(ContentRenderer):
    """Render text with paragraph breaks."""

    content_type = "paragraphs"

    def render(self, content: dict, context: Optional[dict] = None) -> str:
        text = content.get("text", "")
        if not text:
            return ""

        # Try double newlines first, then single
        paragraphs = [p.strip() for p in text.split('\n\n') if p.strip()]
        if not paragraphs:
            paragraphs = [p.strip() for p in text.split('\n') if p.strip()]
        if not paragraphs:
            paragraphs = [text.strip()]

        html = "".join([f"<p>{self.markdown_bold(p)}</p>" for p in paragraphs])
        css_class = content.get("class", "text-content")
        return f'<div class="{css_class}">{html}</div>'


# =============================================================================
# LIST RENDERERS
# =============================================================================

class BulletsRenderer(ContentRenderer):
    """Render bullet point list."""

    content_type = "bullets"

    def render(self, content: dict, context: Optional[dict] = None) -> str:
        items = content.get("items", [])
        css_class = content.get("class", "ability-bullets")

        bullets_html = "".join([
            f'<li>{self.markdown_bold(item)}</li>'
            for item in items
        ])
        return f'<ul class="{css_class}">{bullets_html}</ul>'


class StyledListRenderer(ContentRenderer):
    """Render a styled list (for equipment, proficiencies, etc.)."""

    content_type = "styled_list"

    def render(self, content: dict, context: Optional[dict] = None) -> str:
        items = content.get("items", [])
        css_class = content.get("class", "styled-list")

        if not items:
            return f'<ul class="{css_class}"></ul>'

        list_items = "".join([f"<li>{item}</li>" for item in items])
        return f'<ul class="{css_class}">{list_items}</ul>'


# =============================================================================
# PROPERTY RENDERERS
# =============================================================================

class PropertiesRenderer(ContentRenderer):
    """Render icon + name + description property rows."""

    content_type = "properties"

    TEMPLATE = '''
                        <li class="property-item">
                            <div class="property-icon">{icon}</div>
                            <div class="property-content">
                                <div class="property-name">{name}</div>
                                <div class="property-desc">{desc}</div>
                            </div>
                        </li>'''

    def render(self, content: dict, context: Optional[dict] = None) -> str:
        items = content.get("items", [])

        props_html = "".join([
            self.TEMPLATE.format(
                icon=item.get("icon", ""),
                name=item.get("name", ""),
                desc=item.get("desc", "")
            )
            for item in items
        ])
        return f'<ul class="property-list">{props_html}</ul>'


# =============================================================================
# TABLE RENDERER
# =============================================================================

class TableRenderer(ContentRenderer):
    """Render data table with optional footer."""

    content_type = "table"

    def render(self, content: dict, context: Optional[dict] = None) -> str:
        columns = content.get("columns", [])
        rows = content.get("rows", [])
        footer = content.get("footer", "")
        css_class = content.get("class", "scaling-table")

        # Build header
        header_cells = "".join([f'<th>{col}</th>' for col in columns])
        header_html = f'<thead><tr>{header_cells}</tr></thead>'

        # Build rows
        rows_html = ""
        for row in rows:
            cells = "".join([f'<td>{cell}</td>' for cell in row])
            rows_html += f'<tr>{cells}</tr>'
        body_html = f'<tbody>{rows_html}</tbody>'

        # Build footer if present
        footer_html = ""
        if footer:
            footer_html = f'''
                    <div style="font-size: 6pt; color: var(--text-label); margin-top: 1mm; font-style: italic;">
                        {footer}
                    </div>'''

        return f'''<table class="{css_class}">
                        {header_html}
                        {body_html}
                    </table>{footer_html}'''


# =============================================================================
# QUOTE RENDERER
# =============================================================================

class QuoteRenderer(ContentRenderer):
    """Render lore quote with attribution."""

    content_type = "quote"

    def render(self, content: dict, context: Optional[dict] = None) -> str:
        text = content.get("text", "")
        attribution = content.get("attribution", "")

        attr_html = ""
        if attribution:
            attr_html = f'<div class="lore-attribution">{attribution}</div>'

        return f'''<div class="lore-quote">
                        {text}
                        {attr_html}
                    </div>'''


# =============================================================================
# COMPARISON RENDERER
# =============================================================================

class ComparisonRenderer(ContentRenderer):
    """Render before → after stat comparison rows."""

    content_type = "comparison"

    TEMPLATE = '''
                    <div class="stat-comparison">
                        <div class="stat-before">{before}</div>
                        <div class="stat-arrow">→</div>
                        <div class="stat-after">{after}</div>
                    </div>'''

    def render(self, content: dict, context: Optional[dict] = None) -> str:
        items = content.get("items", [])
        return "".join([
            self.TEMPLATE.format(
                before=item.get("before", ""),
                after=item.get("after", "")
            )
            for item in items
        ])


# =============================================================================
# TALES RENDERER
# =============================================================================

class TalesRenderer(ContentRenderer):
    """Render title + description pairs (legendary tales)."""

    content_type = "tales"

    TEMPLATE = '''
                        <div class="legendary-tale">
                            <span class="tale-title">{title}</span>
                            <span class="tale-desc">{desc}</span>
                        </div>'''

    def render(self, content: dict, context: Optional[dict] = None) -> str:
        items = content.get("items", [])
        tales_html = "".join([
            self.TEMPLATE.format(
                title=item.get("title", ""),
                desc=item.get("desc", "")
            )
            for item in items
        ])
        return f'<div class="section-content" style="margin-top: 2mm;">{tales_html}</div>'


# =============================================================================
# SUBSECTIONS RENDERER
# =============================================================================

class SubsectionsRenderer(ContentRenderer):
    """Render named groups with bullet lists."""

    content_type = "subsections"

    def render(self, content: dict, context: Optional[dict] = None) -> str:
        items = content.get("items", [])
        html = ""

        for item in items:
            name = item.get("name", "")
            bullets = item.get("bullets", [])

            bullets_html = "".join([
                f'<li>{self.markdown_bold(bullet)}</li>'
                for bullet in bullets
            ])

            html += f'''
                    <div class="ability-block">
                        <div class="ability-name">{name}</div>
                        <ul class="ability-bullets">{bullets_html}</ul>
                    </div>'''

        return html


# =============================================================================
# SYNERGY RENDERER
# =============================================================================

class SynergyRenderer(ContentRenderer):
    """Render synergy block (composite type for companion synergies)."""

    content_type = "synergy"

    def render(self, content: dict, context: Optional[dict] = None) -> str:
        header = content.get("header", {})
        comparisons = content.get("comparisons", [])
        subsections = content.get("subsections", [])

        # Build header
        header_html = f'''
                    <div class="synergy-header">
                        <div class="synergy-icon">{header.get("icon", "")}</div>
                        <div>
                            <div class="synergy-title">{header.get("title", "")}</div>
                            <div class="synergy-subtitle">{header.get("subtitle", "")}</div>
                        </div>
                    </div>'''

        # Build comparisons using ComparisonRenderer
        comp_renderer = ComparisonRenderer()
        comparisons_html = comp_renderer.render({"items": comparisons})

        # Build subsections
        subsections_html = ""
        for item in subsections:
            name = item.get("name", "")
            bullets = item.get("bullets", [])

            bullets_html = "".join([
                f'<li>{self.markdown_bold(bullet)}</li>'
                for bullet in bullets
            ])

            subsections_html += f'''
                    <div class="ability-block" style="margin-top: 2mm;">
                        <div class="ability-name">{name}</div>
                        <ul class="ability-bullets">{bullets_html}</ul>
                    </div>'''

        return f'{header_html}{comparisons_html}{subsections_html}'


# =============================================================================
# MIXED RENDERER
# =============================================================================

class MixedRenderer(ContentRenderer):
    """Render multiple content blocks in sequence."""

    content_type = "mixed"

    def render(self, content: dict, context: Optional[dict] = None) -> str:
        blocks = content.get("blocks", [])
        html = ""

        for block in blocks:
            renderer = get_renderer(block.get("type", "text"))
            html += renderer.render(block, context)

        return html


# =============================================================================
# RENDERER REGISTRY
# =============================================================================

# Registry of all available renderers
_RENDERER_REGISTRY: dict[str, ContentRenderer] = {}


def register_renderer(renderer_class: type[ContentRenderer]) -> type[ContentRenderer]:
    """Register a renderer class in the global registry."""
    instance = renderer_class()
    _RENDERER_REGISTRY[instance.content_type] = instance
    return renderer_class


def get_renderer(content_type: str) -> ContentRenderer:
    """Get renderer instance by content type."""
    if content_type not in _RENDERER_REGISTRY:
        # Fall back to text renderer
        return _RENDERER_REGISTRY.get("text", TextRenderer())
    return _RENDERER_REGISTRY[content_type]


def render_content(content: dict, context: Optional[dict] = None) -> str:
    """Convenience function to render any content dict."""
    content_type = content.get("type", "text")
    renderer = get_renderer(content_type)
    return renderer.render(content, context)


# Register all base renderers
register_renderer(TextRenderer)
register_renderer(TextItalicRenderer)
register_renderer(ParagraphsRenderer)
register_renderer(BulletsRenderer)
register_renderer(StyledListRenderer)
register_renderer(PropertiesRenderer)
register_renderer(TableRenderer)
register_renderer(QuoteRenderer)
register_renderer(ComparisonRenderer)
register_renderer(TalesRenderer)
register_renderer(SubsectionsRenderer)
register_renderer(SynergyRenderer)
register_renderer(MixedRenderer)
