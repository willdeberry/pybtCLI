# Copyright 2016 GetWellNetwork, Inc., BSD copyright and disclaimer apply

import dbus
import bjarkan



SERVICE_NAME = 'org.bluez'
ADAPTER_INTERFACE = SERVICE_NAME + '.Adapter1'
DEVICE_INTERFACE = SERVICE_NAME + '.Device1'



class DeviceNotFound( Exception ):
	pass


class AdapterNotFound( Exception ):
	pass



def get_managed_objects():
	"""Fetch and return all things in the dbus bluetooth database

	Returns:
		All objects that are in the dbus dictionary and the properties that go along with those devices
	"""
	bus = dbus.SystemBus()
	manager = dbus.Interface(bus.get_object( SERVICE_NAME, '/' ), 'org.freedesktop.DBus.ObjectManager' )
	return manager.GetManagedObjects()



def find_adapter( pattern = None ):
	"""Find the adapter for this specific host.

	Args:
		pattern: the name of the bluetooth adapter

	Returns:
		Object that represents the bluetooth adapter installed in the host.
	"""
	return find_adapter_in_objects( get_managed_objects(), pattern )



def find_adapter_in_objects( objects, pattern = None ):
	"""Does the heavy lifting of sifting through the dbus bluetooth database to find the adapter
	that is installed and used on the host system.

	Args:
		objects: the current contents of the dbus bluetooth
		pattern: the name of the bluetooth adapter

	Returns:
		Object that represents the bluetooth adapter installed in the host.

	Raises:
		AdapterNotFound: bluetooth adapter was not found in the dbus bluetooth database.
	"""
	bus = dbus.SystemBus()
	for path, ifaces in objects.items():
		adapter = ifaces.get( ADAPTER_INTERFACE )
		if not adapter:
			continue
		# If pattern is None
		# or
		# If pattern is equal to the value of the 'Address' property of the assumed adapter
		# or
		# If the assumed adapter ends with the pattern provided i.e: hci0
		if not pattern or pattern == adapter['Address'] or path.endswith( pattern ):
			obj = bus.get_object( SERVICE_NAME, path )
			return dbus.Interface( obj, ADAPTER_INTERFACE )

	raise AdapterNotFound( 'Bluetooth adapter not found: {}'.format( pattern ) )



def find_device( device_address, adapter_pattern = None ):
	"""Attempt to find the device in the list of known devices in the dbus bluetooth database.

	Args:
		device_address: the mac address of the bluetooth device
		pattern: the name of the bluetooth adapter

	Returns:
		Object that represents the bluetooth adapter installed in the host.
	"""
	return find_device_in_objects( get_managed_objects(), device_address, adapter_pattern )



def find_device_in_objects( objects, device_address, adapter_pattern=None ):
	"""Does the heavy lifting of sifting through the dbus bluetooth database to match
	upon the device_address provided.

	Args:
		objects: the current contents of the dbus bluetooth
		device_address: the mac address of the bluetooth device
		pattern: the name of the bluetooth adapter

	Returns:
		Object that represents the bluetooth device.

	Raises:
		DeviceNotFound: bluetooth device was not found in the dbus bluetooth database.
	"""
	bus = dbus.SystemBus()
	path_prefix = ''
	if adapter_pattern:
		adapter = find_adapter_in_objects( objects, adapter_pattern )
		path_prefix = adapter.object_path
	for path, ifaces in objects.items():
		device = ifaces.get( DEVICE_INTERFACE )
		if not device:
			continue
		if device['Address'] == device_address and path.startswith( path_prefix ):
			obj = bus.get_object( SERVICE_NAME, path )
			return dbus.Interface( obj, DEVICE_INTERFACE )

	raise DeviceNotFound( 'Bluetooth device not found: {} {}'.format( device_address, adapter_pattern ) )
