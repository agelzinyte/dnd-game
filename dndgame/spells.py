from typing import TYPE_CHECKING, Dict

if TYPE_CHECKING:
    from dndgame.character import Entity


class Spell:
    """Represents a spell with various properties.

    Attributes:
        name: The spell's name.
        level: The spell level (0-9, where 0 is a cantrip).
        school: The school of magic (e.g., "Evocation", "Abjuration").
        spell_power: The power/damage of the spell.
    """

    def __init__(self, name: str, level: int, school: str, spell_power: int) -> None:
        """Initialize a spell instance.

        Args:
            name: The name of the spell.
            level: The level of the spell (0-9).
            school: The school of magic.
            spell_power: The power/damage dealt by the spell.
        """
        self.name: str = name
        self.level: int = level
        self.school: str = school
        self.spell_power: int = spell_power

    def cast(self, caster: "Entity", target: "Entity") -> int:
        """Cast the spell on a target.

        Args:
            caster: The entity casting the spell.
            target: The target of the spell.

        Returns:
            The damage dealt to the target.
        """
        damage = self.spell_power + caster.get_modifier("INT")
        if damage < 0:
            damage = 0
        target.hp -= damage
        if target.hp < 0:
            target.hp = 0
        return damage

    def __str__(self) -> str:
        """Return a string representation of the spell.

        Returns:
            A string describing the spell.
        """
        level_str = "Cantrip" if self.level == 0 else f"Level {self.level}"
        return f"{self.name} ({level_str}, {self.school}, Power: {self.spell_power})"


class SpellBook:
    def __init__(self) -> None:
        """
        Initialize a spellbook instance.
        """
        self.spells: list[Spell] = []

    def add_spell(self, spell: Spell) -> None:
        """
        Add a spell to the spellbook.

        Args:
            spell (Spell): The spell to add.
        """
        self.spells.append(spell)

    def get_available_spells(self, spell_level: int) -> list[Spell]:
        """
        Retrieve all spells available for a given level.

        Args:
            spell_level (int): The level of spells to retrieve.

        Returns:
            list[Spell]: A list of spells available for the given level.
        """
        available = []
        for spell in self.spells:
            if spell.level <= spell_level:
                available.append(spell)
        return available


# Spell registry with common D&D spells
SPELLS: Dict[str, Spell] = {
    # Cantrips (Level 0)
    "Fire Bolt": Spell("Fire Bolt", 0, "Evocation", 5),
    "Ray of Frost": Spell("Ray of Frost", 0, "Evocation", 4),
    "Shocking Grasp": Spell("Shocking Grasp", 0, "Evocation", 4),
    # Level 1 Spells
    "Magic Missile": Spell("Magic Missile", 1, "Evocation", 7),
    "Burning Hands": Spell("Burning Hands", 1, "Evocation", 6),
    "Shield": Spell("Shield", 1, "Abjuration", 0),  # Defensive spell
    "Cure Wounds": Spell("Cure Wounds", 1, "Evocation", -5),  # Healing spell (negative damage)
    # Level 2 Spells
    "Scorching Ray": Spell("Scorching Ray", 2, "Evocation", 10),
    "Shatter": Spell("Shatter", 2, "Evocation", 9),
    # Level 3 Spells
    "Fireball": Spell("Fireball", 3, "Evocation", 15),
    "Lightning Bolt": Spell("Lightning Bolt", 3, "Evocation", 14),
}


def get_spellbook() -> Dict[str, Spell]:
    """Retrieve the spellbook containing all available spells.

    Returns:
        A dictionary of spell names to Spell objects.
    """
    return SPELLS
