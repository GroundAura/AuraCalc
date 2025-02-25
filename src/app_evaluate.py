### IMPORTS ###

# builtins
import cmath
from collections.abc import Callable, Sequence
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
#import fractions
import math
#import numbers
#import random
import re
import statistics
from string import ascii_letters as ASCII_LETTERS, whitespace as WHITESPACE
from typing import Any

# external
from sympy import simplify, sympify, nsimplify, S, SympifyError
import sympy

# internal
from app_random import roll_dice, quad_zero
from app_logging import logging_print
from app_type import function_exists
from app_window import delayed_display, display_result



### CONSTANTS ###

ALLOWED_CHARS: re.Pattern[str] = re.compile(
	#r'^(?:\d+|?(?:pi|e|inf)|(?:root\(|sqrt\(|ln\(|log\(log10\(|log2\(|log1p\(|sin\(|cos\(|tan\(|csc\(|sec\(|cot\(|fabs\(|exp\(|exp2\(|expm1\(|gcd\(|factorial\(|trunc\(|ceil\(|floor\(|hex\(|bin\(|oct\()\s*|\+\-\*/\^%().!, ]+)+$'
	r'^(?:'
	r'\d+|' # Digits
	r'(?:pi|e|[nN][aA][nN])|' # Constants: pi, e, NaN
	#r'(?:i|inf)|'
	r'(?:0x[0-9a-f]+|0b[01]+|0o[0-7]+)|' # Hex, binary, octal numbers
	r'(?:' # Allowed function names
	r'exp\(|pow\('
	r'|cbrt\(|sqrt\(|root\('
	r'|log\(|ln\('
	r'|acos\(|acosh\(|acot\(|acoth\(|acsc\(|acsch\(|asec\(|asech\(|asin\(|asinh\(|atan\(|atan2\(|atanh\(|cos\(|cosh\(|cot\(|coth\(|csc\(|csch\(|sec\(|sech\(|sin\(|sinh\|tan\(|tanh\('
	r'|abs\('
	r'|gcd\(|lcm\('
	r'|factorial\('
	r'|ceiling\(|floor\(|trunc\('
	r'|erf\(|erfc\(|gamma\('
	#r'|log10\(|log2\(|log1p\('
	#r'|comb\(|perm\('
	#r'|remainder\('
	#r'|bin\(|hex\(|oct\('
	#r'|add\(|sub\(|subtract\(|mul\(|mult\(|multiply\(|div\(|divide\('
	#r'|ldiv\(|longdiv\(|longdivide\(|longdivision\('
	#r'|average\(|mean\(|median\(|mode\('
	r'|roll\('
	#r')|'
	r')\s*'
	#r'|[a-zA-Z](?!\s*\()' # Variables, letters that are not followed by '('
	r'|[a-zA-Z]'
	r'|[\+\-\*/\^%().!, ]+'
	r')+$'
)

