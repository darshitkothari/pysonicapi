#!/usr/bin/env Python
__author__ = "Darshit Kothari"
__copyright__ = "Copyright 2017, Darshit Kothari"
__license__ = "MIT"
__version__ = "0.1.1"


import urllib3
from collections import OrderedDict
import requests

# Disable requests' warnings for insecure connections
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class SonicWall:
    def __init__(self, ipaddr, username, password, timeout=30, port="443"):
        self.ipaddr = ipaddr
        self.username = username
        self.password = password
        self.port = port
        self.timeout = timeout
        self.urlbase = "https://{ipaddr}:{port}/".format(ipaddr=self.ipaddr, port=self.port)
        self.urlapi = "https://{ipaddr}:{port}/api/sonicos/".format(ipaddr=self.ipaddr, port=self.port)
        # Supported HTTP Headers & Supported HTTP MIME Types
        self.headers = OrderedDict([('Accept', 'application/json'), ('Content-Type', 'application/json'),
                                    ('Accept-Encoding', 'application/json'), ('charset', 'UTF-8')])

    # API: Client Authentication (Login / Logout Handlers)
    def login(self):
        """
            Login to SonicWall with info provided during class instantiation
            :return: Open Session
        """
        session = requests.session()
        url = self.urlapi + 'auth'
        session.post(url, auth=(self.username, self.password), headers=self.headers, timeout=self.timeout, verify=False)
        return session

    def logout(self, session):
        """
            Logout of SonicWall device
            :param session: Session created by login method
            :return: None
        """
        url = self.urlbase + 'auth'
        session.delete(url, headers=self.headers, timeout=self.timeout, verify=False)

    # General Logic Methods
    def does_exist(self, object_url):
        """
            GET URL to assert whether an object exists within the firewall
            :param object_url: Object to locate
            :return: Bool - True if exists, False if not
        """
        session = self.login()
        request = session.get(object_url, headers=self.headers, timeout=self.timeout, verify=False)
        self.logout(session)
        if request.status_code == 200:
            return True
        else:
            return False

    # API Interaction Methods
    def get(self, url):
        """
            Perform GET operation on provided URL
            :param url: Target of GET operation
            :return: Request result if successful (type dict), HTTP status code otherwise (type int)
        """
        session = self.login()
        request = session.get(url, headers=self.headers, timeout=self.timeout, verify=False)
        self.logout(session)
        if request.status_code == 200:
            return request.json()
        else:
            return request.status_code

    def put(self, url, data):
        """
            Perform PUT operation on provided URL
            :param url: Target of PUT operation
            :param data: JSON data. MUST be a correctly formatted string. e.g. "{'key': 'value'}"
            :return: HTTP status code returned from PUT operation
        """
        session = self.login()
        result = session.put(url, data=data, headers=self.headers, timeout=self.timeout, verify=False)
        self.logout(session)
        return result.status_code

    def post(self, url, data):
        """
            Perform POST operation on provided URL
            :param url: Target of POST operation
            :param data: JSON data. MUST be a correctly formatted string. e.g. "{'key': 'value'}"
            :return: HTTP status code returned from POST operation
        """
        session = self.login()
        result = session.post(url, data=data, headers=self.headers, timeout=self.timeout, verify=False)
        self.logout(session)
        return result.status_code

    def delete(self, url):
        """
            Perform DELETE operation on provided URL
            :param url: Target of DELETE operation
            :return: HTTP status code returned from DELETE operation
        """
        session = self.login()
        result = session.delete(url, headers=self.headers, timeout=self.timeout, verify=False)
        self.logout(session)
        return result.status_code

    # API: Config - Pending (About Modifying Configuration API)
    def get_pending_changes(self):
        """
            Get all pending changes information from the firewall
            :return: Request result if successful (type dict), HTTP status code otherwise (type int)
        """
        api_url = self.urlapi + 'config/pending/'
        results = self.get(api_url)
        return results

    def commit_pending_changes(self):
        """
            Commit all pending (unsaved) changes information in the firewall
            :return: HTTP status code returned from POST operation
        """
        api_url = self.urlapi + 'config/pending/'
        results = self.post(api_url, data='')
        return results

    def delete_pending_changes(self):
        """
            Deletes all pending (unsaved) changes information in the firewall
            :return: HTTP Status Code returned from DELETE operation
        """
        api_url = self.urlapi + 'config/pending/'
        results = self.delete(api_url)
        return results

    # API: Address Objects - IPv4, IPv6, MAC, FQDN
    def get_firewall_address(self, version='ipv4', specific=False):
        """
            Get address object information from the firewall
            :param version: Type of address objects. Expected values are ipv4, ipv6, mac, fqdn
            :param specific: If provided, a specific object will be returned. If not, all objects will be returned.
            :return: JSON data for all objects in scope of request, as a dict with single key 'address_object' and value
             being a list of address objects in the device
        """
        api_url = self.urlapi + 'address-objects/' + version
        if specific:
            api_url += '/name/' + specific
            if not self.does_exist(api_url):
                return 404
        result = self.get(api_url)
        return result

    def create_firewall_address(self, version, address_name, data):
        """
            Create firewall address record
            :param version: Type of address objects. Expected values are ipv4, ipv6, mac, fqdn
            :param address_name: Address record to be created
            :param data: JSON Data with which to create the address record
                Ex: 1. Multiple Address Objects:
                    payload = '{"address_objects": [{"ipv4": {"name": "Test Address", "zone":"LAN", "host": {"ip": "192.168.168.20"}}}]}'
                    2. Single Address Object:
                    payload = '{"address_object": {"ipv4": {"name": "Test Address", "zone":"LAN", "host": {"ip": "192.168.168.20"}}}}'
            :return: HTTP Status Code
        """
        api_url = self.urlapi + 'address-objects/' + version
        # Check whether target object already exists
        if self.does_exist(api_url + '/name/' + address_name):
            return 403
        result = self.post(api_url, data)
        if result == 200:
            self.commit_pending_changes()
        return result

    def update_firewall_address(self, version, address_name, data):
        """
            Update firewall address record with provided data
            :param version: Type of address objects. Expected values are ipv4, ipv6, mac, fqdn
            :param address_name: name of the address record being updated
            :param data: JSON Data with which to upate the address record
                Any parameter like name, host, zone or others that are to be updated should be provided in the json
                Ex: payload = '{"address_object": {"ipv4": {"name": "Updating Test Address", "host": {"ip": "192.168.168.15"}}}}'
            :return: HTTP Status Code
        """
        api_url = self.urlapi + 'address-objects/' + version + '/name/' + address_name
        # Check whether target object already exists
        if not self.does_exist(api_url):
            return 404
        result = self.put(api_url, data)
        if result == 200:
            self.commit_pending_changes()
        return result

    def delete_firewall_address(self, version, address_name):
        """
            Delete firewall address record
            :param version: Type of address objects. Expected values are ipv4, ipv6, mac, fqdn
            :param address_name: Address record to be deleted
            :return: HTTP status code returned from DELETE operation
        """
        api_url = self.urlapi + 'address-objects/' + version + '/name/' + address_name
        if not self.does_exist(api_url):
            return 404
        result = self.delete(api_url)
        if result == 200:
            self.commit_pending_changes()
        return result

    # API: Address Groups - IPv4, IPv6, MAC, FQDN
    def get_address_group(self, version, specific=False):
        """
            Get address group object information from firewall
            :param version: Type of address objects. Expected values are ipv4, ipv6, mac, fqdn
            :param specific: If provided, a specific object will be returned. If not, all objects will be returned.
            :return: JSON data for all objects in scope of request, as a dict with single key 'address_groups' and value
             being a list of address objects in the device
        """
        api_url = self.urlapi + 'address-groups/' + version
        if specific:
            api_url += '/name/' + specific
            if not self.does_exist(api_url):
                return 404
        result = self.get(api_url)
        return result

    def create_address_group(self, version, group_name, data):
        """
            Create address group object
            :param version: Type of address objects. Expected values are ipv4, ipv6, mac, fqdn
            :param group_name: Address record to be created
            :param data: JSON Data with which to create the address record
                Ex: 1. Multiple Address Groups:
                    payload = '{"address_groups": [{"ipv4": {"name": "Testing Group Creation", "address_object": {"ipv4": [{"name": "New Address"}]}}}]}'
                    2. Single Address Group:
                    payload = '{"address_group": {"ipv4": {"name": "Testing Group Creation", "address_object": {"ipv4": [{"name": "New Address"}]}}}}'
            :return: HTTP Status Code
        """
        api_url = self.urlapi + 'address-groups/' + version
        # Check whether target object already exists
        if self.does_exist(api_url + '/name/' + group_name):
            return 424
        result = self.post(api_url, data)
        if result == 200:
            self.commit_pending_changes()
        return result

    def update_address_group(self, version, group_name, data):
        """
            Create address group object
            :param version: Type of address objects. Expected values are ipv4, ipv6, mac, fqdn
            :param group_name: Address record to be created
            :param data: JSON Data with which to create the address record
                Any parameter like name, address objects or others that are to be updated should be provided in the json:
                Ex: payload = '{"address_group": {"ipv4": {"name": "Testing Group Creation", "address_object": {"ipv4": [{"name": "New Address"}]}}}}'
            :return: HTTP Status Code
        """
        api_url = self.urlapi + 'address-groups/' + version + '/name/' + group_name
        # Check whether target object already exists
        if not self.does_exist(api_url):
            return 404
        result = self.put(api_url, data)
        if result == 200:
            self.commit_pending_changes()
        return result

    def delete_address_group(self, version, group_name):
        """
            Delete firewall address group object
            :param version: Type of address objects. Expected values are ipv4, ipv6, mac, fqdn
            :param group_name: Address record to be deleted
            :return: HTTP Status Code
        """
        api_url = self.urlapi + 'address-groups/' + version + '/name/' + group_name
        if not self.does_exist(api_url):
            return 404
        result = self.delete(api_url)
        self.commit_pending_changes()
        return result

    # API: Service Objects
    def get_service_object(self, specific=False):
        """
            Retrieve service object configuration from the firewall
            :param specific: If provided, a specific object will be returned. If not, all objects will be returned.
            :return: JSON data for all objects in scope of request, nested in a list.
        """
        api_url = self.urlapi + 'service-objects'
        if specific:
            api_url += '/name/' + specific
            if not self.does_exist(api_url):
                return 404
        result = self.get(api_url)
        return result

    def create_service_object(self):
        pass

    def update_service_object(self):
        pass

    def delete_service_object(self, object_name):
        """
            Delete firewall service object
            :param object_name: Address record to be deleted
            :return: HTTP Status Code
        """
        api_url = self.urlapi + 'service-objects/name/' + object_name
        if not self.does_exist(api_url):
            return 404
        result = self.delete(api_url)
        self.commit_pending_changes()
        return result

    # API: Service Groups
    def get_service_group(self, specific=False):
        """
            Retrieve service group configuration from the firewall
            :param specific: If provided, a specific object will be returned. If not, all objects will be returned.
            :return: JSON data for all objects in scope of request, nested in a list.
        """
        api_url = self.urlapi + 'service-groups'
        if specific:
            api_url += '/name/' + specific
            if not self.does_exist(api_url):
                return 404
        result = self.get(api_url)
        return result

    def create_service_group(self):
        pass

    def update_service_group(self):
        pass

    def delete_service_group(self, group_name):
        """
            Delete firewall service group object
            :param group_name: Address record to be deleted
            :return: HTTP Status Code
        """
        api_url = self.urlapi + 'service-groups/name/' + group_name
        if not self.does_exist(api_url):
            return 404
        result = self.delete(api_url)
        self.commit_pending_changes()
        return result

