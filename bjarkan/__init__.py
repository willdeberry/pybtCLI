# Copyright 2016 GetWellNetwork, Inc., BSD copyright and disclaimer apply

SERVICE_NAME = 'org.bluez'
ADAPTER_INTERFACE = SERVICE_NAME + '.Adapter1'
DEVICE_INTERFACE = SERVICE_NAME + '.Device1'


class DeviceNotFound( Exception ):
    pass


class AdapterNotFound( Exception ):
    pass

