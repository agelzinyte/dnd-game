from typing import Dict, List, Optional

from dndgame.dice import roll
from dndgame.weapons import Weapon, WEAPONS
from dndgame.spells import Spell

# Race configuration registry
# Each race maps to a dictionary of ability score bonuses
RACES: Dict[str, Dict[str, int]] = {
    "Human": {
        "STR": 1,
        "DEX": 1,
        "CON": 1,
        "INT": 1,
        "WIS": 1,
        "CHA": 1,
    },
    "Elf": {
        "DEX": 2,
    },
    "Dwarf": {
        "CON": 2,
    },
    "Halfling": {
        "DEX": 2,
        "CHA": 1,
    },
    "Orc": {
        "STR": 2,
        "CON": 1,
        "INT": -1,
    },
}

# XP required for each level (D&D 5e progression)
XP_TABLE: Dict[int, int] = {
    1: 0,
    2: 300,
    3: 900,
    4: 2700,
    5: 6500,
    6: 14000,
    7: 23000,
    8: 34000,
    9: 48000,
    10: 64000,
}

# Spell slots by character level
SPELL_SLOTS_BY_LEVEL: Dict[int, Dict[int, int]] = {
    1: {1: 2, 2: 0, 3: 0},
    2: {1: 3, 2: 0, 3: 0},
    3: {1: 4, 2: 2, 3: 0},
    4: {1: 4, 2: 3, 3: 0},
    5: {1: 4, 2: 3, 3: 2},
    6: {1: 4, 2: 3, 3: 3},
    7: {1: 4, 2: 3, 3: 3},
    8: {1: 4, 2: 3, 3: 3},
    9: {1: 4, 2: 3, 3: 3},
    10: {1: 4, 2: 3, 3: 3},
}


class Entity:
    """Base class for all entities in the game (characters, enemies, etc.).

    Attributes:
        name: The entity's name.
        stats: Dictionary mapping ability score names to their values.
        hp: Current hit points.
        max_hp: Maximum hit points.
        armor_class: Armor class value.
        weapon: The entity's equipped weapon.
    """

    def __init__(
        self,
        name: str,
        stats: Dict[str, int],
        hp: int,
        armor_class: int = 10,
        weapon: Optional[Weapon] = None,
    ) -> None:
        """Initialize an Entity instance.

        Args:
            name: The entity's name.
            stats: Dictionary mapping ability score names to their values.
            hp: Maximum/starting hit points.
            armor_class: Armor class value (defaults to 10).
            weapon: The entity's equipped weapon (defaults to None).
        """
        self.name: str = name
        self.stats: Dict[str, int] = stats
        self.max_hp: int = hp
        self.hp: int = hp
        self.armor_class: int = armor_class
        self.weapon: Optional[Weapon] = weapon if weapon else WEAPONS["Club"]

    def get_modifier(self, stat: str) -> int:
        """Calculate ability modifier for a given ability score.

        The modifier is calculated as (ability_score - 10) // 2, following
        standard D&D rules.

        Args:
            stat: The ability score name (e.g., "STR", "DEX", "CON").

        Returns:
            The ability modifier as an integer.

        Raises:
            KeyError: If the stat name is not in the stats dictionary.
        """
        return (self.stats[stat] - 10) // 2

    def is_alive(self) -> bool:
        """Check if the entity is still alive.

        Returns:
            True if HP is greater than 0, False otherwise.
        """
        return self.hp > 0


