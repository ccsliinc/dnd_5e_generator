"""
Character-Specific Content Renderers

Specialized renderers for D&D character sheet elements.
"""

from typing import Optional
from .renderers import ContentRenderer, register_renderer


# =============================================================================
# ABILITY SCORES
# =============================================================================

class AbilityScoresRenderer(ContentRenderer):
    """Render the six ability score boxes."""

    content_type = "ability_scores"

    TEMPLATE = '''
                    <div class="box ability-score">
                        <div class="box__label">{name}</div>
                        <div class="value--large">{score}</div>
                        <div class="ability-modifier">{modifier}</div>
                    </div>'''

    def render(self, content: dict, context: Optional[dict] = None) -> str:
        abilities = content.get("abilities", [])
        html = "".join([
            self.TEMPLATE.format(
                name=a.get("name", ""),
                score=a.get("score", 10),
                modifier=a.get("modifier", "+0")
            )
            for a in abilities
        ])
        return f'<div class="ability-block">{html}</div>'


# =============================================================================
# SAVING THROWS
# =============================================================================

class SavingThrowsRenderer(ContentRenderer):
    """Render saving throw rows with proficiency circles."""

    content_type = "saving_throws"

    TEMPLATE = '''
                    <div class="save-row">
                        <div class="prof-circle {filled}"></div>
                        <div class="save-mod">{modifier}</div>
                        <div class="save-name">{name}</div>
                    </div>'''

    def render(self, content: dict, context: Optional[dict] = None) -> str:
        saves = content.get("saves", [])
        html = "".join([
            self.TEMPLATE.format(
                filled="filled" if s.get("proficient") else "",
                modifier=s.get("modifier", "+0"),
                name=s.get("name", "")
            )
            for s in saves
        ])
        return html


# =============================================================================
# SKILLS
# =============================================================================

class SkillsRenderer(ContentRenderer):
    """Render skill rows with proficiency circles."""

    content_type = "skills"

    TEMPLATE = '''
                    <div class="skill-row">
                        <div class="prof-circle {filled}"></div>
                        <div class="skill-mod">{modifier}</div>
                        <div class="skill-name">{name} <span class="skill-ability">({ability})</span></div>
                    </div>'''

    def render(self, content: dict, context: Optional[dict] = None) -> str:
        skills = content.get("skills", [])
        html = "".join([
            self.TEMPLATE.format(
                filled="filled" if s.get("proficient") else "",
                modifier=s.get("modifier", "+0"),
                name=s.get("name", ""),
                ability=s.get("ability", "")
            )
            for s in skills
        ])
        return html


# =============================================================================
# ATTACKS
# =============================================================================

class AttacksRenderer(ContentRenderer):
    """Render attack rows with name, bonus, and damage."""

    content_type = "attacks"

    TEMPLATE = '''
                    <div class="attack-row">
                        <div class="attack-name">{name}</div>
                        <div class="attack-bonus">{atk_bonus}</div>
                        <div class="attack-damage">{damage_type}</div>
                    </div>'''

    EMPTY_TEMPLATE = '''
                    <div class="attack-row">
                        <div class="attack-name"></div>
                        <div class="attack-bonus"></div>
                        <div class="attack-damage"></div>
                    </div>'''

    def render(self, content: dict, context: Optional[dict] = None) -> str:
        attacks = content.get("attacks", [])
        min_rows = content.get("min_rows", 5)

        html = "".join([
            self.TEMPLATE.format(
                name=a.get("name", ""),
                atk_bonus=a.get("atk_bonus", ""),
                damage_type=a.get("damage_type", "")
            )
            for a in attacks
        ])

        # Pad with empty rows
        empty_count = max(0, min_rows - len(attacks))
        html += self.EMPTY_TEMPLATE * empty_count

        return html


# =============================================================================
# COMBAT STATS
# =============================================================================

class CombatStatsRenderer(ContentRenderer):
    """Render combat stat boxes (AC, Initiative, Speed)."""

    content_type = "combat_stats"

    def render(self, content: dict, context: Optional[dict] = None) -> str:
        stats = content.get("stats", [])
        html = ""

        for stat in stats:
            html += f'''
                    <div class="box box--label-bottom combat-stat">
                        <div class="combat-value value--xlarge">{stat.get("value", "")}</div>
                        <div class="box__label">{stat.get("label", "")}</div>
                    </div>'''

        return f'<div class="combat-row">{html}</div>'


