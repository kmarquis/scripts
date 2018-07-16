#!/usr/bin/env python
import json
import xmltodict
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
port = '2222'
password = 'Juniper'
dev = Device(host=host, user=username, passwd=password, port=port)

dev.open()
fp = dev.rpc.get_firewall_policies(detail=True)
dev.close()
x = xmltodict.parse(etree.tostring(fp))
for k in x["security-policies"]["security-context"]:
    for q in k["policies"].values():
        destZone = q["context-information"]["destination-zone-name"]
        srcZone = q["context-information"]["source-zone-name"]
        polName = q["policy-name"]
        polAction = q["policy-action"]["action-type"]
        src = q["source-addresses"]["source-address"]
        srcDetails = src if isinstance(src, list) else [src]
        for p in srcDetails:
            srcName = p["address-name"]
            srcPfx = p["prefixes"]["address-prefix"]
            print(srcPfx, srcName)
        dest = q["destination-addresses"]["destination-address"]
        destDetails = src if isinstance(dest, list) else [dest]
        for o in destDetails:
            destName = o["address-name"]
            destPfx = o["prefixes"]["address-prefix"]
            print(destPfx, destName)
        if "policy-log" != None:
            polLog = q["policy-log"]
            print(polLog)            
        app = q["applications"]["application"]
        appDetails = app if isinstance(app, list) else [app]
        for i in appDetails: 
            appl = i["application-name"]
            print(appl)