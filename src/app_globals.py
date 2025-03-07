### IMPORTS ###

# internal
from app_config import read_config, get_config_value
from app_path import get_full_path



### CONSTANTS ###

# Metadata
META_NAME: str = 'AuraCalc'
META_VERSION: str = '0.7.0-alpha'
META_AUTHOR: str = 'GroundAura'

# Paths
DIR_RESOURCES: str = 'resources'
FILE_CONFIG: str = f"{META_NAME}.ini"
FILE_HISTORY: str = 'history.json'
FILE_ICON: str = 'icon.ico'
FILE_LOG: str = 'debug.log'

# Config
FORCE_DEBUG: bool = False
USE_CONFIG: bool = True



### VARIABLES ###

# Paths
PATH_LOG = get_full_path(DIR_RESOURCES, FILE_LOG)
PATH_CONFIG = get_full_path(DIR_RESOURCES, FILE_CONFIG)

# Config
if FORCE_DEBUG:
	DEBUG_MODE: bool = True
else:
	DEBUG_MODE = False

if USE_CONFIG:
	CONFIG: dict | None = read_config(str(PATH_CONFIG), preserve_key_case=True)
	DEBUG_MODE = get_config_value(CONFIG, 'DEBUG', 'bDebugMode', False)
else:
	CONFIG = None
