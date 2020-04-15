Getting Started

Create Firewall Object
To start using "**pysonicapi**", you'll need to create a firewall object:
>>> import pysonicapi
>>> device = pysonicapi.SonicWall(ipaddr="", username="", password="", timeout=30, port=9443)
The parameters displayed above are broken down into mandatory and optional::
Mandatory Parameters::
* ipaddr: ip of the target device
* username: username of the account being used to log in to the device
* password: password for the username provided above
Optional Parameters::
* timeout: specifies the timeout for every subsequent api call
* port: port number where the device is configured
