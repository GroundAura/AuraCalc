### IMPORTS ###

# builtins
import random

# external

# internal
#import app_globals



### FUNCTIONS ###

def roll_dice(dice_string: str):
	"""
	Generates a random number based on the dice string.

	Args:
		dice_string (str): The dice notation (e.g., `"3d6"`).

	Returns:
		int: The random number.
		list: The individual results of each die.
	"""
	try:
		num_dice, num_sides = map(int, dice_string.lower().split('d'))
		rolls = [random.randint(1, num_sides) for _ in range(num_dice)]
		total = str(sum(rolls))
		return total, rolls
	except ValueError:
		#return 0, []
		raise ValueError("Invalid dice notation. Use 'XdY' format, e.g., '3d6'.")

if __name__ == "__main__":
	dice_input = "3d6"
	total, rolls = roll_dice(dice_input)
	print(f"Rolling {dice_input}\n Total: {total}\n Rolls: {rolls}")


