# Copyright 2016 GetWellNetwork, Inc., BSD copyright and disclaimer apply

import sys
import dbus
from dbus.mainloop.glib import DBusGMainLoop
from gi.repository import GObject

from bjarkan import find_adapter, get_managed_objects



def quit( mainloop ):
	mainloop.quit()



def scan_devices( duration = 10 ):
	""" This causes the bluetooth system to scan for any broadcasting devices. Once found, the devices get added to a
	dbus backed database specific for bluetooth for retrieval later.

	Args:
		duration (int): the amount of time that the scan should run for in seconds.
	"""
	DBusGMainLoop( set_as_default = True )
	bus = dbus.SystemBus()
	adapter = find_adapter()

	adapter.StartDiscovery()

	mainloop = GObject.MainLoop()
	GObject.timeout_add( duration * 1000, quit, mainloop )
	mainloop.run()



def gather_device_info():
	"""This function is responsible for digging through the dbus bluetooth database and retrieving all the known
	devices and the information about those devices. The database is seeded from scan_devices.

	Returns:
		List of device objects. Each object is one device and consisting of the properties of that device.
			[
				{
					'alias': 'Bluetooth Keyboard',
					'address': '00:00:00:00:00:00',
					'rssi': '-54',
					'icon': 'input-keyboard',
					'paired': 0,
					'connected': 0
				}
			]
	"""
	devices = []
	bus = dbus.SystemBus()
	objects = get_managed_objects()
	all_devices = ( str( path ) for path, interfaces in objects.items() if DEVICE_INTERFACE in interfaces )
	for path, ifaces in objects.items():
		if ADAPTER_INTERFACE not in ifaces:
			continue
		device_list = [ d for d in all_devices if d.startswith( path + '/' ) ]
		for dev_path in device_list:
			dev = objects[dev_path]
			properties = dev[DEVICE_INTERFACE]
			rssi = None
			icon = None
			if 'RSSI' in properties:
				rssi = int( properties['RSSI'] )
			if 'Icon' in properties:
				icon = str( properties['Icon'] )
			alias = properties['Alias']
			address = properties['Address']
			paired = properties['Paired']
			connected = properties['Connected']
			devices.append( { 'alias': str( alias ), 'address': str( address ), 'rssi': rssi, 'icon': icon, 'paired': int( paired ), 'connected': int( connected ) } )

	return devices



def connected_devices():
	"""Fetches the dbus bluetooth database and returns a list of devices that have a connected value of '1'

	Returns:
		List of device objects. Each object is one device and consisting of the properties of that device.
			[
				{
					'alias': 'Bluetooth Keyboard',
					'address': '00:00:00:00:00:00',
					'rssi': '-54',
					'icon': 'input-keyboard',
					'paired': 1,
					'connected': 1
				}
			]
	"""
	devices = gather_device_info()
	connected = []
	for device in devices:
		if device['connected']:
			connected.append( device )

	return connected



def paired_devices():
	"""Fetches the dbus bluetooth database and returns a list of devices that have a paired value of '1'

	Returns:
		List of device objects. Each object is one device and consisting of the properties of that device.
			[
				{
					'alias': 'Bluetooth Keyboard',
					'address': '00:00:00:00:00:00',
					'rssi': '-54',
					'icon': 'input-keyboard',
					'paired': 1,
					'connected': 0
				}
			]
	"""
	devices = gather_device_info()
	paired = []
	for device in devices:
		if device['paired']:
			paired.append( device )

	return paired


def all_devices():
	"""Forces a scan to populate the bluetooth dbus database, fetches the database information and returns it.

	Returns:
		List of device objects. Each object is one device and consisting of the properties of that device.
			[
				{
					'alias': 'Bluetooth Keyboard',
					'address': '00:00:00:00:00:00',
					'rssi': '-54',
					'icon': 'input-keyboard',
					'paired': 1,
					'connected': 0
				}
			]
	"""
	scan_devices()
	devices = gather_device_info()
	return devices
