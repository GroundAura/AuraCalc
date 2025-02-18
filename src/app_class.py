### IMPORTS ###

# builtins

# external
import customtkinter as ctk
from pathlib import Path
import sys

# internal
from app_config import read_config, get_config_value
from app_type import validate_type



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
		self._set_icon_path(icon_file)
		self._set_log_path(log_file)

		# config
		self._set_config(config_file, use_config)


	# private methods
	def _set_author(self, value: str) -> None:
		validate_type(value, str)
		self._author = value

	def _set_config(self, file_name: str, use_config: bool = True) -> None:
		if use_config:
			validate_type(self._resources_path, Path)
			validate_type(file_name, str)
			self._config_path = self._resources_path / file_name
			validate_type(self._config_path, Path)
			if not self._config_path.exists():
				raise FileNotFoundError(f"File `{self._config_path}` does not exist")
			self._config = read_config(self._config_path, preserve_key_case=True)
		else:
			self._config_path = None
			self._config = None

	def _set_icon_path(self, file_name: str) -> None:
		validate_type(self._resources_path, Path)
		validate_type(file_name, str)
		self._icon_path = self._resources_path / file_name

	def _set_log_path(self, file_name: str) -> None:
		validate_type(self._resources_path, Path)
		validate_type(file_name, str)
		self._log_path = self._resources_path / file_name

	def _set_name(self, value: str) -> None:
		validate_type(value, str)
		self._name = value

	def _set_resources_path(self, dir_name: str) -> None:
		validate_type(self._root_path, Path)
		if dir_name:
			validate_type(dir_name, str)
			self._resources_path = self._root_path / dir_name
		else:
			self._resources_path = self._root_path

	def _set_root_path(self) -> None:
		try:
			# PyInstaller creates a temporary folder and stores the path in _MEIPASS
			root_path = Path(sys.MEIPASS)
			#return Path(sys.executable).parent
		except AttributeError:
			root_path = Path.cwd()
		validate_type(root_path, Path)
		self._root_path = root_path

	def _set_version(self, value: str) -> None:
		validate_type(value, str)
		self._version = value


	# public methods
	def print_info(self) -> None:
		data = []
		data.append(f'App Name: {self.name}')
		data.append(f'App Version: {self.version}')
		data.append(f'App Author: {self.author}')
		data.append(f'Root Path: {self.root_path}')
		data.append(f'Icon Path: {self._icon_path}')
		data.append(f'Log Path: {self._log_path}')
		if self._config_path is not None:
			data.append(f'Config Path: {self._config_path}')
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
			win_resize_width: bool = True,
			win_resize_height: bool = True
		) -> None:
		# parent constructor
		App.__init__(self, name, version, author, resources_dir, icon_file, log_file, config_file, use_config)

		# window default values
		self._set_win_width_min(win_width_min, use_config)
		self._set_win_height_min(win_height_min, use_config)
		self._set_win_width_def(win_width, use_config)
		self._set_win_height_def(win_height, use_config)
		self._set_win_x_pos_def(win_x_pos, use_config)
		self._set_win_y_pos_def(win_y_pos, use_config)
		self._set_win_centered_def(win_centered, use_config)
		self._set_win_pinned_def(win_pinned, use_config)

		# window state
		self._win_width = self._win_width_def
		self._win_height = self._win_height_def
		self._win_x_pos = self._win_x_pos_def
		self._win_y_pos = self._win_y_pos_def
		self._set_win_resize_width(win_resize_width)
		self._set_win_resize_height(win_resize_height)
		self._win_pinned = False

		# window
		self._window = ctk.CTk()
		validate_type(self._window, ctk.CTk)
		validate_type(self._name, str)
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
	def _set_win_centered_def(self, new_val: bool, use_config: bool = False) -> None:
		value = get_config_value(self._config, "WIN_POS", "bCenterWindow", new_val, use_config)
		validate_type(new_val, bool)
		self._win_centered_def = value

	def _set_win_height_def(self, new_val: int, use_config: bool = False) -> None:
		value = get_config_value(self._config, "WIN_BASIC", "iDefaultHeight", new_val, use_config)
		validate_type(value, int, 0)
		try:
			min_value = self._win_width_min
			validate_type(min_value, int, 0)
		except AttributeError:
			min_value = None
		if min_value is not None and value < min_value:
			self._win_height_def = min_value
		else:
			self._win_height_def = value

	def _set_win_height_min(self, new_val: int, use_config: bool = False) -> None:
		value = get_config_value(self._config, "WIN_BASIC", "iMinHeight", new_val, use_config)
		validate_type(value, int, 0)
		self._win_height_min = value

	def _set_win_pinned_def(self, new_val: bool, use_config: bool = False) -> None:
		value = get_config_value(self._config, "WIN_FLAGS", "bStartPinned", new_val, use_config)
		validate_type(new_val, bool)
		self._win_pinned_def = value

	def _set_win_resize_height(self, new_val: bool) -> None:
		validate_type(new_val, bool)
		self._win_resize_height = new_val

	def _set_win_resize_width(self, new_val: bool) -> None:
		validate_type(new_val, bool)
		self._win_resize_width = new_val

	def _set_win_width_def(self, new_val: int, use_config: bool = False) -> None:
		value = get_config_value(self._config, "WIN_BASIC", "iDefaultWidth", new_val, use_config)
		validate_type(value, int, 0)
		try:
			min_value = self._win_width_min
			validate_type(min_value, int, 0)
		except AttributeError:
			min_value = None
		if min_value is not None and value < min_value:
			self._win_width_def = min_value
		else:
			self._win_width_def = value

	def _set_win_width_min(self, new_val: int, use_config: bool = False) -> None:
		value = get_config_value(self._config, "WIN_BASIC", "iMinWidth", new_val, use_config)
		validate_type(value, int, 0)
		self._win_width_min = value

	def _set_win_x_pos_def(self, new_val: int, use_config: bool = False) -> None:
		value = get_config_value(self._config, "WIN_POS", "iXOffset", new_val, use_config)
		validate_type(value, int, 0)
		self._win_x_pos_def = value

	def _set_win_y_pos_def(self, new_val: int, use_config: bool = False) -> None:
		value = get_config_value(self._config, "WIN_POS", "iYOffset", new_val, use_config)
		validate_type(value, int, 0)
		self._win_y_pos_def = value

	def _set_window_icon(self) -> None:
		validate_type(self._icon_path, Path)
		if not self._icon_path.exists():
			raise FileNotFoundError(f"File `{self._icon_path}` does not exist")
		self._window.iconbitmap(self._icon_path)


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
		self._window.resizable(self._win_resize_width, self._win_resize_height)
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
			win_resize_width: bool = True,
			win_resize_height: bool = False
		) -> None:
		# parent constructor
		GuiApp.__init__(self, name, version, author, resources_dir, icon_file, log_file, config_file, use_config, win_width, win_height, win_width_min, win_height_min, win_x_pos, win_y_pos, win_centered, win_pinned, win_resize_width, win_resize_height)

		# paths
		self._set_history_path(history_file)

		# window default values
		self._set_win_width_adv(400, use_config)
		self._set_win_height_adv(410, use_config)
		self._set_win_width_min_adv(400, use_config)
		self._set_win_height_min_adv(410, use_config)
		self._set_win_advanced_def(False, use_config)
		self._set_win_force_focus(False, use_config)

		#self._set_win_restore_mod()
		#self._set_win_restore_dimensions()
		#self._set_win_restore_position()
		#self._set_win_restore_pinned()
		#self._set_win_restore_advanced()
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
		self._set_key_advanced("<F3>", use_config)
		self._set_key_clear("<Alt-BackSpace>", use_config)
		self._set_key_del_l("<Control-BackSpace>", use_config)
		self._set_key_del_r("<Control-Delete>", use_config)
		#self._set_key_del_term_r("<Shift-BackSpace>", use_config)
		#self._set_key_del_term_l("<Shift-Delete>", use_config)
		self._set_key_eval("<Enter>", use_config)
		#self._set_key_help("<F1>", use_config)
		#self._set_key_options("<F2>", use_config)
		#self._set_key_redo("<Control-y>", use_config)
		#self._set_key_undo("<Control-z>", use_config)
		self._set_key_quit("<Escape>", use_config)

		# debug
		self._debug_mode = self._config["DEBUG"]["bDebugMode"] if self._config else False
		if self._debug_mode:
			print(f"Settings: {self._config}")


	# private methods
	def _set_history_path(self, new_val: str) -> None:
		validate_type(self._resources_path, Path)
		validate_type(new_val, str)
		self._history_path = self._resources_path / new_val

	def _set_key_advanced(self, new_val: str, use_config: bool = False) -> None:
		value = get_config_value(self._config, "KEYBINDS", "sAdvancedKey", new_val, use_config)
		validate_type(new_val, str)
		self._key_advanced = value

	def _set_key_clear(self, new_val: str, use_config: bool = False) -> None:
		value = get_config_value(self._config, "KEYBINDS", "sClearKey", new_val, use_config)
		validate_type(new_val, str)
		self._key_clear = value

	def _set_key_del_l(self, new_val: str, use_config: bool = False) -> None:
		value = get_config_value(self._config, "KEYBINDS", "sDeleteAllLKey", new_val, use_config)
		validate_type(new_val, str)
		self._key_del_l = value

	def _set_key_del_r(self, new_val: str, use_config: bool = False) -> None:
		value = get_config_value(self._config, "KEYBINDS", "sDeleteAllRKey", new_val, use_config)
		validate_type(new_val, str)
		self._key_del_r = value

	def _set_key_del_term_l(self, new_val: str, use_config: bool = False) -> None:
		value = get_config_value(self._config, "KEYBINDS", "sDeleteTermLKey", new_val, use_config)
		validate_type(new_val, str)
		self._key_del_term_l = value

	def _set_key_del_term_r(self, new_val: str, use_config: bool = False) -> None:
		value = get_config_value(self._config, "KEYBINDS", "sDeleteTermRKey", new_val, use_config)
		validate_type(new_val, str)
		self._key_del_term_r = value

	def _set_key_eval(self, new_val: str, use_config: bool = False) -> None:
		value = get_config_value(self._config, "KEYBINDS", "sEvaluateKey", new_val, use_config)
		validate_type(new_val, str)
		self._key_eval = value

	def _set_key_help(self, new_val: str, use_config: bool = False) -> None:
		value = get_config_value(self._config, "KEYBINDS", "sHelpKey", new_val, use_config)
		validate_type(new_val, str)
		self._key_help = value

	def _set_key_options(self, new_val: str, use_config: bool = False) -> None:
		value = get_config_value(self._config, "KEYBINDS", "sOptionsKey", new_val, use_config)
		validate_type(new_val, str)
		self._key_options = value

	def _set_key_redo(self, new_val: str, use_config: bool = False) -> None:
		value = get_config_value(self._config, "KEYBINDS", "sRedoKey", new_val, use_config)
		validate_type(new_val, str)
		self._key_redo = value

	def _set_key_undo(self, new_val: str, use_config: bool = False) -> None:
		value = get_config_value(self._config, "KEYBINDS", "sUndoKey", new_val, use_config)
		validate_type(new_val, str)
		self._key_undo = value

	def _set_key_quit(self, new_val: str, use_config: bool = False) -> None:
		value = get_config_value(self._config, "KEYBINDS", "sQuitKey", new_val, use_config)
		validate_type(new_val, str)
		self._key_quit = value

	def _set_win_advanced_def(self, new_val: bool, use_config: bool = False) -> None:
		value = get_config_value(self._config, "WIN_FLAGS", "bStartAdvanced", new_val, use_config)
		validate_type(new_val, bool)
		self._win_advanced_def = value

	def _set_win_force_focus(self, new_val: bool, use_config: bool = False) -> None:
		value = get_config_value(self._config, "DEBUG", "bForceFocus", new_val, use_config)
		validate_type(new_val, bool)
		self._win_force_focus = value

	def _set_win_height_adv(self, new_val: int, use_config: bool = False) -> None:
		value = get_config_value(self._config, "WIN_ADV", "iDefaultHeight", new_val, use_config)
		validate_type(value, int, 0)
		try:
			min_value = self._win_height_min_adv
			validate_type(min_value, int, 0)
		except AttributeError:
			min_value = None
		if min_value is not None and value < min_value:
			self._win_height_adv = min_value
		else:
			self._win_height_adv = value

	def _set_win_height_min_adv(self, new_val: int, use_config: bool = False) -> None:
		value = get_config_value(self._config, "WIN_ADV", "iMinHeight", new_val, use_config)
		validate_type(value, int, 0)
		self._win_height_min_adv = value

	def _set_win_width_adv(self, new_val: int, use_config: bool = False) -> None:
		value = get_config_value(self._config, "WIN_ADV", "iDefaultWidth", new_val, use_config)
		validate_type(value, int, 0)
		try:
			min_value = self._win_width_min_adv
			validate_type(min_value, int, 0)
		except AttributeError:
			min_value = None
		if min_value is not None and value < min_value:
			self._win_width_adv = min_value
		else:
			self._win_width_adv = value

	def _set_win_width_min_adv(self, new_val: int, use_config: bool = False) -> None:
		value = get_config_value(self._config, "WIN_ADV", "iMinWidth", new_val, use_config)
		validate_type(value, int, 0)
		self._win_width_min_adv = value


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