# =============================================================================
# HIT POINTS
# =============================================================================

class HitPointsRenderer(ContentRenderer):
    """Render HP section with max, current, and temporary."""

    content_type = "hit_points"

    def render(self, content: dict, context: Optional[dict] = None) -> str:
        hp_max = content.get("hp_maximum", "")
        hp_current = content.get("hp_current", "")
        hp_temp = content.get("hp_temporary", "")

        return f'''
                <div class="box box--label-bottom hp-section">
                    <div class="hp-max-row">
                        <div class="hp-max-label">Hit Point Maximum</div>
                        <div class="hp-max-value">{hp_max}</div>
                    </div>
                    <div class="hp-current">{hp_current}</div>
                    <div class="box__label">Current Hit Points</div>
                </div>
                <div class="box box--label-bottom hp-temp">
                    <div class="hp-temp-value">{hp_temp}</div>
                    <div class="box__label">Temporary Hit Points</div>
                </div>'''


# =============================================================================
# HIT DICE & DEATH SAVES
# =============================================================================

class HitDiceDeathSavesRenderer(ContentRenderer):
    """Render hit dice and death saves row."""

    content_type = "hit_dice_death"

    def render(self, content: dict, context: Optional[dict] = None) -> str:
        hit_dice = content.get("hit_dice", {})
        death_saves = content.get("death_saves", {})

        return f'''
                <div class="hitdice-death-row">
                    <div class="box box--label-bottom hitdice-box">
                        <div class="hitdice-total">Total: {hit_dice.get("total", "")}</div>
                        <div class="hitdice-value">{hit_dice.get("current", "")}</div>
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
                </div>'''


# =============================================================================
# CURRENCY
# =============================================================================

class CurrencyRenderer(ContentRenderer):
    """Render currency coin row."""

    content_type = "currency"

    def render(self, content: dict, context: Optional[dict] = None) -> str:
        currency = content.get("currency", {})
        return f'''
                    <div class="coin-row">
                        <div class="coin coin--cp"><div class="coin-icon">{currency.get("cp", 0)}</div><div class="coin-label">Copper</div></div>
                        <div class="coin coin--sp"><div class="coin-icon">{currency.get("sp", 0)}</div><div class="coin-label">Silver</div></div>
                        <div class="coin coin--ep"><div class="coin-icon">{currency.get("ep", 0)}</div><div class="coin-label">Electrum</div></div>
                        <div class="coin coin--gp"><div class="coin-icon">{currency.get("gp", 0)}</div><div class="coin-label">Gold</div></div>
                        <div class="coin coin--pp"><div class="coin-icon">{currency.get("pp", 0)}</div><div class="coin-label">Platinum</div></div>
                    </div>'''


# =============================================================================
# SPELL LEVEL
# =============================================================================

class SpellLevelRenderer(ContentRenderer):
    """Render a single spell level box."""

    content_type = "spell_level"

    SPELL_TEMPLATE = '''
                    <div class="spell-item">
                        <div class="spell-prepared {filled}"></div>
                        <span>{name}</span>
                    </div>'''

    EMPTY_TEMPLATE = '''
                    <div class="spell-item">
                        <div class="spell-prepared"></div>
                        <span></span>
                    </div>'''

    def render(self, content: dict, context: Optional[dict] = None) -> str:
        level = content.get("level", 0)
        slots_total = content.get("slots_total", 0)
        slots_expended = content.get("slots_expended", 0)
        spells = content.get("spells", [])
        min_rows = content.get("min_rows", 8)

        # Render spells
        spells_html = "".join([
            self.SPELL_TEMPLATE.format(
                name=s.get("name", ""),
                filled="filled" if s.get("prepared") else ""
            )
            for s in spells
        ])

        # Pad with empty rows
        empty_count = max(0, min_rows - len(spells))
        spells_html += self.EMPTY_TEMPLATE * empty_count

        if level == 0:
            # Cantrips box
            return f'''
            <div class="box spell-level-box cantrip-box">
                <div class="spell-level-header">
                    <div class="spell-level-num">0</div>
                    <div style="font-size: 6.5pt; font-weight: 700; text-transform: uppercase;">Cantrips</div>
                </div>
                <div class="spell-list">{spells_html}
                </div>
            </div>'''
        else:
            return f'''
            <div class="box spell-level-box">
                <div class="spell-level-header">
                    <div class="spell-level-num">{level}</div>
                    <div class="spell-slots">
                        <div class="spell-slots-row">
                            <span>Slots:</span>
                            <div class="spell-slot-box">{slots_total}</div>
                        </div>
                        <div class="spell-slots-row">
                            <span>Used:</span>
                            <div class="spell-slot-box">{slots_expended}</div>
                        </div>
                    </div>
                </div>
                <div class="spell-list">{spells_html}
                </div>
            </div>'''


