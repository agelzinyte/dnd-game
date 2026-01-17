"""Comprehensive tests for the character module."""

import pytest
from dndgame.character import Character, Enemy, Entity, RACES
from dndgame.weapons import WEAPONS
from dndgame.spells import Spell


class TestEntity:
    """Tests for the Entity base class."""

    def test_entity_creation(self):
        """Test basic entity creation."""
        stats = {"STR": 10, "DEX": 12, "CON": 14, "INT": 8, "WIS": 10, "CHA": 10}
        entity = Entity("TestEntity", stats, hp=20, armor_class=15)

        assert entity.name == "TestEntity"
        assert entity.stats == stats
        assert entity.hp == 20
        assert entity.max_hp == 20
        assert entity.armor_class == 15

    def test_entity_default_weapon(self):
        """Test that entity gets default weapon if none provided."""
        stats = {"STR": 10, "DEX": 10, "CON": 10, "INT": 10, "WIS": 10, "CHA": 10}
        entity = Entity("TestEntity", stats, hp=10)

        assert entity.weapon is not None
        assert entity.weapon.name == "Club"

    def test_entity_custom_weapon(self):
        """Test entity creation with custom weapon."""
        stats = {"STR": 10, "DEX": 10, "CON": 10, "INT": 10, "WIS": 10, "CHA": 10}
        entity = Entity("TestEntity", stats, hp=10, weapon=WEAPONS["Longsword"])

        assert entity.weapon.name == "Longsword"

    def test_get_modifier(self):
        """Test ability modifier calculation."""
        stats = {
            "STR": 8,   # -1
            "DEX": 10,  # +0
            "CON": 12,  # +1
            "INT": 14,  # +2
            "WIS": 16,  # +3
            "CHA": 20,  # +5
        }
        entity = Entity("TestEntity", stats, hp=10)

        assert entity.get_modifier("STR") == -1
        assert entity.get_modifier("DEX") == 0
        assert entity.get_modifier("CON") == 1
        assert entity.get_modifier("INT") == 2
        assert entity.get_modifier("WIS") == 3
        assert entity.get_modifier("CHA") == 5

    def test_is_alive(self):
        """Test is_alive method."""
        stats = {"STR": 10, "DEX": 10, "CON": 10, "INT": 10, "WIS": 10, "CHA": 10}
        entity = Entity("TestEntity", stats, hp=10)

        assert entity.is_alive() is True

        entity.hp = 1
        assert entity.is_alive() is True

        entity.hp = 0
        assert entity.is_alive() is False

        entity.hp = -5
        assert entity.is_alive() is False


