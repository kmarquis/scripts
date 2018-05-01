#!/usr/bin/env python
import sys
import getpass
import json
import xmltodict
import platform
import socket
from lxml import etree
from huepy import *
from jnpr.junos import Device
from jnpr.junos.exception import *

def lict(lict_data):
    try:
        if isinstance(lict_data, list):
            return lict_data
        elif isinstance(lict_data, dict):
            return [lict_data]
    except (RuntimeError, TypeError, NameError):
        pass

def deviceLogins():
    host = sys.argv[1]
    username = input('Please enter username: ')
    password = getpass.getpass(prompt='Please enter password: ')
    dev = Device(host=host, user=username, passwd=password, port='22')
    getRoutes(dev)

def getRoutes(dev):
    showRoute = sys.argv[2]
    try:
        dev.open()
    except (ConnectError, ConnectAuthError, ConnectTimeoutError) as conErr:
        print(bad(f"Cannot connect to device: {conErr}"))
        sys.exit(1)
    hostname = dev.facts['hostname']
    routetbl = dev.rpc.get_route_information(table='inet.0', destination=showRoute)
    routeJson = json.loads(json.dumps(xmltodict.parse(etree.tostring(routetbl))))
    for route, routeVal in routeJson["route-information"].items():
        routeValDict = dict(routeVal)
        active_route = routeValDict["rt"]["rt-entry"]
        active_rt = active_route if isinstance(active_route, list) else [active_route]
        for active in active_rt:
            if active["active-tag"] == '*':
                route = routeValDict["rt"]["rt-destination"]
                protocol = active["protocol-name"]
                nh = active["nh"]
                next_hop = nh if isinstance(nh, list) else [nh]
                for anh in next_hop:
                    if "selected-next-hop" in anh:
                        active_next_hop = anh["to"]
                if protocol == 'BGP':
                    neighbor = active["learned-from"]
                    print(good(f"{showRoute} is part of {route} on {hostname}"))
                    print(good(f"The BGP next-hop neighbor is {neighbor}"))
                    try:
                        name, alias, addresslist = socket.gethostbyaddr(neighbor)
                        print(info(f"The next-hop device is {name}"))
                    except socket.herror as e:
                        print(bad(f"{neighbor} does't have rDNS: {e}"))
                else:
                    print(good(f"{showRoute} is part of {route} on {hostname}"))
                    print(good(f"{showRoute} is learnt via {protocol} with the nexthop {active_next_hop}"))
    dev.close()

def main():
    deviceLogins()

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print(info(lightred('Please provide the following "python3 showRoute.py host route"')))
        sys.exit(1)
    main()