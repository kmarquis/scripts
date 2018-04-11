#!/usr/bin/env python
import sys
import os
import getpass
from jnpr.junos import Device
from jnpr.junos.op.routes import RouteTable
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
        print("Cannot connect to device: {0}".format(conErr))
        sys.exit(1)
    except ConnectAuthError as conAuth:
        print("Cannot connect to device: {0}".format(conAuth))
        sys.exit(1)
    except ConnectTimeoutError as conTimeOut:
        print("Cannot connect to device: {0}".format(conAuth))
        sys.exit(1)
    hostname = dev.facts['hostname']
    routetbl = RouteTable(dev).get(showRoute)
    for prefix, details in routetbl.items():
        pfixDetails = dict(details)
        pfix = prefix
    print('Route: ' + pfix)
    print('Protocol: '+ pfixDetails['protocol'])
    print('Inteface: ' + pfixDetails['via'] )
    print('BGP neighbor: ' + pfixDetails['learnt'])
    dev.close()

def main():
    deviceLogins()

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print('Please provide the following "python3 showRoute.py host route"')
        sys.exit(1)
    main()