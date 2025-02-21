### IMPORTS ###

# builtins
#import re

# external

# internal
from app_type import validate_type



### GLOBAL VARIABLES ###
#key_symbols: set[str] = {
#	'Control', 'Shift', 'Alt', 'Tab', 'Return', 'Escape', 'BackSpace', 'Delete', 'Space',
#	'F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9', 'F10', 'F11', 'F12',
#	'Left', 'Right', 'Up', 'Down', 'Home', 'End', 'PageUp', 'PageDown', 'Insert', 'Pause',
#	#'KeyPress', 'KeyRelease',
#}
#key_symbols: set[str] = {
#	'<Control>', '<Shift>', '<Alt>', '<Tab>', '<Return>', '<Escape>', '<BackSpace>', '<Delete>', '<Space>',
#	'<F1>', '<F2>', '<F3>', '<F4>', '<F5>', '<F6>', '<F7>', '<F8>', '<F9>', '<F10>', '<F11>', '<F12>',
#	'<Left>', '<Right>', '<Up>', '<Down>', '<Home>', '<End>', '<PageUp>', '<PageDown>', '<Insert>', '<Pause>',
#	#'<KeyPress>', '<KeyRelease>,'
#}
#key_symbols: set[str] = {
#	'<F1>', '<F2>', '<F3>', '<F4>', '<F5>', '<F6>', '<F7>', '<F8>', '<F9>', '<F10>', '<F11>', '<F12>',
#	'<Control>', '<Control_L>', '<Control_R>', '<Shift>', '<Shift_L>', '<Shift_R>', '<Alt>', '<Alt_L>', '<Alt_R>', '<Meta>', '<Meta_L>', '<Meta_R>',
#	'<BackSpace>', '<Tab>', '<Return>', '<Linefeed>', '<Enter>', '<Pause>', '<Scroll_Lock>', '<Sys_Req>', '<Escape>', '<Insert>', '<Delete>', '<Home>', '<End>', '<Page_Up>', '<Page_Down>',
#	'<Arrow_Left>', '<Arrow_Right>', '<Arrow_Up>', '<Arrow_Down>', '<Arrow_First>', '<Arrow_Last>',
#	'<KP_0>', '<KP_1>', '<KP_2>', '<KP_3>', '<KP_4>', '<KP_5>', '<KP_6>', '<KP_7>', '<KP_8>', '<KP_9>',
#	'<KP_Decimal>', '<KP_Divide>', '<KP_Multiply>', '<KP_Subtract>', '<KP_Add>', '<KP_Enter>',
#	'<KP_Equal>',
#}
#keybind_pattern: re.Pattern = re.compile(r'^<([A-Za-z]+-)*(KeyPress|KeyRelease)-?[A-Za-z0-9]*>$')

## Define valid modifier keys
#VALID_MODIFIERS = {
#	"Control", "Shift", "Alt", "Meta", "Command", "Option",
#	"Mod1", "Mod2", "Mod3", "Mod4", "Mod5", "Lock"
#}


## Define valid main keys (letters, numbers, function keys, special keys)
##VALID_KEYS = set('abcdefghijklmnopqrstuvwxyz0123456789') | {
##	'Return', 'Escape', 'Tab', 'BackSpace', 'Delete',
##	'Left', 'Right', 'Up', 'Down', 'Home', 'End', 'Insert',
##	'F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9', 'F10', 'F11', 'F12',
##	'space', 'minus', 'equal', 'bracketleft', 'bracketright',
##	'backslash', 'semicolon', 'apostrophe', 'comma', 'period', 'slash',
##}
#VALID_KEYS = set('abcdefghijklmnopqrstuvwxyz0123456789') | {
#	'return', 'escape', 'tab', 'backspace', 'Delete',
#	'Left', 'Right', 'Up', 'Down', 'Home', 'End', 'Insert',
#	'F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9', 'F10', 'F11', 'F12',
#	'space', 'minus', 'equal', 'bracketleft', 'bracketright',
#	'backslash', 'semicolon', 'apostrophe', 'comma', 'period', 'slash',
#}


### FUNCTIONS ###

#def bind_event(widget, sequence: str, excluded_sequences: list[str] | tuple[str], func) -> None:
#	if not sequence or sequence.lower().strip() in ('', '<>', 'none', '<none>'):
#		return
#	if type(widget) in (list, tuple):
#		for w in widget:
#			if type(sequence) in (list, tuple):
#				for seq in sequence:
#					#validate_type(func, function)
#					w.bind(seq, func)
#			elif type(sequence) == str:
#				#validate_type(func, function)
#				w.bind(sequence, func)
#	else:
#		validate_type(sequence, str)
#		#validate_type(func, function)
#		widget.bind(sequence, func)

