### IMPORTS ###

# external
import customtkinter as ctk

# internal
from app_logging import logging_print



### FUNCTIONS ###
#def copy_text(app, element: ctk.CTkEntry | ctk.CTkTextbox) -> None:
#	"""
#	Copies the text in the element to the clipboard.
	
#	Args:
#		window (ctk.CTk): The window to copy the text in.
#		element (ctk.CTkEntry | ctk.CTkTextbox): The element to copy the text from.
#	"""
#	app.window.clipboard_clear()
#	if isinstance(element, ctk.CTkEntry):
#		element.get(0, 'end')
#	elif isinstance(element, ctk.CTkText):
#		element.get('1.0', 'end-1c')
#	app.window.clipboard_append(element.get())
#	logging_print(f"Text copied to clipboard: `{app.clipboard}`")
#	app.window.update()

def focus_element(element: ctk.CTkEntry | ctk.CTkTextbox) -> None:
	"""
	Sets cursur focus to a given element.

	Args:
		element (ctk.CTkEntry | ctk.CTkTextbox): The element to set focus on.
	"""
	element.focus_set()
	if isinstance(element, ctk.CTkEntry):
		element.select_range('0', 'end')
	elif isinstance(element, ctk.CTkText):
		element.tag_add('sel', '1.0', 'end-1c')

def text_clear(element: ctk.CTkEntry | ctk.CTkTextbox) -> None:
	"""
	Clears the text in a given element.

	Args:
		element (ctk.CTkEntry | ctk.CTkTextbox): The element to clear the text in.
	"""
	if type(element) == ctk.CTkEntry:
		text_remove(element, '0', 'end')
	elif type(element) == ctk.CTkTextbox:
		text_remove(element, '1.0', 'end')
	else:
		raise ValueError(f"Invalid element type: {type(element)}. Must be 'ctk.CTkEntry' or 'ctk.CTkTextbox'")

def text_remove(element: ctk.CTkEntry | ctk.CTkTextbox, start: str, end: str) -> None:
	"""
	Removes the text in a given element.

	Args:
		element (ctk.CTkEntry | ctk.CTkTextbox): The element to remove the text in.
		start (int): The start index of the text to remove.
		end (int): The end index of the text to remove.
	"""
	if type(element) == ctk.CTkEntry:
		element.delete(start, end)
	elif type(element) == ctk.CTkTextbox:
		if element.state_disabled:
			disable = True
			element.configure(state='normal')
			element.state_disabled = False
		element.delete(start, end)
		if disable:
			element.configure(state='disabled')
			element.state_disabled = True
	else:
		raise ValueError(f"Invalid element type: {type(element)}. Must be 'ctk.CTkEntry' or 'ctk.CTkTextbox'")

def text_set(element, text: str) -> None:
	"""
	Sets the text in a given element.

	Args:
		element (ctk.CTkEntry | ctk.CTkTextbox): The element to set the text in.
		text (str): The text to set in the element.
	"""
	text_clear(element)
	if type(element) == ctk.CTkEntry:
		element.insert('0', text)
	elif type(element) == ctk.CTkTextbox:
		if element.state_disabled:
			disable = True
			element.configure(state='normal')
			element.state_disabled = False
		element.insert('1.0', text)
		if disable:
			element.configure(state='disabled')
			element.state_disabled = True



### TESTING ###

def _test():
	pass

if __name__ == '__main__':
	_test()


