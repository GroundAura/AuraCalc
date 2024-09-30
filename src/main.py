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
from app_evaluate import evaluate_expression
from app_window import center_window, clear_io, close_window, display_result, expand_options, focus_element, pin_window



### FUNCTIONS ###

def on_key_release(window, input_element, output_element):
	"""
	Executes when a key is released.
	Evaluates the expression in the `entry_input` element and updates the `result_display` element.
	"""
	expression = input_element.get()
	if app_globals.TIMEOUT_ID is not None:
		window.after_cancel(app_globals.TIMEOUT_ID)
		app_globals.TIMEOUT_ID = None
	try:
		result = evaluate_expression(expression)
		print(f"Expr (10: final):{' '*7}`{result.replace('\n', '  ')}`\n")
		if expression and expression[-1] in app_globals.WAIT_CHARS:
			app_globals.TIMEOUT_ID = window.after(app_globals.TIMEOUT_DURATION, lambda: display_result(output_element, "Incomplete expression"))
			display_result(output_element, app_globals.LAST_RESULT)
		else:
			display_result(output_element, result)
	except ValueError:
		app_globals.TIMEOUT_ID = window.after(app_globals.TIMEOUT_DURATION, lambda: display_result(output_element, "Invalid characters in expression"))
		display_result(output_element, app_globals.LAST_RESULT)



### MAIN ###

def main():
	### WINDOW SETUP ###

	# Initialize window
	print("Starting application...")
	root = ctk.CTk()

	# Configure window
	root.title("AuraCalc")
	#root.geometry(f"{app_globals.WIDTH}x{app_globals.HEIGHT}")
	center_window(root)
	root.minsize(app_globals.WIDTH, app_globals.HEIGHT)
	root.resizable(width=True, height=False)

	# Theme
	root.iconbitmap(app_globals.ICON_FILE)
	ctk.set_appearance_mode("dark")
	ctk.set_default_color_theme("green")

	# Configure grid
	root.grid_columnconfigure(0, weight=1)
	root.grid_columnconfigure(1, weight=1)
	root.grid_columnconfigure(2, weight=1)
	root.grid_columnconfigure(3, weight=1)

	root.grid_rowconfigure(0, weight=0)
	root.grid_rowconfigure(1, weight=0)
	root.grid_rowconfigure(2, weight=0)

	# Configure padding
	x_padding = 2

	y_padding = 3
	#y_pad_try = window_height / 2 - 25
	#y_padding = y_pad_try if y_pad_try > 5 and window_height > 100 else 5



	### GUI ELEMENTS ###

	# Entry Input Element (CTkEntry)
	entry_input = ctk.CTkEntry(root)
	entry_input.grid(row=0, column=0, columnspan=5, sticky="new", padx=x_padding, pady=y_padding)
	entry_input.insert(ctk.END, app_globals.DEF_EXPRESSION)

	# Result Display Element (CTkTextbox)
	result_display = ctk.CTkTextbox(root, height=1)
	result_display.grid(row=1, column=0, columnspan=5, sticky="new", padx=x_padding, pady=y_padding)
	result_display.insert(ctk.END, app_globals.DEF_RESULT)
	result_display.configure(state="disabled")

	# Pin Window ELement (CTkButton)
	pin_button = ctk.CTkButton(root, text="Pin", command=lambda: pin_window(root, pin_button), width=30)
	pin_button.grid(row=2, column=0, columnspan=1, sticky="new", padx=x_padding, pady=y_padding)
	if app_globals.DEF_PINNED:
		pin_window(root, pin_button)

	# Clear Entry/Result Element (CTkButton)
	clear_button = ctk.CTkButton(root, text="Clear", command=lambda: clear_io(entry_input, result_display), width=30)
	clear_button.grid(row=2, column=1, columnspan=3, sticky="new", padx=x_padding, pady=y_padding)

	# Expand Options Element (CTkButton)
	expand_button = ctk.CTkButton(root, text="Expand", command=lambda: expand_options(root, expand_button), width=30)
	expand_button.grid(row=2, column=4, columnspan=1, sticky="new", padx=x_padding, pady=y_padding)
	if app_globals.DEF_EXPANDED:
		expand_options(root, expand_button)



	### APP FUNCTIONALITY ###

	# Focus
	root.focus_force()
	root.after(100, lambda: focus_element(entry_input))
	#entry.focus_set()

	# Keybinds
	root.bind("<Escape>", lambda event: close_window(root))
	entry_input.bind("<KeyRelease>", lambda event: on_key_release(root, entry_input, result_display))

	# Close app
	root.protocol("WM_DELETE_WINDOW", lambda: close_window(root))

	# Set saved statuses
	#pin_window(root, pin_button)
	#if app_globals.PINNED:
	#	root.after(1000, lambda: pin_window(root, pin_button))
	#if app_globals.EXPANDED:
	#	root.after(1000, lambda: expand_options(expand_button))

	# Main loop
	root.mainloop()

if __name__ == "__main__":
	main()


