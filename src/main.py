### IMPORTS ###

# builtins
#from decimal import Decimal, getcontext, InvalidOperation, ROUND_HALF_UP
#import math
#from pathlib import Path
#import random
#import sys
#import tkinter as tk

# external
import customtkinter as ctk

# internal
#from app_globals import *
import app_globals
from app_debug import print_debug
from app_evaluate import evaluate_expression, sanitize_input
from app_keybinds import keybind_enabled
from app_window import clear_io, close_window, display_result, toggle_advanced, focus_element, pin_window, update_window



### FUNCTIONS ###

def delayed_display(window: ctk.CTk, output_element, message: str) -> None:
	"""
	Displays the result in the the output element after a delay.

	Args:
		window (ctk.CTk): The window to display the result in.
		output_element: The element to display the result in.
		message (str): The message to display in the output element.
	"""
	#if app_globals.TIMEOUT_ID is not None:
	#	window.after_cancel(app_globals.TIMEOUT_ID)
	#	app_globals.TIMEOUT_ID = None
	app_globals.TIMEOUT_ID = window.after(app_globals.TIMEOUT_DURATION, lambda: display_result(output_element, message))
	display_result(output_element, app_globals.LAST_RESULT)

def evaluate_input(window, input_element, output_element, live_mode: bool = False) -> None:
	"""
	Evaluates or simplifies the expression in the input element and displays the result in the output element.

	Args:
		window (ctk.CTk): The window to display the result in.
		input_element: The element to get the expression to evaluate from.
		output_element: The element to display the result in.
		live_mode (bool, optional): Whether to update the result in real-time. Defaults to `False`.
	"""
	expression = input_element.get()
	if app_globals.TIMEOUT_ID is not None:
		window.after_cancel(app_globals.TIMEOUT_ID)
		app_globals.TIMEOUT_ID = None
	print_debug(f"Expr (initial):{' '*6}`{expression}`")
	if not expression:
		display_result(output_element, app_globals.DEF_RESULT)
		return
	try:
		expression = sanitize_input(expression)
		result = evaluate_expression(expression)
		display_result(output_element, result)
		return
	except ZeroDivisionError:
		display_result(output_element, "Undefined (division by zero)")
		return
	except Exception as e:
		if live_mode and app_globals.PATIENCE > 0 and expression[-1] in app_globals.WAIT_CHARS:
			delayed_display(window, output_element, "ERROR: Incomplete expression")
			return
		elif live_mode and app_globals.PATIENCE > 1:
			delayed_display(window, output_element, f"ERROR: {e}")
			return
		else:
			display_result(output_element, f"ERROR: {e}")
			return
	#except Exception as e:
	#	if live_mode and app_globals.PATIENCE > 1:
	#		delayed_display(window, output_element, f"ERROR: {e}")
	#		return
	#	else:
	#		display_result(output_element, f"ERROR: {e}")
	#		return



### MAIN ###

