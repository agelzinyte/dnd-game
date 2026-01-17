from dndgame.character import RACES, Character, Enemy
from dndgame.combat import Combat


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
    for i, race_name in enumerate(race_list, start=1):
        bonuses = RACES[race_name]
        bonus_desc = ", ".join(
            f"{'+' if bonus >= 0 else ''}{bonus} {stat}"
            for stat, bonus in bonuses.items()
        )
        print(f"{i}. {race_name} ({bonus_desc})")

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

    character = Character(name, race, 10)
    character.roll_stats()
    character.apply_racial_bonuses()
    return character


def display_character(character: Character) -> None:
    """Display character information to the console.

    Prints the character's name, race, all ability scores with modifiers,
    and current hit points.

    Args:
        character: The Character instance to display.
    """
    print(f"\n{character.name} the {character.race}")
    print("\nStats:")
    for stat, value in character.stats.items():
        modifier = character.get_modifier(stat)
        print(f"{stat}: {value} ({'+' if modifier >= 0 else ''}{modifier})")
    print(f"\nHP: {character.hp}")


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
    goblin = Enemy("Goblin", goblin_stats, hp=5, armor_class=10)

    print(f"\nA {goblin.name} appears!")
    combat = Combat(player, goblin)
    combat.roll_initiative()

    while player.is_alive() and goblin.is_alive():
        print(f"\n--- Round {combat.round + 1} ---")
        print(f"{player.name} HP: {player.hp}/{player.max_hp}")
        print(f"{goblin.name} HP: {goblin.hp}/{goblin.max_hp}")

        # Player's turn
        print("\nYour turn!")
        print("1. Attack")
        print("2. Run away")
        print()

        while True:
            choice = input("What do you do? ").strip()
            if choice in ("1", "2"):
                break
            print("Please enter 1 to attack or 2 to run away.")

        if choice == "2":
            print("You run away from the fight!")
            return False

        # Player attacks
        damage = combat.attack(player, goblin)
        if damage > 0:
            print(f"You hit the {goblin.name} for {damage} damage!")
        else:
            print("You missed!")

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
        print("3. Quit")

        while True:
            choice = input("Enter choice (1-3): ").strip()
            if choice in ("1", "2", "3"):
                break
            print("Please enter 1, 2, or 3.")

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
            break


if __name__ == "__main__":
    main()
