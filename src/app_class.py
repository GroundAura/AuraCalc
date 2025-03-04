### IMPORTS ###

# builtins
from typing import Any

# external
import customtkinter as ctk
#from decimal import getcontext
from pathlib import Path

# internal
from app_config import read_config, get_config_value
from app_logging import logging_print
from app_evaluate import sanitize_input, evaluate_expression
from app_globals import CONFIG, FORCE_DEBUG, PATH_CONFIG, USE_CONFIG
from app_keybinds import bind_event
from app_path import get_root_path
from app_type import validate_type
from app_window import focus_element, text_set



### CLASSES ###

class App:
	# constructor
	def __init__(self,
			name: str = 'App',
			version: str = '1.0.0',
			author: str = 'Unknown',
			resources_dir: str = 'resources',
			icon_file: str = 'icon.ico',
			log_file: str = 'debug.log',
			config_file: str = 'config.ini',
			use_config: bool = USE_CONFIG
		) -> None:

		# metadata
		self._set_name(name)
		self._set_version(version)
		self._set_author(author)

		# paths
		self._root_path = get_root_path()
		self._set_resources_path(resources_dir)
		self._set_icon_path(icon_file)
		self._set_log_path(log_file)

		# config
		self._set_config(config_file, use_config)

		# debug
		self._set_debug_mode(FORCE_DEBUG, use_config)
		#self._set_debug_mode(app_globals.DEBUG_MODE, use_config)


	# private methods
	def _logging_print(self,
			message: str = '',
			indent: int = 0,
			timestamp: bool = True,
			print_to_console: bool = True,
			print_to_file: bool = True,
			debug_mode_only: bool = True
		) -> None:
		#try:
		#	validate_type(self._log_path, Path)
		#except AttributeError:
		#	raise AttributeError('Log path not set')
		#try:
		#	validate_type(self._debug_mode, bool)
		#except AttributeError:
		#	self._set_debug_mode(app_globals.DEBUG_MODE)
		try:
			validate_type(message, str)
		except TypeError:
			message = str(message)
		validate_type(indent, int)
		validate_type(timestamp, bool)
		validate_type(print_to_console, bool)
		validate_type(print_to_file, bool)
		validate_type(debug_mode_only, bool)
		logging_print(
			message=message,
			indent=indent,
			timestamp=timestamp,
			print_to_console=print_to_console,
			print_to_file=print_to_file,
			debug_mode_only=debug_mode_only
		)

	def _set_author(self, value: str) -> None:
		validate_type(value, str)
		self._author = value

	def _set_config(self, file_name: str, use_config: bool = True) -> None:
		if use_config:
			if CONFIG and PATH_CONFIG:
				self._config_path = PATH_CONFIG
				self._config = CONFIG
			else:
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

	def _set_debug_mode(self, new_val: bool, use_config: bool = False) -> None:
		value = get_config_value(self._config, 'DEBUG', 'bDebugMode', new_val, use_config)
		#print(self._config['DEBUG']['bDebugMode'])
		validate_type(new_val, bool)
		self._debug_mode = value
		#app_globals.DEBUG_MODE = self._debug_mode
		#print(self._debug_mode, app_globals.DEBUG_MODE)
		if self._debug_mode:
			self._logging_print(f"Config Settings: {self._config}")

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

	def _set_version(self, value: str) -> None:
		validate_type(value, str)
		self._version = value


	# public methods
	def print_info(self) -> None:
		data = []
		data.append(f"App Name: {self.name}")
		data.append(f"App Version: {self.version}")
		data.append(f"App Author: {self.author}")
		data.append(f"Root Path: {self.root_path}")
		data.append(f"Icon Path: {self._icon_path}")
		data.append(f"Log Path: {self._log_path}")
		if self._config_path is not None:
			data.append(f"Config Path: {self._config_path}")
		for line in data:
			self._logging_print(line)


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
			name: str = 'App',
			version: str = '1.0.0',
			author: str = 'Unknown',
			resources_dir: str = 'resources',
			icon_file: str = 'icon.ico',
			log_file: str = 'debug.log',
			config_file: str = 'config.ini',
			use_config: bool = USE_CONFIG,
			win_width: int = 800,
			win_height: int = 600,
			win_width_min: int = 400,
			win_height_min: int = 300,
			win_x_pos: int = 0,
			win_y_pos: int = 0,
			win_centered: bool = False,
			win_pinned: bool = False,
			win_resize_width: bool = True,
			win_resize_height: bool = True,
			win_layout: str = 'grid'
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
		self._set_theme_mode('dark')
		self._set_theme_color('green')
		self._set_win_layout(win_layout)
		try:
			self._set_window_icon()
		except FileNotFoundError as e:
			print(f"ERROR: Error while trying to set window icon: {e}")
		#self._window.geometry(f"{self._win_width_def}x{self._win_height_def}+{self._win_x_pos_def}+{self._win_y_pos_def}")
		self.update_window(reset_pos=True)
		if self._win_pinned_def:
			self.toggle_pinned()
		#print('Initialized Window')

		# window elements
		self._win_frame_base = ctk.CTkFrame(self._window)

		# event bindings
		self._bound_keys = set()
		self._set_key_quit('<Escape>', use_config)
		self._window.protocol('WM_DELETE_WINDOW', self.close_window)


	# private methods
	def _add_bound_key(self, sequence: str) -> None:
		validate_type(sequence, str)
		if sequence[0] != '<' or sequence[-1] != '>':
			raise ValueError(f"ERROR: Invalid key sequence: '{sequence}'. Must be in the format '<sequence>'")
		sequence = sequence.lstrip('<').rstrip('>')
		#sequence = sequence[1:-1]
		if '-' in sequence:
			#keys = sequence.split('-')
			#key = keys[-1]
			return
		else:
			key = sequence
			self._bound_keys.add(key)
		#self._bound_keys.add(key)

	def _set_key_quit(self, new_val: str, use_config: bool = False) -> None:
		value = get_config_value(self._config, 'KEYBINDS', 'sQuitKey', new_val, use_config)
		validate_type(new_val, str)
		self._key_quit = value
		bind_event(self._window, self._key_quit, command=self.close_window)
		self._add_bound_key(self._key_quit)

	def _set_theme_mode(self, new_val: str) -> None:
		validate_type(new_val, str)
		if new_val not in ('light', 'dark', 'system'):
			raise ValueError(f"ERROR: Invalid theme mode: '{new_val}'. Must be 'light', 'dark', or 'system'")
		self._theme_mode = new_val
		ctk.set_appearance_mode(self._theme_mode)

	def _set_theme_color(self, new_val: str) -> None:
		validate_type(new_val, str)
		self._theme_color = new_val
		ctk.set_default_color_theme(self._theme_color)

	def _set_win_centered_def(self, new_val: bool, use_config: bool = False) -> None:
		value = get_config_value(self._config, 'WIN_POS', 'bCenterWindow', new_val, use_config)
		validate_type(new_val, bool)
		self._win_centered_def = value

	def _set_win_height_def(self, new_val: int, use_config: bool = False) -> None:
		value = get_config_value(self._config, 'WIN_BASIC', 'iDefaultHeight', new_val, use_config)
		try:
			value = self._win_height_min if value < self._win_height_min else value
		except AttributeError:
			pass # ignore if self._win_height_min is not set
		validate_type(value, int)
		value = 0 if value < 0 else value
		self._win_height_def = value

	def _set_win_height_min(self, new_val: int, use_config: bool = False) -> None:
		value = get_config_value(self._config, 'WIN_BASIC', 'iMinHeight', new_val, use_config)
		validate_type(value, int)
		value = 0 if value < 0 else value
		self._win_height_min = value

	def _set_win_layout(self, new_val: str) -> None:
		validate_type(new_val, str)
		if new_val not in ('grid', 'pack'):
			raise ValueError(f"Invalid layout: '{new_val}'. Must be 'grid' or 'pack'")
		self._win_layout = new_val

	def _set_win_pinned_def(self, new_val: bool, use_config: bool = False) -> None:
		value = get_config_value(self._config, 'WIN_FLAGS', 'bStartPinned', new_val, use_config)
		validate_type(new_val, bool)
		self._win_pinned_def = value

	def _set_win_resize_height(self, new_val: bool) -> None:
		validate_type(new_val, bool)
		self._win_resize_height = new_val

	def _set_win_resize_width(self, new_val: bool) -> None:
		validate_type(new_val, bool)
		self._win_resize_width = new_val

	def _set_win_width_def(self, new_val: int, use_config: bool = False) -> None:
		value = get_config_value(self._config, 'WIN_BASIC', 'iDefaultWidth', new_val, use_config)
		try:
			value = self._win_width_min if value < self._win_width_min else value
		except AttributeError:
			pass # ignore if self._win_width_min is not set
		validate_type(value, int)
		value = 0 if value < 0 else value
		self._win_width_def = value

	def _set_win_width_min(self, new_val: int, use_config: bool = False) -> None:
		value = get_config_value(self._config, 'WIN_BASIC', 'iMinWidth', new_val, use_config)
		validate_type(value, int)
		value = 0 if value < 0 else value
		self._win_width_min = value

	def _set_win_x_pos_def(self, new_val: int, use_config: bool = False) -> None:
		value = get_config_value(self._config, 'WIN_POS', 'iXOffset', new_val, use_config)
		validate_type(value, int)
		value = 0 if value < 0 else value
		self._win_x_pos_def = value

	def _set_win_y_pos_def(self, new_val: int, use_config: bool = False) -> None:
		value = get_config_value(self._config, 'WIN_POS', 'iYOffset', new_val, use_config)
		validate_type(value, int)
		value = 0 if value < 0 else value
		self._win_y_pos_def = value

	def _set_window_icon(self) -> None:
		validate_type(self._icon_path, Path)
		if not self._icon_path.exists():
			raise FileNotFoundError(f"File `{self._icon_path}` does not exist")
		self._window.iconbitmap(self._icon_path)


	# public methods
	def close_window(self) -> None:
		self._logging_print(f"Closing {self.name}.")
		self._logging_print('\n\n', timestamp=False, print_to_console=False) # add delimiter to end of log
		self._window.destroy()

	def focus_window(self) -> None:
		self._window.focus_force()

	#def maximize_window(self) -> None:
	#	self._window.attributes('-zoomed', True)

	def minimize_window(self) -> None:
		self._window.iconify()

	def open_window(self) -> None:
		self._logging_print(f"Opening {self.name}.")
		if self._win_force_focus:
			logging_print('Forcing window focus.')
			self.focus_window()
		self._window.mainloop()

	def print_info(self) -> None: # override
		App.print_info(self)
		data = []
		data.append(f"Screen Dimensions (W x H): {self.screen_dimensions[0]} x {self.screen_dimensions[1]}")
		data.append(f"Window Dimensions (W x H): {self.window_dimensions[0]} x {self.window_dimensions[1]}")
		data.append(f"Window Position (X, Y): ({self.window_position[0]}, {self.window_position[1]})")
		for line in data:
			self._logging_print(line)

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
		#print(f"Screen Dimensions (W x H): {self.screen_dimensions[0]} x {self.screen_dimensions[1]}")
		if reset_pos:
			current_width = self._win_width_def
			current_height = self._win_height_def
		else:
			current_width, current_height = self.window_dimensions
		#print(f"Window Dimensions (W x H): {self.window_dimensions[0]} x {self.window_dimensions[1]}")
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
		#print(f"Target Position: ({target_x_pos}, {target_y_pos})")
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
	def win_frame_base(self) -> ctk.CTkFrame:
		return self._win_frame_base

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
			name: str = 'Calculator',
			version: str = '1.0.0',
			author: str = 'Unknown',
			resources_dir: str = 'resources',
			history_file: str = 'history.txt',
			icon_file: str = 'icon.ico',
			log_file: str = 'debug.log',
			config_file: str = 'config.ini',
			use_config: bool = USE_CONFIG,
			win_width: int = 250,
			win_height: int = 110,
			win_width_min: int = 250,
			win_height_min: int = 110,
			win_x_pos: int = 100,
			win_y_pos: int = 100,
			win_centered: bool = True,
			win_pinned: bool = False,
			win_resize_width: bool = True,
			win_resize_height: bool = False,
			win_layout: str = 'grid'
		) -> None:
		# parent constructor
		GuiApp.__init__(self, name, version, author, resources_dir, icon_file, log_file, config_file, use_config, win_width, win_height, win_width_min, win_height_min, win_x_pos, win_y_pos, win_centered, win_pinned, win_resize_width, win_resize_height, win_layout)

		# paths
		self._set_history_path(history_file)

		# window default values
		self._set_win_width_adv(400, use_config)
		self._set_win_height_adv(410, use_config)
		self._set_win_width_min_adv(400, use_config)
		self._set_win_height_min_adv(410, use_config)
		self._set_win_advanced_def(False, use_config)
		self._set_win_force_focus(False, use_config)

		self._set_win_restore(False, use_config)
		self._set_win_restore_adv(False, use_config)
		self._set_win_restore_dim(False, use_config)
		self._set_win_restore_pin(False, use_config)
		self._set_win_restore_pos(False, use_config)

		## window state
		self._win_expanded = False
		pinned_text = 'Unpin' if self._win_pinned else 'Pin'

		# window elements
		validate_type(self._window, ctk.CTk)
		self._win_frame_adv = ctk.CTkFrame(self._window)
		#self._win_frame_help = ctk.CTkFrame(self._window)
		#self._win_frame_opt = ctk.CTkFrame(self._window)
		self._win_btn_adv = ctk.CTkButton(self._win_frame_base, text='Expand', command=self.toggle_advanced)
		self._win_btn_clear = ctk.CTkButton(self._win_frame_base, text='Clear', command=self._clear_io)
		self._win_btn_pin = ctk.CTkButton(self._win_frame_base, text=pinned_text, command=self.toggle_pinned)
		self._win_txt_input = ctk.CTkEntry(self._win_frame_base)
		self._win_txt_result = ctk.CTkTextbox(self._win_frame_base)

		# calculator default values
		self._set_calc_dec_precision(100, use_config)
		self._set_calc_dec_display(10, use_config)
		self._set_calc_approximate(True, use_config)
		self._set_calc_live_eval(True, use_config)
		self._set_calc_live_eval_delay(1000, use_config)
		self._set_calc_sanitize_input(True, use_config)
		self._calc_def_expr = ''
		self._calc_def_result = '0'
		self._timeout_patience = 1
		self._calc_wait_chars = r'+-*/^%.([{_, '

		# calculator state
		self._calc_last_expr = self._calc_def_expr
		self._calc_last_result = self._calc_def_result
		self._calc_expressions = [self._calc_def_expr]
		self._calc_results = [self._calc_def_result]

		# app state
		self._timeout_id = None
		self._history = {
			'expressions': self._calc_expressions,
			'results': self._calc_results,
			'pinned': self._win_pinned,
			'advanced': self._win_expanded,
			'dimensions': self.window_dimensions,
			'position': self.window_position
		}

		# event bindings
		self._set_key_advanced('<F3>', use_config)
		self._set_key_clear('<Alt-BackSpace>', use_config)
		self._set_key_del_l('<Control-BackSpace>', use_config)
		self._set_key_del_r('<Control-Delete>', use_config)
		#self._set_key_del_term_l('<Shift-Delete>', use_config)
		#bind_event(self._window, self._key_del_term_l, command=lambda: self._del_txt_term(self._win_txt_input, 'left'))
		#self._set_key_del_term_r('<Shift-BackSpace>', use_config)
		#bind_event(self._window, self._key_del_term_r, command=lambda: self._del_txt_term(self._win_txt_input, 'right'))
		self._set_key_eval('<Return>', use_config)
		#self._set_key_help('<F1>', use_config)
		#bind_event(self._window, self._key_help, command=self.show_help)
		#self._set_key_options('<F2>', use_config)
		#bind_event(self._window, self._key_options, command=self.show_options)
		#self._set_key_redo('<Control-y>', use_config)
		#bind_event(self._window, self._key_options, command=self.undo_txt)
		#self._set_key_undo('<Control-z>', use_config)
		#bind_event(self._window, self._key_options, command=self.redo_txt)
		if self._calc_live_eval:
			bind_event(self._win_txt_input, '<KeyRelease>', excluded_seq=self._bound_keys, command=lambda: self.evaluate(live_mode=True))
		self.window.bind('<FocusIn>', lambda event: focus_element(self._win_txt_input))

		# final window setup
		text_set(self._win_txt_input, self._calc_def_expr)
		self._win_txt_result.configure(state='disabled')
		self._win_txt_result.state_disabled = True
		text_set(self._win_txt_result, self.calc_def_result)
		if self._win_advanced_def:
			self.toggle_advanced()

	# private methods
	def _clear_io(self) -> None:
		text_set(self._win_txt_input, self.calc_def_expr)
		text_set(self._win_txt_result, self._calc_def_result)
		focus_element(self._win_txt_input)

	#def _del_txt(self, element, begin, end) -> None:
	#	element.delete(begin, end)

	def _del_txt_cursor(self, element, direction) -> None:
		if direction.lower() in ('left', 'l', '<'):
			if type(element) == ctk.CTkEntry:
				element.delete('0', 'insert')
			elif type(element) == ctk.CTkTextbox:
				element.delete('1.0', 'insert', 'end')
		elif direction.lower() in ('right', 'r', '>'):
			if type(element) == ctk.CTkEntry:
				element.delete('insert', 'end')
			elif type(element) == ctk.CTkTextbox:
				element.delete('insert', 'end-1c')
		else:
			raise ValueError(f"Invalid direction: {direction}. Must be 'left', 'l', '<', 'right', 'r', '>'")

	def _hide_element(self, element: str) -> None:
		if self._win_layout == 'grid':
			element.grid_remove()
		elif self._win_layout == 'pack':
			element.pack_forget()
		else:
			raise ValueError(f"Invalid layout: {self._win_layout}. Must be 'grid' or 'pack'")

	def _set_calc_approximate(self, new_val: bool, use_config: bool = False) -> None:
		value = get_config_value(self._config, 'CALCULATION', 'bApproximate', new_val, use_config)
		validate_type(new_val, bool)
		self._approximate = value

	def _set_calc_dec_display(self, new_val: int, use_config: bool = False) -> None:
		value = get_config_value(self._config, 'CALCULATION', 'iDecimalDisplay', new_val, use_config)
		try:
			value = self._calc_dec_precision if value > self._calc_dec_precision else value
		except AttributeError:
			pass # ignore if self._calc_dec_precision is not set
		validate_type(value, int)
		value = 0 if value < 0 else value
		self._calc_dec_display = value

	def _set_calc_dec_precision(self, new_val: int, use_config: bool = False) -> None:
		value = get_config_value(self._config, 'CALCULATION', 'iDecimalPrecision', new_val, use_config)
		validate_type(value, int)
		value = 0 if value < 0 else value
		self._calc_dec_precision = value
		#getcontext().prec = self._calc_dec_precision

	def _set_calc_live_eval(self, new_val: bool, use_config: bool = False) -> None:
		value = get_config_value(self._config, 'CALCULATION', 'bLiveEval', new_val, use_config)
		validate_type(new_val, bool)
		self._calc_live_eval = value

	def _set_calc_live_eval_delay(self, new_val: int, use_config: bool = False) -> None:
		value = get_config_value(self._config, 'CALCULATION', 'iTimeoutDelay', new_val, use_config)
		validate_type(value, int)
		value = 0 if value < 0 else value
		self._calc_live_eval_delay = value

	def _set_calc_sanitize_input(self, new_val: bool, use_config: bool = False) -> None:
		value = get_config_value(self._config, 'DEBUG', 'bSanitizeInput', new_val, use_config)
		validate_type(new_val, bool)
		self._sanitize_input = value

	def _set_history_path(self, new_val: str) -> None:
		validate_type(self._resources_path, Path)
		validate_type(new_val, str)
		self._history_path = self._resources_path / new_val

	def _set_key_advanced(self, new_val: str, use_config: bool = False) -> None:
		value = get_config_value(self._config, 'KEYBINDS', 'sAdvancedKey', new_val, use_config)
		validate_type(new_val, str)
		self._key_advanced = value
		bind_event(self._window, self._key_advanced, command=self.toggle_advanced)
		self._add_bound_key(self._key_advanced)

	def _set_key_clear(self, new_val: str, use_config: bool = False) -> None:
		value = get_config_value(self._config, 'KEYBINDS', 'sClearKey', new_val, use_config)
		validate_type(new_val, str)
		self._key_clear = value
		bind_event(self._window, self._key_clear, command=self._clear_io)
		self._add_bound_key(self._key_clear)

	def _set_key_del_l(self, new_val: str, use_config: bool = False) -> None:
		value = get_config_value(self._config, 'KEYBINDS', 'sDeleteAllLKey', new_val, use_config)
		validate_type(new_val, str)
		self._key_del_l = value
		bind_event(self._window, self._key_del_l, command=lambda: self._del_txt_cursor(self._win_txt_input, 'left'))
		self._add_bound_key(self._key_del_l)

	def _set_key_del_r(self, new_val: str, use_config: bool = False) -> None:
		value = get_config_value(self._config, 'KEYBINDS', 'sDeleteAllRKey', new_val, use_config)
		validate_type(new_val, str)
		self._key_del_r = value
		bind_event(self._window, self._key_del_r, command=lambda: self._del_txt_cursor(self._win_txt_input, 'right'))
		self._add_bound_key(self._key_del_r)

	def _set_key_del_term_l(self, new_val: str, use_config: bool = False) -> None:
		value = get_config_value(self._config, 'KEYBINDS', 'sDeleteTermLKey', new_val, use_config)
		validate_type(new_val, str)
		self._key_del_term_l = value

	def _set_key_del_term_r(self, new_val: str, use_config: bool = False) -> None:
		value = get_config_value(self._config, 'KEYBINDS', 'sDeleteTermRKey', new_val, use_config)
		validate_type(new_val, str)
		self._key_del_term_r = value

	def _set_key_eval(self, new_val: str, use_config: bool = False) -> None:
		value = get_config_value(self._config, 'KEYBINDS', 'sEvaluateKey', new_val, use_config)
		validate_type(new_val, str)
		self._key_eval = value
		bind_event(self._win_txt_input, self._key_eval, command=self.evaluate)
		self._add_bound_key(self._key_eval)

	def _set_key_help(self, new_val: str, use_config: bool = False) -> None:
		value = get_config_value(self._config, 'KEYBINDS', 'sHelpKey', new_val, use_config)
		validate_type(new_val, str)
		self._key_help = value

	def _set_key_options(self, new_val: str, use_config: bool = False) -> None:
		value = get_config_value(self._config, 'KEYBINDS', 'sOptionsKey', new_val, use_config)
		validate_type(new_val, str)
		self._key_options = value

	def _set_key_redo(self, new_val: str, use_config: bool = False) -> None:
		value = get_config_value(self._config, 'KEYBINDS', 'sRedoKey', new_val, use_config)
		validate_type(new_val, str)
		self._key_redo = value

	def _set_key_undo(self, new_val: str, use_config: bool = False) -> None:
		value = get_config_value(self._config, 'KEYBINDS', 'sUndoKey', new_val, use_config)
		validate_type(new_val, str)
		self._key_undo = value

	def _set_win_advanced_def(self, new_val: bool, use_config: bool = False) -> None:
		value = get_config_value(self._config, 'WIN_FLAGS', 'bStartAdvanced', new_val, use_config)
		validate_type(new_val, bool)
		self._win_advanced_def = value

	def _set_win_force_focus(self, new_val: bool, use_config: bool = False) -> None:
		value = get_config_value(self._config, 'DEBUG', 'bForceFocus', new_val, use_config)
		validate_type(new_val, bool)
		self._win_force_focus = value

	def _set_win_height_adv(self, new_val: int, use_config: bool = False) -> None:
		value = get_config_value(self._config, 'WIN_ADV', 'iDefaultHeight', new_val, use_config)
		try:
			value = self._win_height_min_adv if value < self._win_height_min_adv else value
		except AttributeError:
			pass # ignore if self._win_height_min_adv is not set
		validate_type(value, int)
		value = 0 if value < 0 else value
		self._win_height_adv = value

	def _set_win_height_min_adv(self, new_val: int, use_config: bool = False) -> None:
		value = get_config_value(self._config, 'WIN_ADV', 'iMinHeight', new_val, use_config)
		validate_type(value, int)
		value = 0 if value < 0 else value
		self._win_height_min_adv = value

	def _set_win_restore(self, new_val: bool, use_config: bool = False) -> None:
		value = get_config_value(self._config, 'WIN_RESTORE', 'bRestoreMode', new_val, use_config)
		validate_type(new_val, bool)
		self._win_restore = value

	def _set_win_restore_adv(self, new_val: bool, use_config: bool = False) -> None:
		value = get_config_value(self._config, 'WIN_RESTORE', 'bRestoreAdvanced', new_val, use_config)
		try:
			value = False if not self._win_restore else value
		except AttributeError:
			pass # ignore if self._win_restore is not set
			#value = False # disable if self._win_restore is not set
		validate_type(new_val, bool)
		self._win_restore_adv = value

	def _set_win_restore_dim(self, new_val: bool, use_config: bool = False) -> None:
		value = get_config_value(self._config, 'WIN_RESTORE', 'bRestoreDimensions', new_val, use_config)
		try:
			value = False if not self._win_restore else value
		except AttributeError:
			pass # ignore if self._win_restore is not set
			#value = False # disable if self._win_restore is not set
		validate_type(new_val, bool)
		self._win_restore_dim = value

	def _set_win_restore_pin(self, new_val: bool, use_config: bool = False) -> None:
		value = get_config_value(self._config, 'WIN_RESTORE', 'bRestorePinned', new_val, use_config)
		try:
			value = False if not self._win_restore else value
		except AttributeError:
			pass # ignore if self._win_restore is not set
			#value = False # disable if self._win_restore is not set
		validate_type(new_val, bool)
		self._win_restore_pin = value

	def _set_win_restore_pos(self, new_val: bool, use_config: bool = False) -> None:
		value = get_config_value(self._config, 'WIN_RESTORE', 'bRestorePosition', new_val, use_config)
		try:
			value = False if not self._win_restore else value
		except AttributeError:
			pass # ignore if self._win_restore is not set
			#value = False # disable if self._win_restore is not set
		validate_type(new_val, bool)
		self._win_restore_pos = value

	def _set_win_width_adv(self, new_val: int, use_config: bool = False) -> None:
		value = get_config_value(self._config, 'WIN_ADV', 'iDefaultWidth', new_val, use_config)
		try:
			value = self._win_width_min_adv if value < self._win_width_min_adv else value
		except AttributeError:
			pass # ignore if self._win_width_min_adv is not set
		validate_type(value, int)
		value = 0 if value < 0 else value
		self._win_width_adv = value

	def _set_win_width_min_adv(self, new_val: int, use_config: bool = False) -> None:
		value = get_config_value(self._config, 'WIN_ADV', 'iMinWidth', new_val, use_config)
		validate_type(value, int)
		value = 0 if value < 0 else value
		self._win_width_min_adv = value

	def _show_element(self, element: str) -> None:
		if self._win_layout == 'grid':
			element.grid()
		elif self._win_layout == 'pack':
			element.pack()
		else:
			raise ValueError(f"Invalid layout: {self._win_layout}. Must be 'grid' or 'pack'")


	# public methods
	def display_result(self, message: Any, logging: bool = True, delay: bool = False) -> None:
		if delay:
			self._timeout_id = self._window.after(self._calc_live_eval_delay, self.display_result, message, logging, False)
			return
		message = str(message)
		#message = message.replace('\n', '\\n')
		text_set(self._win_txt_result, message)
		if logging:
			self._logging_print(f"Result:{' '*14}`{message.replace('\n', '\\n')}`")
			#self._logging_print(f"Result:{' '*14}`{message}`")

	def evaluate(self, live_mode: bool = False) -> None:
		# get input
		input_expr = self._win_txt_input.get()
		self._logging_print(f"Expression:{' '*10}`{input_expr.replace('\n', '\\n')}`")
		# handle live mode
		if self._timeout_id is not None:
			self._window.after_cancel(self._timeout_id)
			self._timeout_id = None
		# check if the expression is valid
		try:
			expr = sanitize_input(input_expr, sanitize=self._sanitize_input)
			if not expr:
				self.display_result(self._calc_def_result)
				return
		except ValueError as e:
			self.display_result(f"ERROR: {e}")
			return
		# evaluate the expression
		try:
			self._logging_print(f"Evaluating...")
			result = evaluate_expression(expr, approximate=self._approximate, dec_precision=self.calc_dec_precicion, dec_display=self.calc_dec_display)
			self.calc_last_result = result
			self.display_result(result)
			return
		except ZeroDivisionError as e:
			#self.display_result('Undefined (division by zero)')
			#self.display_result(f"Undefined: {e}")
			#self.display_result(f"Undefined")
			self.display_result(e)
			return
		except Exception as e:
			if live_mode and self._timeout_patience > 0 and expr and expr[-1] in self._calc_wait_chars:
				#self.display_result(self._calc_last_result, logging=False) # temporarily show last result
				self.display_result('ERROR: Incomplete expression', delay=True) # then show error
				return
			elif live_mode and self._timeout_patience > 1:
				#self.display_result(self._calc_last_result, logging=False) # temporarily show last result
				self.display_result(f"ERROR: {e}", delay=True) # then show error
				return
			else:
				self.display_result(f"ERROR: {e}")
				return



	def open_window(self) -> None: # override
		self._logging_print(f"Opening {self.name}.")
		#self._logging_print()
		if self._win_force_focus:
			self._logging_print('Forcing window focus.')
			self.focus_window()
		self._window.after(100, lambda: focus_element(self._win_txt_input))
		self._window.mainloop()

	def print_info(self) -> None: # override
		GuiApp.print_info(self)
		data = []
		data.append(f"History File: {self._history_path}")
		for line in data:
			self._logging_print(line)

	def toggle_advanced(self) -> None:
		if not self._win_expanded:
			#self._win_frame_adv.grid(row=1, column=0, padx=0, pady=0, sticky='NSEW')
			self._show_element(self._win_frame_adv)
			self._win_btn_adv.configure(text='Collapse')
			self._win_expanded = True
			self.win_resize_height = True
			self.update_window(reset_width=False, reset_height=False)
		else:
			#self._win_frame_adv.grid_forget()
			self._hide_element(self._win_frame_adv)
			self._win_btn_adv.configure(text='Expand')
			self._win_expanded = False
			self.win_resize_height = False
			self.update_window(reset_width=True, reset_height=True)
		self._logging_print(f"Advanced = {self._win_expanded}")
		#self._logging_print(f"Viewable = {self._win_frame_adv.winfo_viewable()}")

	def toggle_pinned(self) -> None: # override
		if not self._win_pinned:
			self._window.attributes('-topmost', True)
			self._win_pinned = True
			try:
				self._win_btn_pin.configure(text='Unpin')
			except AttributeError:
				pass
		else:
			self._window.attributes('-topmost', False)
			self._win_pinned = False
			try:
				self._win_btn_pin.configure(text='Pin')
			except AttributeError:
				pass
		self._logging_print(f"Pinned = {self._win_pinned}")

	def update_window(self, reset_pos: bool = False, reset_width: bool = False, reset_height: bool = False) -> None: # override
		self._screen_width, self._screen_height = self.screen_dimensions
		#print(f"Screen Dimensions (W x H): {self.screen_dimensions[0]} x {self.screen_dimensions[1]}")
		if reset_pos:
			current_width = self._win_width_def
			current_height = self._win_height_def
		else:
			current_width, current_height = self.window_dimensions
		#print(f"Window Dimensions (W x H): {self.window_dimensions[0]} x {self.window_dimensions[1]}")
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
		#print(f"Target Position: ({target_x_pos}, {target_y_pos})")
		try:
			expanded = True if self._win_expanded else False
		except AttributeError:
			expanded = False
		if expanded:
			if reset_width:
				target_width = self._win_width_adv
			else:
				target_width = current_width if current_width > self._win_width_min_adv else self._win_width_min_adv
				#target_width = current_width if current_width > self._win_width_adv else self._win_width_adv
			if reset_height:
				target_height = self._win_height_adv
			else:
				target_height = current_height if current_height > self._win_height_min_adv else self._win_height_min_adv
				#target_height = current_height if current_height > self._win_height_adv else self._win_height_adv
			self._window.minsize(self._win_width_min_adv, self._win_height_min_adv)
		else:
			if reset_width:
				target_width = self._win_width_def
			else:
				target_width = current_width if current_width > self._win_width_min else self._win_width_min
				#target_width = current_width if current_width > self._win_width_def else self._win_width_def
				#target_width = current_width if current_width > self._win_width_adv else self._win_width_adv
			if reset_height:
				target_height = self._win_height_def
			else:
				target_height = current_height if current_height > self._win_height_min else self._win_height_min
				#target_height = current_height if current_height > self._win_height_def else self._win_height_def
			self._window.minsize(self._win_width_min, self._win_height_min)
		self._window.geometry(f"{target_width}x{target_height}+{target_x_pos}+{target_y_pos}")
		self._window.resizable(self._win_resize_width, self._win_resize_height)
		self._win_width, self._win_height = self.window_dimensions
		self._win_x_pos, self._win_y_pos = self.window_position
		#self._window.update()
		#print('Window updated.')

	# properties
	@property
	def calc_dec_display(self) -> int:
		return self._calc_dec_display

	@property
	def calc_dec_precicion(self) -> int:
		return self._calc_dec_precision

	@property
	def calc_def_expr(self) -> str:
		return self._calc_def_expr

	@property
	def calc_def_result(self) -> str:
		return self._calc_def_result

	@property
	def calc_last_expr(self) -> str:
		return self._calc_last_expr

	@property
	def calc_last_result(self) -> str:
		return self._calc_last_result
	@calc_last_result.setter
	def calc_last_result(self, new_val: str) -> None:
		validate_type(new_val, str)
		self._calc_last_result = new_val

	@property
	def calc_wait_chars(self) -> str:
		return self._calc_wait_chars

	@property
	def clipboard(self) -> str:
		return self._window.clipboard_get()

	@property
	def timeout_id(self) -> int | None:
		return self._timeout_id
	@timeout_id.setter
	def timeout_id(self, new_val: int | None) -> None:
		validate_type(new_val, int | None)
		self._timeout_id = new_val

	@property
	def timeout_patience(self) -> int:
		return self._timeout_patience

	#@property
	#def win_expanded(self) -> bool:
	#	return self._win_expanded
	#@win_expanded.setter
	#def win_expanded(self, new_val: bool) -> None:
	#	validate_type(new_val, bool)
	#	self._win_expanded = new_val

	@property
	def win_frame_adv(self) -> ctk.CTkFrame:
		return self._win_frame_adv

	@property
	def win_resize_height(self) -> bool:
		return self._win_resize_height
	@win_resize_height.setter
	def win_resize_height(self, new_val: bool) -> None:
		validate_type(new_val, bool)
		self._win_resize_height = new_val



### TESTING ###

def _test():
	#app = App('Test', '0.0.1', 'GroundAura')
	#app = GuiApp('Test App', '0.0.1', 'GroundAura')
	app = CalculatorApp('Test App', '0.0.1', 'GroundAura', win_centered=True, config_file='AuraCalc.ini', use_config=False)

	#print(app.window_position)
	app.print_info()
	#app.update_window()
	#app.print_info()
	app.open_window()



if __name__ == '__main__':
	_test()


