from dndgame.character import RACES, Character, Enemy
from dndgame.combat import Combat
from dndgame.weapons import WEAPONS
from dndgame.spells import SPELLS


def create_character() -> Character:
    """Create a new character through user interaction.

    Prompts the user to enter a character name and select a race, then
    creates a Character instance with rolled stats and racial bonuses applied.

    Returns:
        A new Character instance with stats rolled and racial bonuses applied.
    """
    print("Welcome to D&D Adventure!")
    while True:
        name = input("Enter your character's name: ").strip()
        if name:
            break
        print("Name cannot be empty. Please enter a valid name.")

    # Dynamically generate race menu from RACES registry
    print("\nChoose your race:")
    race_list = list(RACES.keys())
    # Generate menu items using list comprehension and print them
    menu_items = [
        f"{i}. {race_name} ({', '.join(('+' if bonus >= 0 else '') + str(bonus) + ' ' + stat for stat, bonus in RACES[race_name].items())})"
        for i, race_name in enumerate(race_list, start=1)
    ]
    print("\n".join(menu_items))

    while True:
        race_choice = input(f"Enter choice (1-{len(race_list)}): ")
        try:
            choice_num = int(race_choice)
            if 1 <= choice_num <= len(race_list):
                race = race_list[choice_num - 1]
                break
            else:
                print(f"Please enter a number between 1 and {len(race_list)}.")
        except ValueError:
            print("Please enter a valid number.")
    print("\n")

    # Weapon selection
    print("Choose your weapon:")
    weapon_list = list(WEAPONS.keys())
    weapon_menu_items = [
        f"{i}. {WEAPONS[weapon_name]}"
        for i, weapon_name in enumerate(weapon_list, start=1)
    ]
    print("\n".join(weapon_menu_items))

    while True:
        weapon_choice = input(f"Enter choice (1-{len(weapon_list)}): ")
        try:
            choice_num = int(weapon_choice)
            if 1 <= choice_num <= len(weapon_list):
                weapon_name = weapon_list[choice_num - 1]
                weapon = WEAPONS[weapon_name]
                break
            else:
                print(f"Please enter a number between 1 and {len(weapon_list)}.")
        except ValueError:
            print("Please enter a valid number.")
    print("\n")

    character = Character(name, race, 10)
    character.roll_stats()
    character.apply_racial_bonuses()
    character.weapon = weapon

    # Spell selection
    print("Do you want to learn spells? (You can learn 3 spells)")
    print("1. Yes, I want to be a spellcaster")
    print("2. No, I'll stick to weapons")

    while True:
        spell_choice = input("Enter choice (1-2): ").strip()
        if spell_choice in ("1", "2"):
            break
        print("Please enter 1 or 2.")

    if spell_choice == "1":
        print("\nChoose 3 spells to learn:")
        spell_list = list(SPELLS.keys())
        spell_menu_items = [
            f"{i}. {SPELLS[spell_name]}"
            for i, spell_name in enumerate(spell_list, 1)
        ]
        print("\n".join(spell_menu_items))

        chosen_spells = []
        while len(chosen_spells) < 3:
            spell_idx_input = input(
                f"Choose spell {len(chosen_spells) + 1} (1-{len(spell_list)}): "
            )
            try:
                spell_idx = int(spell_idx_input)
                if 1 <= spell_idx <= len(spell_list):
                    spell_name = spell_list[spell_idx - 1]
                    spell = SPELLS[spell_name]
                    if spell in chosen_spells:
                        print("You already chose that spell. Pick a different one.")
                    else:
                        chosen_spells.append(spell)
                        character.add_spell(spell)
                        print(f"Learned {spell.name}!")
                else:
                    print(f"Please enter a number between 1 and {len(spell_list)}.")
            except ValueError:
                print("Please enter a valid number.")

    print("\n")
    return character


def display_character(character: Character) -> None:
    """Display character information to the console.

    Prints the character's name, race, all ability scores with modifiers,
    current hit points, equipped weapon, and known spells.

    Args:
        character: The Character instance to display.
    """
    print(f"\n{character.name} the {character.race}")
    print("\nStats:")
    # Generate stat lines using list comprehension with modifiers calculated once
    stat_lines = [
        f"{stat}: {value} ({'+' if modifier >= 0 else ''}{modifier})"
        for stat, value, modifier in (
            (stat, value, character.get_modifier(stat))
            for stat, value in character.stats.items()
        )
    ]
    print("\n".join(stat_lines))
    print(f"\nHP: {character.hp}/{character.max_hp}")
    print(f"Weapon: {character.weapon}")

    if character.known_spells:
        print("\nKnown Spells:")
        for spell in character.known_spells:
            level_str = "Cantrip" if spell.level == 0 else f"Level {spell.level}"
            print(f"  - {spell.name} ({level_str})")
        print("\nSpell Slots:")
        for level in sorted(character.spell_slots.keys()):
            if character.max_spell_slots[level] > 0:
                print(
                    f"  Level {level}: {character.spell_slots[level]}/{character.max_spell_slots[level]}"
                )


