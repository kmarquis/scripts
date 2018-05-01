#!/usr/bin/env/python
import sys
import yaml
from devicecred import *
from jnpr.junos.exception import *
from jnpr.junos import Device
from jnpr.junos.factory.factory_loader import FactoryLoader

def openFile():
    with open(sys.argv[1]) as f:
        for line in f:
            ip_addr, port = line.strip().split()
            dev = Device(host=ip_addr, user=username,
                         passwd=password, port=port)
            getPrefixList(dev)

def getPrefixList(dev):
    #Open Connection Devices
    try:
        dev.open()
    except (ConnectError, ConnectAuthError, ConnectTimeoutError) as conErr:
        print("Cannot connect to device: {0}".format(conErr))
        sys.exit(1)
    hostname = dev.facts['hostname']
    yaml_data = \
    """---
    PolicyOption:
      get: policy-options/prefix-list
      view: PolicyOptionView
    PolicyOptionView:
      fields:
        name: name
        prefix: prefix-list-item/name
      """
    globals().update(FactoryLoader().load(yaml.load(yaml_data)))
    po = PolicyOption(dev).get()
    for name, prefix in po.items():
        prefixDetails = dict(prefix)
        pListName = prefixDetails['name']
        pfix = prefixDetails['prefix']
        print(hostname, pListName, pfix)
    dev.close()

#This runs openFile() and prints out the table and rows that have been collected
#in printDevices(dev)
def main():
    openFile()

#If there isn't a second file given an error will be thrown out
if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Please provide full path to a ')
        sys.exit(1)
    main()
