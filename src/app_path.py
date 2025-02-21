### IMPORTS ###

# builtins
from pathlib import Path
import sys

# internal
from app_type import validate_type



### FUNCTIONS ###

def get_full_path(dir_name: str, file_name: str, root_path: Path | None = None) -> Path:
	if root_path is None:
		root_path = get_root_path()
	validate_type(root_path, Path)
	validate_type(file_name, str)
	if dir_name:
		validate_type(dir_name, str)
		return root_path / dir_name / file_name
	else:
		return root_path / file_name

def get_root_path() -> Path:
	try:
		# PyInstaller creates a temporary folder and stores the path in _MEIPASS
		root_path = Path(sys.MEIPASS)
		#return Path(sys.executable).parent
	except AttributeError:
		root_path = Path.cwd()
	validate_type(root_path, Path)
	return root_path



### TESTING ###

def _test():
	pass

if __name__ == '__main__':
	_test()


