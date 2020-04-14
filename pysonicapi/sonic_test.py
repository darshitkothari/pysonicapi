from pysonicapi import SonicWall


sonic = SonicWall(ipaddr='10.3.1.254', port=4443, username='darshit', password='D@r$H!t@PyThon')
# print(sonic.commit_pending_changes())
# print(sonic.get_pending_changes())
#print(sonic.get_firewall_address(address_type='ipv4', specific='Test Darshit'))

# payload = '{"address_object":{"ipv4":{"name":"Test Darshit","zone":"LAN","host":{"ip":"192.168.168.10"}}}}'
# address = sonic.create_firewall_address(address_type='ipv4', address='Test Darshit', data=payload)

# print(sonic.get_firewall_address(address_type='ipv4', specific='Test Darshit'))
print(sonic.delete_firewall_address(address_type='ipv4', address='Test Darshit - Update'))
# print(sonic.get_firewall_address(address_type='ipv4', specific='X0 IP'))

# payload = '{"address_object":{"ipv4":{"name":"Test Darshit - Update","zone":"LAN","host":{"ip":"192.168.168.16"}}}}'
# new = sonic.update_firewall_address(address_type='ipv4', address='Test Darshit', data=payload)
# print(sonic.get_firewall_address(address_type='ipv4', specific='Test Darshit - Update'))
