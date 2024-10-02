### IMPORTS ###

# builtins
#import cmath
from decimal import Decimal, getcontext, InvalidOperation, ROUND_HALF_UP
#import fractions
#import math
#import numbers
#import random
import re
#import statistics

# external
from sympy import simplify, sympify

# internal
#from app_globals import *
import app_globals
from app_random import roll_dice



### GLOBAL VARIABLES ###

#ALLOWED_CHARS: re.Pattern[str] = re.compile(r'^[\d\+\-\*/\^()., ]+$')
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
#BUILTIN_FUNCTIONS = [
#	'exp',
#	'pow',
#	'cbrt',
#	'sqrt',
#	'root',
#	'log',
#	'ln',
#	'acos',
#	'acosh',
#	'acot',
#	'acoth',
#	'acsc',
#	'acsch',
#	'asec',
#	'asech',
#	'asin',
#	'asinh',
#	'atan',
#	'atan2',
#	'atanh',
#	'cos',
#	'cosh',
#	'cot',
#	'coth',
#	'csc',
#	'csch',
#	'sec',
#	'sech',
#	'sin',
#	'sinh',
#	'tan',
#	'tanh',
#	'abs',
#	'gcd',
#	'lcm',
#	'factorial',
#	#'comb',
#	#'perm',
#	#'remainder',
#	'ceiling',
#	'floor',
#	'trunc',
#	'erf',
#	'erfc',
#	'gamma',
#	#'bin',
#	#'hex',
#	#'oct',
#	#'average',
#	#'mean',
#	#'median',
#	#'mode',
#]
BUILTIN_FUNCTIONS = {
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
CUSTOM_FUNCTIONS = {
	'roll': {'func': 'roll_dice', 'args': 1, 'returns': 2},
	#'average': {'func': 'statistics.mean', 'args': 1},
}
OPERATORS = {
	'+': lambda x, y: x + y,
	'-': lambda x, y: x - y,
	'*': lambda x, y: x * y,
	'/': lambda x, y: x / y,
	'**': lambda x, y: x ** y
}
KNOWN_FUNCTIONS = (*BUILTIN_FUNCTIONS, *CUSTOM_FUNCTIONS)
#print(KNOWN_FUNCTIONS)
getcontext().prec = app_globals.DEC_PRECISION



### FUNCTIONS ###

def eval_custom_functions(expression: str):
	"""
	"""
	#pattern = re.compile(r'(\b\w+\()([^)]+)\)')
	pattern = re.compile(r'(\b\w+)\(([^)]*)\)')
	def replacer(match):
		function_name = match.group(1).strip('(')
		argument_str = match.group(2)
		args = [arg.strip() for arg in argument_str.split(',')]
		print(f"Function: {function_name}, Arguments: {args}")
		#if function_name in BUILTIN_FUNCTIONS:
		#	return f"{function_name}({', '.join(args)})"
		if function_name in BUILTIN_FUNCTIONS:
			return f"{BUILTIN_FUNCTIONS[function_name]['func']}({', '.join(args)})"
		elif function_name in CUSTOM_FUNCTIONS:
			function = CUSTOM_FUNCTIONS[function_name]
			print(function)
			#if function['args'] != len(args):
			#	if function['args'] == 1:
			#		raise ValueError(f"{function_name}() expects 1 argument.")
			#	else:
			#		raise ValueError(f"{function_name}() expects {function['args']} arguments.")
			if function['returns'] == 1:
				return eval(f"{function['func']}({', '.join(args)})")
			elif function['returns'] == 2:
				print(f"{function['func']}({', '.join(args)})")
				result, _ = eval(f"{function['func']}({', '.join(args)})")
				return result
			else:
				raise ValueError(f"{function_name}() returns {function['returns']} values. Only 1 or 2 values are supported.")
		#elif function_name == 'roll':
		#	if len(args) != 1:
		#		raise ValueError(f"{function_name} expects exactly 1 argument.")
		#	result, _ = roll_dice(args[0])
		#	return result
		#raise ValueError(f"Unknown function: {function_name}()")
	return pattern.sub(replacer, expression)

def eval_with_decimal(expression: any) -> str:
	"""
	Recursively evaluate sympy expressions using Decimal for high precision.
	"""
	if expression.is_Number:
		# Convert sympy numbers to Decimal
		return Decimal(str(expression))
	
	elif expression.is_Add or expression.is_Mul or expression.is_Pow:
		# If it's an addition, multiplication, or power, evaluate the arguments
		args = [eval_with_decimal(arg) for arg in expression.args]
		operator = str(expression.func)
		return OPERATORS[operator](*args)

	# Handle division separately
	elif expression.is_Div:
		args = [eval_with_decimal(arg) for arg in expression.args]
		return args[0] / args[1]

	# If the expression doesn't fit the above, simplify it directly
	else:
		return Decimal(str(expression))

def evaluate_expression(expression: str, dont_evaluate: bool = app_globals.ONLY_SIMPLIFY) -> str:
	#global LAST_RESULT
	#continue_eval: bool = True
	if app_globals.DEBUG:
		print("Evaluating expression...")
	try:
		# Check for empty expression
		#if not expression:
		#	return app_globals.DEF_RESULT
		# Sanitize input
		#try:
		#	expression: str = sanitize_input(expression)
		#	print(f"Expr (1: sanitized):{' '*4}`{expression}`")
		#except ValueError:
		#	#return "ERROR: Invalid characters in expression"
		#	#return LAST_RESULT
		#	raise ValueError
		#except Exception:
		#	raise Exception
		# Handle implied exponentation
		expression = implied_exp(expression)
		if app_globals.DEBUG:
			print(f"Expr (implied_exp):{' '*2}`{expression}`")
		# Handle implied multiplication
		expression = implied_mult(expression)
		if app_globals.DEBUG:
			print(f"Expr (implied_mult):{' '*1}`{expression}`")
		# Handle custom functions
		try:
			expression: str = eval_custom_functions(expression)
			if app_globals.DEBUG:
				print(f"Expr (eval_func):{' '*4}`{expression}`")
		except ValueError as e:
			return f"{e}"
		#except Exception:
		#	raise Exception
		# Simpify
		expression = sympify(expression)
		print(f"Expr (sympify):{' '*6}`{expression}`")
		if str(expression) == 'zoo':
			return "ERROR: Division by zero"
		# Simplify
		expression = simplify(expression)
		if app_globals.DEBUG:
			print(f"Expr (simplify):{' '*5}`{expression}`")
		if dont_evaluate:
			expression: str = format_expression(str(expression))
			if app_globals.DEBUG:
				print(f"Expr (format):{' '*7}`{expression}`")
			app_globals.LAST_RESULT = expression
			return expression
		else:
			# Evalf
			result = expression.evalf(app_globals.DEC_PRECISION)
			if app_globals.DEBUG:
				print(f"Expr (evalf):{' '*8}`{result}`")
			if re.search(r'[a-zA-Z]', str(result)):
				app_globals.LAST_RESULT = result
				return str(result)
			# Eval with Decimal
			result: str = eval_with_decimal(result)
			if app_globals.DEBUG:
				print(f"Expr (eval_dec):{' '*5}`{result}`")
			# Simplify Decimal
			result: str = simplify_decimal(result)
			if app_globals.DEBUG:
				print(f"Expr (simplify_dec):{' '*1}`{result}`")
			# Return result
			app_globals.LAST_RESULT = result
			return result
			#try:
			#	pass
			#	#expression = expression.replace('^', '**')
			#	#result = eval(expression, {'__builtins__': None}, {"Decimal": Decimal})
			#	#result = simplify_float(float(expression))
			#	#result = expression
			#	#print(result)
			#	#print(type(result))
			#	#last_valid_result = simplify_float(float(result))
	except InvalidOperation:
		raise InvalidOperation("Invalid number format")
	except ZeroDivisionError:
		raise ZeroDivisionError("Division by zero")
	#except Exception as e:
	#	return f"ERROR: {e}"

def format_expression(expression: str) -> str:
	"""
	Formats an expression by making it more readable.
	"""
	expression = expression.replace('**', '^')
	expression = re.sub(r'(?<=\d)\*([a-zA-Z])', r'\1', expression) # Remove '*' between a number and variable, e.g., 2*x -> 2x
	expression = re.sub(r'([a-zA-Z])\*\(', r'\1\(', expression) # Remove '*' between a variable and opening parenthesis, e.g., x*(3) -> x(3)
	return expression

def implied_mult(expression: str, functions: list | tuple | set = KNOWN_FUNCTIONS) -> str:
	#pattern = r'(?<=\d)(\()|(\))(?=\d)|(\))(?=\()'
	#pattern = r'(?<=\d)(?=\()|(?<=\))(?=\d)|(?<=\))(?=\()'
	#functions_pattern = r'(' + '|'.join(KNOWN_FUNCTIONS) + r')\('
	#pattern = (
	#	r'(?<=\d)(?=\()'
	#	r'|(?<=\))(?=\d)'
	#	r'|(?<=\))(?=\()'
	#)
	#pattern = (
	#	r'(?<=\d)(?=\()' # Case 1: number followed by an opening parenthesis, e.g., 1(2)
	#	r'|(?<=\))(?=\d)' # Case 2: closing parenthesis followed by a number, e.g., (3)4
	#	r'|(?<=\))(?=\()' # Case 3: two sets of parentheses, e.g., (3)(4)
	#	r'|(?<=\d)(?=' # Case 4: number followed by a function name, e.g., 2sqrt(9)
	#	r'(' + '|'.join(KNOWN_FUNCTIONS) + r')\()'
	#	r'|(?<=\))(?=' # Case 5: closing parenthesis followed by a function name, e.g., (2)sqrt(9)
	#	r'(' + '|'.join(KNOWN_FUNCTIONS) + r')\()'
	#)
	#pattern = (
	#	r'(?<=\d)(?=\()'                                # Case 1: number followed by an opening parenthesis, e.g., 1(2)
	#	r'|(?<=\))(?=\d)'                               # Case 2: closing parenthesis followed by a number, e.g., (3)4
	#	r'|(?<=\))(?=\()'                               # Case 3: two sets of parentheses, e.g., (3)(4)
	#	r'|(?<=\d)(?=(' + '|'.join(functions) + r')\()' # Case 4: number followed by a function, e.g., 2sqrt(9)
	#	r'|(?<=\))(?=(' + '|'.join(functions) + r')\()' # Case 5: closing parenthesis followed by a function, e.g., (2)sqrt(9)
	#	r'|(?<=\d)(?=[a-zA-Z])'                         # Case 6: number followed by a variable, e.g., 2x -> 2*x
	#	r'|(?<=\))(?=[a-zA-Z])'                         # Case 7: closing parenthesis followed by a variable, e.g., (2)x -> (2)*x
	#	r'|(?<=[a-zA-Z])(?=\d)'                         # Case 8: variable followed by a number, e.g., x2 -> x*2
	#	r'|(?<=[a-zA-Z])(?=\()'                         # Case 9: variable followed by an opening parenthesis, e.g., x(3) -> x*(3)
	#)
	#return re.sub(pattern, '*', expression)
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
	#print(pattern)
	modified_expression = re.sub(pattern, '*', expression)
	modified_expression = re.sub(r'(' + functions_pattern + r')\*\(', r'\1(', modified_expression) # Remove '*' between functions and '('
	return modified_expression

def implied_exp(expression: str) -> str:
	return expression.replace('^', '**')

def sanitize_input(expression: str, allowed_chars: str = ALLOWED_CHARS, sanitize: bool = app_globals.SANITIZE) -> str:
	expression = expression.lstrip('=').rstrip('=')
	if sanitize and not allowed_chars.match(expression):
		raise ValueError("Invalid characters in expression")
	if app_globals.DEBUG:
		print(f"Expr (sanitized):{' '*4}`{expression}`")
	return expression

def simplify_decimal(value: any, decimal_places: int = app_globals.DEC_DISPLAY) -> str:
	"""
	Simplifies a number with decimal places by rounding to `DEC_DISPLAY` places and truncating trailing empty decimal places.
	"""
	if not isinstance(value, Decimal):
		value = Decimal(str(value))
	#print(value)
	quatitize_pattern = Decimal(f"1.{'0' * decimal_places}")
	rounded_value = value.quantize(quatitize_pattern, rounding=ROUND_HALF_UP)
	if rounded_value.is_zero():
		return "0"
	simplified_value = str(rounded_value).rstrip('0').rstrip('.')
	return simplified_value
	#if isinstance(value, Decimal):
	#	str_value = str(value)
	#	if value.is_integer():
	#		return value.quantize(Decimal(1))
	#else:
	#	raise ValueError("Input must be a Decimal to be truncated.")

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
#		raise ValueError("Input must be a float to be simplified.")



### MAIN ###

if __name__ == "__main__":
	import math
	print(math.sqrt(9))
	print(math.log(9, 3))
	print(math.fabs(-9))
	print(math.gcd(9, 3))
	print(math.factorial(9))
	print(math.trunc(9.9))
	print(math.ceil(9.9))
	print(math.floor(9.9))
	print(math.pow(9, 3))
	print(math.acosh(9))
	print(math.remainder(9, 3))
	print(math.cbrt(9))
	print(math.comb(9, 3))
	print(math.exp2(9))
	print(math.perm(9, 3))
	print(math.lcm(9, 3))
	#print(math.isqrt(9))
	print(math.atanh(9))
	#print(math.)


