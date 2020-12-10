# Application database back-end

import sqlite3
from datetime import date, datetime

scripts = {
	'bus_types': '''
		CREATE TABLE IF NOT EXISTS bus_types (
			`id` INTEGER PRIMARY KEY,
			`name` VARCHAR(20) UNIQUE NOT NULL
		);
	''',
	'insert_bus_type': '''
		INSERT OR IGNORE INTO bus_types (
			`id`,
			`name`
		) VALUES (?, ?);
	''',
	'buses': '''
		CREATE TABLE IF NOT EXISTS buses (
			`id` INTEGER PRIMARY KEY AUTOINCREMENT,
			`op` VARCHAR(30) NOT NULL,
			`type` INTEGER NOT NULL,
			`from` VARCHAR(30) NOT NULL,
			`to` VARCHAR(30) NOT NULL,
			`date` DATE NOT NULL,
			`dep` VARCHAR(30) DEFAULT '12:00 PM',
			`arr` VARCHAR(30) DEFAULT '12:00 PM',
			`fare` DOUBLE DEFAULT 100,
			`seats` INTEGER DEFAULT 36,
			`admin_id` INTEGER NOT NULL,
			FOREIGN KEY (`type`) REFERENCES bus_types (`id`),
			FOREIGN KEY (`admin_id`) REFERENCES bus_admins (`id`)
		);
	''',
	'bus_admins': '''
		CREATE TABLE IF NOT EXISTS bus_admins (
			`id` INTEGER PRIMARY KEY AUTOINCREMENT,
			`name` VARCHAR(30) NOT NULL,
			`phone` VARCHAR(20) NOT NULL,
			`address` TEXT DEFAULT ''
		);
	''',
	'insert_bus': '''
		INSERT INTO buses (
			`op`, `type`, `from`, `to`, `date`, `dep`, `arr`, `fare`, `seats`, `admin_id`
		) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
	''',
	'get_all_buses': '''
		SELECT 
			`id`, `op`, `type`, `from`, `to`, `date`, `dep`, `arr`, `fare`, `seats`, `admin_id`
		FROM
			buses
		WHERE
			`seats` > 0 AND;
	''',
	'get_buses': '''
		SELECT 
			`id`, `op`, `type`, `from`, `to`, `date`, `dep`, `arr`, `fare`, `seats`, `admin_id`
		FROM
			buses
		WHERE
			`seats` > 0 AND
			`type` = ? AND
			`from` = ? AND
			`to` = ? AND
			`date` = ?
		;
	''',
	'get_buses_all_dates': '''
		SELECT 
			`id`, `op`, `type`, `from`, `to`, `date`, `dep`, `arr`, `fare`, `seats`, `admin_id`
		FROM
			buses
		WHERE
			`seats` > 0 AND
			`type` = ? AND
			`from` = ? AND
			`to` = ?
		;
	''',
	'get_buses_all_types': '''
		SELECT 
			`id`, `op`, `type`, `from`, `to`, `date`, `dep`, `arr`, `fare`, `seats`, `admin_id`
		FROM
			buses
		WHERE
			`seats` > 0 AND
			`from` = ? AND
			`to` = ? AND
			`date` = ?
		;
	''',
	'get_buses_all_dates_all_types': '''
		SELECT 
			`id`, `op`, `type`, `from`, `to`, `date`, `dep`, `arr`, `fare`, `seats`, `admin_id`
		FROM
			buses
		WHERE
			`seats` > 0 AND
			`from` = ? AND
			`to` = ?
		;
	''',
	'get_bus_by_id': '''
		SELECT 
			`id`, `op`, `type`, `from`, `to`, `date`, `dep`, `arr`, `fare`, `seats`, `admin_id`
		FROM
			buses
		WHERE
			`id` = ?
		LIMIT 1
		;
	''',
	'update_seats': '''
		UPDATE
			buses
		SET
			`seats` = ?
		WHERE
			`id` = ?
		;
	''',
	'get_type_id': 'SELECT `id` FROM bus_types WHERE `name` = ? LIMIT 1;',
	'get_type_name': 'SELECT `name` FROM bus_types WHERE `id` = ? LIMIT 1;',
	'get_admin_id': '''
		SELECT `id` FROM bus_admins 
		WHERE 
			`name` = ? AND 
			`phone` = ?
		LIMIT 1;
	''',
	'insert_admin': '''
		INSERT OR IGNORE INTO bus_admins (
			`name`, `phone`, `address`
		) VALUES (?, ?, ?);
	''',
	'tickets': '''
		CREATE TABLE IF NOT EXISTS tickets (
			`bus_id` INTEGER NOT NULL,
			`seats` INTEGER NOT NULL,
			`time` DATETIME DEFAULT CURRENT_TIMESTAMP,
			FOREIGN KEY (`bus_id`) REFERENCES buses (`id`)
		);
	''',
	'ticket_trigger':'''
		CREATE TRIGGER IF NOT EXISTS log_ticket
		BEFORE UPDATE ON buses
		WHEN NEW.`seats` < OLD.`seats`
		BEGIN
			INSERT INTO tickets (
				`bus_id`,
				`seats`
			) VALUES (
				NEW.`id`,
				OLD.`seats` - NEW.`seats`
			);
		END;
	'''
}
bus_types = {
	1: 'AC',
	2: 'Non-AC',
	3: 'AC Sleeper',
	4: 'Non-AC Sleeper'
}

