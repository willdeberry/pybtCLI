# Copyright 2016 GetWellNetwork, Inc., BSD copyright and disclaimer apply

import dbus
import dbus.service
from dbus.mainloop.glib import DBusGMainLoop
from gi.repository import GObject
import json
import os
from random import randint
import sys

from bjarkan import find_adapter, find_device, find_adapter_in_objects, find_device_in_objects, get_managed_objects
import bjarkan.list_devices



DBusGMainLoop( set_as_default=True )



class Agent( dbus.service.Object ):
	"""This is the code that deals with generating a PIN code if needed by the bluetooth device
	we are connecting to in order to complete the authentication handshake.
	"""
	AGENT_INTERFACE = 'org.bluez.Agent1'
	exit_on_release = True


	def set_exit_on_release( self, exit_on_release ):
		self.exit_on_release = exit_on_release


	@dbus.service.method( AGENT_INTERFACE, in_signature = '', out_signature = '' )
	def Release( self ):
		if self.exit_on_release:
			mainloop.quit()


	@dbus.service.method( AGENT_INTERFACE, in_signature = 'os', out_signature = '' )
	def DisplayPinCode( self, device, pincode ):
		print( 'DisplayPinCode ({}, {})'.format( device, pincode ) )


	@dbus.service.method( AGENT_INTERFACE, in_signature = 'ou', out_signature = '' )
	def RequestConfirmation( self, device, passkey ):
		print( 'RequestConfirmation ({}, {})'.format( device, passkey ) )


def pair_device( device ):
	"""Does the act of attempting to pair to the bluetooth device specified.

	Args:
		device: mac address of the bluetooth device to connect to
		json: to change the return format to json instead of plain text. Meant for API use.
	"""
	result = None
	code = None
	results = {}
	mainloop = GObject.MainLoop()
	bus = dbus.SystemBus()
	capability = 'KeyboardDisplay'
	path = '/test/agent'
	agent = Agent( bus, path )
	obj = bus.get_object( 'org.bluez', '/org/bluez' )
	manager = dbus.Interface( obj, 'org.bluez.AgentManager1')
	dev = find_device( device )


	def pair_reply():
		result = 'Success'
		dev_path = dev.object_path
		props = dbus.Interface(bus.get_object( 'org.bluez', dev_path ), 'org.freedesktop.DBus.Properties' )

		props.Set( DEVICE_INTERFACE, 'Trusted', True )
		dev.Connect()
		mainloop.quit()
		results.update( { 'result': result, 'code': code } )


	def pair_error( error ):
		result = 'Error'
		err = error.get_dbus_name()
		if err == 'org.freedesktop.DBus.Error.NoReply' and dev:
			code = 'Timeout'
			dev.CancelPairing()
		if err in ( 'org.bluez.Error.AuthenticationCanceled', 'org.bluez.Error.AuthenticationFailed',
				'org.bluez.Error.AuthenticationRejected', 'org.bluez.Error.AuthenticationTimeout' ):
			code = 'AuthenticationError'
		else:
			code = 'CreatingDeviceFailed'

		mainloop.quit()
		results.update( { 'result': result, 'code': code } )


	manager.RegisterAgent( path, capability )
	agent.set_exit_on_release( False )
	dev.Pair( reply_handler = pair_reply, error_handler = pair_error, timeout = 60000 )
	mainloop.run()
	return results



def unpair_device( device ):
	"""Does the act of attempting to unpair to the bluetooth device specified.

	Args:
		device: mac address of the bluetooth device to connect to
		json: to change the return format to json instead of plain text. Meant for API use.
	"""
	result = None
	code = None
	managed_objects = get_managed_objects()
	adapter = find_adapter_in_objects( managed_objects )
	dev = find_device_in_objects( managed_objects, device )
	dev_path = dev.object_path
	try:
		adapter.RemoveDevice( dev_path )
		result = 'Success'
	except dbus.exceptions.DBusException as e:
		result = 'Error'
		code = e.get_dbus_name()
	except:
		result = 'Error'
		code = 'UnpairFailure'
	finally:
		return { 'result': result, 'code': code }



def disconnect_device( device ):
	"""Does the act of attempting to discconnect to the bluetooth device specified.

	Args:
		device: mac address of the bluetooth device to connect to
		json: to change the return format to json instead of plain text. Meant for API use.
	"""
	result = None
	code = None
	dev = find_device( device )
	try:
		dev.Disconnect()
		result = 'Success'
	except dbus.exceptions.DBusException as e:
		result = 'Error'
		code = e.get_dbus_name()
	except:
		result = 'Error'
		code = 'DisconnectFailure'
	finally:
		return { 'result': result, 'code': code }



def connect_device( device ):
	"""Does the act of attempting to connect to the bluetooth device specified.

	Args:
		device: mac address of the bluetooth device to connect to
		json: to change the return format to json instead of plain text. Meant for API use.
	"""
	result = None
	code = None
	dev = find_device( device )

	try:
		dev.Connect()
		result = 'Success'
	except dbus.exceptions.DBusException as e:
		result = 'Error'
		code = e.get_dbus_name()
	except:
		result = 'Error'
		code = 'ConnectionFailure'
	finally:
		return { 'result': result, 'code': code }
