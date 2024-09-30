### IMPORTS ###

# builtins

# external
import customtkinter as ctk

# internal
import app_globals
#from app_history import save_history



### FUNCTIONS ###

def center_window(window):
	"""
	Centers the window on the screen.
	"""
	app_globals.X_POS = (window.winfo_screenwidth() // 2) - (app_globals.WIDTH // 2)
	app_globals.Y_POS = (window.winfo_screenheight() // 2) - (app_globals.HEIGHT // 2)
	window.geometry(f"{app_globals.WIDTH}x{app_globals.HEIGHT}+{app_globals.X_POS}+{app_globals.Y_POS}")

def clear_io(input_element, output_element):
	"""
	Clears the input and output elements.
	"""
	input_element.delete(0, ctk.END)
	input_element.insert(0, app_globals.DEF_EXPRESSION)
	focus_element(input_element)
	output_element.configure(state="normal")
	output_element.delete(1.0, ctk.END)
	output_element.insert(ctk.END, app_globals.DEF_RESULT)
	output_element.configure(state="disabled")

def close_window(window):
	"""
	Closes the window.
	"""
	#save_history()
	print("Closing application.")
	window.destroy()

def display_result(output_element, message: str):
	output_element.configure(state="normal")
	output_element.delete(1.0, ctk.END)
	output_element.insert(ctk.END, f"{message}")
	output_element.configure(state="disabled")

def expand_options(root, button):
	"""
	Opens the options window.
	"""
	#global EXPANDED
	if not app_globals.EXPANDED:
		#options_window.deiconify()
		button.configure(text="Collapse")
		app_globals.EXPANDED = True
	else:
		#options_window.withdraw()
		app_globals.EXPANDED = False
		button.configure(text="Expand")

def focus_element(element):
	"""
	Sets cursur focus to a given element.
	"""
	element.focus_set()
	if isinstance(element, ctk.CTkEntry):
		element.select_range(0, ctk.END)
	elif isinstance(element, ctk.CTkText):
		element.tag_add("sel", "1.0", "end")

def pin_window(window, button):
	"""
	Pins or un-pins the window relative to other windows.
	"""
	if not app_globals.PINNED:
		window.attributes('-topmost', True)
		button.configure(text="Unpin")
		app_globals.PINNED = True
	else:
		window.attributes('-topmost', False)
		button.configure(text="Pin")
		app_globals.PINNED = False


