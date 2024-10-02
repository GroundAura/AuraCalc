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
from app_evaluate import evaluate_expression, sanitize_input
from app_window import clear_io, close_window, display_result, expand_options, focus_element, pin_window, update_window



### FUNCTIONS ###

def evaluate_input(window, input_element, output_element, live_mode: bool = False) -> None:
	"""
	Evaluates or simplifies the expression in the `entry_input` element and displays the result in the `result_display` element.
	"""
	expression = input_element.get()
	if app_globals.TIMEOUT_ID is not None:
		window.after_cancel(app_globals.TIMEOUT_ID)
		app_globals.TIMEOUT_ID = None
	if app_globals.DEBUG:
		print(f"Expr (initial):{' '*6}`{expression}`")
	if not expression:
		display_result(output_element, app_globals.LAST_RESULT)
		return
	try:
		expression = sanitize_input(expression)
		result = evaluate_expression(expression)
		display_result(output_element, result)
		return
	except Exception as e:
		if live_mode and app_globals.PATIENCE > 0 and expression[-1] in app_globals.WAIT_CHARS:
			delayed_display(window, output_element, f"ERROR: Incomplete expression")
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

def delayed_display(window, output_element, message: str) -> None:
	#if app_globals.TIMEOUT_ID is not None:
	#	window.after_cancel(app_globals.TIMEOUT_ID)
	#	app_globals.TIMEOUT_ID = None
	app_globals.TIMEOUT_ID = window.after(app_globals.TIMEOUT_DURATION, lambda: display_result(output_element, message))
	display_result(output_element, app_globals.LAST_RESULT)



### MAIN ###

def main():
	### WINDOW SETUP ###

	# Initialize window
	print("Starting application...")
	root = ctk.CTk()

	# Configure window
	root.title("AuraCalc")
	update_window(root, update_pos=True)

	# Theme
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
	#print(basic_frame.winfo_pointerxy())
	#print(basic_frame.winfo_manager())
	#print(basic_frame.winfo_screen())
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

	# Expand Options Element (CTkButton)
	expand_button = ctk.CTkButton(layer, text="Expand", command=lambda: expand_options(root, advanced_frame, expand_button), width=30)
	expand_button.grid(row=4, column=4, columnspan=1, sticky="NEW", padx=x_padding, pady=y_padding)
	if app_globals.START_EXPANDED:
		expand_options(advanced_frame, expand_button)



	### APP FUNCTIONALITY ###

	# Focus
	#root.focus_force()
	root.after(100, lambda: focus_element(entry_input))
	#entry.focus_set()

	# Keybinds
	root.bind("<Escape>", lambda event: close_window(root))
	if app_globals.LIVE_EVAL:
		entry_input.bind("<KeyRelease>", lambda event: evaluate_input(root, entry_input, result_display, live_mode=True))

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


