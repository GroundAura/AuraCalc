### IMPORTS ###

# builtins
import cmath
#from decimal import Decimal
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
		dice_string (str): The dice notation (e.g., `'3d6'`).

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

def quadratic_formula(a, b, c):
	# Calculate the discriminant
	#discriminant = sympify(b**2) - sympify(4) * sympify(a) * sympify(c)
	discriminant = b**2 - 4 * a * c
	# Calculate the two solutions
	#root1 = sympify((-sympify(b) + sympify(discriminant)) / (2 * sympify(a)))
	#root2 = sympify((-sympify(b) - sympify(discriminant)) / (2 * sympify(a)))
	root1 = (-b + cmath.sqrt(discriminant)) / (2 * a)
	root2 = (-b - cmath.sqrt(discriminant)) / (2 * a)
	return root1, root2

def quad_zero(a, b, c, positive = '+'):
	a = float(a)
	b = float(b)
	c = float(c)
	root1, root2 = quadratic_formula(a, b, c)
	if positive in ['True', 'p', '+', 'positive']:
		return root1
	elif positive in ['False', 'n', '-', 'negative']:
		return root2
	else:
		raise ValueError("Invalid positive argument. Use 'p' for positive, 'n' for negative.")

if __name__ == '__main__':
	#dice_input = '3d6'
	#total, rolls = roll_dice(dice_input)

	dice_string = '3*d*6'
	expression = sympify(dice_string)
	print(expression)


