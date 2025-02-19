### IMPORTS ###

# builtins
from pathlib import Path
import sys

# external

# internal
#import app_globals



### FUNCTIONS ###

def resource_path(relative_path: str | Path) -> Path:
	"""
	Get absolute path to resource, works for both development and PyInstaller-built EXE.
	"""
	try:
		# PyInstaller creates a temporary folder and stores the path in _MEIPASS
		base_path = Path(sys.MEIPASS)
	except AttributeError:
		base_path = Path.cwd()
	return base_path / relative_path



### MAIN ###

if __name__ == '__main__':
	pass