def init_db():
	with sqlite3.connect('data.db') as db:
		cur = db.cursor()
		cur.execute(scripts['bus_types'])
		cur.executemany(scripts['insert_bus_type'], tuple(bus_types.items()))
		cur.execute(scripts['bus_admins'])
		cur.execute(scripts['buses'])
		cur.execute(scripts['tickets'])
		cur.execute(scripts['ticket_trigger'])
		db.commit()
	
def insert_bus(bus, admin):
	bus_tuple = (
		bus['name'],
		get_type_id(bus['type']),
		bus['from'].upper(),
		bus['to'].upper(),
		bus['date'],
		bus['dep'],
		bus['arr'],
		round(bus['fare'], 2),
		bus['seats'],
		get_admin_id(admin)
	)

	with sqlite3.connect('data.db') as db:
		cur = db.cursor()
		cur.execute(scripts['insert_bus'], bus_tuple)
		db.commit()

def get_type_id(typename):
	typeid = None
	with sqlite3.connect('data.db') as db:
		cur = db.cursor()
		cur.execute(scripts['get_type_id'], (typename,))
		typeid = cur.fetchall()
	if typeid is None or len(typeid) < 1 or len(typeid[0]) < 1:
		return 1
	else:
		return typeid[0][0]

def get_type_name(typeid):
	typename = None
	with sqlite3.connect('data.db') as db:
		cur = db.cursor()
		cur.execute(scripts['get_type_name'], (typeid,))
		typename = cur.fetchall()
	if typename is None or len(typename) < 1 or len(typename[0]) < 1:
		return 1
	else:
		return typename[0][0]

def get_admin_id(admin):
	adminid = None
	with sqlite3.connect('data.db') as db:
		cur = db.cursor()
		cur.execute(scripts['get_admin_id'], (admin['name'], admin['phone']))
		adminid = cur.fetchall()
	if adminid is None or len(adminid) < 1 or len(adminid[0]) < 1:
		create_admin(admin)
		return get_admin_id(admin)
	else:
		return adminid[0][0]

def create_admin(admin):
	admin_tuple = (
		admin['name'],
		admin['phone'],
		admin['address']
	)
	with sqlite3.connect('data.db') as db:
		cur = db.cursor()
		cur.execute(scripts['insert_admin'], admin_tuple)
		db.commit()

def filter_bus(bus):
	bus_filtered = {
		'id': bus[0],
		'name': bus[1],
		'type': get_type_name(bus[2]),
		'from': bus[3].upper(),
		'to': bus[4].upper(),
		'date': datetime.strptime(bus[5], '%Y-%m-%d').date(),
		'dep': bus[6],
		'arr': bus[7],
		'fare': round(bus[8], 2),
		'seats': bus[9]
	}
	return bus_filtered

def unfilter_bus(bus):
	bus_tuple = (
		bus['id'],
		bus['name'],
		get_type_id(bus['type']),
		bus['from'].upper(),
		bus['to'].upper(),
		bus['date'],
		bus['dep'],
		bus['arr'],
		bus['fare'],
		bus['seats']
	)
	return bus_tuple

def get_all_buses():
	buses = []
	with sqlite3.connect('data.db') as db:
		cur = db.cursor()
		cur.execute(scripts['get_all_buses'])
		buses = cur.fetchall()
	return [
		filter_bus(bus) for bus in buses
	]

def get_buses(query):
	bus_query_tuple = (
		get_type_id(query['type']),
		query['from'].upper(),
		query['to'].upper(),
		query['date']
	)
	buses = []
	if query['type'] == 'All Types':
		bus_query_tuple = bus_query_tuple[1:]
		if query['date'] is not None:
			with sqlite3.connect('data.db') as db:
				cur = db.cursor()
				cur.execute(scripts['get_buses_all_types'], bus_query_tuple)
				buses = cur.fetchall()
		else:
			with sqlite3.connect('data.db') as db:
				cur = db.cursor()
				cur.execute(scripts['get_buses_all_dates_all_types'], bus_query_tuple[:2])
				buses = cur.fetchall()
	else:
		if query['date'] is not None:
			with sqlite3.connect('data.db') as db:
				cur = db.cursor()
				cur.execute(scripts['get_buses'], bus_query_tuple)
				buses = cur.fetchall()
		else:
			with sqlite3.connect('data.db') as db:
				cur = db.cursor()
				cur.execute(scripts['get_buses_all_dates'], bus_query_tuple[:3])
				buses = cur.fetchall()
	return [
		filter_bus(bus) for bus in buses
	]

def get_bus(bus_id, filtered=True):
	ret_bus = None
	with sqlite3.connect('data.db') as db:
		cur = db.cursor()
		cur.execute(scripts['get_bus_by_id'], (bus_id,))
		ret_bus = cur.fetchall()
	if ret_bus is not None:
		if len(ret_bus) < 0 or len(ret_bus[0]) < 0:
			return None
		if not filtered:
			return ret_bus[0]
		return filter_bus(ret_bus[0])
	return None

def create_ticket(bus_id, seats=1):
	bus = get_bus(bus_id)
	if seats <= bus['seats']:
		bus['seats'] -= seats
		with sqlite3.connect('data.db') as db:
			cur = db.cursor()
			cur.execute(scripts['update_seats'], (bus['seats'], bus['id']))
			db.commit()


if __name__ != '__main__':
	init_db()