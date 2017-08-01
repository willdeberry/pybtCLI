# Copyright 2016 GetWellNetwork, Inc., BSD copyright and disclaimer apply

import dbus
from gi.repository.GObject import MainLoop

from bjarkan import ADAPTER_INTERFACE, SERVICE_NAME, DEVICE_INTERFACE, DeviceNotFound, AdapterNotFound
from bjarkan.agent import Agent


class DeviceManager:
    def __init__(self, address = None):
        self.mainloop = MainLoop()
        self.bus = dbus.SystemBus()
        self.manager = dbus.Interface(self.bus.get_object( SERVICE_NAME, '/' ), 'org.freedesktop.DBus.ObjectManager' )

        self.result = None
        self.code = None
        self.address = address

        if self.address:
            self.dev = self.find_device(self.address)

    def find_device( self, adapter_pattern = None ):
        """
        Attempt to find the device address in the list of known devices in the dbus bluetooth database.

        Args:
            pattern: the name of the bluetooth adapter

        Returns:
            Object that represents the bluetooth adapter installed in the host.
        """
        return self.find_device_in_objects(self.manager.GetManagedObjects())

    def find_adapter(self, pattern = None):
        """Find the adapter for this specific host.

        Args:
            pattern: the name of the bluetooth adapter

        Returns:
            Object that represents the bluetooth adapter installed in the host.
        """
        return self.find_adapter_in_objects(self.manager.GetManagedObjects())

    def find_adapter_in_objects(self, objects, pattern = None):
        """
        Does the heavy lifting of sifting through the dbus bluetooth database to find the adapter
        that is installed and used on the host system.

        Args:
            objects: the current contents of the dbus bluetooth
            pattern: the name of the bluetooth adapter

        Returns:
            Object that represents the bluetooth adapter installed in the host.

        Raises:
            AdapterNotFound: bluetooth adapter was not found in the dbus bluetooth database.
        """
        for path, ifaces in objects.items():
            adapter = ifaces.get(ADAPTER_INTERFACE)
            if not adapter:
                continue
            # If pattern is None
            # or
            # If pattern is equal to the value of the 'Address' property of the assumed adapter
            # or
            # If the assumed adapter ends with the pattern provided i.e: hci0
            if not pattern or pattern == adapter['Address'] or path.endswith(pattern):
                obj = self.bus.get_object(SERVICE_NAME, path)
                return dbus.Interface(obj, ADAPTER_INTERFACE)

        raise AdapterNotFound('Bluetooth adapter not found: {}'.format(pattern))

    def find_device_in_objects(self, objects, adapter_pattern = None):
        """
        Does the heavy lifting of sifting through the dbus bluetooth database to match
        upon the device_address provided.

        Args:
            objects: the current contents of the dbus bluetooth
            pattern: the name of the bluetooth adapter

        Returns:
            Object that represents the bluetooth device.

        Raises:
            DeviceNotFound: bluetooth device was not found in the dbus bluetooth database.
        """
        path_prefix = ''
        if adapter_pattern:
            adapter = self.find_adapter_in_objects(objects, adapter_pattern)
            path_prefix = adapter.object_path
        for path, ifaces in objects.items():
            device = ifaces.get(DEVICE_INTERFACE)
            if not device:
                continue
            if device['Address'] == self.address and path.startswith(path_prefix):
                obj = self.bus.get_object(SERVICE_NAME, path)
                return dbus.Interface(obj, DEVICE_INTERFACE)

        raise DeviceNotFound('Bluetooth device not found: {} {}'.format(self.address, adapter_pattern))

    def pair_reply(self):
        self.result = 'Success'
        dev_path = self.dev.object_path
        props = dbus.Interface(self.bus.get_object('org.bluez', dev_path), 'org.freedesktop.DBus.Properties')

        props.Set(DEVICE_INTERFACE, 'Trusted', True)
        self.dev.Connect()
        self.mainloop.quit()
        self.results.update({'result': self.result, 'code': self.code})

    def pair_error(self, error):
        self.result = 'Error'
        err = error.get_dbus_name()
        if err == 'org.freedesktop.DBus.Error.NoReply' and self.dev:
            self.code = 'Timeout'
            self.dev.CancelPairing()
        if err in ('org.bluez.Error.AuthenticationCanceled', 'org.bluez.Error.AuthenticationFailed',
                'org.bluez.Error.AuthenticationRejected', 'org.bluez.Error.AuthenticationTimeout'):
            self.code = 'AuthenticationError'
        else:
            self.code = 'CreatingDeviceFailed'

        self.mainloop.quit()
        self.results.update({'result': self.result, 'code': self.code})

    def pair_device(self):
        """
        Does the act of attempting to pair to the bluetooth device specified.

        Returns:
            results (dict): Dictionary consisting of the result of pairing attempt
        """
        self.results = {}
        capability = 'KeyboardDisplay'
        path = '/test/agent'
        agent = Agent(self.bus, path)
        obj = self.bus.get_object('org.bluez', '/org/bluez')
        manager = dbus.Interface( obj, 'org.bluez.AgentManager1')

        manager.RegisterAgent(path, capability)
        agent.set_exit_on_release(False)
        self.dev.Pair(reply_handler = self.pair_reply, error_handler = self.pair_error, timeout = 60000)
        self.mainloop.run()
        return self.results

    def unpair_device(self):
        """
        Does the act of attempting to unpair to the bluetooth device specified.

        Returns:
            results (dict): Dictionary consisting of the result of unpairing attempt
        """
        managed_objects = self.manager.GetManagedObjects()
        adapter = self.find_adapter_in_objects(managed_objects)
        dev = self.find_device_in_objects(managed_objects)
        dev_path = dev.object_path
        try:
            adapter.RemoveDevice(dev_path)
            self.result = 'Success'
        except dbus.exceptions.DBusException as e:
            self.result = 'Error'
            self.code = e.get_dbus_name()
        except:
            self.result = 'Error'
            self.code = 'UnpairFailure'
        finally:
            return {'result': self.result, 'code': self.code}

    def disconnect_device(self):
        """
        Does the act of attempting to discconnect to the bluetooth device specified.

        Returns:
            results (dict): Dictionary consisting of the result of disconnect attempt
        """
        try:
            self.dev.Disconnect()
            self.result = 'Success'
        except dbus.exceptions.DBusException as e:
            self.result = 'Error'
            self.code = e.get_dbus_name()
        except:
            self.result = 'Error'
            self.code = 'DisconnectFailure'
        finally:
            return {'result': self.result, 'code': self.code}

    def connect_device(self):
        """
        Does the act of attempting to connect to the bluetooth device specified.

        Returns:
            results (dict): Dictionary consisting of the result of connection attempt
        """
        try:
            self.dev.Connect()
            self.result = 'Success'
        except dbus.exceptions.DBusException as e:
            self.result = 'Error'
            self.code = e.get_dbus_name()
        except:
            self.result = 'Error'
            self.code = 'ConnectionFailure'
        finally:
            return {'result': self.result, 'code': self.code}
