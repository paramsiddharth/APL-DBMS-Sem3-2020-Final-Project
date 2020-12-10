# Application windows

from tkinter import *
from tkinter.font import Font
import os
from datetime import date

def create_header(root):
	header = Frame(root)
	Label(header, text='Bus Booking Service', font=('Times', 40), background='lightgrey', foreground='blue').grid(
		row=1,
		padx=(10, 10),
		pady=(10, 10)
	)

	bus = PhotoImage(file='bus.png')
	img_label = Label(header, image=bus)
	img_label.photo = bus
	img_label.grid(row=2)

	return header


# Splash
def splash():
	splash_screen = Tk()
	splash_screen.wm_title('Welcome!')
	splash_screen.update_idletasks()
	splash_screen.bind('<Motion>', lambda *params: splash_screen.destroy())

	w = splash_screen.winfo_width() * 5
	h = splash_screen.winfo_height() * 1.1

	ws = splash_screen.winfo_screenwidth()
	hs = splash_screen.winfo_screenheight()

	x = ws / 2 - w / 2
	y = hs / 2 - h / 2

	splash_screen.geometry('%dx%d+%d+%d' % (w, h, x, y))

	Label(splash_screen, text='Project: Bus Booking System', font=('Arial', 30, 'bold')).pack(pady=(20, 0))
	Label(splash_screen, text='Courses: Advanced Programming Laboratory and Database Systems',
		font=('Arial', 20)).pack(padx=(20, 20))
	Label(splash_screen, text='Made by Param Siddharth.', font=('Arial', 18), foreground='blue').pack()
	Label(splash_screen, text='Supervised by Dr. Mahesh Kumar, Dr. Nileshkumar R. Patel, and Dr. Amit Kumar Srivastava.', font=('Arial', 14)).pack()
	Label(splash_screen, text='Hover to close.', foreground='red', font=('Arial', 8)).pack(pady=(5, 20))

	splash_screen.mainloop()


# Main window
def main():
	root = Tk()
	root.wm_title('Bus Booking System')
	create_header(root).grid(row=1)

	add_bus = Button(root, text='Add Bus', width=10, font=Font(size=20, weight='bold'), command=lambda: add_bus_window(root))
	search_bus = Button(root, text='Search Bus', width=10, font=Font(size=20, weight='bold'), command=lambda: search_bus_window(root))
	add_bus.grid(row=2, pady=(5, 5))
	search_bus.grid(row=3, pady=(5, 20))

	return {
		'root': root,
		'add_bus': add_bus,
		'search_bus': search_bus
	}
	# root.mainloop()

# Add bus window
def add_bus_window(root):
	window = Toplevel(root)
	root.wm_withdraw()
	window.wm_protocol('WM_DELETE_WINDOW', lambda: (root.wm_deiconify(), window.destroy()))
	create_header(window).grid(row=1)

	Label(window, text='Bus Operator Details', font=('Arial', 20)).grid(row=2)

	full_name = StringVar()
	contact_no = StringVar()

	form = Frame(window)

	Label(form, text='Full name: ').grid(row=1, column=1)
	Entry(form, textvariable=full_name).grid(row=1, column=2)
	Label(form, text='Contact number: ').grid(row=2, column=1)
	Entry(form, textvariable=contact_no).grid(row=2, column=2)
	Label(form, text='Address: ').grid(row=3, column=1)

	address_frame = Frame(form, height=60, width=125)
	address_frame.grid_propagate(False)
	address = Text(address_frame)
	address.place_configure(x=0, y=0, height=60, width=125)
	address_frame.grid(row=3, column=2, rowspan=3)

	form2 = Frame(form)

	Button(form, text='Add Details', width=20, command=lambda: form2.grid(row=7, column=1, columnspan=2)).grid(
		row=6, column=1, columnspan=2,
		pady=(5, 5)
	)

	operator = StringVar()
	Label(form2, text='Operator: ').grid(row=1, column=1)
	Entry(form2, textvariable=operator).grid(row=1, column=2)
	bus_type = StringVar()
	Label(form2, text='Bus type: ').grid(row=2, column=1)
	Entry(form2, textvariable=bus_type).grid(row=2, column=2)
	bus_from = StringVar()
	Label(form2, text='From: ').grid(row=3, column=1)
	Entry(form2, textvariable=bus_from).grid(row=3, column=2)
	bus_to = StringVar()
	Label(form2, text='To: ').grid(row=4, column=1)
	Entry(form2, textvariable=bus_to).grid(row=4, column=2)
	bus_date = StringVar()
	Label(form2, text='Date: ').grid(row=5, column=1)
	Entry(form2, textvariable=bus_date).grid(row=5, column=2)
	bus_dep = StringVar()
	Label(form2, text='Departure time: ').grid(row=6, column=1)
	Entry(form2, textvariable=bus_dep).grid(row=6, column=2)
	bus_arr = StringVar()
	Label(form2, text='Arrival time: ').grid(row=7, column=1)
	Entry(form2, textvariable=bus_arr).grid(row=7, column=2)
	fare = DoubleVar()
	Label(form2, text='Fare: ').grid(row=8, column=1)
	Entry(form2, textvariable=fare).grid(row=8, column=2)
	seats = IntVar()
	Label(form2, text='Seats: ').grid(row=9, column=1)
	Entry(form2, textvariable=seats).grid(row=9, column=2)

	Button(form2, text='Save', width=18, command=lambda: ()).grid(
		row=10, column=1, columnspan=2,
		pady=(5, 5)
	)

	form.grid(row=3, pady=(5, 15))

	window.mainloop()

