#!/usr/bin/env python
import sys
import getpass
import json
import xmltodict
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

host = 'localhost'
username = 'root'
password = 'Juniper'
port = '2200'
dev = Device(host=host, user=username, passwd=password, port=port)


dev.open()
hostname = dev.facts["hostname"]
x = dev.rpc.get_config(filter_xml='policy-options/prefix-list')
dev.close()
jsonx = xmltodict.parse(etree.tostring(x))
lists = jsonx.get("configuration", {}).get("policy-options", {}).get("prefix-list")

y = lists if isinstance(lists, list) else [lists]

print("Host: {}".format(hostname))
print('{:10} {}'.format("Name", "Prefix"))
for prefixlist in y:
    name = prefixlist.get("name")
    prefix = prefixlist.get("prefix-list-item")
    k = prefix if isinstance(prefix, list) else [prefix]
    for o in k:
        if o and o.get("name", None):
            subnet = o.get("name")
            print('{:10} {}'.format(name, subnet))
        else:
            print('{:10} {}'.format(name, "Empty"))

    # print(json.dumps(prefixlist, indent=4))
# for k, v in jsonx["configuration"]["policy-options"].items():
#     print(f"The following prefix lists are configured on {hostname}: ")
#     y = v if isinstance(v, list) else [v]
#     for u in y:
#         pfxName = u["name"]
#         print(pfxName)
#         if "prefix-list-item" in u:
#             p = u["prefix-list-item"]
#             o = p if isinstance(p, list) else [p]
#             for j in o:
#                 pfx = j["name"]
#                 print(pfx)