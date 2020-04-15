User Operations
===============

Firewall Address Objects
------------------------

Get
~~~
To get all address objects of a specific type from your sonicos firewall device:

>>> addresses = device.get_firewall_address(address_type='ipv4')

Acceptable values for the address_type parameter are as follows:
    1. ipv4
    2. ipv6
    3. mac
    4. fqdn

The output of this function will be a dictionary with 'address_objects' as a single key. The value of this key will be a list of address objects in your device.
Each member of the list will be a Python dictionary, directly mapped from SonicWall API's json result.

You can also fetch a single address object by passing the name of that object by using the 'specific' parameter:

>>> my_address = device.get_firewall_address(address_type='ipv4', specific='Test Address')
{'address_object': {'ipv4': {'name': 'Test Address', 'uuid': 'cfeeb502-52cf-c94a-0100-2cb8ed5e8880', 'zone': 'LAN', 'host': {'ip': '1.2.3.4'}}}}

Create
~~~~~~
Create

Update
~~~~~~
Update

Delete
~~~~~~
To delete an address object, you just need to pass the "address_type" and "address_name" to the delete_firewall_address function:

>>> device.delete_firewall_address('Test Address')
200
>>> device.delete_firewall_address('Test Address')
404


Firewall Address Groups
------------------------