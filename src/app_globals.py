### IMPORTS ###

# builtins
#from decimal import getcontext
from pathlib import Path
#import re

# external

# internal
from app_config import read_config
from app_path import resource_path



### GLOBAL VARIABLES ###

# Files
HISTORY_FILE: Path = resource_path("resources/history.json")
#print(HISTORY_FILE)
ICON_FILE: Path = resource_path("resources/icon.ico")
#print(ICON_FILE)
SETTINGS_FILE: Path = resource_path("resources/AuraCalc.ini")
#print(SETTINGS_FILE)


# Settings
settings: dict[str, dict[str, any]] = read_config(SETTINGS_FILE)

START_HEIGHT: int = settings["WINDOW_DIMENSIONS"]["iDefaultHeight"]
START_WIDTH: int = settings["WINDOW_DIMENSIONS"]["iDefaultWidth"]
MIN_HEIGHT: int = settings["WINDOW_DIMENSIONS"]["iMinHeight"]
MIN_WIDTH: int = settings["WINDOW_DIMENSIONS"]["iMinWidth"]

if settings["WINDOW_POSITION"]["sDefaultPosition"] == "center":
	START_POS: str = "center"
else:
	START_POS: tuple[int, int] = tuple(settings["WINDOW_POSITION"]["iXOffset"], settings["WINDOW_POSITION"]["iYOffset"])

#FORCE_FOCUS: bool = True
START_EXPANDED: bool = settings["WINDOW_FLAGS"]["bStartExpanded"]
START_PINNED: bool = settings["WINDOW_FLAGS"]["bStartPinned"]

DEC_PRECISION: int = settings["CALCULATION"]["iDecimalPrecision"]
DEC_DISPLAY: int = settings["CALCULATION"]["iDecimalDisplay"]
if DEC_DISPLAY > DEC_PRECISION:
	DEC_DISPLAY = DEC_PRECISION
ONLY_SIMPLIFY: bool = settings["CALCULATION"]["bOnlySimplify"]

DEBUG: bool = settings["DEBUG"]["bDebugMode"]
SANITIZE: bool = settings["DEBUG"]["bSanitizeInput"]

DEF_EXPRESSION: str = ""
DEF_RESULT: str = "0"


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



# Saved data
LAST_EXPRESSION: str = DEF_EXPRESSION
LAST_RESULT: str = DEF_RESULT
#HISTORY: list[tuple[str, str]] = []
HISTORY: dict[str, any] = {
	"expression_history": [],
	"result_history": [],
	"pinned_state": False,
	"expanded_state": False,
	"dimensions": (CUR_WIDTH, CUR_HEIGHT),
	"position": CUR_POS
}


# Timeout
TIMEOUT_DURATION: int = 1000
TIMEOUT_ID: any = None
#WAIT_CHARS: list[str] = ['+','-','*','/','^','(',' ']
WAIT_CHARS: str = r'+-*/^%.([{_, '


