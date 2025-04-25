# IMPORTS #

# builtins
import random

# external
from sympy import sympify
import sympy as sp

# internal
from app_logging import logging_print


# CONSTANTS #

TAU = sp.pi * 2

CHAR_EUL = 'e'
CHAR_IMAG = 'i'
CHAR_INF = chr(0x221E)  # '∞'
CHAR_INFJ = 'ComplexInfinity'
CHAR_NAN = 'NaN'
CHAR_PHI = chr(0x03C6)  # 'φ'
CHAR_PI = chr(0x03C0)  # 'π'
CHAR_TAU = chr(0x03C4)  # 'τ'


# FUNCTIONS #

def roll_dice(dice_string: str) -> tuple[int, list[int]]:
    """
    Generates a random number based on a given dice string.

    Args:
        dice_string (str):
            What dice to roll in the format `XdY` (e.g. `roll_dice('3d6'`).

    Returns:
        tuple ((int, list[int])):
            The total result of the roll and a list of individual roll results.
    """
    try:
        num_dice, num_sides = map(int, dice_string.lower().split('d'))
        rolls: list[int] = (
            [random.randint(1, num_sides) for _ in range(num_dice)]
        )
        total: int = sum(rolls)
        logging_print(
            f"Rolling '{dice_string}'... Total: `{total}`,  Rolls: `{rolls}`"
        )
        return total, rolls
    except ValueError:
        raise ValueError(
            "Invalid dice notation. Use 'XdY' format, e.g., '3d6'."
        )


def sym_quad_zero(a: str, b: str, c: str, positive: str = '+') -> str:
    """
    Returns a symbolic expression (for SymPy)
    for one of the zeros of a quadratic equation.

    Args:
        a (str):
            Coefficient of x^2.
        b (str):
            Coefficient of x.
        c (str):
            Constant term.
        positive (str, optional):
            Whether to return the positive or negative root.
            Defaults to `'+'` (positive).
            Valid options: `'True'`, `'+'`, `'p'`, `'pos'`, `'positive'`
            OR `'False'`, `'-'`, `'n'`, `'neg'`, `'negative'`.

    Returns:
        str: Symbolic expression for the zero of the quadratic equation.
    """
    if positive in ['True', '+', 'p', 'pos', 'positive']:
        return f"(-({b}) + sqrt(({b})**2 - 4 * {a} * {c})) / (2 * {a})"
    elif positive in ['False', '-', 'n', 'neg', 'negative']:
        return f"(-({b}) - sqrt(({b})**2 - 4 * {a} * {c})) / (2 * {a})"
    else:
        raise ValueError(
            "Invalid positive argument. "
            "Use 'p' for positive, 'n' for negative."
        )


# TESTING #

def _test():

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
