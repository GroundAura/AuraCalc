### IMPORTS ###

# builtins
import cmath
from collections.abc import Callable, Container, Sequence
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
#import fractions
import math
#import numbers
#import random
import re
#import statistics
from string import ascii_letters as ASCII_LETTERS, whitespace as WHITESPACE
from typing import Any

# external
from sympy import simplify, sympify, nsimplify, S, SympifyError
import sympy as sp

# internal
from app_logging import logging_print
from app_math import roll_dice, sym_quad_zero, CHAR_EUL, CHAR_IMAG, CHAR_INF, CHAR_INFJ, CHAR_NAN, CHAR_PHI, CHAR_PI
from app_type import function_exists, matches_key



### CONSTANTS ###

#FUNCTIONS_BUILTIN: dict[str | Container[str], Callable] = {
#	#'int': int,                 # int(x)
#	#'float': float              # float(x)
#}
FUNCTIONS_CUSTOM: dict[str | Container[str], Callable] = {
	('roll', 'roll_dice'): roll_dice,
	('quad', 'quad_zero', 'quadratic', 'quadratic_formula'): sym_quad_zero
}
#FUNCTIONS_CMATH: dict[str | Container[str], Callable] = {
#	# Conversions to and from polar coordinates
#	'phase': cmath.phase,        # cmath.phase(x)
#	'polar': cmath.polar,        # cmath.polar(x)
#	'rect': cmath.rect,          # cmath.rect(r, phi)
#	# Power and logarithmic functions
#	'exp': cmath.exp,            # cmath.exp(x)
#	'log': cmath.log,            # cmath.log(x[, base])
#	'log10': cmath.log10,        # cmath.log10(x)
#	#'sqrt': cmath.sqrt,          # cmath.sqrt(x)
#	# Trigonometric functions
#	'acos': cmath.acos,          # cmath.acos(x)
#	'asin': cmath.asin,          # cmath.asin(x)
#	'atan': cmath.atan,          # cmath.atan(x)
#	'cos': cmath.cos,            # cmath.cos(x)
#	'sin': cmath.sin,            # cmath.sin(x)
#	'tan': cmath.tan,            # cmath.tan(x)
#	# Hyperbolic functions
#	'acosh': cmath.acosh,        # cmath.acosh(x)
#	'asinh': cmath.asinh,        # cmath.asinh(x)
#	'atanh': cmath.atanh,        # cmath.atanh(x)
#	'cosh': cmath.cosh,          # cmath.cosh(x)
#	'sinh': cmath.sinh,          # cmath.sinh(x)
#	'tanh': cmath.tanh,          # cmath.tanh(x)
#	# Classification functions
#	'isfinite': cmath.isfinite,  # cmath.isfinite(x)
#	'isinf': cmath.isinf,        # cmath.isinf(x)
#	'isnan': cmath.isnan,        # cmath.isnan(x)
#	'isclose': cmath.isclose     # cmath.isclose(a, b, *, rel_tol=1e-09, abs_tol=0.0)
#}
#FUNCTIONS_MATH: dict[str | Container[str], Callable] = {
#	# Number-theoretic functions
#	'comb': math.comb,           # math.comb(n, k)
#	'factorial': math.factorial, # math.factorial(n)
#	'gcd': math.gcd,             # math.gcd(*integers)
#	'isqrt': math.isqrt,         # math.isqrt(n)
#	'lcm': math.lcm,             # math.lcm(*integers)
#	'perm': math.perm,           # math.perm(n, k)
#	# Floating point arithmetic
#	'ceil': math.ceil,           # math.ceil(x)
#	'fabs': math.fabs,           # math.fabs(x)
#	'floor': math.floor,         # math.floor(x)
#	#'fma': math.fma,             # math.fma(x, y, z)
#	'fmod': math.fmod,           # math.fmod(x, y)
#	'modf': math.modf,           # math.modf(x)
#	'remainder': math.remainder, # math.remainder(x, y)
#	'trunc': math.trunc,         # math.trunc(x)
#	# Floating point manipulation functions
#	'copysign': math.copysign,   # math.copysign(x, y)
#	'frexp': math.frexp,         # math.frexp(x)
#	'isclose': math.isclose,     # math.isclose(a, b, rel_tol, abs_tol)
#	'isfinite': math.isfinite,   # math.isfinite(x)
#	'isinf': math.isinf,         # math.isinf(x)
#	'isnan': math.isnan,         # math.isnan(x)
#	'ldexp': math.ldexp,         # math.ldexp(x, i)
#	'nextafter': math.nextafter, # math.nextafter(x, y, steps)
#	'ulp': math.ulp,             # math.ulp(x)
#	# Power, exponential and logarithmic functions
#	'cbrt': math.cbrt,           # math.cbrt(x)
#	'exp': math.exp,             # math.exp(x)
#	'exp2': math.exp2,           # math.exp2(x)
#	'expm1': math.expm1,         # math.expm1(x)
#	'log': math.log,             # math.log(x, base)
#	'log1p': math.log1p,         # math.log1p(x)
#	'log2': math.log2,           # math.log2(x)
#	'log10': math.log10,         # math.log10(x)
#	'pow': math.pow,             # math.pow(x, y)
#	#'sqrt': math.sqrt,           # math.sqrt(x)
#	# Summation and product functions
#	'dist': math.dist,           # math.dist(p, q)
#	'fsum': math.fsum,           # math.fsum(iterable)
#	'hypot': math.hypot,         # math.hypot(*coordinates)
#	'prod': math.prod,           # math.prod(iterable, start)
#	'sumprod': math.sumprod,     # math.sumprod(p, q)
#	# Angular conversion
#	'degrees': math.degrees,     # math.degrees(x)
#	'radians': math.radians,     # math.radians(x)
#	# Trigonometric functions
#	'acos': math.acos,           # math.acos(x)
#	'asin': math.asin,           # math.asin(x)
#	'atan': math.atan,           # math.atan(x)
#	'atan2': math.atan2,         # math.atan2(y, x)
#	'cos': math.cos,             # math.cos(x)
#	'sin': math.sin,             # math.sin(x)
#	'tan': math.tan,             # math.tan(x)
#	# Hyperbolic functions
#	'acosh': math.acosh,         # math.acosh(x)
#	'asinh': math.asinh,         # math.asinh(x)
#	'atanh': math.atanh,         # math.atanh(x)
#	'cosh': math.cosh,           # math.cosh(x)
#	'sinh': math.sinh,           # math.sinh(x)
#	'tanh': math.tanh,           # math.tanh(x)
#	# Special functions
#	'erf': math.erf,             # math.erf(x)
#	'erfc': math.erfc,           # math.erfc(x)
#	'gamma': math.gamma,         # math.gamma(x)
#	'lgamma': math.lgamma        # math.lgamma(x)
#}
#FUNCTIONS_STATISTICS: dict[str | Container[str], Callable] = {
	
