### IMPORTS ###

# builtins
#import cmath
import random
#import re

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

def roll_dice(dice_string: str) -> tuple[int, list[int]]:
	"""
	Generates a random number based on the dice string.

	Args:
		dice_string (str): The dice notation (e.g., `'3d6'`).

	Returns:
		int: The random number.
		list[int]: The individual results of each die.
	"""
	try:
		num_dice, num_sides = map(int, dice_string.lower().split('d'))
		rolls: list[int] = [random.randint(1, num_sides) for _ in range(num_dice)]
		total: int = sum(rolls)
		logging_print(f"Rolling '{dice_string}'... Total: `{total}`,  Rolls: `{rolls}`")
		return total, rolls
	except ValueError:
		raise ValueError("Invalid dice notation. Use 'XdY' format, e.g., '3d6'.")

def sym_quad_zero(a: str, b: str, c: str, positive: str = '+') -> str:
	"""
	Returns a symbolic expression (for SymPy) for one of the zeros of a quadratic equation.

	Args:
		a (str): Coefficient of x^2.
		b (str): Coefficient of x.
		c (str): Constant term.
		positive (str, optional): Whether to return the positive or negative root. Defaults to '+' (positive). Valid options: `'True'`, `'+'`, `'p'`, `'pos'`, `'positive'` OR `'False'`, `'-'`, `'n'`, `'neg'`, `'negative'`.

	Returns:
		str: Symbolic expression for the zero of the quadratic equation.
	"""
	if positive in ['True', '+', 'p', 'pos', 'positive']:
		return f"(-({b}) + sqrt(({b})**2 - 4 * {a} * {c})) / (2 * {a})"
	elif positive in ['False', '-', 'n', 'neg', 'negative']:
		return f"(-({b}) - sqrt(({b})**2 - 4 * {a} * {c})) / (2 * {a})"
	else:
		raise ValueError("Invalid positive argument. Use 'p' for positive, 'n' for negative.")

#def _parse_dice_expr(expr: str) -> str:
#	pattern = re.compile(r'(\d*d\d+|\d+|[+\-*/])')
#	tokens = pattern.findall(expr)
#	for i, token in enumerate(tokens):
#		if 'd' in token:
#			result, _ = roll_dice(token)
#			tokens[i] = str(result)
#	return str(''.join(tokens))

#def _quadratic_formula(a: float, b: float, c: float):
#	# Calculate the discriminant
#	#discriminant = sympify(b**2) - sympify(4) * sympify(a) * sympify(c)
#	discriminant = b**2 - 4 * a * c
#	# Calculate the two solutions
#	#root1 = sympify((-sympify(b) + sympify(discriminant)) / (2 * sympify(a)))
#	#root2 = sympify((-sympify(b) - sympify(discriminant)) / (2 * sympify(a)))
#	root1 = (-b + cmath.sqrt(discriminant)) / (2 * a)
#	root2 = (-b - cmath.sqrt(discriminant)) / (2 * a)
#	return root1, root2

#def _quad_zero(a: str | float, b: str | float, c: str | float, positive: str = '+'):
#	a = float(a)
#	b = float(b)
#	c = float(c)
#	root1, root2 = _quadratic_formula(a, b, c)
#	if positive in ['True', 'p', '+', 'positive']:
#		return root1
#	elif positive in ['False', 'n', '-', 'negative']:
#		return root2
#	else:
#		raise ValueError("Invalid positive argument. Use 'p' for positive, 'n' for negative.")



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

	#import math
	#print(math.sqrt(9))
	#print(math.log(9, 3))
	#print(math.fabs(-9))
	#print(math.gcd(9, 3))
	#print(math.factorial(9))
	#print(math.trunc(9.9))
	#print(math.ceil(9.9))
	#print(math.floor(9.9))
	#print(math.pow(9, 3))
	#print(math.acosh(9))
	#print(math.remainder(9, 3))
	#print(math.cbrt(9))
	#print(math.comb(9, 3))
	#print(math.exp2(9))
	#print(math.perm(9, 3))
	#print(math.lcm(9, 3))
	##print(math.isqrt(9))
	#print(math.atanh(9))
	##print(math.)

	#print(sp.sqrt(9))
	#print(int('9'))

	#x,y,z = sp.symbols('x y z')
	#expr = x**2 + x*y
	#print(expr)
	#print(sp.simplify(expr))
	#expr2 = sp.sqrt(2)
	#print(expr2)
	#print(sp.simplify(expr2))
	#print(expr2.evalf())

if __name__ == '__main__':
	_test()


