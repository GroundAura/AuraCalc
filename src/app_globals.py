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
settings: dict[str, dict[str, any]] = read_config(SETTINGS_FILE, preserve_key_case=True)

BASE_MIN_HEIGHT: int = settings["WIN_BASIC"]["iMinHeight"]
BASE_MIN_WIDTH: int = settings["WIN_BASIC"]["iMinWidth"]
BASE_DEF_HEIGHT: int = settings["WIN_BASIC"]["iDefaultHeight"]
BASE_DEF_WIDTH: int = settings["WIN_BASIC"]["iDefaultWidth"]

ADV_DEF_HEIGHT: int = settings["WIN_ADV"]["iDefaultHeight"]
ADV_DEF_WIDTH: int = settings["WIN_ADV"]["iDefaultWidth"]
ADV_MIN_HEIGHT: int = settings["WIN_ADV"]["iMinHeight"]
ADV_MIN_WIDTH: int = settings["WIN_ADV"]["iMinWidth"]

#if settings["WIN_POS"]["bCenterWindow"] == True:
	#START_POS: str = "center"
#else:
	#START_POS: tuple[int, int] = tuple(settings["WIN_POS"]["iXOffset"], settings["WIN_POS"]["iYOffset"])
DEF_CENTERED: bool = settings["WIN_POS"]["bCenterWindow"]
DEF_X_POS: int = settings["WIN_POS"]["iXOffset"]
DEF_Y_POS: int = settings["WIN_POS"]["iYOffset"]

#FORCE_FOCUS: bool = True
START_EXPANDED: bool = settings["WIN_FLAGS"]["bStartExpanded"]
START_PINNED: bool = settings["WIN_FLAGS"]["bStartPinned"]

DEC_PRECISION: int = settings["CALCULATION"]["iDecimalPrecision"]
DEC_DISPLAY: int = settings["CALCULATION"]["iDecimalDisplay"]
if DEC_DISPLAY > DEC_PRECISION:
	DEC_DISPLAY = DEC_PRECISION
ONLY_SIMPLIFY: bool = settings["CALCULATION"]["bOnlySimplify"]
LIVE_EVAL: bool = settings["CALCULATION"]["bLiveEval"]

DEBUG: bool = settings["DEBUG"]["bDebugMode"]
SANITIZE: bool = settings["DEBUG"]["bSanitizeInput"]

DEF_EXPRESSION: str = ""
DEF_RESULT: str = "0"

if DEBUG:
	print(f"Settings: {settings}")


# Window Size and Position
WIDTH: int = 250
HEIGHT: int = 110
X_POS: int = 100
Y_POS: int = 100




# Window State
CUR_WIDTH: int | None = None
CUR_HEIGHT: int | None = None
CUR_X_POS: int | None = None
CUR_Y_POS: int | None = None
#CUR_POS: tuple[int, int] = (CUR_XOffset, CUR_YOffset)
EXPANDED: bool = False
PINNED: bool = False
RESIZE_WIDTH: bool = True
RESIZE_HEIGHT: bool = False
SCREEN_WIDTH: int | None = None
SCREEN_HEIGHT: int | None = None



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
	"position": (CUR_X_POS, CUR_Y_POS)
}


# Timeout
PATIENCE: int = 1
TIMEOUT_DURATION: int = 1000
TIMEOUT_ID: any = None
#WAIT_CHARS: list[str] = ['+','-','*','/','^','(',' ']
WAIT_CHARS: str = r'+-*/^%.([{_, '