#}
FUNCTIONS_SYMPY: dict[str | Container[str], Callable] = {
	('abs', 'Abs'): sp.Abs,
	# Numeric functions
	('int', 'Int', 'Integer'): sp.Integer,
	('float', 'Float'): sp.Float,
	('rational', 'Rational', 'frac', 'fraction', 'Fraction'): sp.Rational,
	# Trigonometric functions
	('acos', 'ArcCos', 'arccos'): sp.acos,
	('acosh', 'ArcCosh', 'arccosh'): sp.acosh,
	('acot', 'ArcCot', 'arccot'): sp.acot,
	('acoth', 'ArcCoth', 'arccoth'): sp.acoth,
	('acsc', 'ArcCsc', 'arccsc'): sp.acsc,
	('acsch', 'ArcCsch', 'arccsch'): sp.acsch,
	('asec', 'ArcSec', 'arcsec'): sp.asec,
	('asech', 'ArcSech', 'arcsech'): sp.asech,
	('asin', 'ArcSin', 'arcsin'): sp.asin,
	('asinh', 'ArcSinh', 'arcsinh'): sp.asinh,
	('atan', 'ArcTan', 'arctan'): sp.atan,
	('atanh', 'ArcTanh', 'arctanh'): sp.atanh,
	('atan2', 'ArcTan2', 'arctan2'): sp.atan2,
	('cos', 'Cos', 'cosine'): sp.cos,
	('cosh', 'Cosh', 'cosh'): sp.cosh,
	('cot', 'Cot', 'cotangent'): sp.cot,
	('coth', 'Coth', 'coth'): sp.coth,
	('csc', 'Csc', 'cosecant'): sp.csc,
	('csch', 'Csch', 'cosech'): sp.csch,
	('sec', 'Sec', 'secant'): sp.sec,
	('sech', 'Sech', 'sech'): sp.sech,
	('sin', 'Sin', 'sine'): sp.sin,
	('sinh', 'Sinh', 'sinh'): sp.sinh,
	('sinc', 'Sinc'): sp.sinc,
	('tan', 'Tan', 'tangent'): sp.tan,
	('tanh', 'Tanh', 'tanh'): sp.tanh,
	# Integer functions
	('ceil', 'Ceiling'): sp.ceiling,
	('floor', 'Floor'): sp.floor,
	# Exponential functions
	('exp', 'Exp'): sp.exp,
	('log', 'ln'): sp.log,
	# Piecewise functions
	('piecewise', 'Piecewise'): sp.Piecewise,
	# Miscellaneous functions
	('min', 'Min'): sp.Min,
	('max', 'Max'): sp.Max,
	('root', 'Root'): sp.root,
	('sqrt', 'Sqrt'): sp.sqrt,
	('cbrt', 'Cbrt'): sp.cbrt,
	('real_root', 'RealRoot'): sp.real_root,
	# Combinatorial functions
	('factorial', 'Factorial'): sp.factorial,
	('factorial2', 'Factorial2'): sp.factorial2,
	('subfactorial', 'Subfactorial'): sp.subfactorial,
	('rising_factorial', 'RisingFactorial'): sp.RisingFactorial,
	('falling_factorial', 'FallingFactorial'): sp.FallingFactorial,
	('fibbonacci', 'Fibonacci'): sp.fibonacci
}

