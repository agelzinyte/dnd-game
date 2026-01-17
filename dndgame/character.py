from typing import Dict

from dndgame.dice import roll

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


class Character:
    """Represents a D&D character with attributes, stats, and racial bonuses.

    Attributes:
        name: The character's name.
        race: The character's race (e.g., "Dwarf", "Elf", "Human").
        stats: Dictionary mapping ability score names to their values.
        base_hp: Base hit points before modifiers.
        hp: Current hit points.
        max_hp: Maximum hit points.
        level: Character level (starts at 1).
        armor_class: Armor class value (defaults to 10).
    """

    def __init__(self, name: str, race: str, base_hp: int) -> None:
        """Initialize a new Character instance.

        Args:
            name: The character's name.
            race: The character's race (e.g., "Dwarf", "Elf", "Human").
            base_hp: Base hit points before modifiers.
        """
        self.name: str = name
        self.race: str = race
        self.stats: Dict[str, int] = {}
        self.base_hp: int = base_hp
        self.hp: int = 0
        self.max_hp: int = 0
        self.level: int = 1
        self.armor_class: int = 10

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

    def roll_stats(self) -> None:
        """Roll ability scores and calculate hit points.

        Rolls 3d6 for each of the six ability scores (STR, DEX, CON, INT, WIS, CHA)
        and updates the character's stats. Also calculates max_hp based on base_hp
        plus the Constitution modifier, and sets current hp to max_hp.
        """
        print("Rolling stats...\n")
        stats = ["STR", "DEX", "CON", "INT", "WIS", "CHA"]
        for stat in stats:
            print(f"Rolling {stat}...")
            self.stats[stat] = roll(6, 3)

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
            for stat, bonus in bonuses.items():
                if stat in self.stats:
                    self.stats[stat] += bonus
