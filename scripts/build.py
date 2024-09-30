### IMPORTS ###

# builtins
from pathlib import Path
import os
import shutil
from subprocess import run, CalledProcessError
#import sys

# external
#from auralib import copy_file, delete_file, is_file, run_command

# internal



### GLOBAL VARIABLES ###
ROOT_PATH: Path = Path().resolve()
RELATIVE_PATH: Path = Path(__file__).parent.resolve()



### FUNCTIONS ###

def copy_file(source_path: str, destination_path: str, force_metadata: bool = False, force_overwrite: bool = False) -> None:
	"""
	Copies a file from source_path to destination_path.

	Args:
		source_path (str): The file path to copy from.
		destination_path (str): The file path to copy to.
		force_metadata (bool, optional): Whether to force copying metadata from the source file. Defaults to False.
		force_overwrite (bool, optional): Whether to force overwriting the destination file. Defaults to False. Warning: If force_metadata is also True, this will delete the destination file before copying, even if copying fails.
	"""
	try:
		if is_file(source_path):
			if not force_metadata:
				if not force_overwrite:
					shutil.copy(source_path, destination_path)
				else:
					shutil.copy(source_path, destination_path, copy=True)
			else:
				try:
					shutil.copy2(source_path, destination_path)
				except FileExistsError:
					if not force_overwrite:
						print(f"WARNING: '{source_path}' already exists at '{destination_path}'. Skipped copying file. Set the argument 'force_overwrite' to 'True' to force overwrite.")
					else:
						delete_file(destination_path)
						shutil.copy2(source_path, destination_path)
		else:
			raise FileNotFoundError(f"'{source_path}' does not exist or is not a file.")
	except Exception as e:
		print(f"ERROR: Error while trying to copy file '{source_path}' to '{destination_path}': {e}")

def delete_file(file_path: str) -> None:
	"""
	Deletes a file.

	Args:
		file_path (str): The file path to delete.
	"""
	try:
		os.remove(file_path)
	except Exception as e:
		print(f"ERROR: Error while trying to delete file '{file_path}': {e}")

def is_file(file_path: str) -> bool:
	"""
	Checks if the specified file path is an existing file.

	Args:
		file_path (str): The file path to check.

	Returns:
		bool: True if the file path is a file, False otherwise.
	"""
	try:
		return os.path.isfile(file_path)
	except Exception as e:
		print(f"ERROR: Error while trying to check if '{file_path}' is a file: {e}")

def run_command(command: str | list[str], print_output: bool = False, use_shell: bool = False) -> None:
	try:
		if not print_output and not use_shell:
			run(command, check=True)
		elif not print_output and use_shell:
			run(command, check=True, shell=True)
		elif print_output and not use_shell:
			output = run(command, check=True, capture_output=True, text=True)
			print(f"INFO: Command output:\n```\n{output.stdout}```")
		elif print_output and use_shell:
			output = run(command, check=True, shell=True, capture_output=True, text=True)
			print(f"INFO: Command output:\n```\n{output.stdout}```")
		print(f"INFO: Finished running command: '{command}'")
	except CalledProcessError as e:
		print(f"ERROR: Error running command:\n```\n{e}\n```")
	except Exception as e:
		print(f"ERROR: Error running command '{command}':\"\n{e}\n\"")

def true_path(relative_path: str) -> str:
	"""
	Converts a relative path to an absolute path.

	Args:
		relative_path (str): The relative path to convert.

	Returns:
		str: The absolute path.
	"""
	#return os.path.abspath(os.path.join(os.getcwd(), relative_path))
	true_path: Path = ROOT_PATH / relative_path
	return str(true_path)



### MAIN ###

def main():
	print(f"INFO: root_path: '{ROOT_PATH}'")
	print(f"INFO: relative_path: '{RELATIVE_PATH}'")
	paths = {
		'icon.ico': true_path("resources/icon.ico"),
		'AuraCalc.ini': true_path("resources/AuraCalc.ini"),
		'history.json': true_path("resources/history.json"),
		'LICENSE.txt': true_path("LICENSE.txt"),
		'README.md': true_path("README.md"),
		'main.py': true_path("src/main.py"),
		'app_config.py': true_path("src/app_config.py"),
		'app_evaluate.py': true_path("src/app_evaluate.py"),
		'app_globals.py': true_path("src/app_globals.py"),
		'app_history.py': true_path("src/app_history.py"),
		'app_path.py': true_path("src/app_path.py"),
		'app_random.py': true_path("src/app_random.py"),
		'app_window.py': true_path("src/app_window.py"),
		'dist': Path("dist")
	}

	# Build to EXE
	cmd_pyinstaller = [
		'pyinstaller',
		'--onefile',
		'--windowed',
		'--name AuraCalc',
		'--icon=' + paths['icon.ico'],
		'--add-data \"' + paths['icon.ico'] + ';resources\"',
		'--add-data \"' + paths['AuraCalc.ini'] + ';resources\"',
		'--add-data \"' + paths['history.json'] + ';resources\"',
		'--add-data \"' + paths['LICENSE.txt'] + ';resources\"',
		'--add-data \"' + paths['README.md'] + ';resources\"',
		'--add-data \"' + paths['app_config.py'] + ';.\"',
		'--add-data \"' + paths['app_evaluate.py'] + ';.\"',
		'--add-data \"' + paths['app_globals.py'] + ';.\"',
		'--add-data \"' + paths['app_history.py'] + ';.\"',
		'--add-data \"' + paths['app_path.py'] + ';.\"',
		'--add-data \"' + paths['app_random.py'] + ';.\"',
		'--add-data \"' + paths['app_window.py'] + ';.\"',
		paths['main.py']
	]
	run_command(cmd_pyinstaller, print_output=True, use_shell=True)

	# Copy resources
	copy_file(paths['AuraCalc.ini'], true_path('dist/AuraCalc/resources/AuraCalc.ini'))
	copy_file(paths['history.json'], true_path('dist/AuraCalc/resources/history.json'))
	copy_file(paths['icon.ico'], true_path('dist/AuraCalc/resources/icon.ico'))
	copy_file(paths['LICENSE.txt'], true_path('dist/AuraCalc/resources/LICENSE.txt'))
	copy_file(paths['README.md'], true_path('dist/AuraCalc/resources/README.md'))

if __name__ == "__main__":
	main()