# =============================================================================
# GALLERY
# =============================================================================

class GalleryRenderer(ContentRenderer):
    """Render image gallery row."""

    content_type = "gallery"

    TEMPLATE = '''
                        <div class="gallery-item">
                            <img src="{src}" alt="Character Art" class="gallery-img">
                        </div>'''

    def render(self, content: dict, context: Optional[dict] = None) -> str:
        images = content.get("images", [])
        if not images:
            return ""

        items_html = "".join([
            self.TEMPLATE.format(src=img)
            for img in images
        ])

        return f'''
                <div class="gallery-row">{items_html}
                </div>'''


# =============================================================================
# REFERENCE CARDS
# =============================================================================

class WeaponCardRenderer(ContentRenderer):
    """Render weapon reference card."""

    content_type = "weapon_card"

    TEMPLATE = '''
                    <div class="weapon-card ref-card">
                        <div class="weapon-name">{name}</div>
                        <div class="weapon-type">{type}</div>
                        <div class="weapon-stats">
                            <span class="weapon-damage">{damage}</span>
                        </div>
                        <div class="weapon-properties">{properties}</div>
                        <div class="weapon-notes">{notes}</div>
                    </div>'''

    def render(self, content: dict, context: Optional[dict] = None) -> str:
        weapons = content.get("weapons", [])
        return "".join([
            self.TEMPLATE.format(
                name=w.get("name", ""),
                type=w.get("type", ""),
                damage=w.get("damage", ""),
                properties=w.get("properties", ""),
                notes=w.get("notes", "")
            )
            for w in weapons
        ])


class SpellCardRenderer(ContentRenderer):
    """Render spell reference card."""

    content_type = "spell_card"

    TEMPLATE = '''
                    <div class="spell-card ref-card">
                        <div class="spell-name">{name} <span class="spell-level-tag">({level})</span></div>
                        <div class="spell-meta">
                            <span><span class="spell-meta-label">Cast:</span> {casting_time}</span>
                            <span><span class="spell-meta-label">Range:</span> {range}</span>
                            <span><span class="spell-meta-label">Duration:</span> {duration}</span>
                        </div>
                        <div class="spell-desc">{description}</div>
                    </div>'''

    def render(self, content: dict, context: Optional[dict] = None) -> str:
        spells = content.get("spells", [])
        return "".join([
            self.TEMPLATE.format(
                name=s.get("name", ""),
                level=s.get("level", ""),
                casting_time=s.get("casting_time", ""),
                range=s.get("range", ""),
                duration=s.get("duration", ""),
                description=s.get("description", "")
            )
            for s in spells
        ])


class FeatureCardRenderer(ContentRenderer):
    """Render feature reference card."""

    content_type = "feature_card"

    TEMPLATE = '''
                    <div class="feature-card ref-card">
                        <div class="feature-name">{name}</div>
                        <div class="feature-desc">{description}</div>
                    </div>'''

    def render(self, content: dict, context: Optional[dict] = None) -> str:
        features = content.get("features", [])
        return "".join([
            self.TEMPLATE.format(
                name=f.get("name", ""),
                description=f.get("description", "")
            )
            for f in features
        ])


# =============================================================================
# TURN STRUCTURE
# =============================================================================

class TurnStructureRenderer(ContentRenderer):
    """Render turn structure reference box."""

    content_type = "turn_structure"

    PHASE_TEMPLATE = '''
                        <div class="turn-phase">
                            <span class="turn-phase-name">{name}</span>
                            <span class="turn-phase-desc">{desc}</span>
                        </div>'''

    def render(self, content: dict, context: Optional[dict] = None) -> str:
        title = content.get("title", "Your Turn")
        phases = content.get("phases", [])
        reaction = content.get("reaction", "")

        phases_html = "".join([
            self.PHASE_TEMPLATE.format(
                name=p.get("name", ""),
                desc=p.get("desc", "")
            )
            for p in phases
        ])

        return f'''
                <div class="box ref-box turn-box">
                    <div class="ref-section-title">{title}</div>{phases_html}
                    <div class="turn-reaction">
                        <span class="turn-phase-name">Reaction</span>
                        <span class="turn-phase-desc">{reaction}</span>
                    </div>
                </div>'''