FUNCTION_MAP: dict[str, tuple[str, Callable]] = dict()
#for dictionary in (FUNCTIONS_BUILTIN, FUNCTIONS_CMATH, FUNCTIONS_CUSTOM, FUNCTIONS_MATH, FUNCTIONS_STATISTICS, FUNCTIONS_SYMPY):
for dictionary, name in ((FUNCTIONS_CUSTOM, 'CUSTOM'), (FUNCTIONS_SYMPY, 'SYMPY')):
	for keys in dictionary.keys():
		if isinstance(keys, str):
			key = keys
			FUNCTION_MAP[key] = (name, dictionary[keys])
		elif issubclass(type(keys), Container):
			for key in keys:
				FUNCTION_MAP[key] = (name, dictionary[keys])
logging_print(f"FUNCTION_MAP: {FUNCTION_MAP}")

FUNCTIONS_PATTERN: str = r'|'.join(FUNCTION_MAP.keys())


#CONSTANTS_CMATH: dict[str | Container[str], Any] = {
#	#'pi': cmath.pi,
#	#'e': cmath.e,
#	#'tau': cmath.tau,
#	#'inf': cmath.inf,
#	#'infj': cmath.infj,
#	#'nan': cmath.nan,
#	#'nanj': cmath.nanj
#}
CONSTANTS_CUSTOM: dict[str | Container[str], Any] = {
	
}
#CONSTANTS_MATH: dict[str | Container[str], Any] = {
#	#'pi': math.pi,
#	#'e': math.e,
#	#'tau': math.tau,
#	#'inf': math.inf,
#	#'nan': math.nan
#}
CONSTANTS_SYMPY: dict[str | Container[str], Any] = {
	('pi', 'Pi', r'\pi', chr(0x03C0)): sp.pi,                                     # pi (~3.14159)
	('e', 'E', r'\e', r'\E'): sp.E,                                               # e (~2.71828)
	('oo', 'infinity', 'infty', 'inf', r'\infty', chr(0x221E)): sp.oo,            # infinity
	('nan', 'NaN', 'NAN', r'\NaN'): sp.nan,                                      # not a number (0/0)
	('i', 'I', 'j', 'J', r'\i', r'\I', r'\j', r'\J'): sp.I,                      # imaginary unit (sqrt(-1))
	#('infj', 'complexinfinity', 'ComplexInfinity', r'\infj'): sp.ComplexInfinity, # complex infinity
	('tau', 'Tau', r'\tau', chr(0x03C4)): sp.pi*2,                               # 2pi (~6.28319)
	('phi', 'goldenratio', 'GoldenRatio', r'\phi', chr(0x03C6)): sp.GoldenRatio, # golden ratio
}

