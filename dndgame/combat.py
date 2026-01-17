from typing import TYPE_CHECKING, List

from dndgame.dice import roll

if TYPE_CHECKING:
    from dndgame.character import Entity


class Combat:
    """Manages combat encounters between entities."""

    def __init__(self, player: "Entity", enemy: "Entity") -> None:
        """Initialize a combat instance.

        Args:
            player: The player entity.
            enemy: The enemy entity.
        """
        self.player = player
        self.enemy = enemy
        self.round: int = 0
        self.initiative_order: List["Entity"] = []

    def roll_initiative(self) -> List["Entity"]:
        """Roll initiative to determine the combat order.

        Returns:
            List of entities in initiative order (highest first).
        """
        player_init = roll(20, 1) + self.player.get_modifier("DEX")
        enemy_init = roll(20, 1) + self.enemy.get_modifier("DEX")

        if player_init >= enemy_init:
            self.initiative_order = [self.player, self.enemy]
        else:
            self.initiative_order = [self.enemy, self.player]

        return self.initiative_order

    def attack(self, attacker: "Entity", defender: "Entity") -> int:
        """Perform an attack from one entity to another.

        Args:
            attacker: The attacking entity.
            defender: The defending entity.

        Returns:
            The damage dealt to the defender, or 0 if the attack misses.
        """
        attack_roll = roll(20, 1) + attacker.get_modifier("STR")
        weapon_max_damage = 6
        if attack_roll >= defender.armor_class:
            damage = roll(weapon_max_damage, 1)
            defender.hp -= damage
            if defender.hp < 0:
                defender.hp = 0
            return damage
        return 0