# =============================================================================
# COMBAT REFERENCE
# =============================================================================

class CombatReferenceRenderer(ContentRenderer):
    """Render combat reference (actions, conditions, cover)."""

    content_type = "combat_reference"

    ACTION_TEMPLATE = '''
                        <div class="combat-action">
                            <span class="combat-action-name">{name}</span>
                            <span class="combat-action-desc">{desc}</span>
                        </div>'''

    CONDITION_TEMPLATE = '''
                        <div class="combat-condition">
                            <span class="combat-condition-name">{name}</span>
                            <span class="combat-condition-desc">{desc}</span>
                        </div>'''

    COVER_TEMPLATE = '''
                        <div class="combat-cover">
                            <span class="combat-cover-type">{type}</span>
                            <span class="combat-cover-bonus">{bonus}</span>
                        </div>'''

    def render(self, content: dict, context: Optional[dict] = None) -> str:
        actions = content.get("actions", [])
        conditions = content.get("conditions_quick", [])
        cover = content.get("cover", [])

        actions_html = "".join([
            self.ACTION_TEMPLATE.format(name=a.get("name", ""), desc=a.get("desc", ""))
            for a in actions
        ])
        conditions_html = "".join([
            self.CONDITION_TEMPLATE.format(name=c.get("name", ""), desc=c.get("desc", ""))
            for c in conditions
        ])
        cover_html = "".join([
            self.COVER_TEMPLATE.format(type=c.get("type", ""), bonus=c.get("bonus", ""))
            for c in cover
        ])

        return f'''
                <div class="box ref-box combat-ref-box">
                    <div class="ref-section-title">Actions</div>{actions_html}
                    <div class="ref-section-title" style="margin-top: 2mm;">Conditions</div>{conditions_html}
                    <div class="ref-section-title" style="margin-top: 2mm;">Cover</div>{cover_html}
                </div>'''


# =============================================================================
# COMPANION STAT BLOCK
# =============================================================================

class CompanionRenderer(ContentRenderer):
    """Render companion stat block."""

    content_type = "companion"

    ABILITY_TEMPLATE = '''
                        <div class="companion-ability">
                            <div class="companion-ability-name">{name}</div>
                            <div class="companion-ability-score">{score}</div>
                            <div class="companion-ability-mod">({mod})</div>
                        </div>'''

    TRAIT_TEMPLATE = '''
                        <div class="companion-trait">
                            <span class="companion-trait-name">{name}.</span>
                            <span class="companion-trait-desc">{description}</span>
                        </div>'''

    ACTION_TEMPLATE = '''
                        <div class="companion-action">
                            <span class="companion-action-name">{name}.</span>
                            <span class="companion-action-desc">{description}</span>
                        </div>'''

    def render(self, content: dict, context: Optional[dict] = None) -> str:
        companion = content.get("companion", {})
        if not companion:
            return ""

        # Companion abilities
        abilities = companion.get("abilities", {})
        ability_items = []
        for ability in ["str", "dex", "con", "int", "wis", "cha"]:
            score = abilities.get(ability, 10)
            mod = (score - 10) // 2
            mod_str = f"+{mod}" if mod >= 0 else str(mod)
            ability_items.append({"name": ability.upper(), "score": score, "mod": mod_str})

        abilities_html = "".join([
            self.ABILITY_TEMPLATE.format(**a) for a in ability_items
        ])

        # Traits and actions
        traits_html = "".join([
            self.TRAIT_TEMPLATE.format(name=t.get("name", ""), description=t.get("description", ""))
            for t in companion.get("traits", [])
        ])
        actions_html = "".join([
            self.ACTION_TEMPLATE.format(name=a.get("name", ""), description=a.get("description", ""))
            for a in companion.get("actions", [])
        ])

        # Commands
        commands_html = "".join([f"<li>{cmd}</li>" for cmd in companion.get("commands", [])])

        # Image
        companion_image = companion.get("image", "")
        image_html = ""
        if companion_image:
            image_html = f'''
                        <div class="companion-portrait">
                            <img src="{companion_image}" alt="{companion.get("name", "Companion")}" class="companion-img">
                        </div>'''

        return f'''
                <div class="box companion-block box--flex">
                    <div class="companion-header-row">
                        <div class="companion-header">
                            <div class="companion-name">{companion.get("name", "")}</div>
                            <div class="companion-type">{companion.get("size", "")} {companion.get("type", "")}</div>
                        </div>{image_html}
                    </div>
                    <div class="companion-stats-row">
                        <div class="companion-stat"><span class="companion-stat-label">AC</span> {companion.get("armor_class", "")}</div>
                        <div class="companion-stat"><span class="companion-stat-label">HP</span> {companion.get("hit_points", "")} <span style="font-size: 6pt; color: #666;">({companion.get("hp_notes", "")})</span></div>
                        <div class="companion-stat"><span class="companion-stat-label">Speed</span> {companion.get("speed", "")}</div>
                    </div>
                    <div class="companion-abilities">{abilities_html}
                    </div>
                    <div class="companion-stats-row">
                        <div class="companion-stat"><span class="companion-stat-label">Skills</span> {companion.get("skills", "")}</div>
                        <div class="companion-stat"><span class="companion-stat-label">Senses</span> {companion.get("senses", "")}</div>
                    </div>
                    <div class="companion-section">
                        <div class="companion-section-title">Traits</div>{traits_html}
                    </div>
                    <div class="companion-section">
                        <div class="companion-section-title">Actions</div>{actions_html}
                    </div>
                    <div class="companion-section">
                        <div class="companion-section-title">Beast Master Commands</div>
                        <ul class="companion-commands">{commands_html}</ul>
                    </div>
                </div>'''


