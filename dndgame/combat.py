from typing import List

from dndgame.character import Character
from dndgame.dice import roll


class Combat:
    def __init__(self, player: "Character", enemy: "Character") -> None:
        """
        Initialize a combat instance.

        Args:
            player (Character): The player character.
            enemy (Character): The enemy character.
        """
        self.player = player
        self.enemy = enemy
        self.round: int = 0
        self.initiative_order: List["Character"] = []

    def roll_initiative(self) -> List["Character"]:
        """
        Roll initiative to determine the combat order.

        Returns:
            List[Character]: The order of combatants based on initiative rolls.
        """
        player_init = roll(20, 1) + self.player.get_modifier("DEX")
        enemy_init = roll(20, 1) + self.enemy.get_modifier("DEX")

        if player_init >= enemy_init:
            self.initiative_order = [self.player, self.enemy]
        else:
            self.initiative_order = [self.enemy, self.player]

        return self.initiative_order

    def attack(self, attacker: "Character", defender: "Character") -> int:
        """
        Perform an attack from one character to another.

        Args:
            attacker (Character): The attacking character.
            defender (Character): The defending character.

        Returns:
            int: The damage dealt to the defender, or 0 if the attack misses.
        """
        attack_roll = roll(20, 1) + attacker.get_modifier("STR")
        weapon_max_damage = 6
        if attack_roll >= defender.armor_class:
            damage = roll(weapon_max_damage, 1)
            defender.hp -= damage
            return damage
        return 0