def bind_event(widget, sequence: str, excluded_seq: str | list[str] | set[str] | tuple[str] = None, pass_event: bool = False, command = lambda: None, *args, **kwargs) -> None:
	if not sequence or sequence.lower().strip() in ('', '<>', 'none', '<none>'):
		return
	validate_type(sequence, str)
	#validate_type(command, function)
	if excluded_seq and excluded_seq is not None:
		print('a')
		#widget.bind(valid_seq, lambda event: on_event(event, excluded_seq, command))
		widget.bind(sequence, lambda event: on_event(event, excluded_seq, command, *args, **kwargs))
	elif pass_event:
		print('b')
		widget.bind(sequence, lambda event: command(event, *args, **kwargs))
	else:
		print('c')
		#widget.bind(valid_seq, lambda event: command)
		widget.bind(sequence, lambda event: command(*args, **kwargs))

#def delete_term(element, direction: str) -> None:
#	"""
#	Deletes a single term in the given direction.
#
#	Args:
#		element: The element to delete a term in.
#		direction (str): The direction to delete a term in.
#	"""
#	if direction.lower() in ('left', 'l'):
#		...
#	elif direction.lower in ('right', 'r'):
#		...
#	else:
#		raise ValueError(f"Invalid direction: {direction}. Must be 'left', 'l', 'right', or 'r'.")
#	...

#def keybind_enabled(keybind: str) -> bool:
#	"""
#	Checks if the keybind is enabled.

#	Args:
#		keybind (str): The keybind to check.

#	Returns:
#		bool: Whether the keybind is enabled.
#	"""
#	if keybind.lower().strip() in ('', '<>', 'none', '<none>'):
#		return False
#	return True

def on_event(event, excluded_keys: str | list[str] | set[str] | tuple[str], func, *args, **kwargs) -> None:
	#print(excluded_keys)
	#print(event)
	#print(type(event))
	#print(event.keysym)
	if not excluded_keys or excluded_keys is None:
		func(*args, **kwargs)
		return
	if type(excluded_keys) in (list, set, tuple):
		if event.keysym in excluded_keys:
			#print('excluded')
			return
		else:
			func(*args, **kwargs)
			return
	elif type(excluded_keys) == str:
		if event.keysym == excluded_keys:
			#print('excluded')
			return
		else:
			func(*args, **kwargs)
			return
	else:
		raise ValueError(f"Invalid type for excluded_seq: {type(excluded_keys)}. Must be list, tuple, or str.")
	#func(*args, **kwargs)
	#func()

#def valid_keybind(keybind: str) -> bool:
#	"""
#	Validates that the string is a valid Tkinter keybind.

#	Args:
#		keybind (str): The keybind to validate.

#	Returns:
#		bool: Whether the keybind is valid.
#	"""
#	if keybind.lower().strip() in ('', '<>', 'none', '<none>'):
#		return False
#	#if keybind[0] != '<':
#	#	keybind = '<' + keybind
#	#if keybind[-1] != '>':
#	#	keybind = keybind + '>'
#	if keybind in key_symbols:
#		return True
#	elif keybind_pattern.match(keybind):
#		return True
#	else:
#		raise Exception(f"Invalid keybind: `{keybind}`")

#def is_valid_tkinter_keybind(keybind):
#	#"""Checks if a string is a valid Tkinter keybind."""
#	## Regex for valid Tkinter keybind format: <Modifier-Key>
#	#pattern = re.compile(r'^<(?:(?:Control|Shift|Alt|Meta|Command|Option)-)?(?:[A-Za-z0-9]+|Return|Escape|Tab|BackSpace|Delete|Left|Right|Up|Down|Home|End|Insert|F[1-9]|F1[0-2])>$')
#	#return bool(pattern.match(keybind))

#	"""Validates a Tkinter keybind string."""
#	if not (keybind.startswith("<") and keybind.endswith(">")):
#		return False  # Must be enclosed in <>
	
#	# Remove angle brackets
#	keybind_content = keybind[1:-1]

#	# Split keybind into parts (modifiers + key)
#	parts = keybind_content.split("-")

#	# Last part must be the main key
#	main_key = parts[-1]
#	modifiers = set(parts[:-1])  # All other parts are modifiers

#	# Validate main key
#	if main_key not in VALID_KEYS:
#		return False

#	## Validate modifiers (if any)
#	#if not modifiers.issubset(VALID_MODIFIERS):
#	#	return False
#	# Check if all modifiers are valid or follow _L or _R pattern
#	for modifier in modifiers:
#		if modifier.rstrip('_L').rstrip('_R').lower() not in VALID_MODIFIERS:
#			return False

#	return True



### MAIN ###

if __name__ == '__main__':
	pass


