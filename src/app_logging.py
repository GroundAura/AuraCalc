### IMPORTS ###

# builtins
from datetime import datetime
from pathlib import Path

# internal
#from app_path import get_full_path
from app_globals import DEBUG_MODE, PATH_LOG



### CONSTANTS ###

#PATH_LOG: Path = get_full_path(DIR_RESOURCES, FILE_LOG)



### FUNCTIONS ###

def logging_print(message: object = '', indent: int = 0, timestamp: bool = True, print_to_console: bool = True, print_to_file: bool = True, debug_mode_only: bool = True, log_path: Path = PATH_LOG, debug_mode: bool = DEBUG_MODE) -> None:
	"""
	Displays a debug message in the console and in the debug log file.

	Args:
		message (object): The message to display. Defaults to `''`.
		indent (int, optional): The indentation level, in spaces. Defaults to `0`.
		timestamp (bool, optional): Whether to include a timestamp. Defaults to `True`.
		print_to_console (bool, optional): Whether to print the message to the console. Defaults to `True`.
		print_to_file (bool, optional): Whether to print the message to the debug log file. Defaults to `True`.
		debug_mode_only (bool, optional): Whether to only print the message in debug mode. Defaults to `True`.
		log_path (Path, optional): The path to the debug log file. Defaults to `PATH_LOG`.
		debug_mode (bool, optional): Whether debug mode is enabled. Defaults to `DEBUG_MODE`.
	"""
	message = str(message)
	if debug_mode or not debug_mode_only:
		#message = str(message)
		if timestamp or indent > 0:
			if '\n' in message:
				lines = message.split('\n')
				for line in lines:
					logging_print(line, indent=indent, timestamp=timestamp, print_to_console=print_to_console, print_to_file=print_to_file, debug_mode_only=debug_mode_only)
				return
		if indent > 0:
			#message = ' ' * indent + message
			message = f"{' ' * indent}{message}"
		if timestamp:
			message = f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S:%f')}] {message}"
		if print_to_console:
			print(message)
		if print_to_file:
			with open(log_path, 'a') as log_file:
				#print(message, file=log_file)
				log_file.write(f"{message}\n")



### TESTING ###

def _test():
	pass

if __name__ == '__main__':
	_test()


