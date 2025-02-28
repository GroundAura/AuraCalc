## IMPORTS ###

# builtins
import builtins
from collections.abc import Collection, Container, Iterable, Sequence
import sys
from typing import Any, TypeAlias, Tuple, Union
from types import ModuleType, UnionType



### TYPES ###

if sys.version_info >= (3, 10):
	_ClassInfo: TypeAlias = Union[type, UnionType, Tuple['_ClassInfo', ...]]
else:
	_ClassInfo: TypeAlias = Union[type, Tuple['_ClassInfo', ...]]



### FUNCTIONS ###
def fits_typing(object: Any, class_or_tuple: _ClassInfo) -> bool:
	"""
	Determines if an object is an instance or subclass of a given class or tuple of classes.

	Args:
		object (Any): The object to check.
		class_or_tuple (_ClassInfo): The class or tuple of classes to check against.

	Returns:
		bool: `True` if the object is an instance or subclass of the given class or tuple of classes, `False` otherwise.
	"""
	try:
		return isinstance(object, class_or_tuple) or issubclass(type(object), class_or_tuple)
	except Exception as e:
		raise Exception(f"Error while trying to check if {object} is instance or subclass of {class_or_tuple}:\n  {e}")

def function_exists(func_name: str, check_builtins: bool = True, check_global: bool = True, check_local: bool = False, modules_to_check: Container[ModuleType] | None = None) -> bool:
	"""
	Determines if a function exists in the global or builtins namespace and is callable.

	Args:
		func_name (str): The name of the function to check.
		check_builtins (bool, optional): Whether to check the builtins namespace. Defaults to `True`.
		check_globals (bool, optional): Whether to check the global scope. Defaults to `True`.
		check_locals (bool, optional): Whether to check the local scope. Defaults to `False`.
		modules_to_check (Container[ModuleType] | None, optional): A list-like container of modules to check. Defaults to `None`.

	Returns:
		bool: `True` if the function is found and callable, `False` otherwise.
	"""
	if check_global and func_name in globals() and callable(globals()[func_name]):
		return True
	elif check_local and func_name in locals() and callable(locals()[func_name]):
		return True
	elif check_builtins and func_name in dir(builtins) and callable(getattr(builtins, func_name)):
		return True
	elif modules_to_check is not None and len(modules_to_check) > 0 and any(func_name in dir(module) and callable(getattr(module, func_name)) for module in modules_to_check):
		return True
	return False

def get_type(obj: Any) -> str:
	"""
	Gets the class name of a given object.

	Args:
		obj (Any): The object to get the class name of.

	Returns:
		str: The class name of the object.
	"""
	try:
		return type(obj).__name__
	except Exception as e:
		raise Exception(f"Error while trying to get type of data {obj}:\n  {e}")

def matches_key(string: str, key: str | Container[str]) -> bool:
	try:
		#print(f"string: {type(string).__name__} = '{string}'")
		#print(f"key: {type(key).__name__} = '{key}'")
		#print(issubclass(type(key), Container))
		if isinstance(key, str):
			#print(f"string == key :: {string == key}")
			return string == key
		elif issubclass(type(key), Container):
			#print(f"string in key :: {string in key}")
			return string in key
		else:
			#print(f"string == key | string in key :: False")
			return False
	except Exception as e:
		raise Exception(f"Error while trying to check if string '{string}' matches key '{key}':\n  {e}")

def str_to_bool(string: str, case_sensitive: bool = False, true_values: str | Container[str] = ('TRUE', 'True', 'true', 'T', 't', '1'), false_values: str | Container[str] = ('FALSE', 'False', 'false', 'F', 'f', '0')) -> bool:
	try:
		if not case_sensitive:
			string = string.lower()
			true_values: list[str] = sorted(set(value.lower() for value in true_values))
			false_values: list[str] = sorted(set(value.lower() for value in false_values))
		if string in true_values:
			return True
		elif string in false_values:
			return False
		else:
			true_values: list[str] = sorted(set(true_values))
			false_values: list[str] = sorted(set(false_values))
			raise Exception(f"Failed to convert str to bool. Valid values are: {true_values + false_values}. Case sensitive: '{case_sensitive}'.")
	except Exception as e:
		raise Exception(f"Error while trying to convert string '{string}' to a boolean:\n  {e}")

