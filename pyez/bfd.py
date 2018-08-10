#!/usr/bin/env python
import sys
import os
import getpass
import json
import xmltodict
from datetime import datetime
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
    username = input("Enter Username: ")
    password = getpass.getpass("Enter Password: ")
    with open(sys.argv[1]) as f:
        for line in f:
            ip_addr, port = line.strip().split()
            dev = Device(host=ip_addr, user=username,
                         passwd=password, port=port)
            bfdSession(dev)

def bfdSession(dev):
	try:
	    dev.open()
	except ConnectError as conErr:
	    print(f"Cannot connect the device: {conErr}")
	    sys.exit(1)
	bfd_session = dev.rpc.get_bfd_session_information(extensive=True)
	hostname = dev.facts.get("hostname")
	dev.close()
	data = xmltodict.parse(etree.tostring(bfd_session))

	bfd = data.get("bfd-session-information", {}).get("bfd-session")

	print(f'Host: {hostname}')
	print(f'{"Interface":11} {"Status":10} {"Interval":10} {"Detect":10} {"Protocols"}')
	for info in bfd:
		intf = info.get("session-interface")
		status = info.get("session-state")
		detect = info.get("session-detection-time")
		interval = info.get("session-transmission-interval")
		bfd_client = info.get("bfd-client")
		client = bfd_client if isinstance(bfd_client, list) else [bfd_client]
		for details in client:
			proto = details.get("client-name")
			print(f'{intf:11} {status:10} {interval:10} {detect:10} {proto}')

def main():
    start_time = datetime.now()
    openFile()
    print("\nElapsed time: " + str(datetime.now() - start_time))

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(f'Please provide the following: "python {sys.argv[0]} path/to/device_list"')
        sys.exit(1)
    main()
	