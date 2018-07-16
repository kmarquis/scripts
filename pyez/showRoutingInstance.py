#!/usr/bin/env python
import sys
import json
import xmltodict
import re
from huepy import *
from lxml import etree
from pprint import pprint as pp
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

host = 'localhost'
username = 'root'
port = '2200'
password = 'Juniper'
dev = Device(host=host, user=username, passwd=password, port=port)
dev.open()
ri = dev.rpc.get_config(filter_xml='routing-instances')
dev.close()
y = json.loads(json.dumps(xmltodict.parse(etree.tostring(ri))))
for instance in y["configuration"]["routing-instances"]["instance"]:
    instName = instance["name"]
    instType = instance["instance-type"]
    if "interface" in instance:
        instintf = instance["interface"]
        inst = instintf if isinstance(instintf, list) else [instintf]
        for riIntf in inst:
            riIntName = riIntf["name"]
            print("{0} {1} {2}".format(instName, instType, riIntName) )