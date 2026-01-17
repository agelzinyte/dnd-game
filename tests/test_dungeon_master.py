"""Tests for the DungeonMaster class."""

import pytest
from dndgame.dungeon_master import DungeonMaster


def test_dungeon_master_disabled():
    """Test that DungeonMaster can be initialized in disabled mode."""
    dm = DungeonMaster(enabled=False)
    assert dm.enabled is False

    # All narration methods should return None when disabled
    assert dm.narrate_combat_start("Player", "Goblin") is None
    assert dm.narrate_attack("Player", "Goblin", "Sword", 5, True) is None
    assert dm.narrate_spell_cast("Player", "Goblin", "Fireball", 10) is None
    assert dm.narrate_victory("Player", "Goblin") is None
    assert dm.narrate_defeat("Player", "Goblin") is None
    assert dm.narrate_action_choice("Player", ["attack", "defend"]) is None


def test_dungeon_master_without_api_key():
    """Test that DungeonMaster handles missing API key gracefully."""
    # This should auto-disable if API key is not configured
    dm = DungeonMaster(enabled=True)

    # If API key is not set or is placeholder, should be disabled
    # Note: This test may pass or fail depending on if .env has a real API key
    # The important part is that it doesn't crash
    result = dm.narrate_combat_start("Player", "Goblin")

    # Result should either be None (disabled) or a string (enabled with valid API key)
    assert result is None or isinstance(result, str)