def str_to_dict(string: str) -> dict:
	try:
		if string.startswith('{') and string.endswith('}'):
			string: dict = eval(string)
		else:
			string: dict = eval('{' + string + '}')
		if type(string) == dict:
			return string
		else:
			raise Exception('Failed to convert str to dict.')
	except Exception as e:
		raise Exception(f"Error while trying to convert string '{string}' to a list:\n  {e}")

def str_to_float(string: str) -> float:
	try:
		string: float = float(string)
		if type(string) == float:
			return string
		else:
			raise Exception('Failed to convert str to float.')
	except Exception as e:
		raise Exception(f"Error while trying to convert string '{string}' to a float:\n  {e}")

def str_to_int(string: str) -> int:
	try:
		string: int = int(string)
		if type(string) == int:
			return string
		else:
			raise Exception('Failed to convert str to int.')
	except Exception as e:
		raise Exception(f"Error while trying to convert string '{string}' to an integer:\n  {e}")

def str_to_list(string: str) -> list:
	try:
		string: str = string.lstrip('[').rstrip(']')
		string: list = string.split(', ')
		if type(string) == list:
			return string
		else:
			raise Exception('Failed to convert str to list.')
	except Exception as e:
		raise Exception(f"Error while trying to convert string '{string}' to a list:\n  {e}")

def str_to_set(string: str) -> set:
	try:
		string: str = string.lstrip('{').rstrip('}')
		string: set = set(string.split(', '))
		if type(string) == set:
			return string
		else:
			raise Exception('Failed to convert str to set.')
	except Exception as e:
		raise Exception(f"Error while trying to convert string '{string}' to a set:\n  {e}")

def str_to_tuple(string: str) -> tuple:
	try:
		string: str = string.lstrip('(').rstrip(')')
		string: tuple = tuple(string.split(', '))
		if type(string) == tuple:
			return string
		else:
			raise Exception('Failed to convert str to tuple.')
	except Exception as e:
		raise Exception(f"Error while trying to convert string '{string}' to a tuple:\n  {e}")

def validate_type(value, valid_type: type) -> bool:
	if not isinstance(value, valid_type):
		raise TypeError(f"Expected type '{valid_type.__name__}', got '{type(value).__name__}'")
	return True



### TESTING ###