BUILTIN_FUNCTIONS: dict[str, dict[str, Any]] = {
	'exp': {'func': 'exp', 'args': 1},
	'pow': {'func': 'pow', 'args': 2},
	'cbrt': {'func': 'cbrt', 'args': 1},
	'sqrt': {'func': 'sqrt', 'args': 1},
	'root': {'func': 'root', 'args': 2},
	'log': {'func': 'log', 'args': 2},
	'ln': {'func': 'log', 'args': 1},
	'acos': {'func': 'acos', 'args': 1},
	'acosh': {'func': 'acosh', 'args': 1},
	'acot': {'func': 'acot', 'args': 1},
	'acoth': {'func': 'acoth', 'args': 1},
	'acsc': {'func': 'acsc', 'args': 1},
	'acsch': {'func': 'acsch', 'args': 1},
	'asec': {'func': 'asec', 'args': 1},
	'asech': {'func': 'asech', 'args': 1},
	'asin': {'func': 'asin', 'args': 1},
	'asinh': {'func': 'asinh', 'args': 1},
	'atan': {'func': 'atan', 'args': 1},
	'atan2': {'func': 'atan2', 'args': 2},
	'atanh': {'func': 'atanh', 'args': 1},
	'cos': {'func': 'cos', 'args': 1},
	'cosh': {'func': 'cosh', 'args': 1},
	'cot': {'func': 'cot', 'args': 1},
	'coth': {'func': 'coth', 'args': 1},
	'csc': {'func': 'csc', 'args': 1},
	'csch': {'func': 'csch', 'args': 1},
	'sec': {'func': 'sec', 'args': 1},
	'sech': {'func': 'sech', 'args': 1},
	'sin': {'func': 'sin', 'args': 1},
	'sinh': {'func': 'sinh', 'args': 1},
	'tan': {'func': 'tan', 'args': 1},
	'tanh': {'func': 'tanh', 'args': 1},
	'abs': {'func': 'fabs', 'args': 1},
	'gcd': {'func': 'gcd', 'args': 2},
	'lcm': {'func':' lcm', 'args': 2},
	'factorial': {'func': 'factorial', 'args': 1},
	#'comb': {'func': 'comb', 'args': 2},
	#'perm': {'func':' perm', 'args': 2},
	#'remainder': {'func': 'remainder', 'args': 2},
	'ceiling': {'func': 'ceil', 'args': 1},
	'floor': {'func': 'floor', 'args': 1},
	'trunc': {'func': 'trunc', 'args': 1},
	'erf': {'func': 'erf', 'args': 1},
	'erfc': {'func': 'erfc', 'args': 1},
	'gamma': {'func': 'gamma', 'args': 1},
	#'bin': {'func': 'bin', 'args': 1},
	#'hex': {'func': 'hex', 'args': 1},
	#'oct': {'func': 'oct', 'args': 1},
	#'average': {'func': 'statistics.mean', 'args': 1},
	#'mean': {'func': 'statistics.mean', 'args': 1},
	#'median': {'func': 'statistics.median', 'args': 1},
	#'mode': {'func': 'statistics.mode', 'args': 1},
	'Add': {'func': 'Add'},
	'add': {'func': 'Add'},
	'Mult': {'func': 'Mult'},
	'mult': {'func': 'Mult'},
	'Pow': {'func': 'Pow'},
	'pow': {'func': 'Pow'},
	'Integer': {'func': 'Integer'},
	'integer': {'func': 'Integer'},
	'int': {'func': 'Integer'},
	'Rational': {'func': 'Rational'},
	'rational': {'func': 'Rational'},
	'Float': {'func': 'Float'},
	'float': {'func': 'Float'},
	'Infinity': {'func': 'Infinity'},
	'Inf': {'func': 'Infinity'},
	'inf': {'func': 'Infinity'},
	'NaN': {'func': 'NaN'},
	'nan': {'func': 'NaN'},
	'Zero': {'func': 'Zero'},
	'zero': {'func': 'Zero'},
	'I': {'func': 'I'},
	'pi': {'func': 'pi'},
	'E': {'func': 'E'},
	'oo': {'func': 'oo'},
	'Poly': {'func': 'Poly'},
	'poly': {'func': 'Poly'},
	'Polynomial': {'func': 'Poly'},
	'polynomial': {'func': 'Poly'},
	'RootOf': {'func': 'RootOf'},
	'rootof': {'func': 'RootOf'},
}
CUSTOM_FUNCTIONS: dict[str, dict[str, Any]] = {
	'roll': {'func': 'roll_dice', 'args': 1, 'returns': 2},
	'quad': {'func': 'quad_zero', 'args': 4, 'returns': 1},
	'quadratic': {'func': 'quad_zero', 'args': 4, 'returns': 1},
	'quadratic_formula': {'func': 'quad_zero', 'args': 4, 'returns': 1},
	#'average': {'func': 'statistics.mean', 'args': 1},
}
KNOWN_FUNCTIONS: tuple[str] = (*BUILTIN_FUNCTIONS, *CUSTOM_FUNCTIONS)
#logging_print(KNOWN_FUNCTIONS)

#OPERATIONS: dict[str, any] = {
#	'+': lambda x, y: x + y,
#	'-': lambda x, y: x - y,
#	'*': lambda x, y: x * y,
#	'/': lambda x, y: x / y,
#	'**': lambda x, y: x ** y
#}

