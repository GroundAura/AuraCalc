### IMPORTS ###

# builtins
#from decimal import getcontext
from pathlib import Path
#import re

# external

# internal
#from app_config import read_config
from app_path import resource_path



### GLOBAL VARIABLES ###

# Files
HISTORY_FILE: Path = resource_path("resources/history.json")
#print(HISTORY_FILE)
ICON_FILE: Path = resource_path("resources/icon.ico")
#print(ICON_FILE)
SETTINGS_FILE: Path = resource_path("resources/AuraCalc.ini")
#print(SETTINGS_FILE)


# Window Size and Position
WIDTH: int = 250
HEIGHT: int = 110
X_POS: int = 100
Y_POS: int = 100


# Window State
CUR_WIDTH: int = 250
CUR_HEIGHT: int = 110
CUR_POS: tuple[int, int] = (100, 100)
EXPANDED: bool = False
PINNED: bool = False


# Settings
DEF_HEIGHT: int = 110
DEF_WIDTH: int = 250
DEF_POS: tuple[int, int] | str = "center"
#DEF_POS: tuple[int, int] | str = (100, 100)
MIN_WIDTH: int = DEF_WIDTH
MIN_HEIGHT: int = DEF_HEIGHT

DEF_EXPRESSION: str = ""
DEF_RESULT: str = "0"

#FORCE_FOCUS: bool = True
DEF_EXPANDED: bool = False
DEF_PINNED: bool = True

DEC_PRECISION: int = 100
DEC_DISPLAY: int = 20
if DEC_DISPLAY > DEC_PRECISION:
	DEC_DISPLAY = DEC_PRECISION
ONLY_SIMPLIFY: bool = True
SANITIZE: bool = False


# Saved data
LAST_EXPRESSION: str = DEF_EXPRESSION
LAST_RESULT: str = DEF_RESULT
#HISTORY: list[tuple[str, str]] = []
HISTORY: dict[str, any] = {
	"expression_history": [],
	"result_history": [],
	"pinned_state": False,
	"expanded_state": False
}


# Timeout
TIMEOUT_DURATION: int = 1000
TIMEOUT_ID: any = None
#WAIT_CHARS: list[str] = ['+','-','*','/','^','(',' ']
WAIT_CHARS: str = r'+-*/^%.([{_, '


