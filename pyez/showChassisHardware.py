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

xml = etree.parse('4550_chassis_hardware.xml')
data = xmltodict.parse(etree.tostring(xml))

inventory = data.get("rpc-reply", {}).get("chassis-inventory")#, {}).get("chassis")
# print(json.dumps(inventory, indent=4))


for d in inventory:
	print(d)
	# chassis_name = d.get("name")
	# print(type(chassis_name))
# chassis_serial = inventory.get("serial-number")
# chassis_desc = inventory.get("description")
# chassis_part = inventory.get("part-number")
# chassis_model = inventory.get("model-number")

# print( chassis_name, chassis_serial, chassis_desc, chassis_part, chassis_model )