# =============================================================================
# NOTES BOX
# =============================================================================

class NotesRenderer(ContentRenderer):
    """Render empty notes box with lines."""

    content_type = "notes"

    def render(self, content: dict, context: Optional[dict] = None) -> str:
        title = content.get("title", "Notes")
        return f'''
                <div class="box box--label-top notes-box box--flex">
                    <div class="box__label">{title}</div>
                    <div class="notes-lines"></div>
                </div>'''


# =============================================================================
# TRAIT BOX
# =============================================================================

class TraitBoxRenderer(ContentRenderer):
    """Render personality trait box."""

    content_type = "trait_box"

    def render(self, content: dict, context: Optional[dict] = None) -> str:
        label = content.get("label", "")
        text = content.get("text", "")
        return f'''
                <div class="box box--label-bottom trait-box">
                    <div class="trait-content">{text}</div>
                    <div class="box__label">{label}</div>
                </div>'''


# =============================================================================
# ITEM STAT (for item headers)
# =============================================================================

class ItemStatRenderer(ContentRenderer):
    """Render item stat row (for item header)."""

    content_type = "item_stats"

    TEMPLATE = '''
                    <div class="item-stat">
                        <span class="item-stat-label">{label}</span>
                        <span class="item-stat-value {css_class}">{value}</span>
                    </div>'''

    def render(self, content: dict, context: Optional[dict] = None) -> str:
        stats = content.get("stats", [])
        return "".join([
            self.TEMPLATE.format(
                label=s.get("label", ""),
                value=s.get("value", ""),
                css_class=s.get("class", "")
            )
            for s in stats
        ])


# =============================================================================
# REGISTER ALL CHARACTER RENDERERS
# =============================================================================

register_renderer(AbilityScoresRenderer)
register_renderer(SavingThrowsRenderer)
register_renderer(SkillsRenderer)
register_renderer(AttacksRenderer)
register_renderer(CombatStatsRenderer)
register_renderer(HitPointsRenderer)
register_renderer(HitDiceDeathSavesRenderer)
register_renderer(CurrencyRenderer)
register_renderer(SpellLevelRenderer)
register_renderer(GalleryRenderer)
register_renderer(WeaponCardRenderer)
register_renderer(SpellCardRenderer)
register_renderer(FeatureCardRenderer)
register_renderer(TurnStructureRenderer)
register_renderer(CombatReferenceRenderer)
register_renderer(CompanionRenderer)
register_renderer(NotesRenderer)
register_renderer(TraitBoxRenderer)
register_renderer(ItemStatRenderer)
