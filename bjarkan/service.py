"""
Provides DBus services for the ultimate question of life, the universe, and everything.

:Bus:
    ``system``
:Busname:
    ``com.getwellnetwork.plc.bjarkan1``
:ObjectPath:
    ``/com/getwellnetwork/plc/bjarkan1/Manager``
:Interface:
    ``com.getwellnetwork.plc.bjarkan1.Manager1``

Examples:

    ::

        from gwn.helpers.dbus import find_gwn_service

        bjarkan_service = find_gwn_service(
            bus = 'system',
            bus_name = 'bjarkan1',
            object_path = 'bjarkan1/Manager',
            interface = 'bjarkan1.Manager1'
        )
"""

import dbus.service

from . import BUSNAME, OBJECTPATH, INTERFACE
from .device_manager import DeviceManager
from .logger import logger
from .list_devices import connected_devices, paired_devices, all_devices, gather_device_info


class ManagerService(dbus.service.Object):

    def __init__(self):
        bus_name = dbus.service.BusName(BUSNAME, bus = dbus.SystemBus())
        super().__init__(bus_name = bus_name, object_path = OBJECTPATH)
        self.device_manager = DeviceManager()

    def _format_results(self, results):
        return {'result': results['result'], 'code': results['code']}

    def _format_device_data(self, devices):
        data = []
        for device in devices:
            device_data = {}
            device_data['address'] = device['address']
            device_data['rssi'] = device['rssi']
            device_data['icon'] = device['icon']
            device_data['paired'] = device['paired']
            device_data['connected'] = device['connected']
            device_data['alias'] = device['alias']
            data.append(device_data)

        return data

    def _success(self):
        logger.info('successfully paired')
        self.device_manager.trust_device(self.pairing_device)
        self.device_manager.connect_device(self.pairing_device)
        payload = {'result': 'Success', 'code': ''}
        self.PairingComplete(payload)

    def _error(self):
        logger.info('failed to pair device')
        if err == 'org.freedesktop.DBus.Error.NoReply' and self.dev:
            code = 'Timeout'
            device_manager.cancel_device(self.pairing_device)
        if err in ('org.bluez.Error.AuthenticationCanceled', 'org.bluez.Error.AuthenticationFailed',
                'org.bluez.Error.AuthenticationRejected', 'org.bluez.Error.AuthenticationTimeout'):
            code = 'AuthenticationError'
        else:
            code = 'CreatingDeviceFailed'

        payload = {'result': 'Error', 'code': code}
        self.PairingComplete(payload)


    @dbus.service.method(INTERFACE, in_signature = 's')
    def Pair(self, device):
        """
        Pair to the specified device

        Args:
            device (str): device's bluetooth address
        """
        logger.info('Attempting to pair to {}', device)
        self.pairing_device = device
        self.device_manager.pair_device(device, self._success, self._error)

    @dbus.service.method(INTERFACE, in_signature = 's', out_signature = 'a{sv}')
    def Unpair(self, device):
        """
        Unpair from the specified device

        Args:
            device (str): device's bluetooth address

        Returns:
            results (dict): return message and code of the operation
        """
        logger.info('Attempting to unpair to {}', device)
        return self._format_results(self.device_manager.unpair_device(device))

    @dbus.service.method(INTERFACE, in_signature = 's', out_signature = 'a{sv}')
    def Connect(self, device):
        """
        Connect to the specified device after pairing has already been authenticated

        Args:
            device (str): device's bluetooth address

        Returns:
            results (dict): return message and code of the operation
        """
        logger.info('Attempting to connect to {}', device)
        return self._format_results(self.device_manager.connect_device(device))

    @dbus.service.method(INTERFACE, in_signature = 's', out_signature = 'a{sv}')
    def Disconnect(self, device):
        """
        Disconnect from the specified device

        Args:
            device (str): device's bluetooth address

        Returns:
            results (dict): return message and code of the operation
        """
        logger.info('Attempting to disconnect from {}', device)
        return self._format_results(self.device_manager.disconnect_device(device))

    @dbus.service.method(INTERFACE, out_signature = 'aa{sv}')
    def Connected(self):
        """
        List the currently connected devices

        Returns:
            results (dict): return formatted data listing the currently connected devices
        """
        return self._format_device_data(connected_devices())

    @dbus.service.method(INTERFACE, out_signature = 'aa{sv}')
    def Paired(self):
        """
        List the currently paired devices

        Returns:
            results (dict): return formatted data listing the currently paired devices
        """
        return self._format_device_data(paired_devices())

    @dbus.service.method(INTERFACE)
    def StartDiscovery(self):
        """
        Start discovery or scanning mode on the bluetooth device
        """
        logger.info('Starting discovering of devices')
        adapter = DeviceManager().find_adapter()
        adapter.StartDiscovery()

    @dbus.service.method(INTERFACE, out_signature = 'aa{sv}')
    def GetScannedDevices(self):
        """
        List the devices shown in the scan. Must explicitly call ``StartDiscovery`` to see
        new devices in the listing.

        Returns:
            results (dict): return formatted data listing the devices found during the scan
        """
        logger.info('Retrieving a list of known devices')
        adapter = DeviceManager().find_adapter()
        devices = gather_device_info()
        try:
            adapter.StopDiscovery()
        except Exception:
            pass

        return self._format_device_data(devices)

    @dbus.service.signal(INTERFACE, signature = 'a{ss}')
    def PairingComplete(self, payload):
        """
        Signal emitted after pairing is completed.

        Args:
            payload (dict): dictionary with the response of the pairing
        """
        logger.info('PairingComplete: emitting {}', payload)
