import pytest
from dndgame.spells import Spell, SpellBook


def test_spell_creation():
    """Test spell initialization with all attributes."""
    spell = Spell("Fireball", 3, "Evocation", 8)
    assert spell.name == "Fireball"
    assert spell.level == 3
    assert spell.school == "Evocation"
    assert spell.spell_power == 8


def test_spellbook_creation():
    """Test spellbook initialization."""
    spellbook = SpellBook()
    assert isinstance(spellbook.spells, list)
    assert len(spellbook.spells) == 0


def test_add_spell():
    """Test adding spells to spellbook."""
    spellbook = SpellBook()
    spell = Spell("Magic Missile", 1, "Evocation", 3)

    spellbook.add_spell(spell)
    assert len(spellbook.spells) == 1
    assert spellbook.spells[0] == spell


def test_get_available_spells():
    """Test filtering spells by level."""
    spellbook = SpellBook()

    # Add spells of different levels
    spells = [
        Spell("Magic Missile", 1, "Evocation", 3),
        Spell("Fireball", 3, "Evocation", 8),
        Spell("Shield", 1, "Abjuration", 2),
        Spell("Wish", 9, "Conjuration", 20),
    ]

    for spell in spells:
        spellbook.add_spell(spell)

    # Test filtering
    level_1_spells = spellbook.get_available_spells(1)
    assert len(level_1_spells) == 2
    assert all(spell.level <= 1 for spell in level_1_spells)

    level_3_spells = spellbook.get_available_spells(3)
    assert len(level_3_spells) == 3
    assert all(spell.level <= 3 for spell in level_3_spells)


def test_empty_spellbook_available_spells():
    """Test getting available spells from empty spellbook."""
    spellbook = SpellBook()
    available = spellbook.get_available_spells(1)
    assert len(available) == 0


def test_spell_cast():
    """Test spell cast method."""
    from dndgame.character import Character

    # Create a simple caster and target
    caster = Character("Wizard", "Human", 10)
    caster.stats = {"STR": 10, "DEX": 10, "CON": 10, "INT": 16, "WIS": 10, "CHA": 10}
    caster.hp = 10
    caster.max_hp = 10

    target = Character("Target", "Human", 10)
    target.stats = {"STR": 10, "DEX": 10, "CON": 10, "INT": 10, "WIS": 10, "CHA": 10}
    target.hp = 10
    target.max_hp = 10

    spell = Spell("Test Spell", 1, "Test", 5)
    initial_target_hp = target.hp

    # Cast spell - should deal spell_power + INT modifier damage
    # INT 16 = +3 modifier, so damage should be 5 + 3 = 8
    damage = spell.cast(caster, target)
    assert damage == 8
    assert target.hp == initial_target_hp - 8


def test_spell_string_representation_cantrip():
    """Test string representation of a cantrip."""
    spell = Spell("Fire Bolt", 0, "Evocation", 5)
    assert str(spell) == "Fire Bolt (Cantrip, Evocation, Power: 5)"


def test_spell_string_representation_leveled():
    """Test string representation of a leveled spell."""
    spell = Spell("Fireball", 3, "Evocation", 15)
    assert str(spell) == "Fireball (Level 3, Evocation, Power: 15)"


def test_spell_cast_negative_damage_clamped_to_zero():
    """Test that negative damage is clamped to 0."""
    from dndgame.character import Character

    caster = Character("Wizard", "Human", 10)
    # Very low INT and negative spell power
    caster.stats = {"STR": 10, "DEX": 10, "CON": 10, "INT": 3, "WIS": 10, "CHA": 10}  # INT 3 = -4 modifier
    caster.hp = 10
    caster.max_hp = 10

    target = Character("Target", "Human", 10)
    target.stats = {"STR": 10, "DEX": 10, "CON": 10, "INT": 10, "WIS": 10, "CHA": 10}
    target.hp = 10
    target.max_hp = 10

    # Spell with negative power that will result in overall negative damage
    spell = Spell("Weak Spell", 1, "Test", -10)
    initial_target_hp = target.hp

    damage = spell.cast(caster, target)
    
    # Damage should be clamped to 0
    assert damage == 0
    assert target.hp == initial_target_hp  # Target HP shouldn't change


def test_get_spellbook():
    """Test getting the global spellbook."""
    from dndgame.spells import get_spellbook, SPELLS

    spellbook = get_spellbook()
    
    assert spellbook is SPELLS
    assert isinstance(spellbook, dict)
    assert len(spellbook) > 0
    assert "Fireball" in spellbook
    assert "Magic Missile" in spellbook
