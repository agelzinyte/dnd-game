"""Comprehensive tests for the combat module."""

import pytest
from dndgame.combat import Combat
from dndgame.character import Character, Enemy
from dndgame.weapons import WEAPONS


class TestCombat:
    """Tests for the Combat class."""

    def test_combat_creation(self):
        """Test basic combat initialization."""
        player_stats = {"STR": 14, "DEX": 12, "CON": 14, "INT": 10, "WIS": 10, "CHA": 10}
        player = Character("TestPlayer", "Human", 10)
        player.stats = player_stats
        player.max_hp = 15
        player.hp = 15

        enemy_stats = {"STR": 12, "DEX": 14, "CON": 10, "INT": 8, "WIS": 8, "CHA": 8}
        enemy = Enemy("Goblin", enemy_stats, hp=10)

        combat = Combat(player, enemy)

        assert combat.player == player
        assert combat.enemy == enemy
        assert combat.round == 0
        assert combat.initiative_order == []

    def test_roll_initiative_player_wins(self):
        """Test initiative rolling when player wins."""
        player_stats = {"STR": 10, "DEX": 20, "CON": 10, "INT": 10, "WIS": 10, "CHA": 10}  # High DEX
        player = Character("TestPlayer", "Human", 10)
        player.stats = player_stats

        enemy_stats = {"STR": 10, "DEX": 8, "CON": 10, "INT": 10, "WIS": 10, "CHA": 10}  # Low DEX
        enemy = Enemy("SlowEnemy", enemy_stats, hp=10)

        combat = Combat(player, enemy)
        
        # Run multiple times to account for randomness
        player_first_count = 0
        for _ in range(10):
            initiative_order = combat.roll_initiative()
            if initiative_order[0] == player:
                player_first_count += 1

        # With DEX +5 vs -1, player should win most of the time
        assert player_first_count >= 5  # At least 50% of the time

    def test_roll_initiative_enemy_wins(self):
        """Test initiative rolling when enemy wins."""
        player_stats = {"STR": 10, "DEX": 8, "CON": 10, "INT": 10, "WIS": 10, "CHA": 10}  # Low DEX
        player = Character("TestPlayer", "Human", 10)
        player.stats = player_stats

        enemy_stats = {"STR": 10, "DEX": 20, "CON": 10, "INT": 10, "WIS": 10, "CHA": 10}  # High DEX
        enemy = Enemy("FastEnemy", enemy_stats, hp=10)

        combat = Combat(player, enemy)
        
        # Run multiple times to account for randomness
        enemy_first_count = 0
        for _ in range(10):
            initiative_order = combat.roll_initiative()
            if initiative_order[0] == enemy:
                enemy_first_count += 1

        # With DEX -1 vs +5, enemy should win most of the time
        assert enemy_first_count >= 5  # At least 50% of the time

    def test_attack_hit(self):
        """Test successful attack."""
        attacker_stats = {"STR": 20, "DEX": 10, "CON": 10, "INT": 10, "WIS": 10, "CHA": 10}  # High STR
        attacker = Character("Attacker", "Human", 10)
        attacker.stats = attacker_stats
        attacker.weapon = WEAPONS["Longsword"]

        defender_stats = {"STR": 10, "DEX": 10, "CON": 10, "INT": 10, "WIS": 10, "CHA": 10}
        defender = Enemy("Defender", defender_stats, hp=20, armor_class=10)  # Low AC

        combat = Combat(attacker, defender)
        
        # Run multiple attacks
        total_damage = 0
        hits = 0
        for _ in range(20):
            initial_hp = defender.hp
            defender.hp = 20  # Reset HP
            damage = combat.attack(attacker, defender)
            if damage > 0:
                hits += 1
                total_damage += damage
                assert defender.hp == 20 - damage
                assert 1 <= damage <= 8  # Longsword is 1d8

        # With STR +5 vs AC 10, should hit most of the time
        assert hits >= 10  # At least 50% hit rate (AC 10 requires 10+ on d20, modifier gives +5)

    def test_attack_miss(self):
        """Test missed attack."""
        attacker_stats = {"STR": 8, "DEX": 10, "CON": 10, "INT": 10, "WIS": 10, "CHA": 10}  # Low STR
        attacker = Character("Attacker", "Human", 10)
        attacker.stats = attacker_stats

        defender_stats = {"STR": 10, "DEX": 10, "CON": 10, "INT": 10, "WIS": 10, "CHA": 10}
        defender = Enemy("Defender", defender_stats, hp=20, armor_class=20)  # Very high AC

        combat = Combat(attacker, defender)
        
        # Run multiple attacks
        misses = 0
        for _ in range(20):
            defender.hp = 20  # Reset HP
            damage = combat.attack(attacker, defender)
            if damage == 0:
                misses += 1
                assert defender.hp == 20  # HP unchanged

        # With STR -1 vs AC 20, should miss most of the time
        assert misses >= 10  # At least 50% miss rate (AC 20 very high)

    def test_attack_reduces_hp(self):
        """Test that attacks reduce defender HP."""
        attacker_stats = {"STR": 20, "DEX": 10, "CON": 10, "INT": 10, "WIS": 10, "CHA": 10}
        attacker = Character("Attacker", "Human", 10)
        attacker.stats = attacker_stats
        attacker.weapon = WEAPONS["Greatsword"]  # 2d6

        defender_stats = {"STR": 10, "DEX": 10, "CON": 10, "INT": 10, "WIS": 10, "CHA": 10}
        defender = Enemy("Defender", defender_stats, hp=50, armor_class=10)

        combat = Combat(attacker, defender)
        
        initial_hp = defender.hp
        damage = combat.attack(attacker, defender)
        
        if damage > 0:  # If hit
            assert defender.hp == initial_hp - damage
            assert defender.hp < initial_hp

    def test_attack_hp_not_negative(self):
        """Test that HP doesn't go below 0."""
        attacker_stats = {"STR": 20, "DEX": 10, "CON": 10, "INT": 10, "WIS": 10, "CHA": 10}
        attacker = Character("Attacker", "Human", 10)
        attacker.stats = attacker_stats
        attacker.weapon = WEAPONS["Greataxe"]  # 1d12

        defender_stats = {"STR": 10, "DEX": 10, "CON": 10, "INT": 10, "WIS": 10, "CHA": 10}
        defender = Enemy("Defender", defender_stats, hp=1, armor_class=5)  # Very low HP and AC

        combat = Combat(attacker, defender)
        
        # Attack multiple times to ensure a hit
        for _ in range(20):
            damage = combat.attack(attacker, defender)
            if damage > 0:
                assert defender.hp == 0  # Should be 0, not negative
                break

    def test_attack_with_different_weapons(self):
        """Test attacks with different weapon types."""
        attacker_stats = {"STR": 15, "DEX": 10, "CON": 10, "INT": 10, "WIS": 10, "CHA": 10}
        attacker = Character("Attacker", "Human", 10)
        attacker.stats = attacker_stats

        defender_stats = {"STR": 10, "DEX": 10, "CON": 10, "INT": 10, "WIS": 10, "CHA": 10}
        defender = Enemy("Defender", defender_stats, hp=100, armor_class=5)  # Low AC for guaranteed hits

        combat = Combat(attacker, defender)

        # Test different weapons
        weapons_to_test = ["Dagger", "Longsword", "Greatsword", "Greataxe"]
        
        for weapon_name in weapons_to_test:
            attacker.weapon = WEAPONS[weapon_name]
            defender.hp = 100  # Reset HP
            
            # Attack until we get a hit
            for _ in range(20):
                damage = combat.attack(attacker, defender)
                if damage > 0:
                    weapon = WEAPONS[weapon_name]
                    # Damage should be within weapon's range
                    assert 1 <= damage <= (weapon.damage_die * weapon.damage_dice_count)
                    break

    def test_attack_without_weapon_uses_unarmed(self):
        """Test that entities without weapons use unarmed strike."""
        attacker_stats = {"STR": 20, "DEX": 10, "CON": 10, "INT": 10, "WIS": 10, "CHA": 10}
        attacker = Character("Attacker", "Human", 10)
        attacker.stats = attacker_stats
        attacker.weapon = None  # No weapon

        defender_stats = {"STR": 10, "DEX": 10, "CON": 10, "INT": 10, "WIS": 10, "CHA": 10}
        defender = Enemy("Defender", defender_stats, hp=20, armor_class=5)

        combat = Combat(attacker, defender)
        
        # Attack until we get a hit
        for _ in range(20):
            defender.hp = 20
            damage = combat.attack(attacker, defender)
            if damage > 0:
                assert damage == 1  # Unarmed strike deals 1 damage
                break

    def test_combat_round_tracking(self):
        """Test that combat rounds are tracked."""
        player_stats = {"STR": 10, "DEX": 10, "CON": 10, "INT": 10, "WIS": 10, "CHA": 10}
        player = Character("Player", "Human", 10)
        player.stats = player_stats

        enemy_stats = {"STR": 10, "DEX": 10, "CON": 10, "INT": 10, "WIS": 10, "CHA": 10}
        enemy = Enemy("Enemy", enemy_stats, hp=10)

        combat = Combat(player, enemy)

        assert combat.round == 0
        combat.round += 1
        assert combat.round == 1
        combat.round += 1
        assert combat.round == 2

    def test_multiple_attacks_in_combat(self):
        """Test multiple attacks in a combat scenario."""
        attacker_stats = {"STR": 18, "DEX": 10, "CON": 10, "INT": 10, "WIS": 10, "CHA": 10}
        attacker = Character("Attacker", "Human", 10)
        attacker.stats = attacker_stats
        attacker.weapon = WEAPONS["Longsword"]

        defender_stats = {"STR": 10, "DEX": 10, "CON": 10, "INT": 10, "WIS": 10, "CHA": 10}
        defender = Enemy("Defender", defender_stats, hp=30, armor_class=12)

        combat = Combat(attacker, defender)
        
        total_damage = 0
        attacks = 0
        
        # Simulate several rounds of combat
        while defender.hp > 0 and attacks < 20:
            damage = combat.attack(attacker, defender)
            total_damage += damage
            attacks += 1

        assert defender.hp == max(0, 30 - total_damage)
        assert not defender.is_alive() or attacks == 20
