### IMPORTS ###

# builtins

# external

# internal
#from app_logging import logging_print
from app_type import validate_type



### FUNCTIONS ###

def bind_event(widget, sequence: str, excluded_seq: str | list[str] | set[str] | tuple[str] = None, pass_event: bool = False, command = lambda: None, *args, **kwargs) -> None:
	if not sequence or sequence.lower().strip() in ('', '<>', 'none', '<none>'):
		return
	validate_type(sequence, str)
	if excluded_seq and excluded_seq is not None:
		widget.bind(sequence, lambda event: _on_event(event, excluded_seq, command, *args, **kwargs))
	elif pass_event:
		widget.bind(sequence, lambda event: command(event, *args, **kwargs))
	else:
		widget.bind(sequence, lambda event: command(*args, **kwargs))

def _on_event(event, excluded_keys: str | list[str] | set[str] | tuple[str], func, *args, **kwargs) -> None:
	#logging_print(excluded_keys)
	#logging_print(event)
	#logging_print(type(event))
	#logging_print(event.keysym)
	if not excluded_keys or excluded_keys is None:
		func(*args, **kwargs)
		return
	if type(excluded_keys) in (list, set, tuple):
		if event.keysym in excluded_keys:
			#logging_print('excluded')
			return
		else:
			func(*args, **kwargs)
			return
	elif type(excluded_keys) == str:
		if event.keysym == excluded_keys:
			#logging_print('excluded')
			return
		else:
			func(*args, **kwargs)
			return
	else:
		raise ValueError(f"Invalid type for excluded_seq: {type(excluded_keys)}. Must be list, tuple, or str.")



### TESTING ###

def _test():
	pass

if __name__ == '__main__':
	_test()