class TestCharacter:
    """Tests for the Character class."""

    def test_character_creation(self):
        """Test basic character creation."""
        character = Character("TestChar", "Human", 10)

        assert character.name == "TestChar"
        assert character.race == "Human"
        assert character.base_hp == 10
        assert character.level == 1
        assert character.xp == 0
        assert character.known_spells == []

    def test_roll_stats(self, capsys):
        """Test stat rolling."""
        character = Character("TestChar", "Human", 10)
        character.roll_stats()

        # Check that all stats are present
        assert "STR" in character.stats
        assert "DEX" in character.stats
        assert "CON" in character.stats
        assert "INT" in character.stats
        assert "WIS" in character.stats
        assert "CHA" in character.stats

        # Check that stats are in reasonable range (3-18 for 3d6)
        for stat_value in character.stats.values():
            assert 3 <= stat_value <= 18

        # Check that HP was calculated
        assert character.hp > 0
        assert character.max_hp > 0

        # Check that rolling message was printed
        captured = capsys.readouterr()
        assert "Rolling stats..." in captured.out

    def test_apply_racial_bonuses_human(self):
        """Test applying Human racial bonuses."""
        character = Character("TestChar", "Human", 10)
        character.stats = {"STR": 10, "DEX": 10, "CON": 10, "INT": 10, "WIS": 10, "CHA": 10}
        character.apply_racial_bonuses()

        # Humans get +1 to all stats
        assert all(value == 11 for value in character.stats.values())

    def test_apply_racial_bonuses_elf(self):
        """Test applying Elf racial bonuses."""
        character = Character("TestChar", "Elf", 10)
        character.stats = {"STR": 10, "DEX": 10, "CON": 10, "INT": 10, "WIS": 10, "CHA": 10}
        character.apply_racial_bonuses()

        # Elves get +2 to DEX only
        assert character.stats["DEX"] == 12
        assert character.stats["STR"] == 10

    def test_apply_racial_bonuses_orc(self):
        """Test applying Orc racial bonuses (including negative)."""
        character = Character("TestChar", "Orc", 10)
        character.stats = {"STR": 10, "DEX": 10, "CON": 10, "INT": 10, "WIS": 10, "CHA": 10}
        character.apply_racial_bonuses()

        # Orcs get +2 STR, +1 CON, -1 INT
        assert character.stats["STR"] == 12
        assert character.stats["CON"] == 11
        assert character.stats["INT"] == 9

    def test_add_spell(self):
        """Test adding spells to character."""
        character = Character("TestChar", "Human", 10)
        spell = Spell("Fireball", 3, "Evocation", 15)

        character.add_spell(spell)
        assert spell in character.known_spells
        assert len(character.known_spells) == 1

        # Adding same spell again shouldn't duplicate
        character.add_spell(spell)
        assert len(character.known_spells) == 1

    def test_can_cast_spell_unknown_spell(self):
        """Test that character cannot cast unknown spells."""
        character = Character("TestChar", "Human", 10)
        spell = Spell("Fireball", 3, "Evocation", 15)

        assert character.can_cast_spell(spell) is False

    def test_can_cast_spell_cantrip(self):
        """Test that cantrips can always be cast."""
        character = Character("TestChar", "Human", 10)
        cantrip = Spell("Fire Bolt", 0, "Evocation", 5)

        character.add_spell(cantrip)
        assert character.can_cast_spell(cantrip) is True

        # Should still be castable after many uses
        for _ in range(10):
            assert character.can_cast_spell(cantrip) is True

    def test_can_cast_spell_with_slots(self):
        """Test casting spells with available slots."""
        character = Character("TestChar", "Human", 10)
        spell = Spell("Magic Missile", 1, "Evocation", 7)

        character.add_spell(spell)
        assert character.can_cast_spell(spell) is True

    def test_can_cast_spell_no_slots(self):
        """Test that spell cannot be cast without slots."""
        character = Character("TestChar", "Human", 10)
        spell = Spell("Magic Missile", 1, "Evocation", 7)

        character.add_spell(spell)
        # Use up all spell slots
        character.spell_slots[1] = 0

        assert character.can_cast_spell(spell) is False

    def test_cast_spell(self):
        """Test spell casting mechanics."""
        caster = Character("Wizard", "Human", 10)
        caster.stats = {"STR": 10, "DEX": 10, "CON": 10, "INT": 16, "WIS": 10, "CHA": 10}
        caster.hp = 20
        caster.max_hp = 20

        target = Character("Target", "Human", 10)
        target.stats = {"STR": 10, "DEX": 10, "CON": 10, "INT": 10, "WIS": 10, "CHA": 10}
        target.hp = 20
        target.max_hp = 20

        spell = Spell("Magic Missile", 1, "Evocation", 7)
        caster.add_spell(spell)

        initial_slots = caster.spell_slots[1]
        damage = caster.cast_spell(spell, target)

        # Check that spell slot was consumed
        assert caster.spell_slots[1] == initial_slots - 1

        # Check that damage was dealt
        assert damage > 0
        assert target.hp < 20

    def test_cast_spell_cantrip_no_slot_consumption(self):
        """Test that casting cantrips doesn't consume slots."""
        caster = Character("Wizard", "Human", 10)
        caster.stats = {"STR": 10, "DEX": 10, "CON": 10, "INT": 14, "WIS": 10, "CHA": 10}

        target = Character("Target", "Human", 10)
        target.stats = {"STR": 10, "DEX": 10, "CON": 10, "INT": 10, "WIS": 10, "CHA": 10}
        target.hp = 20
        target.max_hp = 20

        cantrip = Spell("Fire Bolt", 0, "Evocation", 5)
        caster.add_spell(cantrip)

        # Cast cantrip multiple times
        for _ in range(5):
            caster.cast_spell(cantrip, target)

        # Spell slots should remain unchanged
        assert caster.spell_slots[1] == 2  # Level 1 character has 2 level-1 slots

    def test_cast_spell_raises_error_if_cannot_cast(self):
        """Test that casting unavailable spell raises error."""
        caster = Character("Wizard", "Human", 10)
        target = Character("Target", "Human", 10)
        target.stats = {"STR": 10, "DEX": 10, "CON": 10, "INT": 10, "WIS": 10, "CHA": 10}

        spell = Spell("Magic Missile", 1, "Evocation", 7)

        with pytest.raises(ValueError, match="Cannot cast"):
            caster.cast_spell(spell, target)

    def test_rest(self):
        """Test rest restores HP and spell slots."""
        character = Character("TestChar", "Human", 10)
        character.stats = {"STR": 10, "DEX": 10, "CON": 10, "INT": 10, "WIS": 10, "CHA": 10}
        character.hp = 20
        character.max_hp = 20

        # Damage character and use spell slots
        character.hp = 5
        character.spell_slots[1] = 0

        character.rest()

        assert character.hp == character.max_hp
        assert character.spell_slots[1] == character.max_spell_slots[1]

    def test_get_available_spells(self):
        """Test getting list of castable spells."""
        character = Character("TestChar", "Human", 10)

        spell1 = Spell("Fire Bolt", 0, "Evocation", 5)  # Cantrip - always available
        spell2 = Spell("Magic Missile", 1, "Evocation", 7)  # Has slots
        spell3 = Spell("Fireball", 3, "Evocation", 15)  # No slots (level 3)

        character.add_spell(spell1)
        character.add_spell(spell2)
        character.add_spell(spell3)

        available = character.get_available_spells()

        assert spell1 in available  # Cantrip
        assert spell2 in available  # Has level 1 slots
        assert spell3 not in available  # No level 3 slots at level 1

    def test_get_xp_for_next_level(self):
        """Test XP requirement calculation."""
        character = Character("TestChar", "Human", 10)
        character.stats = {"STR": 10, "DEX": 10, "CON": 10, "INT": 10, "WIS": 10, "CHA": 10}

        # Level 1 -> 2 requires 300 XP
        assert character.get_xp_for_next_level() == 300

    def test_get_xp_for_next_level_max_level(self):
        """Test XP requirement at max level."""
        character = Character("TestChar", "Human", 10)
        character.stats = {"STR": 10, "DEX": 10, "CON": 10, "INT": 10, "WIS": 10, "CHA": 10}
        character.level = 10

        assert character.get_xp_for_next_level() == 0

    def test_gain_xp_no_level_up(self, capsys):
        """Test gaining XP without leveling up."""
        character = Character("TestChar", "Human", 10)
        character.stats = {"STR": 10, "DEX": 10, "CON": 10, "INT": 10, "WIS": 10, "CHA": 10}

        leveled_up = character.gain_xp(100)

        assert character.xp == 100
        assert character.level == 1
        assert leveled_up is False

        captured = capsys.readouterr()
        assert "+100 XP!" in captured.out

    def test_gain_xp_with_level_up(self, capsys):
        """Test gaining enough XP to level up."""
        character = Character("TestChar", "Human", 10)
        character.stats = {"STR": 10, "DEX": 10, "CON": 10, "INT": 10, "WIS": 10, "CHA": 10}
        character.max_hp = 10
        character.hp = 10

        leveled_up = character.gain_xp(300)

        assert character.xp == 300
        assert character.level == 2
        assert leveled_up is True

        captured = capsys.readouterr()
        assert "LEVEL UP!" in captured.out

    def test_gain_xp_multiple_levels(self, capsys):
        """Test gaining enough XP to level up multiple times."""
        character = Character("TestChar", "Human", 10)
        character.stats = {"STR": 10, "DEX": 10, "CON": 10, "INT": 10, "WIS": 10, "CHA": 10}
        character.max_hp = 10
        character.hp = 10

        leveled_up = character.gain_xp(3000)

        assert character.xp == 3000
        assert character.level == 4  # Should jump to level 4
        assert leveled_up is True

    def test_level_up(self, capsys):
        """Test level up mechanics."""
        character = Character("TestChar", "Human", 10)
        character.stats = {"STR": 10, "DEX": 10, "CON": 10, "INT": 10, "WIS": 10, "CHA": 10}
        character.max_hp = 10
        character.hp = 10
        initial_max_hp = character.max_hp

        character.level_up()

        assert character.level == 2
        assert character.max_hp > initial_max_hp
        assert character.hp == character.max_hp

        captured = capsys.readouterr()
        assert "LEVEL UP!" in captured.out
        assert "Max HP increased" in captured.out

    def test_level_up_spell_slots_increase(self):
        """Test that spell slots increase on level up."""
        character = Character("TestChar", "Human", 10)
        character.stats = {"STR": 10, "DEX": 10, "CON": 10, "INT": 10, "WIS": 10, "CHA": 10}
        character.max_hp = 10
        character.hp = 10

        # Level 1 has {1: 2, 2: 0, 3: 0}
        assert character.max_spell_slots[1] == 2

        character.level_up()  # Now level 2

        # Level 2 has {1: 3, 2: 0, 3: 0}
        assert character.max_spell_slots[1] == 3

    def test_level_up_ability_score_improvement(self, capsys):
        """Test ability score improvement at level 4."""
        character = Character("TestChar", "Human", 10)
        character.stats = {"STR": 10, "DEX": 10, "CON": 10, "INT": 10, "WIS": 10, "CHA": 10}
        character.max_hp = 10
        character.hp = 10

        # Level up to 4
        for _ in range(3):
            character.level_up()

        # One stat should have increased
        stat_sum = sum(character.stats.values())
        assert stat_sum == 61  # 60 + 1 improvement

        captured = capsys.readouterr()
        assert "Ability Score Improvement!" in captured.out


