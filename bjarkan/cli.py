# Copyright 2016 GetWellNetwork, Inc., BSD copyright and disclaimer apply

from argparse import ArgumentParser
from dbus.mainloop.glib import DBusGMainLoop
from gi.repository.GObject import MainLoop

from .device_manager import DeviceManager
from .list_devices import connected_devices, paired_devices, all_devices


def format_device_data(devices):
    """
    Formats the data that is current devices in the bluetooth database.

    Args:
        devices (list): List of devices and their attributes within dictionaries

    Returns:
        data (list): structured data returned on stdout
    """
    for device in devices:
        print(
            '{!s} {!s} {!s} {!s} {!s} {!s}'.format(
                device['address'],
                device['rssi'],
                device['paired'],
                device['connected'],
                device['icon'],
                device['alias']
            )
        )


def format_results(results):
    """
    Formats the return values and codes from commands.

    Args:
        results (dict): result strind and code from the command that was ran

    Returns:
        results (dict): structured data of the return codes and messages
    """
    print('result: {}, code: {}'.format(results['result'], results['code']))


def pair(args):
    """
    Pair to the specified device

    Args:
        args (dict): args parsed on the command line

    Returns:
        results (dict): return message and code of the operation
    """
    def success():
        try:
            device_manager.trust_device()
            device_manager.connect_device()
            format_results({'result': 'Success', 'code': ''})
        finally:
            mainloop.quit()

    def error(err):
        try:
            if err == 'org.freedesktop.DBus.Error.NoReply' and self.dev:
                code = 'Timeout'
                device_manager.cancel_device()
            if err in ('org.bluez.Error.AuthenticationCanceled', 'org.bluez.Error.AuthenticationFailed',
                    'org.bluez.Error.AuthenticationRejected', 'org.bluez.Error.AuthenticationTimeout'):
                code = 'AuthenticationError'
            else:
                code = 'CreatingDeviceFailed'

            format_results({'result': 'Error', 'code': code})
        finally:
            mainloop.quit()

    mainloop = MainLoop()
    device_manager = DeviceManager(args.device)
    device_manager.pair_device(success, error)
    mainloop.run()


def unpair(args):
    """
    Unpair from the specified device

    Args:
        args (dict): args parsed on the command line

    Returns:
        results (dict): return message and code of the operation
    """
    device_manager = DeviceManager(args.device)
    return format_results(device_manager.unpair_device())


def connect(args):
    """
    Connect to the specified device after pairing has already been authenticated

    Args:
        args (dict): args parsed on the command line

    Returns:
        results (dict): return message and code of the operation
    """
    device_manager = DeviceManager(args.device)
    return format_results(device_manager.connect_device())


def disconnect(args):
    """
    Disconnect from the specified device

    Args:
        args (dict): args parsed on the command line

    Returns:
        results (dict): return message and code of the operation
    """
    device_manager = DeviceManager(args.device)
    return format_results(device_manager.disconnect_device())


def connected(args):
    """
    List the currently connected devices

    Args:
        args (dict): args parsed on the command line

    Returns:
        results (dict): return formatted data listing the currently connected devices
    """
    return format_device_data(connected_devices())


def paired(args):
    """
    List the currently paired devices

    Args:
        args (dict): args parsed on the command line

    Returns:
        results (dict): return formatted data listing the currently paired devices
    """
    return format_device_data(paired_devices())


def scan(args):
    """
    List the devices shown in the scan

    Args:
        args (dict): args parsed on the command line

    Returns:
        results (dict): return formatted data listing the devices found during the scan
    """
    return format_device_data(all_devices())


def main():
    DBusGMainLoop(set_as_default = True)

    parser = ArgumentParser(description = 'Connect to specifed BT device')
    subparsers = parser.add_subparsers(metavar = 'COMMAND')
    subparsers.required = True

    pair_parser = subparsers.add_parser('pair', help = 'Pair a device (pairing will also connect)')
    pair_parser.add_argument('-d', '--device', required = True, help = 'Specify the device to pair')
    pair_parser.set_defaults(func = pair)

    unpair_parser = subparsers.add_parser('unpair', help = 'Unpair a device')
    unpair_parser.add_argument('-d', '--device', required = True, help = 'Specify the device to unpair')
    unpair_parser.set_defaults(func = unpair)

    connect_parser = subparsers.add_parser('connect', help = 'Connect a new device')
    connect_parser.add_argument('-d', '--device', required = True, help = 'Specify the device to connect to')
    connect_parser.set_defaults(func = connect)

    disconnect_parser = subparsers.add_parser('disconnect', help = 'Disconnect a device')
    disconnect_parser.add_argument('-d', '--device', required = True, help = 'Specify the device to disconnect from')
    disconnect_parser.set_defaults(func = disconnect)

    paired_parser = subparsers.add_parser('paired-devices', help = 'Show all paired devices')
    paired_parser.set_defaults(func = paired)

    connected_parser = subparsers.add_parser('connected-devices', help = 'Show all connected devices')
    connected_parser.set_defaults(func = connected)

    list_parser = subparsers.add_parser('scan', help = 'Show all currently known devices')
    list_parser.set_defaults(func = scan)

    args = parser.parse_args()

    result = args.func(args)
    if result:
        return result

    return 0


if __name__ == '__main__':
    main()