FUNCTIONS_BUILTIN: dict[str, Callable] = {
	'int': int,                 # int(x)
	'float': float              # float(x)
}
FUNCTIONS_CUSTOM: dict[str, Callable] = {
	'roll': roll_dice,              # roll_dice(dice_string)
	'roll_dice': roll_dice,         # roll_dice(dice_string)
	'quad': quad_zero,              # quad_zero(a, b, c, positive = '+')
	'quadratic': quad_zero,         # quad_zero(a, b, c, positive = '+')
	'quadratic_formula': quad_zero  # quad_zero(a, b, c, positive = '+')
}
FUNCTIONS_CMATH: dict[str, Callable] = {
	# Conversions to and from polar coordinates
	'phase': cmath.phase,        # cmath.phase(x)
	'polar': cmath.polar,        # cmath.polar(x)
	'rect': cmath.rect,          # cmath.rect(r, phi)
	# Power and logarithmic functions
	'exp': cmath.exp,            # cmath.exp(x)
	'log': cmath.log,            # cmath.log(x[, base])
	'log10': cmath.log10,        # cmath.log10(x)
	'sqrt': cmath.sqrt,          # cmath.sqrt(x)
	# Trigonometric functions
	'acos': cmath.acos,          # cmath.acos(x)
	'asin': cmath.asin,          # cmath.asin(x)
	'atan': cmath.atan,          # cmath.atan(x)
	'cos': cmath.cos,            # cmath.cos(x)
	'sin': cmath.sin,            # cmath.sin(x)
	'tan': cmath.tan,            # cmath.tan(x)
	# Hyperbolic functions
	'acosh': cmath.acosh,        # cmath.acosh(x)
	'asinh': cmath.asinh,        # cmath.asinh(x)
	'atanh': cmath.atanh,        # cmath.atanh(x)
	'cosh': cmath.cosh,          # cmath.cosh(x)
	'sinh': cmath.sinh,          # cmath.sinh(x)
	'tanh': cmath.tanh,          # cmath.tanh(x)
	# Classification functions
	'isfinite': cmath.isfinite,  # cmath.isfinite(x)
	'isinf': cmath.isinf,        # cmath.isinf(x)
	'isnan': cmath.isnan,        # cmath.isnan(x)
	'isclose': cmath.isclose    # cmath.isclose(a, b, *, rel_tol=1e-09, abs_tol=0.0)
}
FUNCTIONS_MATH: dict[str, Callable] = {
	# Number-theoretic functions
	'comb': math.comb,           # math.comb(n, k)
	'factorial': math.factorial, # math.factorial(n)
	'gcd': math.gcd,             # math.gcd(*integers)
	'isqrt': math.isqrt,         # math.isqrt(n)
	'lcm': math.lcm,             # math.lcm(*integers)
	'perm': math.perm,           # math.perm(n, k)
	# Floating point arithmetic
	'ceil': math.ceil,           # math.ceil(x)
	'fabs': math.fabs,           # math.fabs(x)
	'floor': math.floor,         # math.floor(x)
	#'fma': math.fma,             # math.fma(x, y, z)
	'fmod': math.fmod,           # math.fmod(x, y)
	'modf': math.modf,           # math.modf(x)
	'remainder': math.remainder, # math.remainder(x, y)
	'trunc': math.trunc,         # math.trunc(x)
	# Floating point manipulation functions
	'copysign': math.copysign,   # math.copysign(x, y)
	'frexp': math.frexp,         # math.frexp(x)
	'isclose': math.isclose,     # math.isclose(a, b, rel_tol, abs_tol)
	'isfinite': math.isfinite,   # math.isfinite(x)
	'isinf': math.isinf,         # math.isinf(x)
	'isnan': math.isnan,         # math.isnan(x)
	'ldexp': math.ldexp,         # math.ldexp(x, i)
	'nextafter': math.nextafter, # math.nextafter(x, y, steps)
	'ulp': math.ulp,             # math.ulp(x)
	# Power, exponential and logarithmic functions
	'cbrt': math.cbrt,           # math.cbrt(x)
	'exp': math.exp,             # math.exp(x)
	'exp2': math.exp2,           # math.exp2(x)
	'expm1': math.expm1,         # math.expm1(x)
	'log': math.log,             # math.log(x, base)
	'log1p': math.log1p,         # math.log1p(x)
	'log2': math.log2,           # math.log2(x)
	'log10': math.log10,         # math.log10(x)
	'pow': math.pow,             # math.pow(x, y)
	'sqrt': math.sqrt,           # math.sqrt(x)
	# Summation and product functions
	'dist': math.dist,           # math.dist(p, q)
	'fsum': math.fsum,           # math.fsum(iterable)
	'hypot': math.hypot,         # math.hypot(*coordinates)
	'prod': math.prod,           # math.prod(iterable, start)
	'sumprod': math.sumprod,     # math.sumprod(p, q)
	# Angular conversion
	'degrees': math.degrees,     # math.degrees(x)
	'radians': math.radians,     # math.radians(x)
	# Trigonometric functions
	'acos': math.acos,           # math.acos(x)
	'asin': math.asin,           # math.asin(x)
	'atan': math.atan,           # math.atan(x)
	'atan2': math.atan2,         # math.atan2(y, x)
	'cos': math.cos,             # math.cos(x)
	'sin': math.sin,             # math.sin(x)
	'tan': math.tan,             # math.tan(x)
	# Hyperbolic functions
	'acosh': math.acosh,         # math.acosh(x)
	'asinh': math.asinh,         # math.asinh(x)
	'atanh': math.atanh,         # math.atanh(x)
	'cosh': math.cosh,           # math.cosh(x)
	'sinh': math.sinh,           # math.sinh(x)
	'tanh': math.tanh,           # math.tanh(x)
	# Special functions
	'erf': math.erf,             # math.erf(x)
	'erfc': math.erfc,           # math.erfc(x)
	'gamma': math.gamma,         # math.gamma(x)
	'lgamma': math.lgamma,       # math.lgamma(x)
}
FUNCTIONS_SYMPY: dict[str, Callable] = {

}
FUNCTIONS_STATISTICS: dict[str, Callable] = {
	
}
FUNCTIONS_ALL: dict[str, Callable] = {
	**FUNCTIONS_BUILTIN,
	**FUNCTIONS_CUSTOM,
	**FUNCTIONS_CMATH,
	**FUNCTIONS_MATH,
	**FUNCTIONS_SYMPY
}
#logging_print(f"FUNCTIONS_ALL: {FUNCTIONS_ALL}")

