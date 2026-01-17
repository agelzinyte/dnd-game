"""Tests for the weapons module."""

from dndgame.weapons import Weapon, WEAPONS


def test_weapon_string_representation():
    """Test weapon string representation."""
    weapon = Weapon("Test Sword", damage_die=8, damage_dice_count=1)
    assert str(weapon) == "Test Sword (1d8)"

    weapon2 = Weapon("Greatsword", damage_die=6, damage_dice_count=2)
    assert str(weapon2) == "Greatsword (2d6)"


def test_weapons_registry():
    """Test that weapons registry is populated."""
    assert len(WEAPONS) > 0
    assert "Longsword" in WEAPONS
    assert "Dagger" in WEAPONS
