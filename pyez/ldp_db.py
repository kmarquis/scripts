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

dev = Device(host='localhost', user='root', passwd='Juniper', port='2200')

dev.open()
ldp = dev.rpc.get_ldp_database_information()
hostname = dev.facts.get("hostname")
dev.close()
data = xmltodict.parse(etree.tostring(ldp))

print('{:35} {:17} {:14} {:14}'.format("Session ID", "Prefix", "Input Label", "Output Label"))

for ldp_db in data.get("ldp-database-information", {}).get("ldp-database"):
    bind = ldp_db.get("ldp-binding")
    session = ldp_db.get("ldp-session-id")
    x = bind if isinstance(bind, list) else [bind]
    for label in x:
        # print(json.dumps(label, indent=4))
        # for i in range(len(label) // 2):
        #     input_ldp = label[i * 2]
        #     output_ldp = label[i * 2 + 1]
        input_label = label.get("ldp-label")
        output_label = label.get("ldp-label")
        prefix = label.get("ldp-prefix")
        print('{:35} {:17} {:14} {:14}'.format(session, prefix, input_label, output_label))
        # if 'Input' in ldp_db.get("ldp-database-type"):
        #     input_label = label.get("ldp-label")
        #     prefix = label.get("ldp-prefix")
        # elif 'Output' in ldp_db.get("ldp-database-type"):
        #     output_label = label.get("ldp-label")
        #     prefix = label.get("ldp-prefix")
        #     print('{:35} {:17} {:14} {:14}'.format(session, prefix, input_label, output_label))
            # print('='*50)
            # print(json.dumps(input_label, indent=4))
    # elif 'Output' in ldp_db.get("ldp-database-type"):
    #     # x = bind if isinstance(bind, list) else [bind]
    #     for label in x:
    #         output_label = label.get("ldp-label")
    #         # print('{} {}'.format(input_label, output_label))
    #         print(json.dumps(output_label, indent=4))
    #         # print(json.dumps(ldp_db, indent=4))

# for ldp_db in data.get("ldp-database-information", {}).get("ldp-database"):
#   if 'Input' in ldp_db.get("ldp-database-type"):
#       input_label = ldp_db.get("ldp-label")
#       print(json.dumps(input_label, indent=4))
#       # print(json.dumps(ldp_db, indent=4))