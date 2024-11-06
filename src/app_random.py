### IMPORTS ###

# builtins
import random
import re

# external
from sympy import sympify

# internal
#import app_globals
from app_debug import print_debug



### FUNCTIONS ###

def parse_dice_expression(expression: str) -> str:
	pattern = re.compile(r'(\d*d\d+|\d+|[+\-*/])')
	tokens = pattern.findall(expression)
	for i, token in enumerate(tokens):
		if 'd' in token:
			result, _ = roll_dice(token)
			tokens[i] = str(result)
	return str(''.join(tokens))

def roll_dice(dice_string: str) -> tuple[int, list]:
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
		total = sum(rolls)
		print_debug(f"Rolling {dice_string}\n Total: {total}\n Rolls: {rolls}")
		return total, rolls
	except ValueError:
		#return 0, []
		raise ValueError("Invalid dice notation. Use 'XdY' format, e.g., '3d6'.")

if __name__ == "__main__":
	#dice_input = "3d6"
	#total, rolls = roll_dice(dice_input)

	dice_string = "3*d*6"
	expression = sympify(dice_string)
	print(expression)


