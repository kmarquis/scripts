#!/usr/bin/env python
import sys
import os
import getpass
import json
import xmltodict
import iptools
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

def openFile():
    username = 'root'#input('Please enter username: ')
    password = 'Juniper'#getpass.getpass(prompt='Please enter password: ')
    with open(sys.argv[1]) as f:
        for line in f:
            ip_addr, port = line.strip().split()
            dev = Device(host=ip_addr, user=username,
                         passwd=password, port=port)
            getOSPF(dev)

def getOSPF(dev):
    try:
        dev.open()
    except (ConnectError, ConnectAuthError, ConnectTimeoutError) as conErr:
        print("Cannot connect to device: {0}".format(conErr))
        sys.exit(1)

# dev = Device(host='localhost', user='root', passwd='Juniper', port='2200')

# dev.open()
    lldp = dev.rpc.get_lldp_neighbors_information()
    ospf_intf = dev.rpc.get_ospf_interface_information(extensive=True)
    ospf_neig = dev.rpc.get_ospf_neighbor_information(extensive=True)
    hostname = dev.facts.get("hostname")
    dev.close()
    data = xmltodict.parse(etree.tostring(ospf_intf))
    data1 = xmltodict.parse(etree.tostring(ospf_neig))
    data2 = xmltodict.parse(etree.tostring(lldp))
    y = data1.get("ospf-neighbor-information", {}).get("ospf-neighbor")
    i = data2.get("lldp-neighbors-information", {}).get("lldp-neighbor-information")
    # print(json.dumps(data1, indent=4))

    interfaces = []
    x = y if isinstance(y, list) else [y]
    for neig in x:
        ospf_int = neig.get("interface-name")
        interfaces.append(ospf_int)

    print('Host: {}'.format(hostname))
    print('{:12} {:10} {:7} {:7} {:7} {:5} {}'.format("interface", "area" ,"hello", 'dead','auth', "mtu", "mask"))
    for intf in data.get("ospf-interface-information", {}).get("ospf-interface"):
        name = intf.get("interface-name")
        area = intf.get("ospf-area")
        netmask = iptools.ipv4.netmask2prefix(intf.get("address-mask"))
        hello = intf.get("hello-interval")
        dead = intf.get("dead-interval")
        auth = intf.get("authentication-type")
        mtu = intf.get("mtu")
        # p = y if isinstance(y, list) else [y]
        # # for neigs in p:
        # #     state = neigs.get("ospf-neighbor-state")
        # #     # ospf_id = neigs.get("neighbor-address")
        if name in interfaces:
            print('{:12} {:10} {:7} {:7} {:7} {:5} {}'.format(name, area, hello, dead, auth, mtu, netmask))
    print('\nNeighboring Devices are: ')

    k = i if isinstance(i, list) else [i]
    for lldp_neig in k:
        if lldp_neig.get("lldp-local-interface") in interfaces:
            local = lldp_neig.get("lldp-local-interface")
            remote = lldp_neig.get("lldp-remote-port-description")
            neighbor = lldp_neig.get("lldp-remote-system-name")
            print('{} {} {}'.format(local, "is connected to " + neighbor , "on port " + local))
    print('')

def main():
    openFile()

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Please provide the following: python {} path/to/device_list'.format(sys.argv[0]))
        sys.exit(1)
    main()