CONSTANTS_MAP: dict[str, tuple[str, Callable]] = dict()
for dictionary, name in ((CONSTANTS_CUSTOM, 'CUSTOM'), (CONSTANTS_SYMPY, 'SYMPY')):
	for keys in dictionary.keys():
		if isinstance(keys, str):
			key = keys
			CONSTANTS_MAP[key] = (name, dictionary[keys])
		elif issubclass(type(keys), Container):
			for key in keys:
				CONSTANTS_MAP[key] = (name, dictionary[keys])
logging_print(f"CONSTANTS_MAP: {CONSTANTS_MAP}")

CONSTANTS_PATTERN: str = r'|'.join(CONSTANTS_MAP.keys())


ALLOWED_CHARS: re.Pattern[str] = re.compile(
	r'^(?:' +
	r'\d+|' + # Digits
	#r'(?:0x[0-9a-f]+|0b[01]+|0o[0-7]+)|' + # Hex, Binary, Octal Numbers
	'|'.join(re.escape(k) for k in FUNCTION_MAP.keys()) + '|' + # Functions
	'|'.join(re.escape(k) for k in CONSTANTS_MAP.keys()) + '|' + # Constants
	r'[a-zA-Z]' + # Variables
	r'|[\+\-\*\/\^]+' + # Operators
	r'|[ (),.%]+' + # Misc Characters
	r'|[$_{}\\]' + # LaTeX
	r')+$'
)
logging_print(f"ALLOWED_CHARS: {ALLOWED_CHARS}")



### FUNCTIONS ###
def compact_expr(expr: str) -> str:
	"""
	Removes any unnecessary characters from an expression, just as whitespace or leading zeros.

	Args:
		expr (str): The expression to process.

	Returns:
		str: The processed expression.
	"""
	# Remove whitespace
	for char in WHITESPACE:
		expr = expr.replace(char, '')
#	# Remove leading zeros
## ***TO DO***: ensure there's no decimal points before the zero before removing leading zeros
#	expr = re.sub(r'\b0+(\d+)', r'\1', expr)
	return expr