def _test() -> None:
	try:
	# get_type()
		data = 123
		data_type = get_type(data)
		print('get_type():')
		print(f"data = {data}")
		print(f"data_type = {data_type}")
		print()
	# str_to_bool()
		bool_as_str = 'TrUe'
		bool_as_bool = str_to_bool(bool_as_str, case_sensitive=False, true_values=('TRUE', 'True', 'true', 'T', 't', '1'), false_values=('FALSE', 'False', 'false', 'F', 'f', '0'))
		print('str_to_bool():')
		print(f"bool_as_str = {bool_as_str}")
		print(f"bool_as_bool = {bool_as_bool}")
		print(f"data_type = {get_type(bool_as_bool)}")
		print()
	# str_to_dict()
		dict_as_str = '{"key": "value"}'
		dict_as_dict = str_to_dict(dict_as_str)
		print('str_to_dict():')
		print(f"dict_as_str = {dict_as_str}")
		print(f"dict_as_dict = {dict_as_dict}")
		print(f"data_type = {get_type(dict_as_dict)}")
		print()
	# str_to_float()
		float_as_str = '123.456'
		float_as_float = str_to_float(float_as_str)
		print('str_to_float():')
		print(f"float_as_str = {float_as_str}")
		print(f"float_as_float = {float_as_float}")
		print(f"data_type = {get_type(float_as_float)}")
		print()
	# str_to_int()
		int_as_str = '123'
		int_as_int = str_to_int(int_as_str)
		print('str_to_int():')
		print(f"int_as_str = {int_as_str}")
		print(f"int_as_int = {int_as_int}")
		print(f"data_type = {get_type(int_as_int)}")
		print()
	# str_to_list()
		list_as_str = '[1, 2, 3]'
		list_as_list = str_to_list(list_as_str)
		print('str_to_list():')
		print(f"list_as_str = {list_as_str}")
		print(f"list_as_list = {list_as_list}")
		print(f"data_type = {get_type(list_as_list)}")
		print()
	# str_to_set()
		set_as_str = '{1, 2, 3}'
		set_as_set = str_to_set(set_as_str)
		print('str_to_set():')
		print(f"set_as_str = {set_as_str}")
		print(f"set_as_set = {set_as_set}")
		print(f"data_type = {get_type(set_as_set)}")
		print()
	# str_to_tuple()
		tuple_as_str = '(1, 2, 3)'
		tuple_as_tuple = str_to_tuple(tuple_as_str)
		print('str_to_tuple():')
		print(f"tuple_as_str = {tuple_as_str}")
		print(f"tuple_as_tuple = {tuple_as_tuple}")
		print(f"data_type = {get_type(tuple_as_tuple)}")
		print()
	except Exception as e:
		print(f"ERROR: {e}")
		exit()

	#print(f"isinstance(list, Sequence): {isinstance(list, Sequence)}")
	#print(f"isinstance(set, Sequence): {isinstance(set, Sequence)}")
	#print(f"isinstance(tuple, Sequence): {isinstance(tuple, Sequence)}")
	#print(f"isinstance(dict, Sequence): {isinstance(dict, Sequence)}")
	#print(f"isinstance(str, Sequence): {isinstance(str, Sequence)}")

	#print(f"isinstance(list, Iterable): {isinstance(list, Iterable)}")
	#print(f"isinstance(set, Iterable): {isinstance(set, Iterable)}")
	#print(f"isinstance(tuple, Iterable): {isinstance(tuple, Iterable)}")
	#print(f"isinstance(dict, Iterable): {isinstance(dict, Iterable)}")
	#print(f"isinstance(str, Iterable): {isinstance(str, Iterable)}")

	#print(f"isinstance(list, Container): {isinstance(list, Container)}")
	#print(f"isinstance(set, Container): {isinstance(set, Container)}")
	#print(f"isinstance(tuple, Container): {isinstance(tuple, Container)}")
	#print(f"isinstance(dict, Container): {isinstance(dict, Container)}")
	#print(f"isinstance(str, Container): {isinstance(str, Container)}")

	#print(f"isinstance(list, Collection): {isinstance(list, Collection)}")
	#print(f"isinstance(set, Collection): {isinstance(set, Collection)}")
	#print(f"isinstance(tuple, Collection): {isinstance(tuple, Collection)}")
	#print(f"isinstance(dict, Collection): {isinstance(dict, Collection)}")
	#print(f"isinstance(str, Collection): {isinstance(str, Collection)}")

	print(f"issubclass(list, Sequence): {issubclass(list, Sequence)}")       # True
	print(f"issubclass(set, Sequence): {issubclass(set, Sequence)}")         # False
	print(f"issubclass(tuple, Sequence): {issubclass(tuple, Sequence)}")     # True
	print(f"issubclass(dict, Sequence): {issubclass(dict, Sequence)}")       # False
	print(f"issubclass(str, Sequence): {issubclass(str, Sequence)}")         # True
	print()
	print(f"issubclass(list, Iterable): {issubclass(list, Iterable)}")       # True
	print(f"issubclass(set, Iterable): {issubclass(set, Iterable)}")         # True
	print(f"issubclass(tuple, Iterable): {issubclass(tuple, Iterable)}")     # True
	print(f"issubclass(dict, Iterable): {issubclass(dict, Iterable)}")       # True
	print(f"issubclass(str, Iterable): {issubclass(str, Iterable)}")         # True
	print()
	print(f"issubclass(list, Container): {issubclass(list, Container)}")     # True
	print(f"issubclass(set, Container): {issubclass(set, Container)}")       # True
	print(f"issubclass(tuple, Container): {issubclass(tuple, Container)}")   # True
	print(f"issubclass(dict, Container): {issubclass(dict, Container)}")     # True
	print(f"issubclass(str, Container): {issubclass(str, Container)}")       # True
	print()
	print(f"issubclass(list, Collection): {issubclass(list, Collection)}")   # True
	print(f"issubclass(set, Collection): {issubclass(set, Collection)}")     # True
	print(f"issubclass(tuple, Collection): {issubclass(tuple, Collection)}") # True
	print(f"issubclass(dict, Collection): {issubclass(dict, Collection)}")   # True
	print(f"issubclass(str, Collection): {issubclass(str, Collection)}")     # True

if __name__ == '__main__':
	_test()


