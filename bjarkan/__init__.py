# Copyright 2016 GetWellNetwork, Inc., BSD copyright and disclaimer apply

__title__ = 'bjarkan'
__version__ = '1.2.0'
__author__ = 'GetWellNetwork'
__author_email__ = 'willdeberry@gmail.com'
__copyright__ = 'Copyright 2017 GetWellNetwork, Inc., BSD copyright and disclaimer apply'
__description__ = 'Bluetooth command line utility'


SERVICE_NAME = 'org.bluez'
ADAPTER_INTERFACE = SERVICE_NAME + '.Adapter1'
DEVICE_INTERFACE = SERVICE_NAME + '.Device1'


class DeviceNotFound( Exception ):
    pass


class AdapterNotFound( Exception ):
    pass

