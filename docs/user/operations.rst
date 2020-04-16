User Operations
===============

Firewall Address Objects
------------------------

Get
~~~
To get all address objects of a specific type from your sonicos firewall device:

>>> addresses = device.get_firewall_address(version='ipv4')
{'address_object': [{'ipv4': {'name': 'Test Address - 1', 'uuid': 'cfeeb502-52cf-c94a-0100-2cb8ed5e8880', 'zone': 'LAN', 'host': {'ip': '1.2.3.4'}}}, {'ipv4': {'name': 'Test Address - 2', 'uuid': 'cfeeb502-52cf-c94a-0100-2cb8ed5e8880', 'zone': 'LAN', 'host': {'ip': '1.2.3.4'}}}]}

Acceptable values for the 'version' parameter are as follows: ipv4, ipv6, mac, fqdn

The output of this function will be a dictionary with 'address_objects' as a single key. The value of this key will be a list of address objects in your device.
Each member of the list will be a Python dictionary, directly mapped from SonicWall API's json result.

You can also fetch a single address object by passing the name of that object by using the 'specific' parameter:

>>> my_address = device.get_firewall_address(version='ipv4', specific='Test Address')
{'address_object': {'ipv4': {'name': 'Test Address', 'uuid': 'cfeeb502-52cf-c94a-0100-2cb8ed5e8880', 'zone': 'LAN', 'host': {'ip': '1.2.3.4'}}}}

The output of this function will be a dictionary with 'address_object' as a single key.

Create
~~~~~~
Create

Update
~~~~~~
Update

Delete
~~~~~~
To delete an address object, you just need to pass the "address_type" and "address_name" to the delete_firewall_address function:

>>> device.delete_firewall_address(version='ipv4', address_name='Test Address')
200
>>> device.delete_firewall_address(version='ipv4', address_name='Test Address')
404


Firewall Address Groups
------------------------

Get
~~~
To get all address groups of a specific type from your sonicpos firewall device:

>>> groups = device.get_address_group(version='ipv4')
{'address_groups': [{'ipv4': {'name': 'Test Group 1', 'uuid': '9b9b3c30-59f7-f1d4-0200-2cb8ed5e8880', 'address_object': {'ipv4': [{'name': 'Test Address - 1'}, {'name': 'Test Address - 2'}]}}}, {'ipv4': {'name': 'Test Group 2', 'uuid': 'd033fe5a-0c1b-df35-0200-2cb8ed5e8880', 'address_object': {'ipv4': [{'name': 'Test Address - 1'}, {'name': 'Test Address - 2'}]}}}]}

Acceptable values for the 'version' parameter are as follows: ipv4, ipv6, mac, fqdn

The output of this function will be a dictionary with 'address_groups' as a single key. The value of this key will be a list of address groups in your device. Each member of the list will be a Python dictionary, directly mapped from SonicWall APPI's json result.

You can also fetch a single address group by passing the name of that object in the 'specific' parameter:

>>> group = device.get_address_group(version='ipv4', specific='Test Group - 1')
{'address_group': {'ipv4': {'name': 'Test Group 1', 'uuid': '9b9b3c30-59f7-f1d4-0200-2cb8ed5e8880', 'address_object': {'ipv4': [{'name': 'Test Address - 1'}, {'name': 'Test Address - 2'}]}}}}

The output of this function will be a dictionary with 'address_group' as a single key.

Create
~~~~~~
Create

Update
~~~~~~
Update

Delete
~~~~~~
To delete