VALID_FUNCTIONS: set[str] = set()
for key in FUNCTIONS_ALL.keys():
	if isinstance(key, Sequence) and type(key) is not str:
		for k in key:
			VALID_FUNCTIONS.add(k)
	else:
		VALID_FUNCTIONS.add(key)

CONSTANTS_CMATH: dict[str, Any] = {
	'pi': cmath.pi,
	'e': cmath.e,
	'tau': cmath.tau,
	'inf': cmath.inf,
	'infj': cmath.infj,
	'nan': cmath.nan,
	'nanj': cmath.nanj
}
CONSTANTS_MATH: dict[str, Any] = {
	'pi': math.pi,
	'e': math.e,
	'tau': math.tau,
	'inf': math.inf,
	'nan': math.nan
}
CONSTANTS_SYMPY: dict[str, Any] = {
	
}
CONSTANTS_ALL: dict[str, Any] = {
	**CONSTANTS_CMATH,
	**CONSTANTS_MATH,
	**CONSTANTS_SYMPY
}

VALID_CONSTANTS: set[str] = set()
for key in CONSTANTS_ALL.keys():
	if isinstance(key, Sequence):
		for k in key:
			VALID_CONSTANTS.add(k)
	else:
		VALID_CONSTANTS.add(key)



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
	# Remove leading zeros
# ***TO DO***: ensure there's no decimal points before the zero before removing leading zeros
	expr = re.sub(r'\b0+(\d+)', r'\1', expr)
	return expr

