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

xml = os.path('./chassis_hardware')
data = xmltodict.parse(etree.tostring(xml))

print(data)