# Search bus window
def search_bus_window(root):
	window = Toplevel(root)
	root.wm_withdraw()
	window.wm_protocol('WM_WINDOW_DELETE', lambda: (root.wm_deiconify(), window.destroy()))
	create_header(window).pack()

	form = Frame(window)

	Label(form, text='Bus type: ').grid(row=1, column=1)
	bus_type = StringVar(value='AC')
	OptionMenu(form, bus_type, 'AC', *(['Non-AC', 'AC Sleeper', 'Non-AC Sleeper', 'All Types'])).grid(row=1, column=2)
	bus_from = StringVar()
	Label(form, text='From: ').grid(row=2, column=1)
	Entry(form, textvariable=bus_from).grid(row=2, column=2)
	bus_to = StringVar()
	Label(form, text='To: ').grid(row=3, column=1)
	Entry(form, textvariable=bus_to).grid(row=3, column=2)
	bus_date = StringVar()
	Label(form, text='Date: ').grid(row=4, column=1)
	Entry(form, textvariable=bus_date).grid(row=4, column=2)

	def buses_found():
		data = [
			{
				'id': 1,
				'name': 'Kamla Travels',
				'type': 'AC',
				'from': 'Guna',
				'to': 'Indore',
				'date': date(2020, 12, 25),
				'dep': '09:15 AM',
				'arr': '02:30 PM',
				'fare': 650.00,
				'seats': 10
			},
			{
				'id': 2,
				'name': 'Harsh Travels',
				'type': 'Non-AC',
				'from': 'Guna',
				'to': 'Indore',
				'date': date(2020, 12, 25),
				'dep': '12:00 PM',
				'arr': '04:30 PM',
				'fare': 600.00,
				'seats': 5
			}
		]
		buses_found_window(root, window, data)

	Button(form, text='Home', width=18, command=lambda: (root.wm_deiconify(), window.destroy())).grid(
		row=5, column=1,
		pady=(5, 5)
	)
	Button(form, text='Search', width=18, command=buses_found).grid(
		row=5, column=2,
		pady=(5, 5)
	)

	form.pack(pady=(5, 20))

	window.mainloop()

# Buses found window
def buses_found_window(root, parent, data):
	window = Toplevel(root)
	parent.destroy()
	window.wm_protocol('WM_DELETE_WINDOW', lambda: (root.wm_deiconify(), window.destroy()))
	create_header(window).pack(padx=(150, 150))

	table_parent = Frame(window)
	table = Frame(table_parent)
	selected_bus = IntVar(value=0)

	Label(table, text='Operator', font=('Arial', 12)).grid(row=1, padx=(3, 3), column=1)
	Label(table, text='Type', font=('Arial', 12)).grid(row=1, padx=(3, 3), column=2)
	Label(table, text='From', font=('Arial', 12)).grid(row=1, padx=(3, 3), column=3)
	Label(table, text='To', font=('Arial', 12)).grid(row=1, padx=(3, 3), column=4)
	Label(table, text='Date', font=('Arial', 12)).grid(row=1, padx=(3, 3), column=5)
	Label(table, text='Departure', font=('Arial', 12)).grid(row=1, padx=(3, 3), column=6)
	Label(table, text='Arrival', font=('Arial', 12)).grid(row=1, padx=(3, 3), column=7)
	Label(table, text='Fare', font=('Arial', 12)).grid(row=1, padx=(3, 3), column=8)
	Label(table, text='Seats Available', font=('Arial', 12)).grid(row=1, padx=(3, 3), column=9)
	Label(table, text='Select', font=('Arial', 12)).grid(row=1, padx=(3, 3), column=10)

	row = 2
	for bus in data:
		Label(table, text=bus['name']).grid(row=row, padx=(3, 3), column=1)
		Label(table, text=bus['type']).grid(row=row, padx=(3, 3), column=2)
		Label(table, text=bus['from']).grid(row=row, padx=(3, 3), column=3)
		Label(table, text=bus['to']).grid(row=row, padx=(3, 3), column=4)
		Label(table, text=bus['date'].strftime('%d/%m/%Y')).grid(row=row, padx=(3, 3), column=5)
		Label(table, text=bus['dep']).grid(row=row, padx=(3, 3), column=6)
		Label(table, text=bus['arr']).grid(row=row, padx=(3, 3), column=7)
		Label(table, text=str(bus['fare'])).grid(row=row, padx=(3, 3), column=8)
		Label(table, text=str(bus['seats'])).grid(row=row, padx=(3, 3), column=9)
		Radiobutton(table, variable=selected_bus, value=bus['id']).grid(row=row, padx=(3, 3), column=10)
		row += 1

	def book_ticket():
		...
	
	table.grid(row=1, column=1, columnspan=20)
	Button(table_parent, text='Book', width=6, font=('Arial', 14), command=book_ticket).grid(row=2, column=20)

	table_parent.pack(pady=(2, 20))

	window.mainloop()