def eval_custom_functions(expression: str) -> str:
	"""
	Evaluates custom functions in an expression.

	Args:
		expression (str): The expression to evaluate.

	Returns:
		str: The processed expression.
	"""
	func_pattern: re.Pattern = re.compile(r'(\b\w+)\(([^)]*)\)')
	def func_replacer(match) -> str:
		"""
		Replaces a function call with its result.

		Args:
			match: The match object.

		Returns:
			str: The result of the function call or the original expression.
		"""
		func_name: str = match.group(1).strip('(')
		arg_str: str = match.group(2)
		#args: list = [f"'{arg.strip()}'" for arg in arg_str.split(',')]
		args_list: list = [arg.strip() for arg in arg_str.split(',')]
		logging_print(f"Function requested: '{func_name}', Arguments: {args_list}")
		#logging_print(f"Valid functions: {VALID_FUNCTIONS}")
		#logging_print(func_name in globals())
		#logging_print(callable(globals()[func_name]))
		if func_name in VALID_FUNCTIONS:
			func: Callable = FUNCTIONS_ALL[func_name]
			#logging_print(f"Matching function: '{func_name}': {func.__module__}.{func.__name__}")
			args: list = []
			for arg in args_list:
				if func is roll_dice and args_list.index(arg) == 0:
					args.append(arg)
				elif func is quad_zero and args_list.index(arg) == 4:
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
			logging_print(f"Function '{func_name}' not valid. Adding explicit multiplication to ensure no errors.")
			#return '*'.join(match.group(0))
			return match.group(0).replace(func_name, '*'.join(func_name))
		else:
			logging_print(f"Function '{func_name}' not found. Assuming it's not a function.")
			return match.group(0)
		##if function_name in BUILTIN_FUNCTIONS:
		##	return f"{function_name}({', '.join(args)})"
		#if func_name in BUILTIN_FUNCTIONS:
		#	return f"{BUILTIN_FUNCTIONS[func_name]['func']}({', '.join(args)})"
		#elif func_name in CUSTOM_FUNCTIONS:
		#	function_info = CUSTOM_FUNCTIONS[func_name]
		#	logging_print(f"Matching function: '{func_name}': {function_info}")
		#	function_to_call: str = f"{function_info['func']}({', '.join(args)})"
		#	#function_to_call: str = f"{function_info['func']}({', '.join([f"'{arg}'" if 'd' in arg else arg for arg in args])})"
		#	logging_print(f"Function to call: {function_to_call}")
		#	#if function['args'] != len(args):
		#	#	if function['args'] == 1:
		#	#		raise ValueError(f"{function_name}() expects 1 argument.")
		#	#	else:
		#	#		raise ValueError(f"{function_name}() expects {function['args']} arguments.")
		#	if function_info['returns'] == 1:
		#		result = eval(function_to_call)
		#		result = str(result)
		#		logging_print(f"Function result: '{result}' (type: {type(result)})")
		#		return result
		#	elif function_info['returns'] == 2:
		#		result, _ = eval(function_to_call)
		#		result = str(result)
		#		logging_print(f"Function result: '{result}' (type: {type(result)})")
		#		return result
		#	else:
		#		raise ValueError(f"{func_name}() returns {function_info['returns']} values. Only 1 or 2 values are supported.")
		##elif function_name == 'roll':
		##	if len(args) != 1:
		##		raise ValueError(f"{function_name} expects exactly 1 argument.")
		##	result, _ = roll_dice(args[0])
		##	return result
		##raise ValueError(f"Unknown function: {function_name}()")
	#const_pattern: re.Pattern = re.compile(r'(\b\w+)')
	#def const_replacer(match) -> str:
	#	pass
	processed_expression: str = func_pattern.sub(func_replacer, expression)
	#processed_expression: str = const_pattern.sub(const_replacer, processed_expression)
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

