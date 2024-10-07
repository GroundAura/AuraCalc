### IMPORTS ###

# builtins

# external
import customtkinter as ctk

# internal
import app_globals
from app_debug import print_debug
#from app_history import save_history



### FUNCTIONS ###

def clear_io(input_element, output_element) -> None:
	"""
	Clears the input and output elements.

	Args:
		input_element: The element to clear the input from.
		output_element: The element to clear the output from.
	"""
	input_element.delete("0", "end")
	input_element.insert("0", app_globals.DEF_EXPRESSION)
	focus_element(input_element)
	output_element.configure(state="normal")
	output_element.delete("1.0", "end")
	output_element.insert("end", app_globals.DEF_RESULT)
	output_element.configure(state="disabled")

def close_window(window: ctk.CTk) -> None:
	"""
	Closes the window.

	Args:
		window (ctk.CTk): The window to close.
	"""
	#save_history()
	print_debug(f"Closing {app_globals.NAME}.")
	print_debug("\n\n", timestamp=False, print_to_console=False)
	window.destroy()

def copy_text(window: ctk.CTk, element: ctk.CTkEntry | ctk.CTkTextbox) -> None:
	"""
	Copies the text in the element to the clipboard.
	
	Args:
		window (ctk.CTk): The window to copy the text in.
		element (ctk.CTkEntry | ctk.CTkTextbox): The element to copy the text from.
	"""
	window.clipboard_clear()
	if isinstance(element, ctk.CTkEntry):
		element.get(0, "end")
	elif isinstance(element, ctk.CTkText):
		element.get("1.0", "end-1c")
	window.clipboard_append(element.get())
	#clipboard = window.clipboard_get()
	window.update()

def display_result(output_element, message: str) -> None:
	"""
	Displays the result in the output element.

	Args:
		output_element: The element to display the result in.
		message (str): The message to display in the output element.
	"""
	output_element.configure(state="normal")
	output_element.delete("1.0", "end")
	output_element.insert("end", f"{message}")
	output_element.configure(state="disabled")
	print_debug(f"Expr (final):{' '*8}`{message.replace('\n', '  ')}`\n")

def toggle_advanced(window: ctk.CTk, frame: ctk.CTkFrame, button: ctk.CTkButton) -> None:
	"""
	Opens the options window.

	Args:
		window (ctk.CTk): The window to expand the frame in.
		frame (ctk.CTkFrame): The frame to expand.
		button (ctk.CTkButton): The button to update the text of.
	"""
	#global EXPANDED
	if not app_globals.EXPANDED:
		frame.grid(row=1, column=0, padx=0, pady=0, sticky="NSEW")
		button.configure(text="Collapse")
		app_globals.EXPANDED = True
		app_globals.RESIZE_HEIGHT = True
		update_window(window)
	else:
		#if frame.winfo_viewable():
		frame.grid_forget()
		button.configure(text="Expand")
		app_globals.EXPANDED = False
		app_globals.RESIZE_HEIGHT = False
		update_window(window)
	#print_debug(f"Expanded = {app_globals.EXPANDED}")
	#print_debug(f"Viewable = {frame.winfo_viewable()}")

def focus_element(element: ctk.CTkEntry | ctk.CTkTextbox) -> None:
	"""
	Sets cursur focus to a given element.

	Args:
		element (ctk.CTkEntry | ctk.CTkTextbox): The element to set focus on.
	"""
	element.focus_set()
	if isinstance(element, ctk.CTkEntry):
		element.select_range("0", "end")
	elif isinstance(element, ctk.CTkText):
		element.tag_add("sel", "1.0", "end-1c")

def pin_window(window: ctk.CTk, button: ctk.CTkButton) -> None:
	"""
	Pins or un-pins the window relative to other windows.

	Args:
		window (ctk.CTk): The window to pin.
		button (ctk.CTkButton): The button to update the text of.
	"""
	if not app_globals.PINNED:
		window.attributes('-topmost', True)
		button.configure(text="Unpin")
		app_globals.PINNED = True
	else:
		window.attributes('-topmost', False)
		button.configure(text="Pin")
		app_globals.PINNED = False

def update_window(window: ctk.CTk, def_pos: bool = False) -> None:
	"""
	Updates the window's size, position, and related attributes.

	Args:
		window (ctk.CTk): The window to update.
		def_pos (bool, optional): Whether to set the window to the default position. Defaults to `False`.
	"""
	app_globals.SCREEN_HEIGHT = window.winfo_screenheight()
	app_globals.SCREEN_WIDTH = window.winfo_screenwidth()
	#app_globals.X_POS = (window.winfo_screenwidth() // 2) - (app_globals.WIDTH // 2)
	#app_globals.Y_POS = (window.winfo_screenheight() // 2) - (app_globals.HEIGHT // 2)
	#window.geometry(f"{app_globals.WIDTH}x{app_globals.HEIGHT}+{app_globals.X_POS}+{app_globals.Y_POS}")
	app_globals.CUR_HEIGHT = window.winfo_height()
	app_globals.CUR_WIDTH = window.winfo_width()
	app_globals.CUR_X_POS = window.winfo_x() if window.winfo_x() else app_globals.DEF_X_POS
	app_globals.CUR_Y_POS = window.winfo_y() if window.winfo_y() else app_globals.DEF_Y_POS
	#if not app_globals.CUR_X_POS or not app_globals.CUR_Y_POS:
	#	target_x_pos: int = app_globals.DEF_X_POS
	#	target_y_pos: int = app_globals.DEF_Y_POS
	if def_pos:
		if app_globals.DEF_CENTERED:
			target_x_pos: int = (app_globals.SCREEN_WIDTH // 2) - (app_globals.CUR_WIDTH // 2)
			target_y_pos: int = (app_globals.SCREEN_HEIGHT // 2) - (app_globals.CUR_HEIGHT // 2)
		else:
			target_x_pos: int = app_globals.DEF_X_POS
			target_y_pos: int = app_globals.DEF_Y_POS
	else:
		target_x_pos: int = app_globals.CUR_X_POS
		target_y_pos: int = app_globals.CUR_Y_POS
	window.resizable(width=app_globals.RESIZE_WIDTH, height=app_globals.RESIZE_HEIGHT)
	if app_globals.EXPANDED:
		window.minsize(app_globals.ADV_MIN_WIDTH, app_globals.ADV_MIN_HEIGHT)
		target_width: int = app_globals.CUR_WIDTH if app_globals.CUR_WIDTH > app_globals.ADV_DEF_WIDTH else app_globals.ADV_DEF_WIDTH
		window.geometry(f"{target_width}x{app_globals.ADV_DEF_HEIGHT}+{target_x_pos}+{target_y_pos}")
	else:
		window.minsize(app_globals.BASE_MIN_WIDTH, app_globals.BASE_MIN_HEIGHT)
		target_width: int = app_globals.CUR_WIDTH if app_globals.CUR_WIDTH > app_globals.ADV_DEF_WIDTH else app_globals.ADV_DEF_WIDTH
		window.geometry(f"{app_globals.BASE_DEF_WIDTH}x{app_globals.BASE_DEF_HEIGHT}+{target_x_pos}+{target_y_pos}")
	#app_globals.SCREEN_HEIGHT = window.winfo_screenheight()
	#app_globals.SCREEN_WIDTH = window.winfo_screenwidth()
	app_globals.CUR_HEIGHT = window.winfo_height()
	app_globals.CUR_WIDTH = window.winfo_width()
	app_globals.CUR_X_POS = window.winfo_x()
	app_globals.CUR_Y_POS = window.winfo_y()


