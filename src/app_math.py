### IMPORTS ###

# builtins
import cmath
#from decimal import Decimal
import random
import re

# external
from sympy import sympify
import sympy as sp

# internal
from app_logging import logging_print



### CONSTANTS ###

TAU = sp.pi * 2

CHAR_EUL = 'e'
#CHAR_EUL = 'E'

CHAR_IMAG = 'i'
#CHAR_IMAG = 'I'
#CHAR_IMAG = 'j'
#CHAR_IMAG = 'J'
#CHAR_IMAG = chr(0x03B9) # 'ι'
#CHAR_IMAG = chr(0x2148) # 'ⅈ'
##CHAR_IMAG = chr(0x1D4E09) # '𝓲'

#CHAR_INF = 'oo'
#CHAR_INF = 'inf'
#CHAR_INF = 'infty'
#CHAR_INF = 'Infinity'
CHAR_INF = chr(0x221E) # '∞'

#CHAR_INFJ = 'infj'
CHAR_INFJ = 'ComplexInfinity'

#CHAR_NAN = 'nan'
CHAR_NAN = 'NaN'

#CHAR_PHI = 'phi'
#CHAR_PHI = 'GoldenRatio'
CHAR_PHI = chr(0x03C6) # 'φ'
#CHAR_PHI = chr(0x03A6) # 'Φ'

#CHAR_PI = 'pi'
CHAR_PI = chr(0x03C0) # 'π'

#CHAR_TAU = 'tau'
CHAR_TAU = chr(0x03C4) # 'τ'



### FUNCTIONS ###

def parse_dice_expression(expression: str) -> str:
	pattern = re.compile(r'(\d*d\d+|\d+|[+\-*/])')
	tokens = pattern.findall(expression)
	for i, token in enumerate(tokens):
		if 'd' in token:
			result, _ = roll_dice(token)
			tokens[i] = str(result)
	return str(''.join(tokens))

def roll_dice(dice_string: str, return_total: bool = True, return_rolls: bool = False):
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
		logging_print(f"Rolling {dice_string}\n Total: {total}\n Rolls: {rolls}")
		if return_total and return_rolls:
			return total, rolls
		elif return_total:
			return total
		elif return_rolls:
			return rolls
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

def sym_quad_zero(a: str, b: str, c: str, positive: str = '+'):
	if positive in ['True', 'p', '+', 'positive']:
		return f"(-({b}) + sqrt(({b})**2 - 4 * {a} * {c})) / (2 * {a})"
	elif positive in ['False', 'n', '-', 'negative']:
		return f"(-({b}) - sqrt(({b})**2 - 4 * {a} * {c})) / (2 * {a})"
	else:
		raise ValueError("Invalid positive argument. Use 'p' for positive, 'n' for negative.")



### TESTING ###

def _test():
	#dice_input = '3d6'
	#total, rolls = roll_dice(dice_input)

	dice_string = '3*d*6'
	expression = sympify(dice_string)
	print(expression)

	print(CHAR_EUL)
	print(CHAR_IMAG)
	print(CHAR_INF)
	print(CHAR_INFJ)
	print(CHAR_NAN)
	print(CHAR_PHI)
	print(CHAR_PI)

if __name__ == '__main__':
	_test()