def eval_custom_functions(expr: str) -> str:
	"""
	Evaluates custom functions in an expression.

	Args:
		expr (str): The expression to evaluate.

	Returns:
		str: The processed expression.
	"""
	# Evaluate custom functions
	func_pattern: re.Pattern = re.compile(r'(\b\w+)\(([^)]*)\)')
	def func_replacer(match: re.Match) -> str:
		"""
		Replaces a function call with its result.

		Args:
			match (Match): The match object.

		Returns:
			str: The result of the function call or the original expression.
		"""
		func_name: str = match.group(1).lstrip('(')
		arg_str: str = match.group(2)
		args_list: list = [arg.strip() for arg in arg_str.split(',')]
		logging_print(f"Function requested: '{func_name}', Arguments: {args_list}")
		if matches_key(func_name, FUNCTION_MAP.keys()):
			group: str = FUNCTION_MAP[func_name][0]
			func: Callable = FUNCTION_MAP[func_name][1]
			if group == 'SYMPY':
				if func_name in ('log', '\\log') and len(args_list) == 1 and args_list[0]:
					args_list.append('10')
				logging_print(f"Matching SymPy function: `sympy.{func.__name__}`. Letting SymPy handle evaluation.")
				#result = match.group(0).replace(func_name, str(func.__name__))
				result = f"{func.__name__}({','.join(args_list)})"
				return result
			else:
				#logging_print(f"Matching function: '{func_name}': {func.__module__}.{func.__name__}")
				args: list = []
				for arg in args_list:
					if group == 'CUSTOM' and func is roll_dice and args_list.index(arg) == 0:
						args.append(arg)
					#elif group == 'CUSTOM' and func is quad_zero and args_list.index(arg) == 4:
					#	args.append(arg)
					elif group == 'CUSTOM' and func is sym_quad_zero:
						args.append(arg)
					else:
						args.append(float(arg))
				#logging_print(f"Calling function: `{func.__module__}.{func.__name__}({', '.join(map(str, args))})`")
				result = func(*args)
				logging_print(f"Calling function: `{func.__module__}.{func.__name__}({', '.join(map(str, args))})`, Result: `{result}`")
				if result is True:
					return '1'
				elif result is False:
					return '0'
				else:
					return str(result)
		elif function_exists(func_name):
			logging_print(f"Function '{func_name}' not valid. Transforming to variable multiplication to ensure it's not treated as a function.")
			if len(args_list) == 1 and args_list[0] == '':
				return '*'.join(func_name)
			else:
				return match.group(0).replace(func_name, '*'.join(func_name))
		else:
			logging_print(f"Function '{func_name}' not found. Assuming it's not a function.")
			if len(args_list) == 1 and args_list[0] == '':
				return func_name
			else:
				return match.group(0)
	# Evaluate custom constants
	const_pattern: re.Pattern = re.compile('|'.join(re.escape(k) for k in CONSTANTS_MAP.keys()))
	def const_replacer(match: re.Match) -> str:
		"""
		Replaces a constant with its value.

		Args:
			match (Match): The match object.

		Returns:
			str: The value of the constant.
		"""
		const_name: str = match.group(0)
		logging_print(f"Constant requested: '{const_name}'")
		if matches_key(const_name, CONSTANTS_MAP.keys()):
			group: str = CONSTANTS_MAP[const_name][0]
			const: Callable = CONSTANTS_MAP[const_name][1]
			if group == 'SYMPY':
				logging_print(f"Matching SymPy constant: `sympy.{const}`. Letting SymPy handle evaluation.")
				return '(' + str(const) + ')'
			else:
				logging_print(f"Matching constant: '{const_name}': `{CONSTANTS_MAP[const_name]}`")
				return str(CONSTANTS_MAP[const_name])
		elif function_exists(const_name):
			logging_print(f"Constant '{const_name}' not valid. Transforming to variable multiplication to ensure it's not treated as a function.")
			return '(' + match.group(0).replace(const_name, '*'.join(const_name)) + ')'
		else:
			logging_print(f"Constant '{const_name}' not found. Assuming it's not a constant.")
			return match.group(0)
	# Process the expression
	processed_expression: str = func_pattern.sub(func_replacer, expr)
	processed_expression: str = const_pattern.sub(const_replacer, processed_expression)
	return processed_expression

#def eval_with_decimal(expression: any) -> str:
#	"""
#	Recursively evaluate sympy expressions using Decimal for high precision.

#	Args:
#		expression (any): The expression to evaluate.

#	Returns:
#		str: The result of the expression.
#	"""
#	if expression.is_Number:
#		# Convert sympy numbers to Decimal
#		return Decimal(str(expression))
	
#	elif expression.is_Add or expression.is_Mul or expression.is_Pow:
#		# If it's an addition, multiplication, or power, evaluate the arguments
#		args = [eval_with_decimal(arg) for arg in expression.args]
#		operator = str(expression.func)
#		return OPERATIONS[operator](*args)

#	# Handle division separately
#	elif expression.is_Div:
#		args = [eval_with_decimal(arg) for arg in expression.args]
#		return args[0] / args[1]