def main():
	### WINDOW SETUP ###

	# Initialize window
	print_debug(f"{app_globals.NAME} v{app_globals.VERSION} by {app_globals.AUTHOR}")
	print_debug("Initializing...")
	root = ctk.CTk()
	root.title(app_globals.NAME)
	update_window(root, def_pos=True)

	# Configure theme
	root.iconbitmap(app_globals.ICON_FILE)
	ctk.set_appearance_mode("dark")
	ctk.set_default_color_theme("green")

	# Configure grid
	root.grid_columnconfigure(0, weight=1)
	#root.grid_columnconfigure(1, weight=1)
	#root.grid_columnconfigure(2, weight=1)
	#root.grid_columnconfigure(3, weight=1)

	root.grid_rowconfigure(0, weight=0)
	root.grid_rowconfigure(1, weight=1)
	#root.grid_rowconfigure(2, weight=0)

	# Configure padding
	x_padding = 2

	y_padding = 3
	#y_pad_try = window_height / 2 - 25
	#y_padding = y_pad_try if y_pad_try > 5 and window_height > 100 else 5



	### FRAME SETUP ###

	# Basic calculator frame
	basic_frame = ctk.CTkFrame(root)
	basic_frame.grid(row=0, column=0, padx=0, pady=0, sticky="NSEW")
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
	advanced_frame = ctk.CTkFrame(root)
	#advanced_frame.grid(row=1, column=0, padx=0, pady=0, sticky="NSEW")



	### GUI ELEMENTS ###
	layer = basic_frame

	# Entry Input Element (CTkEntry)
	entry_input = ctk.CTkEntry(layer)
	entry_input.grid(row=2, column=0, columnspan=5, sticky="NEW", padx=x_padding, pady=y_padding)
	entry_input.insert(ctk.END, app_globals.DEF_EXPRESSION)

	# Result Display Element (CTkTextbox)
	result_display = ctk.CTkTextbox(layer, height=1)
	result_display.grid(row=3, column=0, columnspan=5, sticky="NEW", padx=x_padding, pady=y_padding)
	result_display.insert(ctk.END, app_globals.DEF_RESULT)
	result_display.configure(state="disabled")

	# Pin Window ELement (CTkButton)
	pin_button = ctk.CTkButton(layer, text="Pin", command=lambda: pin_window(root, pin_button), width=30)
	pin_button.grid(row=4, column=0, columnspan=1, sticky="NEW", padx=x_padding, pady=y_padding)
	if app_globals.START_PINNED:
		pin_window(root, pin_button)

	# Clear Entry/Result Element (CTkButton)
	clear_button = ctk.CTkButton(layer, text="Clear", command=lambda: clear_io(entry_input, result_display), width=30)
	clear_button.grid(row=4, column=1, columnspan=3, sticky="NEW", padx=x_padding, pady=y_padding)

	# Advanced View Element (CTkButton)
	advanced_button = ctk.CTkButton(layer, text="Expand", command=lambda: toggle_advanced(root, advanced_frame, advanced_button), width=30)
	advanced_button.grid(row=4, column=4, columnspan=1, sticky="NEW", padx=x_padding, pady=y_padding)
	if app_globals.START_ADVANCED:
		toggle_advanced(advanced_frame, advanced_button)



	### EVENT HANDLING ###

	# Keybinds
	if keybind_enabled(app_globals.ADVANCED_KEY):
		root.bind(app_globals.ADVANCED_KEY, lambda event: toggle_advanced(root, advanced_frame, advanced_button))
	if keybind_enabled(app_globals.CLEAR_KEY):
		root.bind(app_globals.CLEAR_KEY, lambda event: clear_io(entry_input, result_display))
	if keybind_enabled(app_globals.DELETE_LEFT_KEY):
		entry_input.bind(app_globals.DELETE_LEFT_KEY, lambda event: entry_input.delete(0, ctk.INSERT))
	if keybind_enabled(app_globals.DELETE_RIGHT_KEY):
		entry_input.bind(app_globals.DELETE_RIGHT_KEY, lambda event: entry_input.delete(ctk.INSERT, ctk.END))
	#if keybind_enabled(app_globals.DELETE_TERM_LEFT_KEY):
	#	entry_input.bind(app_globals.DELETE_TERM_LEFT_KEY, lambda event: delete_term(result_display, "L"))
	#if keybind_enabled(app_globals.DELETE_TERM_RIGHT_KEY):
	#	entry_input.bind(app_globals.DELETE_TERM_RIGHT_KEY, lambda event: delete_term(result_display, "R"))
	if keybind_enabled(app_globals.EVALUATE_KEY):
		entry_input.bind(app_globals.EVALUATE_KEY, lambda event: evaluate_input(root, entry_input, result_display, live_mode=False))
	#if keybind_enabled(app_globals.HELP_KEY):
	#	root.bind(app_globals.HELP_KEY, lambda event: toggle_help(root, help_frame, help_button))
	#if keybind_enabled(app_globals.OPTIONS_KEY):
	#	root.bind(app_globals.OPTIONS_KEY, lambda event: toggle_options(root, options_frame, options_button))
	if keybind_enabled(app_globals.QUIT_KEY):
		root.bind(app_globals.QUIT_KEY, lambda event: close_window(root))

	# Key release
	if app_globals.LIVE_EVAL:
		entry_input.bind("<KeyRelease>", lambda event: evaluate_input(root, entry_input, result_display, live_mode=True))

	# Window close
	root.protocol("WM_DELETE_WINDOW", lambda: close_window(root))



	### FINAL INITIALIZATION ###

	# Set focus
	if app_globals.FORCE_FOCUS:
		print_debug("Forcing window focus")
		root.focus_force()
	root.after(100, lambda: focus_element(entry_input))

	# Start main loop
	print_debug("Initialization complete!")
	root.mainloop()

if __name__ == "__main__":
	main()


