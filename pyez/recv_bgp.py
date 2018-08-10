#!/usr/bin/env python
import sys
import os
import getpass
import json
import xmltodict
from lxml import etree
from jnpr.junos import Device
from jnpr.junos.exception import *
from jnpr.junos.factory.factory_loader import FactoryLoader

def lict(lict_data):
    try:
        if isinstance(lict_data, list):
            return lict_data
        elif isinstance(lict_data, dict):
            return [lict_data]
    except (RuntimeError, TypeError, NameError):
        pass

host = sys.argv[1]
user = input("Enter Usename: ")
pwd = getpass.getpass("Enter password: ")
port = '2202'

peer = sys.argv[2]
dev = Device(host=host, user=user, passwd=pwd, port=port)

try:
    dev.open()
except ConnectError as conErr:
    print(f"Cannot connect the device: {conErr}")
    sys.exit(1)
route = dev.rpc.get_route_information(table='inet.0', peer=peer)
hostname = dev.facts.get("hostname")
dev.close()
data = xmltodict.parse(etree.tostring(route))
bgp = data.get("route-information", {}).get("route-table").get("rt")
bgp_data = bgp if isinstance(bgp, list) else [bgp]

print(f'Host: {hostname}')
print(f'{"Routes":20} {"AS Path"}')
for bgp_recv in bgp_data:
    recv_route = bgp_recv.get("rt-destination")
    rt_entry = bgp_recv.get("rt-entry")
    if rt_entry.get("active-tag") == '*':
        as_path = rt_entry.get("as-path")
        print(f'{recv_route:20} {as_path}')
