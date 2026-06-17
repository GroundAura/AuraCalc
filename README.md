# AuraCalc

A text-based calculator app written in Python.

## Requirements

- [Python](https://www.python.org) 3.12.2 or newer
- [CustomTkinter](https://customtkinter.tomschimansky.com)
- [SymPy](https://www.sympy.org/en/index.html)

## Installation
- Install [Python](https://www.python.org/downloads/)

- Install Required Packages

Option A:
```sh
pip install -r scripts/requirements.txt
```

Option B:
```sh
pip install customtkinter sympy
```

- Download calculator source code

## Launch Instructions

- Follow Installation instructions above
- Open a terminal or IDE and navigate to the downloaded source code
- Run `main.py`
```sh
python src/main.py
```

## Features

Basic Arithmetic Operators:
- Addition `+`
- Subtraction `-`
- Multiplication `*`
- Division `/`
- Floor Division `//`
- Modulo `%`
- Exponentiation `**` or `^`

Intuitive, Flexible Formatting:
- eg: `2 + 3`, `2+3`, `2+ 3`, `2 +3`, `2--3`, `2 - -3` evaluates to `5`
- eg: `3**2`, `3^2` evaluates to `9`
- eg: `3*2`, `2*3`, `(2)(3)`, `2(3)` evaluates to `6`

Variable Arithmetic:
- eg: `x + x` evaluates to `2x`

Common Math Functions:
- eg: `sqrt(9)` evaluates to `3`
- eg: `cbrt(27)` evaluates to `3`
- eg: `abs(-3)` evaluates to `3`
- eg: `log(10)` evaluates to `1`
- eg: `ln(e)` evaluates to `1`
- eg: `log(3,3)` evaluates to `1`

Constants:
- eg: `pi` evaluates to `3.1415926536`
- eg: `e` evaluates to `2.7182818285`
- eg: `i^2` evaluates to `-1`

Approximate Mode:
- exact or decimal approximation
- ex. with approximate off `3/9` evaluates to `1/3`
- ex. with approximate on `3/9` evaluates to `0.3333333333`
- toggleable with `Approximate` checkbox in Expanded view
- also toggleable with `F4` key

Stay On Top Window:
- pins the window to stay in front of all other windows
- toggleable with `Pin`/`Unpin` button

Session History:
- save an expression with `Return` (`Enter`) key
- navigate saved expressions with `Up`/`Down` arrow keys
- clear history with `Clear` button
- also clear history with `Alt`+`Backspace` key combo

## Notes

- If you enter an invalid expression, the output will show a custom message such as `ERROR: Invalid characters in expression` or `ERROR: Incomplete expression`. This is intended to provide user feedback and not an issue with the program.
- The program is dependant on the `icon.ico` file to run.
- Includes config and log files.