def evaluate_expression(app, expr: str, dont_approximate: bool = False) -> str:
	"""
	Evaluates an expression.

	Args:
		expression (str): The expression to evaluate.
		dont_evaluate (bool, optional): Whether to only simplify the expression. Defaults to `False`.

	Returns:
		str: The result of the expression.
	"""
	#continue_eval: bool = True
	#logging_print('Evaluating expression...')
	try:
		# Handle custom functions
		expr: str = eval_custom_functions(expr)
		logging_print(f"Expr (eval_func):{' '*4}`{expr}` - type: {type(expr)}")
		# Remove unnecessary characters
		expr = compact_expr(expr)
		logging_print(f"Expr (compacted):{' '*4}`{expr}` - type: {type(expr)}")
		# Handle implied exponentation
		expr = implied_exp(expr)
		logging_print(f"Expr (implied_exp):{' '*2}`{expr}` - type: {type(expr)}")
		# Handle implied multiplication
		expr = implied_mult(expr)
		logging_print(f"Expr (implied_mult):{' '*1}`{expr}` - type: {type(expr)}")
		# Convert to sympy object
		expr = sympify(expr)
		logging_print(f"Expr (sympify):{' '*6}`{expr}` - type: {type(expr)}")
		if expr.has(S.NaN):
			raise ZeroDivisionError('Division by Zero (NaN)')
		elif expr.has(S.ComplexInfinity):
			raise ZeroDivisionError('Division by Zero (ComplexInfinity)')
		# Simplify expression
		expr = simplify(expr)
		logging_print(f"Expr (simplify):{' '*5}`{expr}` - type: {type(expr)}")
		#dont_approximate = False
		if not dont_approximate:
			# Convert floats to rationals
			expr = nsimplify(expr, rational=True)
			logging_print(f"Expr (nsimplify):{' '*4}`{expr}` - type: {type(expr)}")
			# Approximate expression
			expr = expr.evalf(app.calc_dec_precicion)
			logging_print(f"Expr (evalf):{' '*8}`{expr}` - type: {type(expr)}")
			#if re.search(r'[a-zA-Z]', str(expr)):
				#app.calc_last_result = str(expr)
				#return str(expr)
			#else:
			#if not any(char.isalpha() for char in str(expr)):
			#	# Simplify Decimal
			#	expr: str = simplify_decimal(expr, app.calc_dec_display)
			#	logging_print(f"Expr (simplify_dec):{' '*1}`{expr}` - type: {type(expr)}")
		# Round all numbers
		expr = expr.xreplace({n: S(round(n, app.calc_dec_display)) for n in expr.atoms(sympy.Number)})
		logging_print(f"Expr (round):{' '*8}`{expr}` - type: {type(expr)}")
		# Convert floats to integers
		#expr = expr.xreplace({n: int(n) if n == int(n) else n for n in expr.atoms(sympy.Number)})
		#cleaned_expr = expr.xreplace({n: sympy.Integer(n) if isinstance(n, sympy.Float) and n == int(n) else n for n in expr.atoms(sympy.Float)})
		#expr = cleaned_expr
		#expr = expr.xreplace({n: S(round(n, 0)) if n == int(n) else n for n in expr.atoms(sympy.Number)})
		#expr = simplify(expr)
		#logging_print(f"Expr (truncate):{' '*5}`{expr}` - type: {type(expr)}")
		# Format expression for display
		expr: str = format_expression(expr)
		logging_print(f"Expr (format):{' '*7}`{expr}` - type: {type(expr)}")
		# Return result
		app.calc_last_result = expr
		return expr
	except InvalidOperation:
		raise InvalidOperation('Invalid number format')
	#except SympifyError as e:
	#	#logging_print(f"{type(e)} - {str(e).replace('\n', '\\n')}")
	#	#c = e.__cause__
	#	#logging_print(f"{type(c)} - {str(c).replace('\n', '\\n')}")
	#	#if isinstance(e.__cause__, SyntaxError):
	#	#	logging_print('Invalid expression')
	#	#	raise SyntaxError('Invalid expression')
	#	if 'SyntaxError' in str(e):
	#		raise SyntaxError('Invalid expression')
	#	else:
	#		raise e

#def evaluate_input(app, input_element, output_element, live_mode: bool = False) -> None:
#	"""
#	Evaluates or simplifies the expression in the input element and displays the result in the output element.

#	Args:
#		app: The application instance.
#		input_element: The element to get the expression to evaluate from.
#		output_element: The element to display the result in.
#		live_mode (bool, optional): Whether to update the result in real-time. Defaults to `False`.
#	"""
#	expression = input_element.get()
#	logging_print(f"Expression:{' '*10}`{expression}`")
#	logging_print(f"Evaluating...")
#	#logging_print(f"Expr (initial):{' '*6}`{expression}`")
#	#logging_print(f"Evaluating Expr:{' '*5}`{expression}`")
#	if app.timeout_id is not None:
#		app.window.after_cancel(app.timeout_id)
#		app.timeout_id = None
#	if not expression:
#		display_result(output_element, app.calc_def_result)
#		return
#	try:
#		expression = sanitize_input(app, expression, sanitize=app._sanitize_input)
#		result = evaluate_expression(app, expression, dont_evaluate=app._only_simplify)
#		display_result(output_element, result)
#		return
#	except ZeroDivisionError:
#		display_result(output_element, 'Undefined (division by zero)')
#		return
#	except Exception as e:
#		if live_mode and app.timeout_patience > 0 and expression[-1] in app.calc_wait_chars:
#			delayed_display(app, output_element, 'ERROR: Incomplete expression')
#			return
#		elif live_mode and app.timeout_patience > 1:
#			delayed_display(app, output_element, f"ERROR: {e}")
#			return
#		else:
#			display_result(output_element, f"ERROR: {e}")
#			return

