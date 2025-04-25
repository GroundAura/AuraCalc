# IMPORTS #

# builtins
from collections.abc import Callable, Iterable
import re
from string import whitespace as WHITESPACE
from typing import Any

# external
from sympy import simplify, sympify, nsimplify, S, SympifyError
import sympy as sp

# internal
from app_logging import logging_print
from app_math import roll_dice, sym_quad_zero, TAU
from app_math import CHAR_EUL, CHAR_IMAG, CHAR_INF, CHAR_INFJ
from app_math import CHAR_NAN, CHAR_PHI, CHAR_PI
from app_type import function_exists, matches_key


# CONSTANTS #

FUNCTIONS_CUSTOM: dict[str | Iterable[str], Callable] = {
    ('roll', 'roll_dice'): roll_dice,
    ('quad', 'quad_zero', 'quadratic', 'quadratic_formula'): sym_quad_zero
}
FUNCTIONS_SYMPY: dict[str | Iterable[str], Callable] = {
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
for dictionary, name in (
    (FUNCTIONS_CUSTOM, 'CUSTOM'),
    (FUNCTIONS_SYMPY, 'SYMPY')
):
    for keys in dictionary.keys():
        if isinstance(keys, str):
            key = keys
            FUNCTION_MAP[key] = (name, dictionary[keys])
        elif issubclass(type(keys), Iterable):
            for key in keys:
                FUNCTION_MAP[key] = (name, dictionary[keys])

CONSTANTS_CUSTOM: dict[str | Iterable[str], Any] = {
}
CONSTANTS_SYMPY: dict[str | Iterable[str], Any] = {
    # Pi
    ('pi', 'Pi', r'\pi', chr(0x03C0)): sp.pi,
    # Euler's Number
    ('e', 'E', r'\e', r'\E'): sp.E,
    # Infinity
    ('oo', 'infinity', 'infty', 'inf', r'\infty', chr(0x221E)): sp.oo,
    # Not a Number
    ('nan', 'NaN', 'NAN', r'\NaN'): sp.nan,
    # Imaginary Unit
    ('i', 'I', 'j', 'J', r'\i', r'\I', r'\j', r'\J'): sp.I,
    # Tau
    ('tau', 'Tau', r'\tau', chr(0x03C4)): TAU,
    # Golden Ratio
    ('phi', 'goldenratio', 'GoldenRatio', r'\phi',
        chr(0x03C6), chr(0x03A6)): sp.GoldenRatio
}

CONSTANTS_MAP: dict[str, tuple[str, Callable]] = dict()
for dictionary, name in (
    (CONSTANTS_CUSTOM, 'CUSTOM'),
    (CONSTANTS_SYMPY, 'SYMPY')
):
    for keys in dictionary.keys():
        if isinstance(keys, str):
            key = keys
            CONSTANTS_MAP[key] = (name, dictionary[keys])
        elif issubclass(type(keys), Iterable):
            for key in keys:
                CONSTANTS_MAP[key] = (name, dictionary[keys])

ALLOWED_CHARS: re.Pattern[str] = re.compile(
    r'^(?:'
    # Digits
    r'\d+'
    # Operators
    r'|[\+\-\*\/\^\%]+'
    # Variables
    r'|[a-zA-Z]'
    # Misc Characters
    r'|[.,()]+'
    # Whitespace
    r'|[ ]+'
    # Temp semi-handle LaTeX
    r'|[${}\\]'
    # Constants
    f"|{'|'.join(re.escape(k) for k in CONSTANTS_MAP.keys())}"
    # Functions
    f"|{'|'.join(re.escape(k) for k in FUNCTION_MAP.keys())}"
    r')+$'
)


# FUNCTIONS #

def compact_expr(expr: str) -> str:
    """
    Removes any unnecessary characters from an expression, just as whitespace.

    Args:
        expr (str):
            The expression to process.

    Returns:
        str:
            The processed expression.
    """
    # Remove whitespace
    for char in WHITESPACE:
        expr = expr.replace(char, '')
    # Remove '=' at each end
    expr = expr.strip('=')
    # Temp semi-handle LaTeX
    expr = expr.strip('$')
    expr = expr.replace('{', '(').replace('}', ')')
    expr = expr.replace('\\', '')
    return expr


def eval_custom_functions(expr: str) -> str:
    """
    Evaluates custom functions in an expression.

    Args:
        expr (str): The expression to evaluate.

    Returns:
        str: The processed expression.
    """
    def func_replacer(match: re.Match) -> str:
        """
        Replaces a function call with its result.

        Args:
            match (re.Match):
                    The match object.

        Returns:
            str:
                The result of the function call or the original expression.
        """
        func_name: str = match.group(1).lstrip('(')
        arg_str: str = match.group(2)
        args_list: list = [arg.strip() for arg in arg_str.split(',')]
        logging_print(
            f"Function requested: '{func_name}', Arguments: {args_list}"
        )
        if matches_key(func_name, FUNCTION_MAP.keys()):
            group: str = FUNCTION_MAP[func_name][0]
            func: Callable = FUNCTION_MAP[func_name][1]
            if group == 'SYMPY':
                if (
                    func_name in ('log', '\\log')
                    and len(args_list) == 1
                    and args_list[0]
                ):
                    args_list.append('10')
                logging_print(
                    f"Matching SymPy function: `sympy.{func.__name__}`. "
                    "Letting SymPy handle evaluation."
                )
                result = f"{func.__name__}({','.join(args_list)})"
                return result
            else:
                args: list = []
                for arg in args_list:
                    if (
                        group == 'CUSTOM'
                        and func is roll_dice
                        and args_list.index(arg) == 0
                    ):
                        args.append(arg)
                    elif group == 'CUSTOM' and func is sym_quad_zero:
                        args.append(arg)
                    else:
                        args.append(float(arg))
                result = func(*args)
                if func is roll_dice:
                    result = result[0]
                logging_print(
                    f"Calling function: `{func.__module__}.{func.__name__}"
                    f"({', '.join(map(str, args))})`, Result: `{result}`"
                )
                if result is True:
                    return '1'
                elif result is False:
                    return '0'
                else:
                    return str(result)
        elif function_exists(func_name):
            logging_print(
                f"Function '{func_name}' not valid. "
                "Transforming to variable multiplication to ensure "
                "it's not treated as a function."
            )
            if len(args_list) == 1 and args_list[0] == '':
                return '*'.join(func_name)
            else:
                return match.group(0).replace(func_name, '*'.join(func_name))
        else:
            logging_print(
                f"Function '{func_name}' not found. "
                "Assuming it's not a function."
            )
            if len(args_list) == 1 and args_list[0] == '':
                return func_name
            else:
                return match.group(0)

    def const_replacer(match: re.Match) -> str:
        """
        Replaces a constant with its value.

        Args:
            match (re.Match):
                    The match object.

        Returns:
            str:
                The value of the constant.
        """
        const_name: str = match.group(0)
        logging_print(f"Constant requested: '{const_name}'")
        if matches_key(const_name, CONSTANTS_MAP.keys()):
            group: str = CONSTANTS_MAP[const_name][0]
            const: Callable = CONSTANTS_MAP[const_name][1]
            if group == 'SYMPY':
                logging_print(
                    f"Matching SymPy constant: `sympy.{const}`. "
                    "Letting SymPy handle evaluation."
                )
                return '(' + str(const) + ')'
            else:
                logging_print(
                    f"Matching constant: '{const_name}': "
                    f"`{CONSTANTS_MAP[const_name]}`"
                )
                return str(CONSTANTS_MAP[const_name])
        elif function_exists(const_name):
            logging_print(
                f"Constant '{const_name}' not valid. "
                "Transforming to variable multiplication to ensure "
                "it's not treated as a function."
            )
            result: str = '('
            result += match.group(0).replace(const_name, '*'.join(const_name))
            result += ')'
            return result
        else:
            logging_print(
                f"Constant '{const_name}' not found. "
                "Assuming it's not a constant."
            )
            return match.group(0)

    # Process the expression
    func_pattern: re.Pattern = re.compile(r'(\b\w+)\(([^)]*)\)')
    const_pattern: re.Pattern = re.compile(
        '|'.join(re.escape(k) for k in CONSTANTS_MAP.keys())
    )
    expr = func_pattern.sub(func_replacer, expr)
    expr = const_pattern.sub(const_replacer, expr)
    return expr


def evaluate_expression(
    expr: str,
    approximate: bool = True,
    dec_precision: int = 20,
    dec_display: int = 8
) -> str:
    """
    Evaluates an expression.

    Args:
        expr (str):
            The expression to evaluate.
        approximate (bool, optional):
            Whether to approximate the result to a decimal.
            Defaults to `True`.
        dec_precision (int, optional):
            The number of decimal places to use when evaluating.
            Defaults to `20`.
        dec_display (int, optional):
            The number of decimal places to display.
            Defaults to `8`.

    Returns:
        str:
            The result of the expression.
    """
    try:
        # Handle custom functions & constants
        expr_cust: str = eval_custom_functions(expr)
        logging_print(
            f"Expr (eval_func):{' ' * 4}`{expr_cust}`"
            f" - type: {type(expr_cust)}"
        )
        # Handle implied exponentation
        expr_exp: str = implied_exp(expr_cust)
        logging_print(
            f"Expr (implied_exp):{' ' * 2}`{expr_exp}`"
            f" - type: {type(expr_exp)}"
        )
        # Handle implied multiplication
        expr_mult: str = implied_mult(expr_exp)
        logging_print(
            f"Expr (implied_mult):{' ' * 1}`{expr_mult}`"
            f" - type: {type(expr_mult)}"
        )
        # Convert to SymPy object
        expr_sym: sp.Expr = sympify(expr_mult)
        logging_print(
            f"Expr (sympify):{' ' * 6}`{expr_sym}`"
            f" - type: {type(expr_sym)}"
        )
        # Simplify expression
        expr_simp: sp.Expr = simplify(expr_sym)
        logging_print(
            f"Expr (simplify):{' ' * 5}`{expr_simp}`"
            f" - type: {type(expr_simp)}"
        )
        if approximate:
            # Convert floats to rationals
            expr_rat: sp.Expr = nsimplify(expr_simp, rational=True)
            logging_print(
                f"Expr (rational):{' ' * 5}`{expr_rat}`"
                f" - type: {type(expr_rat)}"
            )
            # Approximate expression
            expr_appr: sp.Expr = expr_rat.evalf(dec_precision)
            logging_print(
                f"Expr (float):{' ' * 8}`{expr_appr}`"
                f" - type: {type(expr_appr)}"
            )
            expr_res: sp.Expr = expr_appr
        else:
            expr_res = expr_simp
        # Round all numbers
        expr_round: sp.Expr = simplify_floats(
            expr_res, dec_display, approximate
        )
        logging_print(
            f"Expr (clean_floats):{' ' * 1}`{expr_round}`"
            f" - type: {type(expr_round)}"
        )
        # Format expression
        expr_final: str = format_expression(expr_round)
        logging_print(
            f"Expr (formatted):{' ' * 4}`{expr_final}`"
            f" - type: {type(expr_final)}"
        )
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
        expr (str | sympy.Basic | sympy.Expr):
            The expression to format.

    Returns:
        str:
            The formatted expression.
    """
    # convert to string
    expr_str: str = str(expr)

    # replace exponent symbol ('**' → '^')
    # e.g. '2**3' → '2^3'
    expr_str = expr_str.replace('**', '^')

    # remove multiplication symbol ('*' → '')
    # Case 1: between a number and a variable
    # e.g. '2*x' → '2x'
    while re.search(r'(?<=\d)\*([a-zA-Z])', expr_str):
        expr_str = re.sub(r'(?<=\d)\*([a-zA-Z])', r'\1', expr_str)
    # Case 2: between a variable and opening parenthesis
    # e.g. 'x*(3)' → 'x(3)'
    while re.search(r'([a-zA-Z])\*\(', expr_str):
        expr_str = re.sub(r'([a-zA-Z])\*\(', r'\1\(', expr_str)
    # Case 3: between a closing parenthesis and a variable
    # e.g. '(3)*x' → '(3)x'
    while re.search(r'\)\*([a-zA-Z])', expr_str):
        expr_str = re.sub(r'\)\*([a-zA-Z])', r')\1', expr_str)
    # Case 4: between 2 variables
    # e.g. 'x*y' → 'xy'
    while re.search(r'([a-zA-Z])\*([a-zA-Z])', expr_str):
        expr_str = re.sub(r'([a-zA-Z])\*([a-zA-Z])', r'\1\2', expr_str)

    # replace symbols
    # Golden Ratio
    expr_str = expr_str.replace('GoldenRatio', CHAR_PHI)
    # Complex Infinity
    expr_str = expr_str.replace('zoo', CHAR_INFJ)
    expr_str = expr_str.replace('ComplexInfinity', CHAR_INFJ)
    # Infinity
    expr_str = expr_str.replace('oo', CHAR_INF)
    # Not a Number
    expr_str = expr_str.replace('nan', CHAR_NAN)
    # Pi
    expr_str = expr_str.replace('pi', CHAR_PI)
    # Imaginary Unit
    expr_str = expr_str.replace('I', CHAR_IMAG)
    # Euler's Number
    expr_str = expr_str.replace('E', CHAR_EUL)
    expr_str = expr_str.replace('exp(', CHAR_EUL + '^(')
    # Natural Logarithm
    expr_str = expr_str.replace('log(', 'ln(')

    return expr_str


def implied_exp(expression: str) -> str:
    """
    Evaluates whether an expression contains implied exponentation
    and adds explicit exponentation if necessary.

    Args:
        expression (str):
            The expression to evaluate.

    Returns:
        str:
            The processed expression.
    """
    return expression.replace('^', '**')


def implied_mult(expr: str) -> str:
    """
    Evaluates whether an expression contains implied multiplication
    and adds explicit multiplication if necessary.

    Args:
        expression (str):
            The expression to evaluate.

    Returns:
        str:
            The processed expression.
    """
    # Define patterns
    functions: str = '|'.join(re.escape(k) for k in FUNCTION_MAP.keys())
    pattern: str = (
        # Case 1: number followed by an opening parenthesis
        # e.g. '1(2)' → '1*(2)'
        r'(?<=\d)(?=\()'
        # Case 2: closing parenthesis followed by a number
        # e.g. '(3)4' → '(3)*4'
        r'|(?<=\))(?=\d)'
        # Case 3: two sets of parentheses
        # e.g. '(3)(4)' → '(3)*(4)'
        r'|(?<=\))(?=\()'
        # Case 4: number followed by a function
        # e.g. '2sqrt(9)' → '2*sqrt(9)'
        r'|(?<=\d)(?=(' + functions + r')\()'
        # Case 5: closing parenthesis followed by a function
        # e.g. '(2)sqrt(9)' → '(2)*sqrt(9)'
        r'|(?<=\))(?=(' + functions + r')\()'
        # Case 6: number followed by a variable
        # e.g. '2x' → '2*x'
        r'|(?<=\d)(?=[a-zA-Z])'
        # Case 7: closing parenthesis followed by a variable
        # e.g. '(2)x' → '(2)*x'
        r'|(?<=\))(?=[a-zA-Z])'
        # Case 8: variable followed by a number
        # e.g. 'x2' → 'x*2'
        r'|(?<=[a-zA-Z])(?=\d)'
        # Case 9: variable followed by an opening parenthesis
        # e.g. 'x(3)' → 'x*(3)'
        r'|(?<=[a-zA-Z])(?=\()'
        # Case 10: variable followed by another variable
        # e.g. 'xy' → 'x*y'
        r'|(?<=[a-zA-Z])(?=[a-zA-Z])'
    )

    # Add '*' in all matched cases
    expr_modified: str = re.sub(pattern, '*', expr)

    # Remove '*' inside of function and constant names
    # e.g. 's*q*r*t*(x)' → 'sqrt*(x)'
    sym_except_list: list = []
    for key in list(CONSTANTS_MAP.keys()) + list(FUNCTION_MAP.keys()):
        if len(key) > 1 and all(c.isalpha() for c in key):
            sym_except_list.append('*'.join(list(key)))
    symb_except: str = '|'.join(re.escape(k) for k in sym_except_list)
    expr_modified = re.sub(
        r'(' + symb_except + r')',
        lambda m: m.group(0).replace('*', ''),
        expr_modified
    )

    # Remove '*' between functions and '('
    # e.g. 'sqrt*(x)' → 'sqrt(x)'
    expr_modified = re.sub(r'(' + functions + r')\*\(', r'\1(', expr_modified)

    # Remove '*' between numbers and 'd' in the 'roll_dice()' function
    # e.g. 'roll(3*d*6)' → 'roll(3d6)'
    expr_modified = re.sub(
        r'(?<=roll\()(\d+)\*d\*(\d+)',
        r'\1d\2',
        expr_modified
    )

    return expr_modified


def sanitize_input(
    expr: str,
    allowed_chars: re.Pattern[str] = ALLOWED_CHARS,
    sanitize: bool = True
) -> str:
    """
    Sanitize an expression by removing invalid sequences of characters
    if possible, or raising an exception if not.

    Args:
        expression (str):
            The expression to sanitize.
        allowed_chars (str, optional):
            The allowed characters.
            Defaults to the global variable `ALLOWED_CHARS`.
        sanitize (bool, optional):
            Whether to sanitize the expression.
            Defaults to `True`.

    Returns:
        str:
            The sanitized expression.
    """
    # Remove unnecessary characters
    expr_comp: str = compact_expr(expr)
    logging_print(
        f"Expr (compacted):{' ' * 4}`{expr_comp}`"
        f" - type: {type(expr_comp)}"
    )
    if sanitize and expr_comp and not allowed_chars.match(expr_comp):
        raise ValueError('Invalid characters in expression')
    logging_print(
        f"Expr (sanitized):{' ' * 4}`{expr_comp}`"
        f" - type: {type(expr_comp)}"
    )
    return expr_comp


def simplify_floats(expr: sp.Expr, ndec: int, approx: bool) -> sp.Expr:
    """
    Simplifies floating-point numbers in an expression by rounding,
    then truncating any trailing zeros and the decimal point if applicable.

    Args:
        expr (sympy.Expr):
            The expression to simplify.
        ndec (int):
            The number of decimal places to round to.
        approx (bool):
            Whether to approximate the result to a decimal.

    Returns:
        sympy.Expr: The simplified expression.
    """
    def round_float(term: sp.Basic, ndec: int, approx: bool) -> sp.Basic:
        """
        Rounds a floating-point number to the given number of decimal places,
        then truncates any insignificant decimal places.

        Args:
            term (sympy.Basic):
                The term to round.
            ndec (int):
                The number of decimal places to round to.
            approx (bool):
                Whether to approximate the result to a decimal.

        Returns:
            sympy.Basic: The rounded and truncated term.
        """
        if term.is_number:
            try:
                if approx:
                    # Round to the specified number of decimal places
                    rounded_term: sp.Basic = S(round(term, ndec))
                else:
                    # If not using approximation, leave the term unchanged
                    rounded_term = term
            except Exception:
                # If rounding fails, leave the term unchanged
                rounded_term = term
            # Truncate remaining insignificant decimal places
            try:
                # Number of significant decimal places (after rounding)
                sig_ndec: int = len(
                    str(rounded_term).split('.')[1].rstrip('0')
                )
                if sig_ndec == 0:
                    # No significant decimal places
                    # Return integer
                    return S(int(rounded_term))
                else:
                    # Has significant decimal places
                    # Return float truncated to significant decimal places
                    return S(round(rounded_term, sig_ndec))
            except Exception:
                # If truncating fails, return the term unchanged
                return rounded_term
        # If the term is not a number, return the term unchanged
        return term
    rounded_expr: sp.Expr = expr.xreplace(
        {term: round_float(term, ndec, approx) for term in expr.atoms()}
    )
    return rounded_expr


# TESTING #

def _test():
    pass


if __name__ == '__main__':
    _test()
