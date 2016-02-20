# pybtCLI
A bluez 5 compatible command line utility and python 3 library

* [Usage](#usage)
	* [Pairing/Connecting](#pairingconnecting)
	* [Unpair](#unpair)
	* [Connect](#connect)
	* [Disconnect](#disconnect)
	* [Paired-devices](#paired-devices)
	* [Connected-devices](#connected-devices)
* [Libraries](#libraries)
	* [pybt](#pybt)
	* [connection_manager](#connection_manager)
	* [list_devices](#list_devices)

## Usage
```
usage: bt_manager [-h] [-j] COMMAND ...

Connect to specifed BT device

positional arguments:
	COMMAND
		pair				Pair a device (pairing will also connect)
		unpair				Unpair a device
		connect				Connect a new device
		disconnect			Disconnect a device
		paired-devices		Show all paired devices
		connected-devices	Show all connected devices
		scan				Show all currently known devices

optional arguments:
	-h, --help				show this help message and exit
	-j, --json				Change output format to json instead of plain text
```

### Pairing/Connecting
```
usage: bt_manager pair [-h] -d DEVICE

optional arguments:
	-h, --help					show this help message and exit
	-d DEVICE, --device DEVICE	Specify the device to pair
```

**Example**
```bash
~$ bt_manager pair -d 00:11:22:33:44:55
```

### Unpair
```
usage: bt_manager unpair [-h] -d DEVICE

optional arguments:
	-h, --help					show this help message and exit
	-d DEVICE, --device DEVICE	Specify the device to unpair
```

**Example**
```bash
~$ bt_manager unpair -d 00:11:22:33:44:55
```

### Connect
```
usage: bt_manager connect [-h] -d DEVICE

optional arguments:
	-h, --help					show this help message and exit
	-d DEVICE, --device DEVICE	Specify the device to connect to
```

**Example**
```bash
~$ bt_manager connect -d 00:11:22:33:44:55
```

### Disconnect
```
usage: bt_manager disconnect [-h] -d DEVICE

optional arguments:
	-h, --help					show this help message and exit
	-d DEVICE, --device DEVICE	Specify the device to disconnect from
```

**Example**
```bash
~$ bt_manager disconnect -d 00:11:22:33:44:55
```

### Paired Devices
```
usage: bt_manager paired-devices [-h]

optional arguments:
	-h, --help					show this help message and exit
```

**Example**
```bash
~$ bt_manager paired-devices
```

### Connected Devices
```
usage: bt_manager connected-devices [-h]

optional arguments:
	-h, --help					show this help message and exit
```

**Example**
```bash
~$ bt_manager connected-devices
```

### Scan
```
usage: bt_manager scan [-h]

optional arguments:
	-h, --help					show this help message and exit
```

**Example**
```bash
~$ bt_manager scan
```

## Libraries

### pybt
```python
import pybt

pybt.get_managed_objects()
pybt.find_adapter()
pybt.find_device()
```

### connection_manager
```python
import pybt.connection_manager

pybt.connection_manager.pair_device('00:11:22:33:44:55')
pybt.connection_manager.unpair_device('00:11:22:33:44:55')
pybt.connection_manager.connect_device('00:11:22:33:44:55')
pybt.connection_manager.disconnect_device('00:11:22:33:44:55')
```

### list_devices
```python
import pybt.list_devices

# duration is time in seconds
pybt.list_devices.scan_devices(duration)
pybt.list_devices.gather_device_info()
pybt.list_devices.connected_devices()
pybt.list_devices.paired_devices()
pybt.list_devices.all_devices()
```
