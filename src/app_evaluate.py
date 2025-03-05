### IMPORTS ###

# builtins
#import cmath
from collections.abc import Callable, Container
#import fractions
#import math
#import numbers
#import random
import re
#import statistics
from string import whitespace as WHITESPACE
from typing import Any

# external
from sympy import simplify, sympify, nsimplify, S, SympifyError
import sympy as sp

# internal
from app_logging import logging_print
from app_math import roll_dice, sym_quad_zero, TAU, CHAR_EUL, CHAR_IMAG, CHAR_INF, CHAR_INFJ, CHAR_NAN, CHAR_PHI, CHAR_PI
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
#FUNCTIONS_RANDOM: dict[str | Container[str], Callable] = {
	
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
for dictionary, name in ((FUNCTIONS_CUSTOM, 'CUSTOM'), (FUNCTIONS_SYMPY, 'SYMPY')):
	for keys in dictionary.keys():
		if isinstance(keys, str):
			key = keys
			FUNCTION_MAP[key] = (name, dictionary[keys])
		elif issubclass(type(keys), Container):
			for key in keys:
				FUNCTION_MAP[key] = (name, dictionary[keys])
logging_print(f"FUNCTION_MAP: {FUNCTION_MAP}")


#CONSTANTS_CMATH: dict[str | Container[str], Any] = {
#	#'infj': cmath.infj,
#	#'nanj': cmath.nanj
#}
CONSTANTS_CUSTOM: dict[str | Container[str], Any] = {
	
}
CONSTANTS_SYMPY: dict[str | Container[str], Any] = {
	('pi', 'Pi', r'\pi', chr(0x03C0)): sp.pi,                          # Pi
	('e', 'E', r'\e', r'\E'): sp.E,                                    # Euler's Number
	('oo', 'infinity', 'infty', 'inf', r'\infty', chr(0x221E)): sp.oo, # Infinity
	('nan', 'NaN', 'NAN', r'\NaN'): sp.nan,                            # Not a Number
	('i', 'I', 'j', 'J', r'\i', r'\I', r'\j', r'\J'): sp.I,            # Imaginary Unit
	('tau', 'Tau', r'\tau', chr(0x03C4)): TAU,                         # Tau
	('phi', 'goldenratio', 'GoldenRatio', r'\phi', chr(0x03C6), chr(0x03A6)): sp.GoldenRatio, # Golden Ratio
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


ALLOWED_CHARS: re.Pattern[str] = re.compile(
	r'^(?:' +
	r'\d+' +              # Digits
	r'|[\+\-\*\/\^\%]+' + # Operators
	r'|[a-zA-Z]' +        # Variables
	r'|[.,()]+' +         # Misc Characters
	r'|[ ]+' +            # Whitespace
	r'|[${}\\]' +         # Temp semi-handle LaTeX
	#r'|[$_{}\\]' +       # LaTeX Symbols
	#r'|(?:0x[0-9a-f]+|0b[01]+|0o[0-7]+)|' + # Hex, Binary, Octal Numbers
	'|'.join(re.escape(k) for k in CONSTANTS_MAP.keys()) + '|' + # Constants
	'|'.join(re.escape(k) for k in FUNCTION_MAP.keys()) +        # Functions
	r')+$'
)
logging_print(f"ALLOWED_CHARS: {ALLOWED_CHARS}")



### FUNCTIONS ###
def compact_expr(expr: str) -> str:
	"""
	Removes any unnecessary characters from an expression, just as whitespace.

	Args:
		expr (str): The expression to process.

	Returns:
		str: The processed expression.
	"""
	# Remove whitespace
	#logging_print(repr(WHITESPACE))
	for char in WHITESPACE:
		expr = expr.replace(char, '')
	# Remove '=' at each end
	expr = expr.strip('=')
	# Temp semi-handle LaTeX
	expr = expr.strip('$').replace('{', '(').replace('}', ')').replace('\\', '')
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
			match (re.Match): The match object.

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
				if func is roll_dice:
					result = result[0]
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
			match (re.Match): The match object.

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
	processed_expr: str = func_pattern.sub(func_replacer, expr)
	processed_expr: str = const_pattern.sub(const_replacer, processed_expr)
	return processed_expr

def evaluate_expression(expr: str, approximate: bool = True, dec_precision: int = 20, dec_display: int = 8) -> str:
	"""
	Evaluates an expression.

	Args:
		expr (str): The expression to evaluate.
		approximate (bool, optional): Whether to approximate the result to a decimal. Defaults to `True`.
		dec_precision (int, optional): The number of decimal places to use when evaluating. Defaults to `20`.
		dec_display (int, optional): The number of decimal places to display. Defaults to `8`.

	Returns:
		str: The result of the expression.
	"""
	#approximate = False
	try:
		## Detect LaTeX input
		#if expr.startswith('$') and expr.endswith('$'):
		#	expr_latex: str = expr.strip('$')
		#	expr_res: sp.Expr = sp.latex(expr_latex)
		# Handle custom functions & constants
		expr_cust: str = eval_custom_functions(expr)
		logging_print(f"Expr (eval_func):{' '*4}`{expr_cust}` - type: {type(expr_cust)}")
		# Handle implied exponentation
		expr_exp: str = implied_exp(expr_cust)
		logging_print(f"Expr (implied_exp):{' '*2}`{expr_exp}` - type: {type(expr_exp)}")
		# Handle implied multiplication
		expr_mult: str = implied_mult(expr_exp)
		logging_print(f"Expr (implied_mult):{' '*1}`{expr_mult}` - type: {type(expr_mult)}")
		# Convert to SymPy object
		expr_sym: sp.Expr = sympify(expr_mult)
		logging_print(f"Expr (sympify):{' '*6}`{expr_sym}` - type: {type(expr_sym)}")
		# Simplify expression
		expr_simp: sp.Expr = simplify(expr_sym)
		logging_print(f"Expr (simplify):{' '*5}`{expr_simp}` - type: {type(expr_simp)}")
		if approximate:
			# Convert floats to rationals
			expr_rat: sp.Expr = nsimplify(expr_simp, rational=True)
			logging_print(f"Expr (rational):{' '*5}`{expr_rat}` - type: {type(expr_rat)}")
			# Approximate expression
			expr_appr: sp.Expr = expr_rat.evalf(dec_precision)
			logging_print(f"Expr (float):{' '*8}`{expr_appr}` - type: {type(expr_appr)}")
			expr_res: sp.Expr = expr_appr
		else:
			expr_res: sp.Expr = expr_simp
		# Round all numbers
		expr_round: sp.Expr = simplify_floats(expr_res, dec_display, approximate)
		logging_print(f"Expr (clean_floats):{' '*1}`{expr_round}` - type: {type(expr_round)}")
		# Format expression
		expr_final: str = format_expression(expr_round)
		logging_print(f"Expr (formatted):{' '*4}`{expr_final}` - type: {type(expr_final)}")
		# Return result
		return expr_final
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


def format_expression(expr: str | sp.Basic | sp.Expr) -> str:
	"""
	Formats an expression by making it more readable.

	Args:
		expr (str | sympy.Basic | sympy.Expr): The expression to format.

	Returns:
		str: The formatted expression.
	"""
	# convert to string
	expr_str: str = str(expr)

	# replace exponent symbol
	expr_str = expr_str.replace('**', '^') # Replace '**' with '^', e.g., 2**3 -> 2^3

	# replace multiplication symbol
	while re.search(r'(?<=\d)\*([a-zA-Z])', expr_str):
		expr_str = re.sub(r'(?<=\d)\*([a-zA-Z])', r'\1', expr_str)      # Remove '*' between a number and a variable, e.g., 2*x -> 2x
	while re.search(r'([a-zA-Z])\*\(', expr_str):
		expr_str = re.sub(r'([a-zA-Z])\*\(', r'\1\(', expr_str)         # Remove '*' between a variable and opening parenthesis, e.g., x*(3) -> x(3)
	while re.search(r'\)\*([a-zA-Z])', expr_str):
		expr_str = re.sub(r'\)\*([a-zA-Z])', r')\1', expr_str)          # Remove '*' between a closing parenthesis and a variable, e.g., (3)*x -> (3)x
	while re.search(r'([a-zA-Z])\*([a-zA-Z])', expr_str):
		expr_str = re.sub(r'([a-zA-Z])\*([a-zA-Z])', r'\1\2', expr_str) # Remove '*' between 2 variables, e.g., x*y -> xy

	# replace constant symbols
	expr_str = expr_str.replace('E', CHAR_EUL)                # Euler's Number
	expr_str = expr_str.replace('GoldenRatio', CHAR_PHI)      # Golden Ratio
	expr_str = expr_str.replace('I', CHAR_IMAG)               # Imaginary Unit
	expr_str = expr_str.replace('oo', CHAR_INF)               # Infinity
	expr_str = expr_str.replace('ComplexInfinity', CHAR_INFJ) # Complex Infinity
	expr_str = expr_str.replace('nan', CHAR_NAN)              # Not a Number
	expr_str = expr_str.replace('pi', CHAR_PI)                # Pi

	# replace additional symbols
	expr_str = expr_str.replace('exp(', CHAR_EUL + '^(')      # Euler's Number
	expr_str = expr_str.replace('log(', 'ln(')                # Natural Logarithm)

	return expr_str

def implied_exp(expression: str) -> str:
	"""
	Evaluates whether an expression contains implied exponentation and adds explicit exponentation if necessary.

	Args:
		expression (str): The expression to evaluate.

	Returns:
		str: The processed expression.
	"""
	return expression.replace('^', '**')

def implied_mult(expr: str) -> str:
	"""
	Evaluates whether an expression contains implied multiplication and adds explicit multiplication if necessary.

	Args:
		expression (str): The expression to evaluate.

	Returns:
		str: The processed expression.
	"""
	# Define patterns
	#constants: str = '|'.join(re.escape(k) for k in CONSTANTS_MAP.keys())
	functions: str = '|'.join(re.escape(k) for k in FUNCTION_MAP.keys())
	pattern: str = (
		r'(?<=\d)(?=\()'                              # Case 1: number followed by an opening parenthesis, e.g., 1(2)
		r'|(?<=\))(?=\d)'                             # Case 2: closing parenthesis followed by a number, e.g., (3)4
		r'|(?<=\))(?=\()'                             # Case 3: two sets of parentheses, e.g., (3)(4)
		r'|(?<=\d)(?=(' + functions + r')\()'         # Case 4: number followed by a function, e.g., 2sqrt(9)
		r'|(?<=\))(?=(' + functions + r')\()'         # Case 5: closing parenthesis followed by a function, e.g., (2)sqrt(9)
		r'|(?<=\d)(?=[a-zA-Z])'                       # Case 6: number followed by a variable, e.g., 2x -> 2*x
		r'|(?<=\))(?=[a-zA-Z])'                       # Case 7: closing parenthesis followed by a variable, e.g., (2)x -> (2)*x
		r'|(?<=[a-zA-Z])(?=\d)'                       # Case 8: variable followed by a number, e.g., x2 -> x*2
		r'|(?<=[a-zA-Z])(?=\()'                       # Case 9: variable followed by an opening parenthesis, e.g., x(3) -> x*(3)
		r'|(?<=[a-zA-Z])(?=[a-zA-Z])'                 # Case 10: variable followed by another variable, e.g., xy -> x*y
	)
	#print(pattern)

	# Add '*' in all matched cases
	expr_modified: str = re.sub(pattern, '*', expr)
	#logging_print(expr_modified)

	# Remove '*' inside of function and constant names
	sym_except_list: list = []
	for key in list(CONSTANTS_MAP.keys()) + list(FUNCTION_MAP.keys()):
		if len(key) > 1 and all(c.isalpha() for c in key):
			sym_except_list.append('*'.join(list(key)))
	#print(exceptions_lst)
	symb_except: str = '|'.join(re.escape(k) for k in sym_except_list)
	#print(exceptions)
	expr_modified = re.sub(r'(' + symb_except + r')', lambda m: m.group(0).replace('*', ''), expr_modified)

	# Remove '*' between functions and '('
	expr_modified = re.sub(r'(' + functions + r')\*\(', r'\1(', expr_modified)

	# Remove '*' between numbers and 'd' in the roll_dice() function
	expr_modified = re.sub(r'(?<=roll\()(\d+)\*d\*(\d+)', r'\1d\2', expr_modified)

	return expr_modified

def sanitize_input(expr: str, allowed_chars: str = ALLOWED_CHARS, sanitize: bool = True) -> str:
	"""
	Sanitize an expression by removing invalid sequences of characters if possible, or raising an exception if not.

	Args:
		expression (str): The expression to sanitize.
		allowed_chars (str, optional): The allowed characters. Defaults to `ALLOWED_CHARS`.
		sanitize (bool, optional): Whether to sanitize the expression. Defaults to `True`.

	Returns:
		str: The sanitized expression.
	"""
	# Remove unnecessary characters
	expr_comp: str = compact_expr(expr)
	logging_print(f"Expr (compacted):{' '*4}`{expr_comp}` - type: {type(expr_comp)}")
	if sanitize and expr_comp and not allowed_chars.match(expr_comp):
		raise ValueError('Invalid characters in expression')
	logging_print(f"Expr (sanitized):{' '*4}`{expr_comp}` - type: {type(expr_comp)}")
	return expr_comp

def simplify_floats(expr: sp.Expr, ndec: int, approx: bool) -> sp.Expr:
	"""
	Simplifies floating-point numbers in an expression by rounding, then truncating any trailing zeros and the decimal point if applicable.

	Args:
		expr (sympy.Expr): The expression to simplify.
		ndec (int): The number of decimal places to round to.
		approx (bool): Whether to approximate the result to a decimal.

	Returns:
		sympy.Expr: The simplified expression.
	"""
	def round_float(term: sp.Basic, ndec: int, approx: bool) -> sp.Basic:
		"""
		Rounds a floating-point number to the given number of decimal places, then truncates any insignificant decimal places.

		Args:
			term (sympy.Basic): The term to round.
			ndec (int): The number of decimal places to round to.
			approx (bool): Whether to approximate the result to a decimal.

		Returns:
			sympy.Basic: The rounded and truncated term.
		"""
		#logging_print(f"Raw term:{' '*7}`{term}`")
		if term.is_number:
			try:
				if approx: # Round to the specified number of decimal places
					rounded_term: sp.Basic = S(round(term, ndec))
					#logging_print(f"Rounded term:{' '*3}`{rounded_term}`")
				else:
					rounded_term: sp.Basic = term # If not using approximate simplification, leave the term unchanged
			except Exception:
				rounded_term: sp.Basic = term # If rounding fails, leave the term unchanged
			try: # Truncate remaining insignificant decimal places
				sig_ndec: int = len(str(rounded_term).split('.')[1].rstrip('0')) # Number of significant decimal places (after rounding)
				if sig_ndec == 0: # No significant decimal places
					#logging_print(f"Truncated term:{' '*1}`{int(rounded_term)}`")
					return S(int(rounded_term)) # Return integer
				else: # Has significant decimal places
					#logging_print(f"Truncated term:{' '*1}`{round(rounded_term, term_ndec)}`")
					return S(round(rounded_term, sig_ndec)) # Return float truncated to significant decimal places
			except Exception:
				return rounded_term # If truncating fails, return the term unchanged
		return term  # If the term is not a number, return the term unchanged
	rounded_expr: sp.Expr = expr.xreplace({term: round_float(term, ndec, approx) for term in expr.atoms()})
	return rounded_expr



### TESTING ###

def _test():
	pass

if __name__ == '__main__':
	_test()


