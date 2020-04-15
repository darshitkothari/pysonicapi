Getting Started

Create Firewall Object

To start using "**pysonicapi**", you'll need to create a firewall object:

>>> import pysonicapi
>>> device = pysonicapi.SonicWall(ipaddr="", username="", password="", timeout=30, port=9443)

The parameters displayed above are broken down into mandatory and optional::

Mandatory Parameters:
    1. ipaddr: ip of the target device
    2. username: username of the account being used to log in to the device
    3. password: password for the username provided above

Optional Parameters:
    1. timeout: specifies the timeout for every subsequent api call
    2. port: port number where the device is configured