#	# If the expression doesn't fit the above, simplify it directly
#	else:
#		return Decimal(str(expression))

def evaluate_expression(app, expr: str, approximate: bool = True) -> str:
	"""
	Evaluates an expression.

	Args:
		expr (str): The expression to evaluate.
		approximate (bool, optional): Whether to approximate the result to a decimal. Defaults to `True`.

	Returns:
		str: The result of the expression.
	"""
	#logging_print('Evaluating expression...')
	#approximate = False
	#rational = False if approximate else True
	try:
		## Detect LaTeX input
		#if expr.startswith('$') and expr.endswith('$'):
		#	expr = expr.strip('$')
		#	expr = sp.latex(expr)
		# Handle custom functions & constants
		expr_cust: str = eval_custom_functions(expr)
		logging_print(f"Expr (eval_func):{' '*4}`{expr_cust}` - type: {type(expr_cust)}")
		# Remove unnecessary characters
		expr_comp = compact_expr(expr_cust)
		logging_print(f"Expr (compacted):{' '*4}`{expr_comp}` - type: {type(expr_comp)}")
		# Handle implied exponentation
		expr_exp = implied_exp(expr_comp)
		logging_print(f"Expr (implied_exp):{' '*2}`{expr_exp}` - type: {type(expr_exp)}")
		# Handle implied multiplication
		expr_mult = implied_mult(expr_exp)
		logging_print(f"Expr (implied_mult):{' '*1}`{expr_mult}` - type: {type(expr_mult)}")
		# Convert to sympy object
		expr_sym = sympify(expr_mult)
		logging_print(f"Expr (sympify):{' '*6}`{expr_sym}` - type: {type(expr_sym)}")
		#if expr_sym.has(S.NaN):
		#	raise ZeroDivisionError('Division by Zero (NaN)')
		#elif expr_sym.has(S.ComplexInfinity):
		#	raise ZeroDivisionError('Division by Zero (ComplexInfinity)')
		# Simplify expression
		expr_simp = simplify(expr_sym)
		logging_print(f"Expr (simplify):{' '*5}`{expr_simp}` - type: {type(expr_simp)}")
		if approximate:
			# Convert floats to rationals
			expr_rat = nsimplify(expr_simp, rational=True)
			logging_print(f"Expr (rational):{' '*5}`{expr_rat}` - type: {type(expr_rat)}")
			# Approximate expression
			expr_appr = expr_rat.evalf(app.calc_dec_precicion)
			logging_print(f"Expr (float):{' '*8}`{expr_appr}` - type: {type(expr_appr)}")
			# Round all numbers
			expr_round = expr_appr.xreplace({n: S(round(n, app.calc_dec_display)) for n in expr_appr.atoms(sp.Number)})
			logging_print(f"Expr (round):{' '*8}`{expr_round}` - type: {type(expr_round)}")
			expr_res = expr_round
		else:
			expr_res = expr_simp
		expr_dec = simplify_floats(expr_res)
		logging_print(f"Expr (simplify_floats):{' '*4}`{expr_dec}` - type: {type(expr_dec)}")
		expr_final: str = format_expression(expr_dec)
		logging_print(f"Expr (formatted):{' '*4}`{expr_final}` - type: {type(expr_final)}")
		# Return result
		app.calc_last_result = expr_final
		return expr_final
	except InvalidOperation:
		raise InvalidOperation('Invalid number format')
	except SympifyError as e:
		if 'SyntaxError' in str(e):
			raise SyntaxError('Invalid expression')
		elif 'TokenError' in str(e):
			if expr.count('(') != expr.count(')'):
				raise SyntaxError("Mismatched parentheses '( )'")
			elif expr.count('{') != expr.count('}'):
				raise SyntaxError("Mismatched braces '{ }'")
			elif expr.count('[') != expr.count(']'):
				raise SyntaxError("Mismatched brackets '[ ]'")
			else:
				raise e
		else:
			raise e

