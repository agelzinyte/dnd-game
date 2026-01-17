# type: ignore
from typing import Dict
from dndgame.character import Character

class Spell:
    def __init__(self, name: str, level: int, damage: int) -> None:
        """
        Initialize a spell instance.

        Args:
            name (str): The name of the spell.
            level (int): The level of the spell.
            damage (int): The damage dealt by the spell.
        """
        self.name = name
        self.level = level
        self.damage = damage

    def cast(self, caster: "Character", target: "Character") -> int:
        """
        Cast the spell on a target.

        Args:
            caster (Character): The character casting the spell.
            target (Character): The target of the spell.

        Returns:
            int: The damage dealt to the target.
        """
        pass


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


def get_spellbook() -> Dict[str, Spell]:
    """
    Retrieve the spellbook containing all available spells.

    Returns:
        Dict[str, Spell]: A dictionary of spell names to Spell objects.
    """
    pass
