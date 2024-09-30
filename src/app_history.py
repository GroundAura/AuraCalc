### IMPORTS ###

# builtins

# external

# internal
import app_globals



### FUNCTIONS ###

def add_local_history():
	app_globals.HISTORY.append((app_globals.LAST_EXPRESSION,app_globals.LAST_RESULT))

def clear_local_history():
	app_globals.HISTORY = []

def remove_local_history():
	#app_globals.HISTORY.remove((app_globals.LAST_EXPRESSION,app_globals.LAST_RESULT))
	app_globals.HISTORY.pop()

def append_history():
	for expression, result in app_globals.HISTORY:
		with open(app_globals.HISTORY_FILE, 'a', encoding='utf-8') as f:
			f.write(f"{expression} |=| {result}\n")

def load_history(keep_current_history: bool = False):
	if not keep_current_history:
		clear_local_history()
	loaded_history: list[tuple[str, str]] = []
	with open(app_globals.HISTORY_FILE, 'r', encoding='utf-8') as f:
		for line in f:
			pair: tuple[str, str] = tuple(line.split('|=|'))
			loaded_history.append(pair)
	app_globals.HISTORY = loaded_history + app_globals.HISTORY

def save_history():
	data: str = ""
	for expression, result in app_globals.HISTORY:
		data += f"{expression} |=| {result}\n"
	with open(app_globals.HISTORY_FILE, 'w', encoding='utf-8') as f:
		f.write(data)



### MAIN ###

if __name__ == "__main__":
	pass


