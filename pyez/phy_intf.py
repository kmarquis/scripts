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
from datetime import datetime

intf_type = ['fe', 'ge', 'xe', 'et']

def openFile():
    username = input('Please enter username: ')
    password = getpass.getpass(prompt='Please enter password: ')
    with open(sys.argv[1]) as f:
        for line in f:
            ip_addr, port = line.strip().split()
            dev = Device(host=ip_addr, user=username,
                         passwd=password, port=port)
            hardware(dev)

def hardware(dev):
    try:
        dev.open()
    except (ConnectError, ConnectAuthError, ConnectTimeoutError) as conErr:
        print("Cannot connect to device: {0}".format(conErr))
        sys.exit(1)
    intf = dev.rpc.get_interface_information()
    hostname = dev.facts.get("hostname")
    dev.close()
    data = xmltodict.parse(etree.tostring(intf))

    print('Host: {}'.format(hostname))
    print('{:10} {:10} {:20}'.format('Interface', 'Status', 'MAC Address'))
    for intf_data in data.get("interface-information", {}).get("physical-interface"):
        intfs = intf_data.get("name")
        admin = intf_data.get("admin-status", {}).get("#text")
        oper = intf_data.get("oper-status")
        mac = intf_data.get("current-physical-address")
        if any(intfs.startswith(inf) for inf in (intf_type)):
            print('{:10} {:10} {:20}'.format(intfs, admin + '/' + oper, mac))

def main():
    start_time = datetime.now()
    openFile()
    print("\nElapsed time: " + str(datetime.now() - start_time))

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Please provide the following: python {} path/to/device_list'.format(sys.argv[0]))
        sys.exit(1)
    main()    
