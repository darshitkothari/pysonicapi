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
To create an address object, you''ll need to provide 3 parameters to the create_firewall_address function viz. the ip version type ("**version**"), name of the address_object being created ("**address_name**") and a json formatted object configuration ("**data**"):

>>> payload = '{"address_object": {"ipv4": {"name": "Test Address", "zone": "LAN", "host": {"ip": "192.168.168.20"}}}}'
>>> device.create_firewall_address(version='ipv4', address_name='Test Address', data=payload)
200

Update
~~~~~~
To update an address object, you'll need to provide 3 parameters to the update_firewall_address function viz. the ip version type ("**version**"), name of the address_object being created ("**address_name**") and a json formatted object configuration ("**data**" with onlt the fields that are to be updated):

>>> # To update the name of the firewall address object
>>> payload = '{"address_object": {"ipv4": {"name": "Updating Test Address"}}}'
>>> device.update_firewall_address(version='ipv4', address_name='Test Address', data=payload)
200
>>> # To update the host ip of the firewall address object
>>> payload = '{"address_object": {"ipv4": {"host": {"ip": "192.168.168.15"}}}}'
>>> device.update_firewall_address(version='ipv4', address_name='Test Address', data=payload)

Note: you can’t just use a Python dictionary as your payload. Please refer to the "400" section in :doc:`common_issues`

Delete
~~~~~~
To delete an address object, you just need to pass the 'version' and 'address_name' to the delete_firewall_address function:

>>> device.delete_firewall_address(version='ipv4', address_name='Test Address')
200
>>> device.delete_firewall_address(version='ipv4', address_name='Test Address')
404

Firewall Address Groups
------------------------

Get
~~~
To get all address groups of a specific type from your sonicos firewall device:

>>> groups = device.get_address_group(version='ipv4')
{'address_groups': [{'ipv4': {'name': 'Test Group 1', 'uuid': '9b9b3c30-59f7-f1d4-0200-2cb8ed5e8880', 'address_object': {'ipv4': [{'name': 'Test Address - 1'}, {'name': 'Test Address - 2'}]}}}, {'ipv4': {'name': 'Test Group 2', 'uuid': 'd033fe5a-0c1b-df35-0200-2cb8ed5e8880', 'address_object': {'ipv4': [{'name': 'Test Address - 1'}, {'name': 'Test Address - 2'}]}}}]}

Acceptable values for the 'version' parameter are as follows: ipv4, ipv6, mac, fqdn

The output of this function will be a dictionary with 'address_groups' as a single key. The value of this key will be a list of address groups in your device. Each member of the list will be a Python dictionary, directly mapped from SonicWall API's json result.

You can also fetch a single address group by passing the name of that object in the 'specific' parameter:

>>> group = device.get_address_group(version='ipv4', specific='Test Group - 1')
{'address_group': {'ipv4': {'name': 'Test Group 1', 'uuid': '9b9b3c30-59f7-f1d4-0200-2cb8ed5e8880', 'address_object': {'ipv4': [{'name': 'Test Address - 1'}, {'name': 'Test Address - 2'}]}}}}

The output of this function will be a dictionary with 'address_group' as a single key.

Create
~~~~~~
To create an address group, you'll need to provide 3 parameters to the create_address_group function viz. the ip version type ("**version**"), name of the address_group being created ("**group_name**") and a json formatted object configuration ("**data**"):

>>> payload = '{"address_group": {"ipv4": {"name": "Testing Group Creation", "address_object": {"ipv4": [{"name": "Updating Test Address"}]}}}}'
>>> device.create_address_group(version='ipv4', group_name='Testing Group Creation', data=payload)
200

Update
~~~~~~
To update an address group, you'll need to provide 3 parameters to the create_address_group function viz. the ip version type ("**version**"), name of the address_group being created ("**group_name**") and a json formatted object configuration ("**data**"):

>>> # To update the name of the firewall adress group
>>> payload = '{"address_group": {"ipv4": {"name": "Updating Testing Group Creation"}}}'
>>> device.update_address_group(version='ipv4', group_name='Testing Group Creation', data=payload)
>>> # To update firewall address objects in the firewall adress group
>>> payload =
>>> device.update_address_group(version='ipv4', group_name='Testing Group Creation', data=payload)


Delete
~~~~~~
To delete an address group, you just need to pass the 'version' and 'group_name' to the delete_address_group function:

>>> device.delete_address_group(version='ipv4', group_name='Test Group 1')
200
>>> device.delete_address_group(version='ipv4', group_name='Test Group 1')
404

Service Objects
------------------------

Get
~~~
To get all service objects from your sonicos firewall device:

>>> service_objects = device.get_service_object()

Create
~~~~~~
Create

Update
~~~~~~
Update

Delete
~~~~~~
To delete a service object, you just need to pass the 'object_name' to the delete_service_group function:

>>> device.delete_service_object(object_name='Test Service Object 1')
200
>>> device.delete_service_object(object_name='Test Service Object 1')
404

Service Groups
------------------------

Get
~~~
To get all service groups from your sonicos firewall device:

>>> service_groups = device.get_service_group()
{'service_groups': [{'name': 'Test Service Group - 1', 'service_object': [{'name': 'Test Service Object'}], 'service_group': [{'name': 'AD NetBios Services'}]}, {'name': 'Test Service Group - 2', 'service_object': [{'name': 'Test Service Object - 2'}], 'service_group': [{'name': 'AD NetBios Services'}]}]}

The output of this function will be a dictionary with 'service_groups' as a single key. The value of this key will be a list of service groups in your device. Each member of the list will be a Python dictionary, directly mapped from SonicWall API's json result.

You can also fetch a single service group by passing the name of the service group in the 'specific' parameter:

>>> service_group = device.get_service_group(specific='AD Server')
{'service_group': {'name': 'AD Server', 'service_object': [{'name': 'DCE EndPoint'}], 'service_group': [{'name': 'AD NetBios Services'}]}}

The output of this function will be a dictionary with 'service_group' as a single key.

Create
~~~~~~
Create

Update
~~~~~~
Update

Delete
~~~~~~
To delete a service group, you just need to pass the 'group_name' to the delete_service_group function:

>>> device.delete_service_group(group_name='Test Service Group 1')
200
>>> device.delete_service_group(group_name='Test Service Group 1')
404