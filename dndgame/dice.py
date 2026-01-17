import random


def roll(dice_type: int, number_of_dice: int) -> int:
    """
    Roll a specified number of dice of a given type and return the total.

    Args:
        dice_type (int): The number of sides on the dice.
        number_of_dice (int): The number of dice to roll.

    Returns:
        int: The total sum of the dice rolls.
    """
    rolls = []
    total = 0
    for _ in range(number_of_dice):
        roll_result = random.randint(1, dice_type)
        rolls.append(roll_result)
        total += roll_result
    print(f"Rolling {number_of_dice}d{dice_type}: {rolls} = {total}")
    return total


def roll_with_advantage(dice_type: int) -> int:
    """
    Roll a dice twice and return the higher result (advantage).

    Args:
        dice_type (int): The number of sides on the dice.

    Returns:
        int: The higher of the two rolls.
    """
    roll1 = roll(dice_type, 1)
    roll2 = roll(dice_type, 1)
    return max(roll1, roll2)


def roll_with_disadvantage(dice_type: int) -> int:
    """
    Roll a dice twice and return the lower result (disadvantage).

    Args:
        dice_type (int): The number of sides on the dice.

    Returns:
        int: The lower of the two rolls.
    """
    roll1 = roll(dice_type, 1)
    roll2 = roll(dice_type, 1)
    return min(roll1, roll2)
