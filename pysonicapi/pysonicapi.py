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
            :return: Request result if successful (type list), HTTP status code otherwise (type int)
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
        result = session.put(url, data=data, headers=self.headers, timeout=self.timeout, verify=False).status_code
        self.logout(session)
        return result

    def post(self, url, data):
        """
            Perform POST operation on provided URL
            :param url: Target of POST operation
            :param data: JSON data. MUST be a correctly formatted string. e.g. "{'key': 'value'}"
            :return: HTTP status code returned from POST operation
        """
        session = self.login()
        result = session.post(url, data=data, headers=self.headers, timeout=self.timeout, verify=False).status_code
        self.logout(session)
        return result

    def delete(self, url):
        """
            Perform DELETE operation on provided URL
            :param url: Target of DELETE operation
            :return: HTTP status code returned from DELETE operation
        """
        session = self.login()
        result = session.delete(url, headers=self.headers, timeout=self.timeout, verify=False).status_code
        self.logout(session)
        return result

    # API: Config - Pending (About Modifying Configuration API)
    def get_pending_changes(self, specific=False, filters=False):
        """
            Get pending changes information from firewall
            :param specific: If provided, a specific object will be returned. If not, all objects will be returned.
            :param filters: If provided, the raw filter is appended to the API call.
            :return: JSON data for all objects in scope of request, nested in a list.
        """
        api_url = self.urlapi + 'config/pending/'
        if specific:
            api_url = api_url + specific
        elif filters:
            api_url += "?filter=" + filters
        results = self.get(api_url)
        return results

    def commit_pending_changes(self):
        """
            Get pending changes information from firewall
            :param specific: If provided, a specific object will be returned. If not, all objects will be returned.
            :param filters: If provided, the raw filter is appended to the API call.
            :return: JSON data for all objects in scope of request, nested in a list.
        """
        api_url = self.urlapi + 'config/pending/'
        results = self.post(api_url, data='')
        return results

    def delete_pending_changes(self):
        """
            Delete firewall address record
            :param address: Address record to be deleted
            :return: HTTP Status Code
        """
        api_url = self.urlapi + 'config/pending/'
        results = self.delete(api_url)
        return results

    # API: Address Objects - IPv4, IPv6, MAC, FQDN
    def get_firewall_address(self, address_type='ipv4', specific=False, filters=False):
        """
            Get address object information from firewall
            :param address_type: Type of address objects. Expected values are ipv4, ipv6, mac, fqdn
            :param specific: If provided, a specific object will be returned. If not, all objects will be returned.
            :param filters: If provided, the raw filter is appended to the API call.
            :return: JSON data for all objects in scope of request, nested in a list.
        """
        api_url = self.urlapi + 'address-objects/' + address_type
        if specific:
            api_url += '/name/' + specific
            if not self.does_exist(api_url):
                return 404
        elif filters:
            api_url += "?filter=" + filters
        results = self.get(api_url)
        return results

    def create_firewall_address(self, address_type, address, data):
        """
            Create firewall address record
            :param address_type: Type of address objects. Expected values are ipv4, ipv6, mac, fqdn
            :param address: Address record to be created
            :param data: JSON Data with which to create the address record
                Ex: payload = '{"address_object": [{"ipv4": {"name": "Term Server Private","zone": "LAN","host": {"ip": "192.168.168.10"}}}]}'
            :return: HTTP Status Code
        """
        api_url = self.urlapi + 'address-objects/' + address_type
        # Check whether target object already exists
        if self.does_exist(api_url + '/name/' + address):
            return 424
        result = self.post(api_url, data)
        self.commit_pending_changes()
        return result

    def update_firewall_address(self, address_type, address, data):
        """
            Update firewall address record with provided data
            :param address_type: Type of address objects. Expected values are ipv4, ipv6, mac, fqdn
            :param address: name of the address record being updated
            :param data: JSON Data with which to upate the address record
                Ex: payload = "{'subnet': '192.168.0.0 255.255.255.0'}"
            :return: HTTP Status Code
        """
        api_url = self.urlapi + 'address-objects/' + address_type + '/name/' + address
        # Check whether target object already exists
        if not self.does_exist(api_url):
            return 404
        result = self.put(api_url, data)
        self.commit_pending_changes()
        return result

    def delete_firewall_address(self, address_type, address):
        """
            Delete firewall address record
            :param address_type: Type of address objects. Expected values are ipv4, ipv6, mac, fqdn
            :param address: Address record to be deleted
            :return: HTTP Status Code
        """
        api_url = self.urlapi + 'address-objects/' + address_type + '/name/' + address
        if not self.does_exist(api_url):
            return 404
        result = self.delete(api_url)
        self.commit_pending_changes()
        return result