def format_expression(expr) -> str:
	"""
	Formats an expression by making it more readable.
	"""
	#terms: list = expr.as_ordered_terms()
	#logging_print(f"Terms: `{terms}`")
	#for term in terms:
	#	logging_print(f"Term: `{term}` - type: {type(term)}")
	#	if isinstance(term, sympy.Mul):
	#		coeff, var = term.as_coeff_Mul()
	#		logging_print(f"{coeff} * {var}")

	#tokens = []
	#for node in sympy.preorder_traversal(expr):
	#	if node.is_Atom:
	#		tokens.append(node)
	#	elif node.is_Add or node.is_Mul or node.is_Pow:
	#		tokens.append(node.func)
	#logging_print(f"Tokens: `{tokens}`")

	expr = str(expr)
	expr = expr.replace('**', '^')
	expr = re.sub(r'(?<=\d)\*([a-zA-Z])', r'\1', expr) # Remove '*' between a number and variable, e.g., 2*x -> 2x
	expr = re.sub(r'([a-zA-Z])\*\(', r'\1\(', expr)    # Remove '*' between a variable and opening parenthesis, e.g., x*(3) -> x(3)
# ***TO DO***: truncate decimal places
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

def implied_mult(expression: str, functions: list | set | tuple = VALID_FUNCTIONS) -> str:
	"""
	Evaluates whether an expression contains implied multiplication and adds explicit multiplication if necessary.

	Args:
		expression (str): The expression to evaluate.
		functions (list | tuple | set, optional): The list of known functions. Defaults to `VALID_FUNCTIONS`.

	Returns:
		str: The processed expression.
	"""
	functions_pattern = r'|'.join(functions)
	pattern = (
		r'(?<=\d)(?=\()'                              # Case 1: number followed by an opening parenthesis, e.g., 1(2)
		r'|(?<=\))(?=\d)'                             # Case 2: closing parenthesis followed by a number, e.g., (3)4
		r'|(?<=\))(?=\()'                             # Case 3: two sets of parentheses, e.g., (3)(4)
		r'|(?<=\d)(?=(' + functions_pattern + r')\()' # Case 4: number followed by a function, e.g., 2sqrt(9)
		r'|(?<=\))(?=(' + functions_pattern + r')\()' # Case 5: closing parenthesis followed by a function, e.g., (2)sqrt(9)
		r'|(?<=\d)(?=[a-zA-Z])'                       # Case 6: number followed by a variable, e.g., 2x -> 2*x
		r'|(?<=\))(?=[a-zA-Z])'                       # Case 7: closing parenthesis followed by a variable, e.g., (2)x -> (2)*x
		r'|(?<=[a-zA-Z])(?=\d)'                       # Case 8: variable followed by a number, e.g., x2 -> x*2
		r'|(?<=[a-zA-Z])(?=\()'                       # Case 9: variable followed by an opening parenthesis, e.g., x(3) -> x*(3)
	)
	#logging_print(pattern)
	# add '*' to cases
	modified_expression = re.sub(pattern, '*', expression)                                         # Add '*' in all matched cases
	# exceptions
	modified_expression = re.sub(r'(' + functions_pattern + r')\*\(', r'\1(', modified_expression) # Remove '*' between functions and '('
	modified_expression = re.sub(r'(?<=roll\()(\d+)\*d\*(\d+)', r'\1d\2', modified_expression)     # Remove '*' between numbers and 'd' in the roll() function
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

#def simplify_decimal(number: any, decimal_places: int = 10) -> str:
#	"""
#	Simplifies a number with decimals by rounding to the specified decimal places and truncating trailing empty decimal places.

#	Args:
#		value (any): The number to simplify.
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

#def simplify_float(value: float):
#	value = float(value)
#	if isinstance(value, float):
#		# Convert float to string
#		str_value = str(value)
		
#		# Remove trailing zeros and the decimal point if it's the last character
#		str_value = str_value.rstrip('0').rstrip('.')

#		# Convert to float
#		float_value = float(str_value)
#		if float_value.is_integer():
#			return int(float_value)
#		else:
#			return Decimal(float_value)
#	else:
#		raise ValueError('Input must be a float to be simplified.')

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
	print(sympy.sqrt(9))
	print(int('9'))

if __name__ == '__main__':
	_test()