def format_expression(expr: Any) -> str:
	"""
	Formats an expression by making it more readable.

	Args:
		expr (Any): The expression to format.

	Returns:
		str: The formatted expression.
	"""
	# convert to string
	expr: str = str(expr)

	# replace exponent symbol
	expr = expr.replace('**', '^') # Replace '**' with '^', e.g., 2**3 -> 2^3

	# replace multiplication symbol
	while re.search(r'(?<=\d)\*([a-zA-Z])', expr):
		expr = re.sub(r'(?<=\d)\*([a-zA-Z])', r'\1', expr)      # Remove '*' between a number and a variable, e.g., 2*x -> 2x
	while re.search(r'([a-zA-Z])\*\(', expr):
		expr = re.sub(r'([a-zA-Z])\*\(', r'\1\(', expr)         # Remove '*' between a variable and opening parenthesis, e.g., x*(3) -> x(3)
	while re.search(r'\)\*([a-zA-Z])', expr):
		expr = re.sub(r'\)\*([a-zA-Z])', r')\1', expr)          # Remove '*' between a closing parenthesis and a variable, e.g., (3)*x -> (3)x
	while re.search(r'([a-zA-Z])\*([a-zA-Z])', expr):
		expr = re.sub(r'([a-zA-Z])\*([a-zA-Z])', r'\1\2', expr) # Remove '*' between 2 variables, e.g., x*y -> xy

	# replace constant symbols
	expr = expr.replace('E', CHAR_EUL)                # Euler's Number
	expr = expr.replace('exp(', CHAR_EUL + '^(')      # Euler's Number
	expr = expr.replace('GoldenRatio', CHAR_PHI)      # Golden Ratio
	expr = expr.replace('I', CHAR_IMAG)               # Imaginary Unit
	expr = expr.replace('oo', CHAR_INF)               # Infinity
	expr = expr.replace('ComplexInfinity', CHAR_INFJ) # Complex Infinity
	expr = expr.replace('nan', CHAR_NAN)              # Not a Number
	expr = expr.replace('pi', CHAR_PI)                # Pi

	return expr

def implied_exp(expression: str) -> str:
	"""
	Evaluates whether an expression contains implied exponentation and adds explicit exponentation if necessary.

	Args:
		expression (str): The expression to evaluate.

	Returns:
		str: The processed expression.
	"""
	return expression.replace('^', '**')

def implied_mult(expression: str, functions: re.Pattern[str] = FUNCTIONS_PATTERN) -> str:
	"""
	Evaluates whether an expression contains implied multiplication and adds explicit multiplication if necessary.

	Args:
		expression (str): The expression to evaluate.
		functions (Pattern[str], optional): The list of known functions. Defaults to `FUNCTIONS_PATTERN`.

	Returns:
		str: The processed expression.
	"""
	pattern = (
		r'(?<=\d)(?=\()'                              # Case 1: number followed by an opening parenthesis, e.g., 1(2)
		r'|(?<=\))(?=\d)'                             # Case 2: closing parenthesis followed by a number, e.g., (3)4
		r'|(?<=\))(?=\()'                             # Case 3: two sets of parentheses, e.g., (3)(4)
		r'|(?<=\d)(?=(' + functions + r')\()'         # Case 4: number followed by a function, e.g., 2sqrt(9)
		r'|(?<=\))(?=(' + functions + r')\()'         # Case 5: closing parenthesis followed by a function, e.g., (2)sqrt(9)
		r'|(?<=\d)(?=[a-zA-Z])'                       # Case 6: number followed by a variable, e.g., 2x -> 2*x
		r'|(?<=\))(?=[a-zA-Z])'                       # Case 7: closing parenthesis followed by a variable, e.g., (2)x -> (2)*x
		r'|(?<=[a-zA-Z])(?=\d)'                       # Case 8: variable followed by a number, e.g., x2 -> x*2
		r'|(?<=[a-zA-Z])(?=\()'                       # Case 9: variable followed by an opening parenthesis, e.g., x(3) -> x*(3)
		#r'|(?<=[a-zA-Z])(?=[a-zA-Z])'                 # Case 10: variable followed by another variable, e.g., xy -> x*y
	)
	#logging_print(pattern)
	# add '*' to cases
	modified_expression = re.sub(pattern, '*', expression)                                         # Add '*' in all matched cases
	# exceptions
	#modified_expression = re.sub(r'(' + functions + r')\*+', lambda m: m.group(0).replace('*', ''), modified_expression) # Remove '*' inside of function names
	modified_expression = re.sub(r'(' + functions + r')\*\(', r'\1(', modified_expression)         # Remove '*' between functions and '('
	modified_expression = re.sub(r'(?<=roll\()(\d+)\*d\*(\d+)', r'\1d\2', modified_expression)     # Remove '*' between numbers and 'd' in the roll_dice() function
	return modified_expression

