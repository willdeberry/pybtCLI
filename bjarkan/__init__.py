# Copyright 2016 GetWellNetwork, Inc., BSD copyright and disclaimer apply
"""
Command line utility meant to manage blutooth devices via the command line.

DBus Service
------------

:Bus:
    ``system``
:Busname:
    ``com.getwellnetwork.plc.bjarkan1``
"""


__title__ = 'bjarkan'
__version__ = '1.3.0'
__author__ = 'GetWellNetwork'
__author_email__ = 'willdeberry@gmail.com'
__copyright__ = 'Copyright 2017 GetWellNetwork, Inc., BSD copyright and disclaimer apply'
__description__ = 'Bluetooth command line utility'


BUSNAME = 'com.getwellnetwork.plc.bjarkan1'
OBJECTPATH = '/com/getwellnetwork/plc/bjarkan1/Manager'
INTERFACE = 'com.getwellnetwork.plc.bjarkan1.Manager1'
SUPPORT_OBJECTPATH = '/com/getwellnetwork/plc/bjarkan1/Support'
SUPPORT_INTERFACE = 'com.getwellnetwork.plc.Support1'

SERVICE_NAME = 'org.bluez'
ADAPTER_INTERFACE = SERVICE_NAME + '.Adapter1'
DEVICE_INTERFACE = SERVICE_NAME + '.Device1'


class DeviceNotFound( Exception ):
    pass


class AdapterNotFound( Exception ):
    pass

