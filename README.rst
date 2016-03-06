bjarkan
=======

A bluez 5 compatible command line utility

-  `License <#license>`__
-  `Installation <#installation>`__

   -  `Requirements <#requirements>`__
   -  `Steps <#steps>`__

-  `Usage <#usage>`__

   -  `Pairing/Connecting <#pairingconnecting>`__
   -  `Unpair <#unpair>`__
   -  `Connect <#connect>`__
   -  `Disconnect <#disconnect>`__
   -  `Paired-devices <#paired-devices>`__
   -  `Connected-devices <#connected-devices>`__

License
-------

| Copyright (c) 2016, GetWellNetwork, Inc.
| All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are
met:

#. Redistributions of source code must retain the above copyright
   notice, this list of conditions and the following disclaimer.
#. Redistributions in binary form must reproduce the above copyright
   notice, this list of conditions and the following disclaimer in the
   documentation and/or other materials provided with the distribution.
#. Neither the name of the copyright holder nor the names of its
   contributors may be used to endorse or promote products derived from
   this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS
IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED
TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A
PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED
TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

Installation
------------

Requirements
~~~~~~~~~~~~

::

    python3
    pygobject >= 3.18.2

Steps
~~~~~

::

    git clone https://github.com/willdeberry/bjarkan.git
    cd bjarkan
    python3 setup.py install

Usage
-----

::

    usage: bjarkan [-h] [-j] COMMAND ...

    Connect to specifed BT device

    positional arguments:
        COMMAND
            pair                Pair a device (pairing will also connect)
            unpair              Unpair a device
            connect             Connect a new device
            disconnect          Disconnect a device
            paired-devices      Show all paired devices
            connected-devices   Show all connected devices
            scan                Show all currently known devices

    optional arguments:
        -h, --help              show this help message and exit
        -j, --json              Change output format to json instead of plain text

Pairing/Connecting
~~~~~~~~~~~~~~~~~~

::

    usage: bjarkan pair [-h] -d DEVICE

    optional arguments:
        -h, --help                  show this help message and exit
        -d DEVICE, --device DEVICE  Specify the device to pair

**Example**

.. code:: bash

    ~$ bjarkan pair -d 00:11:22:33:44:55

Unpair
~~~~~~

::

    usage: bjarkan unpair [-h] -d DEVICE

    optional arguments:
        -h, --help                  show this help message and exit
        -d DEVICE, --device DEVICE  Specify the device to unpair

**Example**

.. code:: bash

    ~$ bjarkan unpair -d 00:11:22:33:44:55

Connect
~~~~~~~

::

    usage: bjarkan connect [-h] -d DEVICE

    optional arguments:
        -h, --help                  show this help message and exit
        -d DEVICE, --device DEVICE  Specify the device to connect to

**Example**

.. code:: bash

    ~$ bjarkan connect -d 00:11:22:33:44:55

Disconnect
~~~~~~~~~~

::

    usage: bjarkan disconnect [-h] -d DEVICE

    optional arguments:
        -h, --help                  show this help message and exit
        -d DEVICE, --device DEVICE  Specify the device to disconnect from

**Example**

.. code:: bash

    ~$ bjarkan disconnect -d 00:11:22:33:44:55

Paired Devices
~~~~~~~~~~~~~~

::

    usage: bjarkan paired-devices [-h]

    optional arguments:
        -h, --help                  show this help message and exit

**Example**

.. code:: bash

    ~$ bjarkan paired-devices

Connected Devices
~~~~~~~~~~~~~~~~~

::

    usage: bjarkan connected-devices [-h]

    optional arguments:
        -h, --help                  show this help message and exit

**Example**

.. code:: bash

    ~$ bjarkan connected-devices

Scan
~~~~

::

    usage: bjarkan scan [-h]

    optional arguments:
        -h, --help                  show this help message and exit

**Example**

.. code:: bash

    ~$ bjarkan scan
