# Copyright 2016 GetWellNetwork, Inc., BSD copyright and disclaimer apply

import dbus

from . import ADAPTER_INTERFACE, SERVICE_NAME, DEVICE_INTERFACE, DeviceNotFound, AdapterNotFound
from .agent import Agent
from .logger import logger


class DeviceManager:
    def __init__(self):
        self.bus = dbus.SystemBus()
        self.manager = dbus.Interface(self.bus.get_object( SERVICE_NAME, '/' ), 'org.freedesktop.DBus.ObjectManager' )

        self.result = ''
        self.code = ''

    def find_device(self, address, adapter_pattern = None):
        """
        Attempt to find the device address in the list of known devices in the dbus bluetooth database.

        Args:
            pattern: the name of the bluetooth adapter

        Returns:
            Object that represents the bluetooth adapter installed in the host.
        """
        return self.find_device_in_objects(address, self.manager.GetManagedObjects())

    def find_adapter(self, pattern = None):
        """
        Find the adapter for this specific host.

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

    def find_device_in_objects(self, address, objects, adapter_pattern = None):
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
            if device['Address'] == address and path.startswith(path_prefix):
                obj = self.bus.get_object(SERVICE_NAME, path)
                return dbus.Interface(obj, DEVICE_INTERFACE)

        raise DeviceNotFound('Bluetooth device not found: {} {}'.format(self.address, adapter_pattern))

    def cancel_device(self, address):
        """
        Cancels the pairing attempt

        Args:
            address (str): address of the device
        """
        device = self.find_device(address)

        device.CancelPairing()

    def trust_device(self, address):
        """
        Trusts a device

        Args:
            address (str): address of the device
        """
        device = self.find_device(address)
        dev_path = device.object_path
        props = dbus.Interface(self.bus.get_object('org.bluez', dev_path), 'org.freedesktop.DBus.Properties')

        props.Set(DEVICE_INTERFACE, 'Trusted', True)

    def pair_device(self, address, success, error):
        """
        Does the act of attempting to pair to the bluetooth device specified.

        Args:
            address (str): address of the device

        Returns:
            results (dict): Dictionary consisting of the result of pairing attempt
        """
        device = self.find_device(address)
        self.results = {}
        path = '/test/agent'
        obj = self.bus.get_object('org.bluez', '/org/bluez')
        manager = dbus.Interface( obj, 'org.bluez.AgentManager1')

        try:
            manager.UnregisterAgent(path)
        except Exception:
            logger.info('did not find an agent to unregister')
            pass

        try:
            self.agent = Agent(self.bus, path)
        except Exception:
            pass

        manager.RegisterAgent(path, 'KeyboardDisplay')
        device.Pair(reply_handler = success, error_handler = error, timeout = 60000)
        return self.results

    def unpair_device(self, address):
        """
        Does the act of attempting to unpair to the bluetooth device specified.

        Args:
            address (str): address of the device

        Returns:
            results (dict): Dictionary consisting of the result of unpairing attempt
        """
        managed_objects = self.manager.GetManagedObjects()
        adapter = self.find_adapter_in_objects(managed_objects)
        dev = self.find_device_in_objects(address, managed_objects)
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

    def disconnect_device(self, address):
        """
        Does the act of attempting to discconnect to the bluetooth device specified.

        Args:
            address (str): address of the device

        Returns:
            results (dict): Dictionary consisting of the result of disconnect attempt
        """
        device = self.find_device(address)

        try:
            device.Disconnect()
            self.result = 'Success'
        except dbus.exceptions.DBusException as e:
            self.result = 'Error'
            self.code = e.get_dbus_name()
        except:
            self.result = 'Error'
            self.code = 'DisconnectFailure'
        finally:
            return {'result': self.result, 'code': self.code}

    def connect_device(self, address):
        """
        Does the act of attempting to connect to the bluetooth device specified.

        Args:
            address (str): address of the device

        Returns:
            results (dict): Dictionary consisting of the result of connection attempt
        """
        device = self.find_device(address)

        try:
            device.Connect()
            self.result = 'Success'
        except dbus.exceptions.DBusException as e:
            self.result = 'Error'
            self.code = e.get_dbus_name()
        except:
            self.result = 'Error'
            self.code = 'ConnectionFailure'
        finally:
            return {'result': self.result, 'code': self.code}
