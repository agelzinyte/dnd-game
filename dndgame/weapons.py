from typing import Dict


class Weapon:
    """Represents a weapon with damage dice and properties.

    Attributes:
        name: The weapon's name.
        damage_die: The type of die used for damage (e.g., 4 for d4, 6 for d6).
        damage_dice_count: The number of damage dice to roll (default 1).
    """

    def __init__(self, name: str, damage_die: int, damage_dice_count: int = 1) -> None:
        """Initialize a Weapon instance.

        Args:
            name: The weapon's name.
            damage_die: The type of die used for damage (e.g., 4, 6, 8, 10, 12).
            damage_dice_count: The number of damage dice to roll (default 1).
        """
        self.name: str = name
        self.damage_die: int = damage_die
        self.damage_dice_count: int = damage_dice_count

    def __str__(self) -> str:
        """Return a string representation of the weapon.

        Returns:
            A string in the format "Name (XdY)" where X is the dice count and Y is the die type.
        """
        return f"{self.name} ({self.damage_dice_count}d{self.damage_die})"


# Weapon registry with pre-defined weapons
WEAPONS: Dict[str, Weapon] = {
    "Dagger": Weapon("Dagger", damage_die=4),
    "Shortsword": Weapon("Shortsword", damage_die=6),
    "Longsword": Weapon("Longsword", damage_die=8),
    "Battleaxe": Weapon("Battleaxe", damage_die=8),
    "Greatsword": Weapon("Greatsword", damage_die=6, damage_dice_count=2),
    "Greataxe": Weapon("Greataxe", damage_die=12),
    "Club": Weapon("Club", damage_die=4),
    "Mace": Weapon("Mace", damage_die=6),
    "Warhammer": Weapon("Warhammer", damage_die=8),
}
