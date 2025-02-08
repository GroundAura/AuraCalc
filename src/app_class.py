### IMPORTS ###

# builtins

# external
import customtkinter as ctk
from pathlib import Path
import sys

# internal
from app_config import read_config



### CLASSES ###

class App:
	# constructor
	def __init__(self,
			name: str = "App",
			version: str = "1.0.0",
			author: str = "Unknown",
			resources_dir: str = "resources",
			icon_file: str = "icon.ico",
			log_file: str = "debug.log",
			config_file: str = "config.ini",
			use_config: bool = False
		) -> None:

		# metadata
		self._set_name(name)
		self._set_version(version)
		self._set_author(author)

		# paths
		self._set_root_path()
		self._set_resources_path(resources_dir)
		self._set_resource_icon_path(icon_file)
		self._set_resource_log_path(log_file)
		#self._set_resource_settings_path(config_file)

		# config
		self._set_config(config_file, use_config)
		#self._read_config(use_config)
		#try:
		#	self._read_config()
		#	self._config_exists = True
		#except FileNotFoundError:
		#	#self._config = None
		#	self._config_exists = False


	# private methods
	#def _read_config(self, use_config: bool = True) -> None:
	#	if use_config:
	#		if not isinstance(self._config_file, Path):
	#			raise TypeError(f"Expected type `pathlib.Path` for class `{self.__class__.__name__}` private attribute `_config_file`, got `{type(self._config_file).__name__}`")
	#		if not self._config_file.exists():
	#			raise FileNotFoundError(f"File `{self._config_file}` does not exist")
	#		self._config = read_config(self._config_file, preserve_key_case=True)
	#	else:
	#		self._config = None

	def _set_author(self, author: str) -> None:
		if not isinstance(author, str):
			raise TypeError(f"Expected type `str` for class `{self.__class__.__name__}` constructor argument `author`, got `{type(author).__name__}`")
		self._author = author

	def _set_config(self, file_name: str, use_config: bool = True) -> None:
		if use_config:
			if not isinstance(self._resources_path, Path):
				raise TypeError(f"Expected type `pathlib.Path` for private attribute `_resources_path`, got `{type(self._resources_path).__name__}`")
			if not isinstance(file_name, str):
				raise TypeError(f"Expected type `str` for class `{self.__class__.__name__}` constructor argument `config_file`, got `{type(file_name).__name__}`")
			self._config_file = self._resources_path / file_name
			if not isinstance(self._config_file, Path):
				raise TypeError(f"Expected type `pathlib.Path` for class `{self.__class__.__name__}` private attribute `_config_file`, got `{type(self._config_file).__name__}`")
			if not self._config_file.exists():
				raise FileNotFoundError(f"File `{self._config_file}` does not exist")
			self._config = read_config(self._config_file, preserve_key_case=True)
		else:
			self._config_file = None
			self._config = None

	def _set_name(self, name: str) -> None:
		if not isinstance(name, str):
			raise TypeError(f"Expected type `str` for class `{self.__class__.__name__}` constructor argument `name`, got `{type(name).__name__}`")
		self._name = name

	def _set_resource_icon_path(self, icon_file: str) -> None:
		if not isinstance(self._resources_path, Path):
			raise TypeError(f"Expected type `pathlib.Path` for private attribute `_resources_path`, got `{type(self._resources_path).__name__}`")
		if not isinstance(icon_file, str):
			raise TypeError(f"Expected type `str` for class `{self.__class__.__name__}` constructor argument `icon_file`, got `{type(icon_file).__name__}`")
		self._icon_file = self._resources_path / icon_file

	def _set_resource_log_path(self, log_file: str) -> None:
		if not isinstance(self._resources_path, Path):
			raise TypeError(f"Expected type `pathlib.Path` for private attribute `_resources_path`, got `{type(self._resources_path).__name__}`")
		if not isinstance(log_file, str):
			raise TypeError(f"Expected type `str` for class `{self.__class__.__name__}` constructor argument `log_file`, got `{type(log_file).__name__}`")
		self._log_file = self._resources_path / log_file

	#def _set_resource_settings_path(self, config_file: str) -> None:
	#	if not isinstance(self._resources_path, Path):
	#		raise TypeError(f"Expected type `pathlib.Path` for private attribute `_resources_path`, got `{type(self._resources_path).__name__}`")
	#	if not isinstance(config_file, str):
	#		raise TypeError(f"Expected type `str` for class `{self.__class__.__name__}` constructor argument `config_file`, got `{type(config_file).__name__}`")
	#	self._config_file = self._resources_path / config_file

	def _set_resources_path(self, resources_dir: str) -> None:
		if not isinstance(self._root_path, Path):
			raise TypeError(f"Expected type `pathlib.Path` for private attribute `_root_path`, got `{type(self._root_path).__name__}`")
		if not isinstance(resources_dir, str):
			raise TypeError(f"Expected type `str` for class `{self.__class__.__name__}` constructor argument `resources_dir`, got `{type(resources_dir).__name__}`")
		self._resources_path = self._root_path / resources_dir

	def _set_root_path(self) -> Path:
		try:
			# PyInstaller creates a temporary folder and stores the path in _MEIPASS
			root_path = Path(sys.MEIPASS)
			#return Path(sys.executable).parent
		except AttributeError:
			root_path = Path.cwd()
		if not isinstance(root_path, Path):
			raise TypeError(f"Expected type `pathlib.Path` for class `{self.__class__.__name__}` private attribute `_root_path`, got `{type(root_path).__name__}`")
		self._root_path = root_path

	def _set_version(self, version: str) -> None:
		if not isinstance(version, str):
			raise TypeError(f"Expected type `str` for class `{self.__class__.__name__}` constructor argument `version`, got `{type(version).__name__}`")
		self._version = version


	# public methods
	def print_info(self) -> None:
		data = []
		data.append(f'App Name: {self.name}')
		data.append(f'App Version: {self.version}')
		data.append(f'App Author: {self.author}')
		data.append(f'Root Path: {self.root_path}')
		data.append(f'Icon Path: {self._icon_file}')
		data.append(f'Log Path: {self._log_file}')
		data.append(f'Config Path: {self._config_file}')
		for line in data:
			print(line)


	# properties
	@property
	def author(self) -> str:
		return self._author

	@property
	def name(self) -> str:
		return self._name

	@property
	def root_path(self) -> Path:
		return self._root_path

	@property
	def version(self) -> str:
		return self._version



