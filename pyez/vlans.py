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

def openFile():
    username = input('Please enter username: ')
    password = getpass.getpass(prompt='Please enter password: ')
    with open(sys.argv[1]) as f:
        for line in f:
            ip_addr, port = line.strip().split()
            dev = Device(host=ip_addr, user=username,
                         passwd=password, port=port)
            getVlans(dev)


def getVlans(dev):
    try:
        dev.open()
    except (ConnectError, ConnectAuthError, ConnectTimeoutError) as conErr:
        print("Cannot connect to device: {0}".format(conErr))
        sys.exit(1)
    vlans = dev.rpc.get_vlan_information(extensive=True)
    hostname = dev.facts.get("hostname")
    dev.close()
    data = xmltodict.parse(etree.tostring(vlans))

    print('Host: {}'.format(hostname))
    print('{:20} {:10} {:12} {:10} {:10} {}'.format("vlan name", "vlan id", "interface", 'mode','tagged', "RVI"))
    for vlan in data.get("l2ng-l2ald-vlan-instance-information", {}).get("l2ng-l2ald-vlan-instance-group"):
        name = vlan.get("l2ng-l2rtb-vlan-name")
        vlan_tag = vlan.get("l2ng-l2rtb-vlan-tag")
        members = vlan.get("l2ng-l2rtb-vlan-member")
        rvi = vlan.get("l2ng-l2rtb-vlan-l3-interface")
        member = members if isinstance(members, list) else [members]
        for vlan_mem in member:
            #The line below is broken down into two parts, "if vlan_mem" is saying 
            #if vlan_mem is not False AND with vlan_mem.get("l2ng-l2rtb-vlan-member-interface", None)
            #key doesn't have the default value of "None" as defined with
            #("l2ng-l2rtb-vlan-member-interface", None) then collect all the interface data. If 
            #vlan_mem and/or l2ng-l2rtb-vlan-member-interface comeback as False then it is ignored
            if vlan_mem and vlan_mem.get("l2ng-l2rtb-vlan-member-interface", None):
                intf = vlan_mem.get("l2ng-l2rtb-vlan-member-interface")
                intf_mode = vlan_mem.get("l2ng-l2rtb-vlan-member-interface-mode")
                intf_tag = vlan_mem.get("l2ng-l2rtb-vlan-member-tagness")
                print('{:20} {:10} {:12} {:10} {:10} {}'.format(name, vlan_tag, intf ,intf_mode ,intf_tag, rvi))
            else:
                print('{:20} {:10}'.format(name, vlan_tag))

def main():
    openFile()

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Please provide the following: python {} path/to/device_list'.format(sys.argv[0]))
        sys.exit(1)
    main()                  