class Character(Entity):
    """Represents a D&D character with attributes, stats, and racial bonuses.

    Attributes:
        name: The character's name.
        race: The character's race (e.g., "Dwarf", "Elf", "Human").
        stats: Dictionary mapping ability score names to their values.
        base_hp: Base hit points before modifiers.
        hp: Current hit points.
        max_hp: Maximum hit points.
        level: Character level (starts at 1).
        xp: Current experience points.
        armor_class: Armor class value (defaults to 10).
        known_spells: List of spells the character knows.
        spell_slots: Dictionary mapping spell levels to available slots.
        max_spell_slots: Dictionary mapping spell levels to maximum slots.
    """

    def __init__(self, name: str, race: str, base_hp: int) -> None:
        """Initialize a new Character instance.

        Args:
            name: The character's name.
            race: The character's race (e.g., "Dwarf", "Elf", "Human").
            base_hp: Base hit points before modifiers.
        """
        self.race: str = race
        self.base_hp: int = base_hp
        self.level: int = 1
        self.xp: int = 0
        self.known_spells: List[Spell] = []
        # Spell slots for level 1 character (cantrips have unlimited uses)
        self.max_spell_slots: Dict[int, int] = SPELL_SLOTS_BY_LEVEL[1].copy()
        self.spell_slots: Dict[int, int] = SPELL_SLOTS_BY_LEVEL[1].copy()
        # Initialize Entity with empty stats - they'll be set by roll_stats()
        super().__init__(name, {}, 0)

    def roll_stats(self) -> None:
        """Roll ability scores and calculate hit points.

        Rolls 3d6 for each of the six ability scores (STR, DEX, CON, INT, WIS, CHA)
        and updates the character's stats. Also calculates max_hp based on base_hp
        plus the Constitution modifier, and sets current hp to max_hp.
        """
        print("Rolling stats...\n")
        stats_list = ["STR", "DEX", "CON", "INT", "WIS", "CHA"]
        # Print rolling messages and create stats dict using comprehension
        [print(f"Rolling {stat}...") for stat in stats_list]
        self.stats = {stat: roll(6, 3) for stat in stats_list}

        self.max_hp = self.base_hp + self.get_modifier("CON")
        self.hp = self.max_hp

    def apply_racial_bonuses(self) -> None:
        """Apply racial bonuses to ability scores based on character race.

        Looks up the race in the RACES registry and applies the configured
        bonuses to the character's stats. If the race is not found in the
        registry, no bonuses are applied.
        """
        if self.race in RACES:
            bonuses = RACES[self.race]
            # Apply bonuses only to existing stats using dict comprehension
            self.stats = {
                stat: self.stats[stat] + bonuses.get(stat, 0) for stat in self.stats
            }

    def add_spell(self, spell: Spell) -> None:
        """Add a spell to the character's known spells.

        Args:
            spell: The spell to add to known spells.
        """
        if spell not in self.known_spells:
            self.known_spells.append(spell)

    def can_cast_spell(self, spell: Spell) -> bool:
        """Check if the character can cast a given spell.

        Args:
            spell: The spell to check.

        Returns:
            True if the spell can be cast (in known spells and has slots available).
        """
        if spell not in self.known_spells:
            return False
        # Cantrips (level 0) can always be cast
        if spell.level == 0:
            return True
        # Check if spell slots are available
        return self.spell_slots.get(spell.level, 0) > 0

    def cast_spell(self, spell: Spell, target: "Entity") -> int:
        """Cast a spell on a target.

        Args:
            spell: The spell to cast.
            target: The target entity.

        Returns:
            The damage dealt (or negative for healing).

        Raises:
            ValueError: If the spell cannot be cast.
        """
        if not self.can_cast_spell(spell):
            raise ValueError(f"Cannot cast {spell.name}")

        # Use a spell slot (unless it's a cantrip)
        if spell.level > 0:
            self.spell_slots[spell.level] -= 1

        # Cast the spell
        return spell.cast(self, target)

    def rest(self) -> None:
        """Take a rest to restore spell slots and HP."""
        self.spell_slots = self.max_spell_slots.copy()
        self.hp = self.max_hp

    def get_available_spells(self) -> List[Spell]:
        """Get list of spells that can currently be cast.

        Returns:
            List of castable spells.
        """
        return [spell for spell in self.known_spells if self.can_cast_spell(spell)]

    def get_xp_for_next_level(self) -> int:
        """Get XP required for next level.

        Returns:
            XP needed to reach next level, or 0 if at max level.
        """
        if self.level >= 10:
            return 0
        return XP_TABLE[self.level + 1]

    def gain_xp(self, amount: int) -> bool:
        """Gain experience points and check for level up.

        Args:
            amount: Amount of XP to gain.

        Returns:
            True if character leveled up, False otherwise.
        """
        self.xp += amount
        print(f"\n+{amount} XP! (Total: {self.xp} XP)")

        # Check for level up (can level up multiple times)
        leveled_up = False
        while self.level < 10 and self.xp >= XP_TABLE[self.level + 1]:
            self.level_up()
            leveled_up = True
        return leveled_up

    def level_up(self) -> None:
        """Level up the character, improving stats and abilities."""
        old_level = self.level
        self.level += 1

        print(f"\n{'='*50}")
        print(f"LEVEL UP! You are now level {self.level}!")
        print(f"{'='*50}")

        # Increase max HP (roll hit die + CON modifier)
        hp_increase = roll(10, 1) + self.get_modifier("CON")
        if hp_increase < 1:
            hp_increase = 1
        self.max_hp += hp_increase
        self.hp = self.max_hp
        print(f"Max HP increased by {hp_increase}! New max HP: {self.max_hp}")

        # Update spell slots
        self.max_spell_slots = SPELL_SLOTS_BY_LEVEL[self.level].copy()
        self.spell_slots = SPELL_SLOTS_BY_LEVEL[self.level].copy()

        # Show spell slot improvements
        old_slots = SPELL_SLOTS_BY_LEVEL[old_level]
        new_slots = SPELL_SLOTS_BY_LEVEL[self.level]
        for spell_level in sorted(new_slots.keys()):
            if new_slots[spell_level] > old_slots.get(spell_level, 0):
                if old_slots.get(spell_level, 0) == 0:
                    print(f"Gained Level {spell_level} spell slots: {new_slots[spell_level]}")
                else:
                    print(
                        f"Level {spell_level} spell slots increased: {old_slots[spell_level]} -> {new_slots[spell_level]}"
                    )

        # Every 4 levels, increase a random stat by 1
        if self.level % 4 == 0:
            stats_list = list(self.stats.keys())
            improved_stat = stats_list[roll(len(stats_list), 1) - 1]
            self.stats[improved_stat] += 1
            print(
                f"Ability Score Improvement! {improved_stat} increased to {self.stats[improved_stat]}"
            )


class Enemy(Entity):
    """Represents an enemy entity in combat.

    Attributes:
        name: The enemy's name.
        stats: Dictionary mapping ability score names to their values.
        hp: Current hit points.
        max_hp: Maximum hit points.
        armor_class: Armor class value.
        weapon: The enemy's equipped weapon.
        xp_value: Experience points awarded for defeating this enemy.
    """

    def __init__(
        self,
        name: str,
        stats: Dict[str, int],
        hp: int,
        armor_class: int = 10,
        weapon: Optional[Weapon] = None,
        xp_value: int = 50,
    ) -> None:
        """Initialize an Enemy instance.

        Args:
            name: The enemy's name.
            stats: Dictionary mapping ability score names to their values.
            hp: Maximum/starting hit points.
            armor_class: Armor class value (defaults to 10).
            weapon: The enemy's equipped weapon (defaults to None).
            xp_value: XP awarded for defeating this enemy (defaults to 50).
        """
        super().__init__(name, stats, hp, armor_class, weapon)
        self.xp_value: int = xp_value
