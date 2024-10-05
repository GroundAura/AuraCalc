### IMPORTS ###

# builtins
import re

# external

# internal
import app_globals



### GLOBAL VARIABLES ###
#key_symbols: set[str] = {
#	"Control", "Shift", "Alt", "Tab", "Return", "Escape", "BackSpace", "Delete", "Space",
#	"F1", "F2", "F3", "F4", "F5", "F6", "F7", "F8", "F9", "F10", "F11", "F12",
#	"Left", "Right", "Up", "Down", "Home", "End", "PageUp", "PageDown", "Insert", "Pause",
#	#"KeyPress", "KeyRelease",
#}
#key_symbols: set[str] = {
#	"<Control>", "<Shift>", "<Alt>", "<Tab>", "<Return>", "<Escape>", "<BackSpace>", "<Delete>", "<Space>",
#	"<F1>", "<F2>", "<F3>", "<F4>", "<F5>", "<F6>", "<F7>", "<F8>", "<F9>", "<F10>", "<F11>", "<F12>",
#	"<Left>", "<Right>", "<Up>", "<Down>", "<Home>", "<End>", "<PageUp>", "<PageDown>", "<Insert>", "<Pause>",
#	#"<KeyPress>", "<KeyRelease>,"
#}
#key_symbols: set[str] = {
#	"<F1>", "<F2>", "<F3>", "<F4>", "<F5>", "<F6>", "<F7>", "<F8>", "<F9>", "<F10>", "<F11>", "<F12>",
#	"<Control>", "<Control_L>", "<Control_R>", "<Shift>", "<Shift_L>", "<Shift_R>", "<Alt>", "<Alt_L>", "<Alt_R>", "<Meta>", "<Meta_L>", "<Meta_R>",
#	"<BackSpace>", "<Tab>", "<Return>", "<Linefeed>", "<Enter>", "<Pause>", "<Scroll_Lock>", "<Sys_Req>", "<Escape>", "<Insert>", "<Delete>", "<Home>", "<End>", "<Page_Up>", "<Page_Down>",
#	"<Arrow_Left>", "<Arrow_Right>", "<Arrow_Up>", "<Arrow_Down>", "<Arrow_First>", "<Arrow_Last>",
#	"<KP_0>", "<KP_1>", "<KP_2>", "<KP_3>", "<KP_4>", "<KP_5>", "<KP_6>", "<KP_7>", "<KP_8>", "<KP_9>",
#	"<KP_Decimal>", "<KP_Divide>", "<KP_Multiply>", "<KP_Subtract>", "<KP_Add>", "<KP_Enter>",
#	"<KP_Equal>",
#}
#keybind_pattern: re.Pattern = re.compile(r'^<([A-Za-z]+-)*(KeyPress|KeyRelease)-?[A-Za-z0-9]*>$')



### FUNCTIONS ###

#def valid_keybind(keybind: str) -> bool:
#	"""
#	Validates that the string is a valid Tkinter keybind.

#	Args:
#		keybind (str): The keybind to validate.

#	Returns:
#		bool: Whether the keybind is valid.
#	"""
#	if keybind.lower().strip() in ("", "<>", "none", "<none>"):
#		return False
#	#if keybind[0] != "<":
#	#	keybind = "<" + keybind
#	#if keybind[-1] != ">":
#	#	keybind = keybind + ">"
#	if keybind in key_symbols:
#		return True
#	elif keybind_pattern.match(keybind):
#		return True
#	else:
#		raise Exception(f"Invalid keybind: `{keybind}`")

def keybind_enabled(keybind: str) -> bool:
	"""
	Checks if the keybind is enabled.

	Args:
		keybind (str): The keybind to check.

	Returns:
		bool: Whether the keybind is enabled.
	"""
	if keybind.lower().strip() in ("", "<>", "none", "<none>"):
		return False
	return True



### MAIN ###

if __name__ == "__main__":
	pass