class GuiApp(App):
	# constructor
	def __init__(self,
			name: str = "App",
			version: str = "1.0.0",
			author: str = "Unknown",
			resources_dir: str = "resources",
			icon_file: str = "icon.ico",
			log_file: str = "debug.log",
			config_file: str = "config.ini",
			use_config: bool = False,
			win_width: int = 800,
			win_height: int = 600,
			win_width_min: int = 400,
			win_height_min: int = 300,
			win_x_pos: int = 0,
			win_y_pos: int = 0,
			win_centered: bool = False,
			win_pinned: bool = False,
			win_width_resizable: bool = True,
			win_height_resizable: bool = True
		) -> None:
		# parent constructor
		App.__init__(self, name, version, author, resources_dir, icon_file, log_file, config_file, use_config)

		# window default values
		self._win_width_def = self._config["WIN_BASIC"]["iDefaultWidth"] if self._config else win_width
		self._win_height_def = self._config["WIN_BASIC"]["iDefaultHeight"] if self._config else win_height
		self._win_width_min = self._config["WIN_BASIC"]["iMinWidth"] if self._config else win_width_min
		self._win_height_min = self._config["WIN_BASIC"]["iMinHeight"] if self._config else win_height_min
		self._win_x_pos_def = self._config["WIN_POS"]["iXOffset"] if self._config else win_x_pos
		self._win_y_pos_def = self._config["WIN_POS"]["iYOffset"] if self._config else win_y_pos
		self._win_centered_def = self._config["WIN_POS"]["bCenterWindow"] if self._config else win_centered
		self._win_pinned_def = self._config["WIN_FLAGS"]["bStartPinned"] if self._config else win_pinned

		# window state
		self._win_width = self._win_width_def
		self._win_height = self._win_height_def
		self._win_x_pos = self._win_x_pos_def
		self._win_y_pos = self._win_y_pos_def
		self._win_width_resizable = win_width_resizable
		self._win_height_resizable = win_height_resizable
		self._win_pinned = False

		# window
		self._window = ctk.CTk()
		self._window.title(self._name)
		try:
			self._set_window_icon()
		except FileNotFoundError as e:
			print(f"ERROR: Error while trying to set window icon: {e}")
		#self._window.geometry(f"{self._win_width_def}x{self._win_height_def}+{self._win_x_pos_def}+{self._win_y_pos_def}")
		self._window.protocol("WM_DELETE_WINDOW", self.close_window)
		self.update_window(True)
		if self._win_pinned_def:
			self.toggle_pinned()
		#print('Initialized Window')


	# private methods
	def _set_window_icon(self) -> None:
		if not isinstance(self._icon_file, Path):
			raise TypeError(f"Expected type `pathlib.Path` for class `{self.__class__.__name__}` private attribute `_icon_file`, got `{type(self._icon_file).__name__}`")
		if not self._icon_file.exists():
			raise FileNotFoundError(f"File `{self._icon_file}` does not exist")
		self._window.iconbitmap(self._icon_file)


	# public methods
	def close_window(self) -> None:
		self._window.destroy()

	def focus_window(self) -> None:
		self._window.focus_force()

	#def maximize_window(self) -> None:
	#	self._window.attributes('-zoomed', True)

	def minimize_window(self) -> None:
		self._window.iconify()

	def open_window(self) -> None:
		self._window.mainloop()

	def print_info(self) -> None:
		App.print_info(self)
		data = []
		data.append(f'Screen Dimensions (W x H): {self.screen_dimensions[0]} x {self.screen_dimensions[1]}')
		data.append(f'Window Dimensions (W x H): {self.window_dimensions[0]} x {self.window_dimensions[1]}')
		data.append(f'Window Position (X, Y): ({self.window_position[0]}, {self.window_position[1]})')
		for line in data:
			print(line)

	#def restore_window(self) -> None:
	#	self._window.attributes('-zoomed', False)

	def toggle_pinned(self) -> None:
		if not self._win_pinned:
			self._window.attributes('-topmost', True)
			self._win_pinned = True
		else:
			self._window.attributes('-topmost', False)
			self._win_pinned = False

	def update_window(self, reset_pos: bool = False) -> None:
		self._screen_width, self._screen_height = self.screen_dimensions
		#print(f'Screen Dimensions (W x H): {self.screen_dimensions[0]} x {self.screen_dimensions[1]}')
		if reset_pos:
			current_width = self._win_width_def
			current_height = self._win_height_def
		else:
			current_width, current_height = self.window_dimensions
		#print(f'Window Dimensions (W x H): {self.window_dimensions[0]} x {self.window_dimensions[1]}')
		if reset_pos:
			if self._win_centered_def:
				target_x_pos = (self._screen_width // 2) - (current_width // 2)
				target_y_pos = (self._screen_height // 2) - (current_height // 2)
			else:
				target_x_pos = self._win_x_pos_def
				target_y_pos = self._win_y_pos_def
		else:
			target_x_pos = self._window.winfo_x()
			target_y_pos = self._window.winfo_y()
		#print(f'Target Position: ({target_x_pos}, {target_y_pos})')
		target_width = current_width if current_width > self._win_width_min else self._win_width_min
		target_height = current_height if current_height > self._win_height_min else self._win_height_min
		self._window.geometry(f"{target_width}x{target_height}+{target_x_pos}+{target_y_pos}")
		self._window.minsize(self._win_width_min, self._win_height_min)
		self._window.resizable(self._win_width_resizable, self._win_height_resizable)
		self._win_width, self._win_height = self.window_dimensions
		self._win_x_pos, self._win_y_pos = self.window_position
		#self._window.update()
		#print('Window updated.')


	# properties
	@property
	def screen_dimensions(self) -> tuple[int, int]:
		return self._window.winfo_screenwidth(), self._window.winfo_screenheight()

	@property
	def window(self) -> ctk.CTk:
		return self._window

	@property
	def window_dimensions(self) -> tuple[int, int]:
		return self._window.winfo_width(), self._window.winfo_height()

	@property
	def window_position(self) -> tuple[int, int]:
		return self._window.winfo_x(), self._window.winfo_y()



class CalculatorApp(GuiApp):
	# constructor
	def __init__(self,
			name: str = "Calculator",
			version: str = "1.0.0",
			author: str = "Unknown",
			resources_dir: str = "resources",
			history_file: str = "history.txt",
			icon_file: str = "icon.ico",
			log_file: str = "debug.log",
			config_file: str = "config.ini",
			use_config: bool = True,
			win_width: int = 250,
			win_height: int = 110,
			win_width_min: int = 250,
			win_height_min: int = 110,
			win_x_pos: int = 100,
			win_y_pos: int = 100,
			win_centered: bool = True,
			win_pinned: bool = False,
			win_width_resizable: bool = True,
			win_height_resizable: bool = False
		) -> None:
		# parent constructor
		GuiApp.__init__(self, name, version, author, resources_dir, icon_file, log_file, config_file, use_config, win_width, win_height, win_width_min, win_height_min, win_x_pos, win_y_pos, win_centered, win_pinned, win_width_resizable, win_height_resizable)

		# paths
		self._set_history_path(history_file)

		# window default values
		self._win_width_adv = self._config["WIN_ADV"]["iDefaultWidth"] if self._config else 400
		self._win_height_adv = self._config["WIN_ADV"]["iDefaultHeight"] if self._config else 410
		self._win_width_min_adv = self._config["WIN_ADV"]["iMinWidth"] if self._config else 400
		self._win_height_min_adv = self._config["WIN_ADV"]["iMinHeight"] if self._config else 410
		self._win_advanced_def = self._config["WIN_FLAGS"]["bStartAdvanced"] if self._config else False
		self._win_force_focus = self._config["DEBUG"]["bForceFocus"] if self._config else False
		#self._win_restore_mode = self._config["WIN_RESTORE"]["bRestoreMode"]
		#self._win_restore_dimensions = self._config["WIN_RESTORE"]["bRestoreDimensions"]
		#self._win_restore_position = self._config["WIN_RESTORE"]["bRestorePosition"]
		#self._win_restore_pinned = self._config["WIN_RESTORE"]["bRestorePinned"]
		#self._win_restore_advanced = self._config["WIN_RESTORE"]["bRestoreAdvanced"]

		# window state
		self._win_expanded = False

		# calculator default values
		self._dec_precision = self._config["CALCULATION"]["iDecimalPrecision"] if self._config else 100
		self._dec_display = self._config["CALCULATION"]["iDecimalDisplay"] if self._config else 10
		if self._dec_display > self._dec_precision:
			self._dec_display = self._dec_precision
		self._only_simplify = self._config["CALCULATION"]["bOnlySimplify"] if self._config else False
		self._live_eval = self._config["CALCULATION"]["bLiveEval"] if self._config else True
		self._live_eval_delay = self._config["CALCULATION"]["iTimeoutDelay"] if self._config else 1000
		self._sanitize_input = self._config["DEBUG"]["bSanitizeInput"] if self._config else True
		self._def_expression = ''
		self._def_result = '0'
		self._timeout_patience = 1
		self._calc_wait_chars = r'+-*/^%.([{_, '

		# calculator state
		self._calc_last_expression = self._def_expression
		self._calc_last_result = self._def_result
		self._calc_expressions = [self._def_expression]
		self._calc_results = [self._def_result]

		# app state
		self._timeout_id = None
		self._history = {
			"expressions": self._calc_expressions,
			"results": self._calc_results,
			"pinned": self._win_pinned,
			"advanced": self._win_expanded,
			"dimensions": self.window_dimensions,
			"position": self.window_position
		}

		# keybinds
		self._advanced_key = self._config["KEYBINDS"]["sAdvancedKey"] if self._config else "<F3>"
		self._clear_key = self._config["KEYBINDS"]["sClearKey"] if self._config else "<Alt-BackSpace>"
		self._delete_left_key = self._config["KEYBINDS"]["sDeleteAllLKey"] if self._config else "<Control-BackSpace>"
		self._delete_right_key = self._config["KEYBINDS"]["sDeleteAllRKey"] if self._config else "<Control-Delete>"
		#self._delete_term_left_key = self._config["KEYBINDS"]["sDeleteTermLKey"] if self._config else "<Shift-BackSpace>"
		#self._delete_term_right_key = self._config["KEYBINDS"]["sDeleteTermRKey"] if self._config else "<Shift-Delete>"
		self._evaluate_key = self._config["KEYBINDS"]["sEvaluateKey"] if self._config else "<Enter>"
		#self._help_key = self._config["KEYBINDS"]["sHelpKey"] if self._config else "<F1>"
		#self._options_key = self._config["KEYBINDS"]["sOptionsKey"] if self._config else "<F2>"
		#self._redo_key = self._config["KEYBINDS"]["sRedoKey"] if self._config else "<Control-y>"
		#self._undo_key = self._config["KEYBINDS"]["sUndoKey"] if self._config else "<Control-z>"
		self._quit_key = self._config["KEYBINDS"]["sQuitKey"] if self._config else "<Escape>"

		# debug
		self._debug_mode = self._config["DEBUG"]["bDebugMode"] if self._config else False
		if self._debug_mode:
			print(f"Settings: {self._config}")


	# private methods
	def _set_history_path(self, history_file: str) -> None:
		if not isinstance(self._resources_path, Path):
			raise TypeError(f"Expected type `pathlib.Path` for class `{self.__class__.__name__}` private attribute `_resources_path`, got `{type(self._resources_path).__name__}`")
		if not isinstance(history_file, str):
			raise TypeError(f"Expected type `str` for class `{self.__class__.__name__}` constructor argument `history_file`, got `{type(history_file).__name__}`")
		self._history_path = self._resources_path / history_file


	# public methods
	def print_info(self) -> None:
		GuiApp.print_info(self)
		data = []
		data.append(f'History File: {self._history_path}')
		for line in data:
			print(line)

	# properties



### FUNCTIONS ###


### MAIN ###

def main():
	pass

def _test():
	pass

	#app = App("Test", "0.0.1", "GroundAura")
	#app = GuiApp("Test App", "0.0.1", "GroundAura")
	app = CalculatorApp("Test App", "0.0.1", "GroundAura", win_centered=True, config_file="AuraCalc.ini", use_config=True)

	#print(app.window_position)
	app.print_info()
	#app.update_window()
	#app.print_info()
	app.open_window()



if __name__ == "__main__":
	#main()
	_test()
