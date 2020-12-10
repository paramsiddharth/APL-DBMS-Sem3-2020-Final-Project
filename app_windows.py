# Windows

from tkinter import *
from tkinter.font import Font

# Splash
def splash():
	splash_screen = Tk()
	splash_screen.bind('<Motion>', lambda *params: splash_screen.destroy())

	w = splash_screen.winfo_width()
	h = splash_screen.winfo_height()

	Label(splash_screen, text='Project: Bus Booking System', font=('Arial', 30)).pack(pady=(20, 0))
	Label(splash_screen, text='Courses: Advanced Programming Laboratory and Database Systems',
		font=('Arial', 20)).pack(padx=(20, 20))
	Label(splash_screen, text='Made by Param Siddharth.', font=('Arial', 18), foreground='blue').pack()
	Label(splash_screen, text='Supervised by Dr. Mahesh Kumar, Dr. Nileshkumar R. Patel, and Dr. Amit Kumar Srivastava.', font=('Arial', 14)).pack()
	Label(splash_screen, text='Hover to close.', foreground='red', font=('Arial', 8)).pack(pady=(5, 20))

	splash_screen.mainloop()


# Main window
def main():
	root = Tk()

	Label(root, text='Bus Booking Service', font=('Times', 40), background='lightgrey', foreground='blue').grid(
		row=1,
		padx=(10, 10),
		pady=(10, 10)
	)

	addBus = Button(root, text='Add Bus', width=10, font=Font(size=20, weight='bold'))
	searchBus = Button(root, text='Search Bus', width=10, font=Font(size=20, weight='bold'))
	addBus.grid(row=3, pady=(5, 5))
	searchBus.grid(row=4, pady=(5, 5))

	return {
		'root': root,
		'addBus': addBus,
		'searchBus': searchBus
	}