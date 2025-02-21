### IMPORTS ###

# builtins
#import tkinter as tk
#from tkinter import ttk

# external
import customtkinter as ctk
#import PyQt6 as pyqt
#import tkinterdnd2 as tkdnd
#import tkinterplus as tkp

# internal
from app_class import CalculatorApp
from app_debug import print_debug



### FUNCTIONS ###



### MAIN ###

def main():
	### METADATA ###

	meta_name: str = 'AuraCalc'
	meta_version: str = '0.3.0-alpha'
	meta_author: str = 'GroundAura'

	resources_dir: str = 'resources'
	config_file: str = f"{meta_name}.ini"
	history_file: str = 'history.json'
	icon_file: str = 'icon.ico'
	log_file: str = 'debug.log'



	### WINDOW SETUP ###

	# Initialize window
	print_debug(f"{meta_name} v{meta_version} by {meta_author}")
	print_debug('Initializing...')
	app = CalculatorApp(
		name = meta_name,
		version = meta_version,
		author = meta_author,
		resources_dir = resources_dir,
		history_file = history_file,
		icon_file = icon_file,
		log_file = log_file,
		config_file = config_file,
		use_config = True,
		win_layout = 'grid'
	)

	# Configure theme
	#app._set_theme_mode('dark')
	#app._set_theme_color('green')
	#tk.ttk.Style().theme_use('clam')

	# Configure grid
	app.window.grid_columnconfigure(0, weight=1)
	#app.window.grid_columnconfigure(1, weight=1)
	#app.window.grid_columnconfigure(2, weight=1)
	#app.window.grid_columnconfigure(3, weight=1)

	app.window.grid_rowconfigure(0, weight=0)
	app.window.grid_rowconfigure(1, weight=1)
	#app.window.grid_rowconfigure(2, weight=0)

	# Configure padding
	x_padding = 2
	
	y_padding = 3
	#y_pad_try = window_height / 2 - 25
	#y_padding = y_pad_try if y_pad_try > 5 and window_height > 100 else 5



	### FRAME SETUP ###

	# Basic calculator frame
	app.win_frame_base.grid(row=0, column=0, padx=0, pady=0, sticky='NSEW')
	#app.print_log(app.win_frame_base.winfo_pointerxy())
	#app.print_log(app.win_frame_base.winfo_manager())
	#app.print_log(app.win_frame_base.winfo_screen())
	app.win_frame_base.grid_columnconfigure(0, weight=1)
	app.win_frame_base.grid_columnconfigure(1, weight=1)
	app.win_frame_base.grid_columnconfigure(2, weight=1)
	app.win_frame_base.grid_columnconfigure(3, weight=1)

	app.win_frame_base.grid_rowconfigure(0, weight=0)
	app.win_frame_base.grid_rowconfigure(1, weight=0)
	app.win_frame_base.grid_rowconfigure(2, weight=0)

	## Advanced calculator frame
	app.win_frame_adv.grid(row=1, column=0, padx=0, pady=0, sticky='NSEW')
	app.win_frame_adv.grid_remove()



	### MENU BAR SETUP ###

	## Create the menu bar
	#menu_bar = tk.Menu(app.window)

	## Create the File menu
	#file_menu = tk.Menu(menu_bar, tearoff=0, activebackground='#106a43')
	#file_menu.add_command(label='Exit', command=app.close_window)
	###file_menu.grid(row=0, column=0, padx=x_padding, pady=y_padding)

	## Add the menus to the menu bar
	#menu_bar.add_cascade(label='File', menu=file_menu)
	#app.window.config(menu=menu_bar)



	### GUI ELEMENTS ###

	# Entry Input Element (CTkEntry)
	app._win_txt_input.grid(row=2, column=0, columnspan=5, sticky='NEW', padx=x_padding, pady=y_padding)
	app._win_txt_input.insert(ctk.END, app.calc_def_expr)

	# Result Display Element (CTkTextbox)
	app._win_txt_result.configure(height=1)
	app._win_txt_result.grid(row=3, column=0, columnspan=5, sticky='NEW', padx=x_padding, pady=y_padding)
	app._win_txt_result.insert(ctk.END, app.calc_def_result)
	app._win_txt_result.configure(state='disabled')

	# Pin Window ELement (CTkButton)
	app._win_btn_pin.configure(width=30)
	app._win_btn_pin.grid(row=4, column=0, columnspan=1, sticky='NEW', padx=x_padding, pady=y_padding)

	# Clear Entry/Result Element (CTkButton)
	app._win_btn_clear.configure(width=30)
	app._win_btn_clear.grid(row=4, column=1, columnspan=3, sticky='NEW', padx=x_padding, pady=y_padding)

	# Advanced View Element (CTkButton)
	app._win_btn_adv.configure(width=30)
	app._win_btn_adv.grid(row=4, column=4, columnspan=1, sticky='NEW', padx=x_padding, pady=y_padding)


	### FINAL INITIALIZATION ###

	# Start main loop
	app.print_log('Initialization complete!')
	app.open_window()

if __name__ == '__main__':
	main()


