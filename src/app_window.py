### IMPORTS ###

# external
import customtkinter as ctk

# internal
from app_logging import logging_print



### FUNCTIONS ###

def clear_io(app, input_element, output_element) -> None:
	"""
	Clears the input and output elements.

	Args:
		input_element: The element to clear the input from.
		output_element: The element to clear the output from.
	"""
	input_element.delete('0', 'end')
	input_element.insert('0', app.calc_def_expr)
	focus_element(input_element)
	output_element.configure(state='normal')
	output_element.delete('1.0', 'end')
	output_element.insert('end', app._calc_def_result)
	output_element.configure(state='disabled')

def copy_text(app, element: ctk.CTkEntry | ctk.CTkTextbox) -> None:
	"""
	Copies the text in the element to the clipboard.
	
	Args:
		window (ctk.CTk): The window to copy the text in.
		element (ctk.CTkEntry | ctk.CTkTextbox): The element to copy the text from.
	"""
	app.window.clipboard_clear()
	if isinstance(element, ctk.CTkEntry):
		element.get(0, 'end')
	elif isinstance(element, ctk.CTkText):
		element.get('1.0', 'end-1c')
	app.window.clipboard_append(element.get())
	logging_print(f"Text copied to clipboard: `{app.clipboard}`")
	app.window.update()

def delayed_display(app, output_element, message: str) -> None:
	"""
	Displays the result in the the output element after a delay.

	Args:
		app: The application instance.
		output_element: The element to display the result in.
		message (str): The message to display in the output element.
	"""
	#app.timeout_id = app.window.after(app._calc_live_eval_delay, lambda: display_result(app, output_element, message))
	app.delayed_func(lambda: display_result(app, output_element, message))
	display_result(app, output_element, app.calc_last_result)

def display_result(app, output_element, message: str) -> None:
	"""
	Displays the result in the output element.

	Args:
		output_element: The element to display the result in.
		message (str): The message to display in the output element.
	"""
	output_element.configure(state='normal')
	output_element.delete('1.0', 'end')
	output_element.insert('end', f"{message}")
	output_element.configure(state='disabled')
	logging_print(f"Expr (final):{' '*8}`{message.replace('\n', '  ')}`\n")

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



### TESTING ###

def _test():
	pass

if __name__ == '__main__':
	_test()


