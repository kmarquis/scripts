#!/usr/bin/env python
import sys
import os
import getpass
import json
import xmltodict
import platform
from lxml import etree
from huepy import *
from jnpr.junos import Device
from jnpr.junos.exception import *

def deviceLogins():
    host = sys.argv[1]
    username = input('Please enter username: ')
    port = input('Please enter port: ')
    password = getpass.getpass(prompt='Please enter password: ')
    dev = Device(host=host, user=username, passwd=password, port=port)
    getRoutes(dev)

def getRoutes(dev):
    showRoute = sys.argv[2]
    try:
        dev.open()
    except ConnectError as conErr:
        print(bad("Cannot connect to device: {0}".format(conErr)))
        sys.exit(1)
    except ConnectAuthError as conAuth:
        print(bad("Cannot connect to device: {0}".format(conAuth)))
        sys.exit(1)
    except ConnectTimeoutError as conTimeOut:
        print(bad("Cannot connect to device: {0}".format(conAuth)))
        sys.exit(1)
    hostname = dev.facts['hostname']
    routetbl = dev.rpc.get_route_information(table='inet.0', destination=showRoute)
    routeJson = json.loads(json.dumps(xmltodict.parse(etree.tostring(routetbl))))
    for route, routeVal in routeJson["route-information"].items():
        routeValDict = dict(routeVal)
        if routeValDict["rt"]["rt-entry"]["active-tag"] == '*':
            route = routeValDict["rt"]["rt-destination"]
            protocol = routeValDict["rt"]["rt-entry"]["protocol-name"]
            next_hop = routeValDict["rt"]["rt-entry"]["nh"]["to"]
            if protocol == 'BGP':
                neighbor = routeValDict["rt"]["rt-entry"]["learned-from"]
                print(good(showRoute + " route is " + route))
                print(good("The BGP next-hop neighbor is " + neighbor))
                if platform.system() == 'windows':
                    os.system('nslookup ' + neighbor)
                else:
                    os.system('host ' + neighbor)
            else:
                print(good(showRoute + " route is " + route))
                print(good(showRoute + " is learnt by " + protocol + " with the nexthop " + next_hop))
    dev.close()

def main():
    deviceLogins()

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print(info(lightred('Please provide the following "python3 showRoute.py host route"')))
        sys.exit(1)
    main()