def start_combat(player: Character) -> bool:
    """Start a combat encounter with a goblin using the Combat class.

    Uses the Combat class to manage combat rounds. The goblin attacks the player
    each round. Combat continues until either the player or goblin reaches 0 HP,
    or the player chooses to run away.

    Args:
        player: The player's Character instance.

    Returns:
        True if the goblin was defeated, False if the player ran away or was defeated.
    """
    # Create goblin enemy with appropriate stats
    goblin_stats = {
        "STR": 8,
        "DEX": 14,
        "CON": 10,
        "INT": 10,
        "WIS": 8,
        "CHA": 8,
    }
    goblin = Enemy("Goblin", goblin_stats, hp=5, armor_class=10, weapon=WEAPONS["Shortsword"])

    print(f"\nA {goblin.name} appears!")
    combat = Combat(player, goblin)
    combat.roll_initiative()

    while player.is_alive() and goblin.is_alive():
        print(f"\n--- Round {combat.round + 1} ---")
        print(f"{player.name} HP: {player.hp}/{player.max_hp}")
        print(f"{goblin.name} HP: {goblin.hp}/{goblin.max_hp}")

        # Player's turn
        print("\nYour turn!")
        print("1. Attack with weapon")
        print("2. Cast spell")
        print("3. Run away")
        print()

        while True:
            choice = input("What do you do? ").strip()
            if choice in ("1", "2", "3"):
                break
            print("Please enter 1, 2, or 3.")

        if choice == "3":
            print("You run away from the fight!")
            return False

        if choice == "1":
            # Player attacks with weapon
            damage = combat.attack(player, goblin)
            if damage > 0:
                print(f"You hit the {goblin.name} for {damage} damage!")
            else:
                print("You missed!")
        elif choice == "2":
            # Cast spell
            available_spells = player.get_available_spells()
            if not available_spells:
                print("You have no spells available to cast!")
                print("Using weapon attack instead...")
                damage = combat.attack(player, goblin)
                if damage > 0:
                    print(f"You hit the {goblin.name} for {damage} damage!")
                else:
                    print("You missed!")
            else:
                print("\nAvailable spells:")
                for i, spell in enumerate(available_spells, 1):
                    slots_info = ""
                    if spell.level > 0:
                        slots_info = f" (Slots: {player.spell_slots[spell.level]}/{player.max_spell_slots[spell.level]})"
                    print(f"{i}. {spell.name} - Level {spell.level}{slots_info}")

                while True:
                    spell_choice = input(f"Choose spell (1-{len(available_spells)}) or 0 to cancel: ").strip()
                    try:
                        spell_idx = int(spell_choice)
                        if spell_idx == 0:
                            # Use weapon attack instead
                            damage = combat.attack(player, goblin)
                            if damage > 0:
                                print(f"You hit the {goblin.name} for {damage} damage!")
                            else:
                                print("You missed!")
                            break
                        if 1 <= spell_idx <= len(available_spells):
                            spell = available_spells[spell_idx - 1]
                            damage = player.cast_spell(spell, goblin)
                            if damage > 0:
                                print(f"You cast {spell.name} and deal {damage} damage!")
                            elif damage < 0:
                                print(f"You cast {spell.name} and heal for {-damage} HP!")
                            else:
                                print(f"You cast {spell.name}!")
                            break
                        else:
                            print(f"Please enter a number between 0 and {len(available_spells)}.")
                    except ValueError:
                        print("Please enter a valid number.")

        # Check if goblin is defeated
        if not goblin.is_alive():
            print(f"You defeated the {goblin.name}!")
            return True

        # Goblin's turn (if still alive)
        if goblin.is_alive():
            print(f"\n{goblin.name}'s turn!")
            damage = combat.attack(goblin, player)
            if damage > 0:
                print(f"The {goblin.name} hits you for {damage} damage!")
            else:
                print(f"The {goblin.name} missed!")

            # Check if player is defeated
            if not player.is_alive():
                print("\nYou have been defeated! Your HP reached 0.")
                return False

        combat.round += 1

    # Should not reach here, but handle edge cases
    if not player.is_alive():
        return False
    return True


def main() -> None:
    """Main game loop for the D&D Adventure game.

    Creates a character and presents a menu allowing the player to fight goblins,
    view their character stats, or quit the game.
    """
    player = create_character()

    while True:
        print("\nWhat would you like to do?")
        print("1. Fight a goblin")
        print("2. View character")
        print("3. Rest (restore HP and spell slots)")
        print("4. Quit")

        while True:
            choice = input("Enter choice (1-4): ").strip()
            if choice in ("1", "2", "3", "4"):
                break
            print("Please enter 1, 2, 3, or 4.")

        if choice == "1":
            victory = start_combat(player)
            if victory:
                print("Victory!")
            elif not player.is_alive():
                print("You have been defeated!")
                break
            else:
                print("You ran away!")
        elif choice == "2":
            display_character(player)
        elif choice == "3":
            player.rest()
            print("You take a rest and feel refreshed!")
            print(f"HP restored to {player.hp}/{player.max_hp}")
            if player.known_spells:
                print("All spell slots restored!")
        elif choice == "4":
            break


if __name__ == "__main__":
    main()