def sanitize_input(expression: str, allowed_chars: str = ALLOWED_CHARS, sanitize: bool = True) -> str:
	"""
	Sanitize an expression by removing invalid sequences of characters if possible, or raising an exception if not.

	Args:
		expression (str): The expression to sanitize.
		allowed_chars (str, optional): The allowed characters. Defaults to `ALLOWED_CHARS`.
		sanitize (bool, optional): Whether to sanitize the expression. Defaults to `True`.

	Returns:
		str: The sanitized expression.
	"""
	#logging_print(repr(WHITESPACE + '='))
	stripped_expr = expression.strip(WHITESPACE + '=')
	logging_print(f"Expr (stripped):{' '*5}`{stripped_expr}`")
	if sanitize and stripped_expr and not allowed_chars.match(stripped_expr):
		raise ValueError('Invalid characters in expression')
	logging_print(f"Expr (sanitized):{' '*4}`{stripped_expr}`")
	return stripped_expr

#def simplify_decimal(number: Any, decimal_places: int = 10) -> str:
#	"""
#	Simplifies a number with decimals by rounding to the specified decimal places and truncating trailing empty decimal places.

#	Args:
#		value (Any): The number to simplify.
#		decimal_places (int, optional): The number of decimal places to round to. Defaults to `10`.

#	Returns:
#		str: The simplified number.
#	"""
#	if not isinstance(number, Decimal):
#		number = Decimal(str(number))
#	#logging_print(value)
#	quatitize_pattern = Decimal(f"1.{'0' * decimal_places}")
#	rounded_number = number.quantize(quatitize_pattern, rounding=ROUND_HALF_UP)
#	if rounded_number.is_zero():
#		return '0'
#	simplified_number = str(rounded_number).rstrip('0').rstrip('.')
#	return simplified_number

def simplify_floats(expr: Any) -> Any:
	"""
	Simplifies floating-point numbers in an expression by truncating trailing zeros and the decimal point.

	Args:
		expr (Any): The expression to simplify.

	Returns:
		str: The simplified expression.
	"""
	def float_to_int(term: Any) -> Any:
		#print(f"term: {term} - type: {type(term)}")
		#print(float(term))
		if term.is_number:
			try:
				# If it's a number, check if it's effectively an integer
				if float(term) == int(term):  # If the float is mathematically an integer
					return int(term)  # Convert it to integer
				else:
					#return term  # Leave as float
					return float(term) # Leave as float but truncate trailing zeros
			except Exception:
				# If it's not a simple number, return the term unchanged
				return term
		return term  # If it's not a number, return the term unchanged
	converted_expr = expr.xreplace({term: float_to_int(term) for term in expr.atoms()})
	#print(f"Expr (ints):{' '*4}`{converted_expr}` - type: {type(converted_expr)}")
	return converted_expr

#def split_terms(expression: str) -> list[str]:
#	terms = expression.split()
#	return terms



### TESTING ###

def _test():
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
	x,y,z = sp.symbols('x y z')
	expr = x**2 + x*y
	print(expr)
	print(sp.simplify(expr))
	expr2 = sp.sqrt(2)
	print(expr2)
	print(sp.simplify(expr2))
	print(expr2.evalf())

if __name__ == '__main__':
	_test()


