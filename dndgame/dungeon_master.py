"""DungeonMaster class that uses OpenAI's API to narrate the game."""

import os
from typing import Optional
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()


class DungeonMaster:
    """AI-powered Dungeon Master that narrates the game using OpenAI's API.

    Attributes:
        client: OpenAI client instance.
        model: The OpenAI model to use for narration.
        enabled: Whether the DM narration is enabled.
    """

    def __init__(self, model: str = "gpt-4o-mini", enabled: bool = True) -> None:
        """Initialize the DungeonMaster.

        Args:
            model: The OpenAI model to use (default: gpt-4o-mini for cost efficiency).
            enabled: Whether to enable DM narration (default: True).
        """
        self.enabled = enabled
        self.model = model

        if self.enabled:
            api_key = os.getenv("OPENAI_API_KEY")
            if not api_key or api_key == "your_api_key_here":
                print(
                    "\n⚠️  Warning: OpenAI API key not configured. DM narration disabled."
                )
                print("Add your API key to the .env file to enable narration.\n")
                self.enabled = False
            else:
                self.client = OpenAI(api_key=api_key)

    def narrate_combat_start(self, player_name: str, enemy_name: str) -> Optional[str]:
        """Narrate the start of a combat encounter.

        Args:
            player_name: The name of the player character.
            enemy_name: The name of the enemy.

        Returns:
            The narration text, or None if disabled.
        """
        if not self.enabled:
            return None

        prompt = f"""You are a Dungeon Master narrating a D&D combat encounter.
A player character named {player_name} has just encountered a {enemy_name}.
Write a brief, vivid narration (2-3 sentences) describing the encounter as it begins.
Make it atmospheric and exciting, but keep it concise."""

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=150,
                temperature=0.8,
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"\n⚠️  DM narration error: {e}")
            return None

    def narrate_attack(
        self,
        attacker_name: str,
        defender_name: str,
        weapon_name: str,
        damage: int,
        hit: bool,
    ) -> Optional[str]:
        """Narrate a weapon attack.

        Args:
            attacker_name: The name of the attacker.
            defender_name: The name of the defender.
            weapon_name: The name of the weapon used.
            damage: The damage dealt (0 if missed).
            hit: Whether the attack hit.

        Returns:
            The narration text, or None if disabled.
        """
        if not self.enabled:
            return None

        if hit:
            prompt = f"""You are a Dungeon Master narrating a D&D combat action.
{attacker_name} attacked {defender_name} with a {weapon_name} and dealt {damage} damage.
Write a brief, vivid narration (1-2 sentences) describing this successful attack.
Make it exciting but concise."""
        else:
            prompt = f"""You are a Dungeon Master narrating a D&D combat action.
{attacker_name} attacked {defender_name} with a {weapon_name} but missed.
Write a brief, vivid narration (1-2 sentences) describing this failed attack.
Make it engaging but concise."""

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=100,
                temperature=0.8,
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"\n⚠️  DM narration error: {e}")
            return None

    def narrate_spell_cast(
        self,
        caster_name: str,
        target_name: str,
        spell_name: str,
        damage: int,
    ) -> Optional[str]:
        """Narrate a spell being cast.

        Args:
            caster_name: The name of the spellcaster.
            target_name: The name of the target.
            spell_name: The name of the spell.
            damage: The damage dealt (negative for healing).

        Returns:
            The narration text, or None if disabled.
        """
        if not self.enabled:
            return None

        if damage > 0:
            effect = f"dealing {damage} damage"
        elif damage < 0:
            effect = f"healing for {-damage} HP"
        else:
            effect = "with magical energy"

        prompt = f"""You are a Dungeon Master narrating a D&D combat action.
{caster_name} cast {spell_name} on {target_name}, {effect}.
Write a brief, vivid narration (1-2 sentences) describing this spell being cast.
Make it magical and exciting but concise."""

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=100,
                temperature=0.8,
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"\n⚠️  DM narration error: {e}")
            return None

    def narrate_victory(self, player_name: str, enemy_name: str) -> Optional[str]:
        """Narrate a combat victory.

        Args:
            player_name: The name of the victorious player.
            enemy_name: The name of the defeated enemy.

        Returns:
            The narration text, or None if disabled.
        """
        if not self.enabled:
            return None

        prompt = f"""You are a Dungeon Master narrating a D&D combat encounter.
{player_name} has defeated the {enemy_name}.
Write a brief, triumphant narration (1-2 sentences) describing the victory.
Make it satisfying and heroic but concise."""

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=100,
                temperature=0.8,
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"\n⚠️  DM narration error: {e}")
            return None

    def narrate_defeat(self, player_name: str, enemy_name: str) -> Optional[str]:
        """Narrate a player defeat.

        Args:
            player_name: The name of the defeated player.
            enemy_name: The name of the victorious enemy.

        Returns:
            The narration text, or None if disabled.
        """
        if not self.enabled:
            return None

        prompt = f"""You are a Dungeon Master narrating a D&D combat encounter.
{player_name} has been defeated by the {enemy_name}.
Write a brief, dramatic narration (1-2 sentences) describing the defeat.
Make it tense but not overly grim, and keep it concise."""

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=100,
                temperature=0.8,
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"\n⚠️  DM narration error: {e}")
            return None

    def narrate_action_choice(
        self, player_name: str, available_actions: list[str]
    ) -> Optional[str]:
        """Narrate a player's turn and available actions.

        Args:
            player_name: The name of the player.
            available_actions: List of available actions (e.g., ["Attack", "Cast Spell", "Run"]).

        Returns:
            The narration text, or None if disabled.
        """
        if not self.enabled:
            return None

        actions_str = ", ".join(available_actions[:-1]) + f", or {available_actions[-1]}"
        prompt = f"""You are a Dungeon Master narrating a D&D combat turn.
It's {player_name}'s turn. They can {actions_str}.
Write a brief narration (1 sentence) asking what they will do.
Make it engaging and keep it very concise."""

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=50,
                temperature=0.7,
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"\n⚠️  DM narration error: {e}")
            return None
