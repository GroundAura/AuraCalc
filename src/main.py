### IMPORTS ###

# builtins
#import tkinter as tk
#from tkinter import ttk

# external
import customtkinter as ctk
#import PyQt6 as pyqt
#import tkinterdnd2 as tkdnd
#import tkinterplus as tkp

# internal
from app_class import CalculatorApp
from app_debug import print_debug
from app_evaluate import evaluate_expression, sanitize_input
from app_keybinds import keybind_enabled
from app_window import clear_io, display_result, toggle_advanced, focus_element, pin_window



### FUNCTIONS ###

def delayed_display(app, output_element, message: str) -> None:
	"""
	Displays the result in the the output element after a delay.

	Args:
		app: The application instance.
		output_element: The element to display the result in.
		message (str): The message to display in the output element.
	"""
	#if app.timeout_id is not None:
	#	app.window.after_cancel(app.timeout_id)
	#	app.timeout_id = None
	#app.timeout_id = app.window.after(app._calc_live_eval_delay, lambda: display_result(app, output_element, message))
	app.delayed_func(lambda: display_result(app, output_element, message))
	display_result(app, output_element, app.calc_last_result)

def evaluate_input(app, input_element, output_element, live_mode: bool = False) -> None:
	"""
	Evaluates or simplifies the expression in the input element and displays the result in the output element.

	Args:
		app: The application instance.
		input_element: The element to get the expression to evaluate from.
		output_element: The element to display the result in.
		live_mode (bool, optional): Whether to update the result in real-time. Defaults to `False`.
	"""
	expression = input_element.get()
	if app.timeout_id is not None:
		app.window.after_cancel(app.timeout_id)
		app.timeout_id = None
	app.log_debug(f"Expr (initial):{' '*6}`{expression}`")
	if not expression:
		display_result(app, output_element, app.calc_def_result)
		return
	try:
		expression = sanitize_input(app, expression, sanitize=app._sanitize_input)
		result = evaluate_expression(app, expression, dont_evaluate=app._only_simplify)
		display_result(app, output_element, result)
		return
	except ZeroDivisionError:
		display_result(app, output_element, 'Undefined (division by zero)')
		return
	except Exception as e:
		if live_mode and app.timeout_patience > 0 and expression[-1] in app.calc_wait_chars:
			delayed_display(app, output_element, 'ERROR: Incomplete expression')
			return
		elif live_mode and app.timeout_patience > 1:
			delayed_display(app, output_element, f"ERROR: {e}")
			return
		else:
			display_result(app, output_element, f"ERROR: {e}")
			return
	#except Exception as e:
	#	if live_mode and app.timeout_patience > 1:
	#		delayed_display(app, output_element, f"ERROR: {e}")
	#		return
	#	else:
	#		display_result(app, output_element, f"ERROR: {e}")
	#		return



### MAIN ###

