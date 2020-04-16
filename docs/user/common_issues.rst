Common Issues
=============

400 error when creating / updating objects
------------------------------------------

400 is basically the HTTP status code for "Failed Dependency". With SOnicWall API, this most frequently appears if an invalid request was submitted where in either the request URI was incorrect or the request body isn't as expected.

When creating or updating an object via **pysonicapi**, you need to provide a JSON formatted string of parameters. While it may look like the examples provided in the user guide are python dictionaries, they're not *exactly*. All of the parameter payloads used in the examples provided are JSON formatted string representations of python dictionaries.

Take for example, what happens when we fire a straight dictionary of values to the device:

>>> payload = {"address_object": {"ipv4": {"name": "Test Address", "zone": "LAN", "host": {"ip": "192.168.168.20"}}}}
>>> device.create_firewall_address(version='ipv4', address_name='Test Address', data=payload)
400

However, if you repr the dictionary to create a string representation:

>>> payload = {"address_object": {"ipv4": {"name": "Test Address", "zone": "LAN", "host": {"ip": "192.168.168.20"}}}}
>>> device.create_firewall_address(version='ipv4', address_name='Test Address', data=repr(payload))
200
