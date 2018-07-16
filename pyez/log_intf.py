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

intf_type = ['fe', 'ge', 'xe', 'et', 'irb', 'st0', 'vlan']

dev = Device(host='localhost', user='root', passwd='Juniper', port='2222')

dev.open()
intf = dev.rpc.get_interface_information()
hostname = dev.facts.get("hostname")
dev.close()
data = xmltodict.parse(etree.tostring(intf))
print(json.dumps(data, indent=4))