class TestEnemy:
    """Tests for the Enemy class."""

    def test_enemy_creation(self):
        """Test basic enemy creation."""
        stats = {"STR": 12, "DEX": 10, "CON": 14, "INT": 8, "WIS": 10, "CHA": 8}
        enemy = Enemy("Goblin", stats, hp=10, armor_class=12, xp_value=50)

        assert enemy.name == "Goblin"
        assert enemy.stats == stats
        assert enemy.hp == 10
        assert enemy.max_hp == 10
        assert enemy.armor_class == 12
        assert enemy.xp_value == 50

    def test_enemy_default_xp_value(self):
        """Test enemy creation with default XP value."""
        stats = {"STR": 10, "DEX": 10, "CON": 10, "INT": 10, "WIS": 10, "CHA": 10}
        enemy = Enemy("TestEnemy", stats, hp=10)

        assert enemy.xp_value == 50

    def test_enemy_with_weapon(self):
        """Test enemy creation with weapon."""
        stats = {"STR": 14, "DEX": 10, "CON": 12, "INT": 8, "WIS": 10, "CHA": 8}
        enemy = Enemy("Orc", stats, hp=15, weapon=WEAPONS["Battleaxe"])

        assert enemy.weapon.name == "Battleaxe"

    def test_level_up_minimum_hp_increase(self):
        """Test that HP increase is at least 1 even with very low CON."""
        character = Character("TestChar", "Human", 10)
        # Very low CON to test minimum HP increase
        character.stats = {"STR": 10, "DEX": 10, "CON": 3, "INT": 10, "WIS": 10, "CHA": 10}  # CON 3 = -4 modifier
        character.max_hp = 5
        character.hp = 5
        initial_max_hp = character.max_hp

        # Level up multiple times to test the minimum
        for _ in range(5):
            old_max_hp = character.max_hp
            character.level_up()
            # HP should always increase by at least 1
            assert character.max_hp >= old_max_hp + 1
