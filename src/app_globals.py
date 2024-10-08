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

# Metadata
NAME: str = "AuraCalc"
VERSION: str = "0.3.0-alpha"
AUTHOR: str = "GroundAura"



# Files
HISTORY_FILE: Path = resource_path("resources/history.json")
#print(f"HISTORY FILE: {HISTORY_FILE}")
ICON_FILE: Path = resource_path("resources/icon.ico")
#print(f"ICON FILE: {ICON_FILE}")
LOG_FILE: Path = resource_path("resources/debug.log")
#print(f"LOG FILE: {LOG_FILE}")
SETTINGS_FILE: Path = resource_path("resources/AuraCalc.ini")
#print(f"SETTINGS FILE: {SETTINGS_FILE}")



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

DEF_CENTERED: bool = settings["WIN_POS"]["bCenterWindow"]
DEF_X_POS: int = settings["WIN_POS"]["iXOffset"]
DEF_Y_POS: int = settings["WIN_POS"]["iYOffset"]

START_ADVANCED: bool = settings["WIN_FLAGS"]["bStartAdvanced"]
START_PINNED: bool = settings["WIN_FLAGS"]["bStartPinned"]

#RESTORE_MODE: bool = settings["WIN_RESTORE"]["bRestoreMode"]
#RESTORE_DIMENSIONS: bool = settings["WIN_RESTORE"]["bRestoreDimensions"]
#RESTORE_POSITION: bool = settings["WIN_RESTORE"]["bRestorePosition"]
#RESTORE_PINNED: bool = settings["WIN_RESTORE"]["bRestorePinned"]
#RESTORE_ADVANCED: bool = settings["WIN_RESTORE"]["bRestoreAdvanced"]

DEC_PRECISION: int = settings["CALCULATION"]["iDecimalPrecision"]
DEC_DISPLAY: int = settings["CALCULATION"]["iDecimalDisplay"]
if DEC_DISPLAY > DEC_PRECISION:
	DEC_DISPLAY = DEC_PRECISION
ONLY_SIMPLIFY: bool = settings["CALCULATION"]["bOnlySimplify"]
LIVE_EVAL: bool = settings["CALCULATION"]["bLiveEval"]
TIMEOUT_DURATION: int = settings["CALCULATION"]["iTimeoutDelay"]

ADVANCED_KEY: str = settings["KEYBINDS"]["sAdvancedKey"]
CLEAR_KEY: str = settings["KEYBINDS"]["sClearKey"]
DELETE_LEFT_KEY: str = settings["KEYBINDS"]["sDeleteAllLKey"]
DELETE_RIGHT_KEY: str = settings["KEYBINDS"]["sDeleteAllRKey"]
#DELETE_TERM_LEFT_KEY: str = settings["KEYBINDS"]["sDeleteTermLKey"]
#DELETE_TERM_RIGHT_KEY: str = settings["KEYBINDS"]["sDeleteTermRKey"]
EVALUATE_KEY: str = settings["KEYBINDS"]["sEvaluateKey"]
#HELP_KEY: str = settings["KEYBINDS"]["sHelpKey"]
#OPTIONS_KEY: str = settings["KEYBINDS"]["sOptionsKey"]
#REDO_KEY: str = settings["KEYBINDS"]["sRedoKey"]
#UNDO_KEY: str = settings["KEYBINDS"]["sUndoKey"]
QUIT_KEY: str = settings["KEYBINDS"]["sQuitKey"]

DEBUG: bool = settings["DEBUG"]["bDebugMode"]
FORCE_FOCUS: bool = settings["DEBUG"]["bForceFocus"]
SANITIZE: bool = settings["DEBUG"]["bSanitizeInput"]

DEF_EXPRESSION: str = ""
DEF_RESULT: str = "0"

if DEBUG:
	print(f"Settings: {settings}")



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
TIMEOUT_ID: any = None



# Timeout
PATIENCE: int = 1
#WAIT_CHARS: list[str] = ['+','-','*','/','^','(',' ']
WAIT_CHARS: str = r'+-*/^%.([{_, '