def main():
	### METADATA ###

	meta_name: str = 'AuraCalc'
	meta_version: str = '0.3.0-alpha'
	meta_author: str = 'GroundAura'

	resources_dir: str = 'resources'
	config_file: str = f"{meta_name}.ini"
	history_file: str = 'history.json'
	icon_file: str = 'icon.ico'
	log_file: str = 'debug.log'



	### WINDOW SETUP ###

	# Initialize window
	print_debug(f"{meta_name} v{meta_version} by {meta_author}")
	print_debug('Initializing...')
	app = CalculatorApp(
		name=meta_name,
		version=meta_version,
		author=meta_author,
		resources_dir = resources_dir,
		history_file = history_file,
		icon_file = icon_file,
		log_file = log_file,
		config_file = config_file,
		use_config = True,
	)
	#root = app.window

	# Configure theme
	ctk.set_appearance_mode('dark')
	ctk.set_default_color_theme('green')
	#tk.ttk.Style().theme_use('clam')

	# Configure grid
	app.window.grid_columnconfigure(0, weight=1)
	#app.window.grid_columnconfigure(1, weight=1)
	#app.window.grid_columnconfigure(2, weight=1)
	#app.window.grid_columnconfigure(3, weight=1)

	app.window.grid_rowconfigure(0, weight=0)
	app.window.grid_rowconfigure(1, weight=1)
	#app.window.grid_rowconfigure(2, weight=0)

	# Configure padding
	x_padding = 2

	y_padding = 3
	#y_pad_try = window_height / 2 - 25
	#y_padding = y_pad_try if y_pad_try > 5 and window_height > 100 else 5



	### FRAME SETUP ###

	# Basic calculator frame
	basic_frame = ctk.CTkFrame(app.window)
	basic_frame.grid(row=0, column=0, padx=0, pady=0, sticky='NSEW')
	#print_debug(basic_frame.winfo_pointerxy())
	#print_debug(basic_frame.winfo_manager())
	#print_debug(basic_frame.winfo_screen())
	basic_frame.grid_columnconfigure(0, weight=1)
	basic_frame.grid_columnconfigure(1, weight=1)
	basic_frame.grid_columnconfigure(2, weight=1)
	basic_frame.grid_columnconfigure(3, weight=1)

	basic_frame.grid_rowconfigure(0, weight=0)
	basic_frame.grid_rowconfigure(1, weight=0)
	basic_frame.grid_rowconfigure(2, weight=0)

	## Advanced calculator frame
	advanced_frame = ctk.CTkFrame(app.window)
	#advanced_frame.grid(row=1, column=0, padx=0, pady=0, sticky='NSEW')



	### MENU BAR SETUP ###

	## Create the menu bar
	#menu_bar = tk.Menu(app.window)

	## Create the File menu
	#file_menu = tk.Menu(menu_bar, tearoff=0, activebackground='#106a43')
	#file_menu.add_command(label='Exit', command=app.close_window)
	###file_menu.grid(row=0, column=0, padx=x_padding, pady=y_padding)

	## Add the menus to the menu bar
	#menu_bar.add_cascade(label='File', menu=file_menu)
	#app.window.config(menu=menu_bar)



	### GUI ELEMENTS ###
	layer = basic_frame

	# Entry Input Element (CTkEntry)
	entry_input = ctk.CTkEntry(layer)
	entry_input.grid(row=2, column=0, columnspan=5, sticky='NEW', padx=x_padding, pady=y_padding)
	entry_input.insert(ctk.END, app.calc_def_expr)

	# Result Display Element (CTkTextbox)
	result_display = ctk.CTkTextbox(layer, height=1)
	result_display.grid(row=3, column=0, columnspan=5, sticky='NEW', padx=x_padding, pady=y_padding)
	result_display.insert(ctk.END, app.calc_def_result)
	result_display.configure(state='disabled')

	# Pin Window ELement (CTkButton)
	pin_button = ctk.CTkButton(layer, text='Pin', command=lambda: pin_window(app, pin_button), width=30)
	pin_button.grid(row=4, column=0, columnspan=1, sticky='NEW', padx=x_padding, pady=y_padding)
	if app._win_pinned_def:
		pin_window(app, pin_button)

	# Clear Entry/Result Element (CTkButton)
	clear_button = ctk.CTkButton(layer, text='Clear', command=lambda: clear_io(app, entry_input, result_display), width=30)
	clear_button.grid(row=4, column=1, columnspan=3, sticky='NEW', padx=x_padding, pady=y_padding)

	# Advanced View Element (CTkButton)
	advanced_button = ctk.CTkButton(layer, text='Expand', command=lambda: toggle_advanced(app, advanced_frame, advanced_button), width=30)
	advanced_button.grid(row=4, column=4, columnspan=1, sticky='NEW', padx=x_padding, pady=y_padding)
	if app._win_advanced_def:
		toggle_advanced(app, advanced_frame, advanced_button)



	### EVENT HANDLING ###

	# Keybinds
	if keybind_enabled(app._key_advanced):
		app.window.bind(app._key_advanced, lambda event: toggle_advanced(app, advanced_frame, advanced_button))
	if keybind_enabled(app._key_clear):
		app.window.bind(app._key_clear, lambda event: clear_io(app, entry_input, result_display))
	if keybind_enabled(app._key_del_l):
		entry_input.bind(app._key_del_l, lambda event: entry_input.delete(0, ctk.INSERT))
	if keybind_enabled(app._key_del_r):
		entry_input.bind(app._key_del_r, lambda event: entry_input.delete(ctk.INSERT, ctk.END))
	#if keybind_enabled(app._key_del_term_l):
	#	entry_input.bind(app._key_del_term_l, lambda event: delete_term(result_display, 'L'))
	#if keybind_enabled(app._key_del_term_r):
	#	entry_input.bind(app._key_del_term_r, lambda event: delete_term(result_display, 'R'))
	if keybind_enabled(app._key_eval):
		entry_input.bind(app._key_eval, lambda event: evaluate_input(app, entry_input, result_display, live_mode=False))
	#if keybind_enabled(app._key_help):
	#	app.window.bind(app._key_help, lambda event: toggle_help(app.window, help_frame, help_button))
	#if keybind_enabled(app._key_options):
	#	app.window.bind(app._key_options, lambda event: toggle_options(app.window, options_frame, options_button))
	if keybind_enabled(app._key_quit):
		app.window.bind(app._key_quit, lambda event: app.close_window())

	# Key release
	if app._calc_live_eval:
		entry_input.bind('<KeyRelease>', lambda event: evaluate_input(app, entry_input, result_display, live_mode=True))



	### FINAL INITIALIZATION ###

	# Set focus
	if app._win_force_focus:
		print_debug('Forcing window focus')
		app.focus_window()
	app.window.after(100, lambda: focus_element(entry_input))

	# Start main loop
	print_debug('Initialization complete!')
	app.open_window()

if __name__ == '__main__':
	main()


