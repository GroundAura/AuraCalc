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
from sympy import simplify, sympify, nsimplify

# internal
import app_globals
from app_random import roll_dice, quad_zero
from app_window import delayed_display, display_result



### GLOBAL VARIABLES ###

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
BUILTIN_FUNCTIONS: dict[str, dict[str, any]] = {
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
CUSTOM_FUNCTIONS: dict[str, dict[str, any]] = {
	'roll': {'func': 'roll_dice', 'args': 1, 'returns': 2},
	'quad': {'func': 'quad_zero', 'args': 4, 'returns': 1},
	'quadratic': {'func': 'quad_zero', 'args': 4, 'returns': 1},
	'quadratic_formula': {'func': 'quad_zero', 'args': 4, 'returns': 1},
	#'average': {'func': 'statistics.mean', 'args': 1},
}
OPERATIONS: dict[str, any] = {
	'+': lambda x, y: x + y,
	'-': lambda x, y: x - y,
	'*': lambda x, y: x * y,
	'/': lambda x, y: x / y,
	'**': lambda x, y: x ** y
}
KNOWN_FUNCTIONS: tuple[str] = (*BUILTIN_FUNCTIONS, *CUSTOM_FUNCTIONS)
#print_debug(KNOWN_FUNCTIONS)
getcontext().prec = app_globals.DEC_PRECISION



### FUNCTIONS ###

def eval_custom_functions(app, expression: str) -> str:
	"""
	Evaluates custom functions in an expression.

	Args:
		expression (str): The expression to evaluate.

	Returns:
		str: The processed expression.
	"""
	#pattern = re.compile(r'(\b\w+\()([^)]+)\)')
	pattern: re.Pattern = re.compile(r'(\b\w+)\(([^)]*)\)')
	def replacer(match) -> str:
		"""
		Replaces a function call with its result.

		Args:
			match: The match object.

		Returns:
			str: The result of the function call.
		"""
		function_name = match.group(1).strip('(')
		argument_str = match.group(2)
		args = [f"'{arg.strip()}'" for arg in argument_str.split(',')]
		app.print_log(f"Function requested: {function_name}, Arguments: {args}")
		#if function_name in BUILTIN_FUNCTIONS:
		#	return f"{function_name}({', '.join(args)})"
		if function_name in BUILTIN_FUNCTIONS:
			return f"{BUILTIN_FUNCTIONS[function_name]['func']}({', '.join(args)})"
		elif function_name in CUSTOM_FUNCTIONS:
			function_info = CUSTOM_FUNCTIONS[function_name]
			app.print_log(f"Matching function: '{function_name}': {function_info}")
			function_to_call: str = f"{function_info['func']}({', '.join(args)})"
			#function_to_call: str = f"{function_info['func']}({', '.join([f"'{arg}'" if 'd' in arg else arg for arg in args])})"
			app.print_log(f"Function to call: {function_to_call}")
			#if function['args'] != len(args):
			#	if function['args'] == 1:
			#		raise ValueError(f"{function_name}() expects 1 argument.")
			#	else:
			#		raise ValueError(f"{function_name}() expects {function['args']} arguments.")
			if function_info['returns'] == 1:
				result = eval(function_to_call)
				result = str(result)
				app.print_log(f"Function result: '{result}' (type: {type(result)})")
				return result
			elif function_info['returns'] == 2:
				result, _ = eval(function_to_call)
				result = str(result)
				app.print_log(f"Function result: '{result}' (type: {type(result)})")
				return result
			else:
				raise ValueError(f"{function_name}() returns {function_info['returns']} values. Only 1 or 2 values are supported.")
		#elif function_name == 'roll':
		#	if len(args) != 1:
		#		raise ValueError(f"{function_name} expects exactly 1 argument.")
		#	result, _ = roll_dice(args[0])
		#	return result
		#raise ValueError(f"Unknown function: {function_name}()")
	processed_expression: str = pattern.sub(replacer, expression)
	return processed_expression

def eval_with_decimal(expression: any) -> str:
	"""
	Recursively evaluate sympy expressions using Decimal for high precision.

	Args:
		expression (any): The expression to evaluate.

	Returns:
		str: The result of the expression.
	"""
	if expression.is_Number:
		# Convert sympy numbers to Decimal
		return Decimal(str(expression))
	
	elif expression.is_Add or expression.is_Mul or expression.is_Pow:
		# If it's an addition, multiplication, or power, evaluate the arguments
		args = [eval_with_decimal(arg) for arg in expression.args]
		operator = str(expression.func)
		return OPERATIONS[operator](*args)

	# Handle division separately
	elif expression.is_Div:
		args = [eval_with_decimal(arg) for arg in expression.args]
		return args[0] / args[1]

	# If the expression doesn't fit the above, simplify it directly
	else:
		return Decimal(str(expression))

def evaluate_expression(app, expression: str, dont_evaluate: bool = False) -> str:
	"""
	Evaluates an expression.

	Args:
		expression (str): The expression to evaluate.
		dont_evaluate (bool, optional): Whether to only simplify the expression. Defaults to `app_globals.ONLY_SIMPLIFY`.

	Returns:
		str: The result of the expression.
	"""
	#continue_eval: bool = True
	app.print_log('Evaluating expression...')
	try:
		# Remove leading zeros
		expression = strip_leading_zeros(expression)
		app.print_log(f"Expr (strip_zeros):{' '*2}`{expression}`")
		# Handle implied exponentation
		expression = implied_exp(expression)
		app.print_log(f"Expr (implied_exp):{' '*2}`{expression}`")
		# Handle implied multiplication
		expression = implied_mult(expression)
		app.print_log(f"Expr (implied_mult):{' '*1}`{expression}`")
		# Handle custom functions
		expression: str = eval_custom_functions(app, expression)
		app.print_log(f"Expr (eval_func):{' '*4}`{expression}`")
		# Simpify
		expression = sympify(expression)
		app.print_log(f"Expr (sympify):{' '*6}`{expression}`")
		if str(expression) == 'zoo':
			raise ZeroDivisionError('Division by zero')
		# Simplify
		expression = simplify(expression)
		#app.print_log(type(expression))
		app.print_log(f"Expr (simplify):{' '*5}`{expression}`")
		expression = nsimplify(expression, rational=True)
		app.print_log(f"Expr (nsimplify):{' '*4}`{expression}`")
		if dont_evaluate:
			expression: str = format_expression(str(expression))
			app.print_log(f"Expr (format):{' '*7}`{expression}`")
			app.calc_last_result = expression
			return expression
		else:
			# Eval with Float
			result = expression.evalf(app.calc_dec_precicion)
			app.print_log(f"Expr (evalf):{' '*8}`{result}`")
			if re.search(r'[a-zA-Z]', str(result)):
				app.calc_last_result = str(result)
				return str(result)
			# Eval with Decimal
			result: str = eval_with_decimal(result)
			app.print_log(f"Expr (eval_dec):{' '*5}`{result}`")
			# Simplify Decimal
			result: str = simplify_decimal(result, app.calc_dec_display)
			app.print_log(f"Expr (simplify_dec):{' '*1}`{result}`")
			# Return result
			app.calc_last_result = result
			return result
	except InvalidOperation:
		raise InvalidOperation('Invalid number format')
	except ZeroDivisionError:
		raise ZeroDivisionError('Division by zero')

def evaluate_input(app, input_element, output_element, live_mode: bool = False) -> None:
	"""
	Evaluates or simplifies the expression in the input element and displays the result in the output element.

	Args:
		app: The application instance.
		input_element: The element to get the expression to evaluate from.
		output_element: The element to display the result in.
		live_mode (bool, optional): Whether to update the result in real-time. Defaults to `False`.
	"""
	expression = input_element.get()
	if app.timeout_id is not None:
		app.window.after_cancel(app.timeout_id)
		app.timeout_id = None
	app.print_log(f"Expr (initial):{' '*6}`{expression}`")
	if not expression:
		display_result(app, output_element, app.calc_def_result)
		return
	try:
		expression = sanitize_input(app, expression, sanitize=app._sanitize_input)
		result = evaluate_expression(app, expression, dont_evaluate=app._only_simplify)
		display_result(app, output_element, result)
		return
	except ZeroDivisionError:
		display_result(app, output_element, 'Undefined (division by zero)')
		return
	except Exception as e:
		if live_mode and app.timeout_patience > 0 and expression[-1] in app.calc_wait_chars:
			delayed_display(app, output_element, 'ERROR: Incomplete expression')
			return
		elif live_mode and app.timeout_patience > 1:
			delayed_display(app, output_element, f"ERROR: {e}")
			return
		else:
			display_result(app, output_element, f"ERROR: {e}")
			return

def format_expression(expression: str) -> str:
	"""
	Formats an expression by making it more readable.
	"""
	expression = expression.replace('**', '^')
	expression = re.sub(r'(?<=\d)\*([a-zA-Z])', r'\1', expression) # Remove '*' between a number and variable, e.g., 2*x -> 2x
	expression = re.sub(r'([a-zA-Z])\*\(', r'\1\(', expression) # Remove '*' between a variable and opening parenthesis, e.g., x*(3) -> x(3)
	return expression

def implied_mult(expression: str, functions: list | tuple | set = KNOWN_FUNCTIONS) -> str:
	"""
	Evaluates whether an expression contains implied multiplication and adds explicit multiplication if necessary.

	Args:
		expression (str): The expression to evaluate.
		functions (list | tuple | set, optional): The list of known functions. Defaults to `KNOWN_FUNCTIONS`.

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
	#print_debug(pattern)
	modified_expression = re.sub(pattern, '*', expression)                                         # Add '*' in all matched cases
	modified_expression = re.sub(r'(' + functions_pattern + r')\*\(', r'\1(', modified_expression) # Remove '*' between functions and '('
	modified_expression = re.sub(r'(?<=roll\()(\d+)\*d\*(\d+)', r'\1d\2', modified_expression)     # Remove '*' between numbers and 'd' in the roll() function
	return modified_expression

def implied_exp(expression: str) -> str:
	"""
	Evaluates whether an expression contains implied exponentation and adds explicit exponentation if necessary.

	Args:
		expression (str): The expression to evaluate.

	Returns:
		str: The processed expression.
	"""
	return expression.replace('^', '**')

def sanitize_input(app, expression: str, allowed_chars: str = ALLOWED_CHARS, sanitize: bool = True) -> str:
	"""
	Sanitize an expression by removing invalid sequences of characters if possible, or raising an exception if not.

	Args:
		expression (str): The expression to sanitize.
		allowed_chars (str, optional): The allowed characters. Defaults to `ALLOWED_CHARS`.
		sanitize (bool, optional): Whether to sanitize the expression. Defaults to `app_globals.SANITIZE`.

	Returns:
		str: The sanitized expression.
	"""
	sanitized_expression = expression.lstrip('=').rstrip('=')
	if sanitize and not allowed_chars.match(sanitized_expression):
		raise ValueError('Invalid characters in expression')
	app.print_log(f"Expr (sanitized):{' '*4}`{sanitized_expression}`")
	return sanitized_expression

def simplify_decimal(number: any, decimal_places: int = 10) -> str:
	"""
	Simplifies a number with decimals by rounding to the specified decimal places and truncating trailing empty decimal places.

	Args:
		value (any): The number to simplify.
		decimal_places (int, optional): The number of decimal places to round to. Defaults to `10`.

	Returns:
		str: The simplified number.
	"""
	if not isinstance(number, Decimal):
		number = Decimal(str(number))
	#print_debug(value)
	quatitize_pattern = Decimal(f"1.{'0' * decimal_places}")
	rounded_number = number.quantize(quatitize_pattern, rounding=ROUND_HALF_UP)
	if rounded_number.is_zero():
		return '0'
	simplified_number = str(rounded_number).rstrip('0').rstrip('.')
	return simplified_number

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

def strip_leading_zeros(expression: str) -> str:
	"""
	Strip leading zeros from any numbers in an expression.

	Args:
		expression (str): The expression to process.

	Returns:
		str: The processed expression.
	"""
	processed_expression = re.sub(r'\b0+(\d+)', r'\1', expression)
	return processed_expression



### MAIN ###

if __name__ == '__main__':
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


