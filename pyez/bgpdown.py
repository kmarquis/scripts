#!/usr/bin/env python
"""
$ python3 bgpdown.py devices
srx1 1.1.1.1 Idle 1 None 2:44:41
srx1 2.2.2.0 Idle 2 None 2:44:41
srx1 29.29.2.10 Idle 18 None 2:39:35
srx1 29.29.2.9 Idle 20 None 2:39:35
"""
import sys
import yaml
from devicecred import *
from jnpr.junos import Device
from jnpr.junos.exception import *
from jnpr.junos.factory.factory_loader import FactoryLoader

yml = '''
---
bgpSummary:
  rpc: get-bgp-summary-information
  item: bgp-peer
  view: summaryView
  key: peer-address

summaryView:
  fields:
    peer-state: peer-state
    peer-as: {peer-as: int}
    elapsed-time: elapsed-time
    description: description
'''

# Load Table and View definitions via YAML into namespace
globals().update(FactoryLoader().load(yaml.load(yml)))

# This function opens the named file (sys.argv[1]) with the following 
# device details: hostname and port, with the username and password 
# being taken from imported devicecred.py. It will iternate the file
# line by line access each device then running the function bgpDown
def openFile():
    with open(sys.argv[1]) as f:
        for line in f:
            ip_addr, port = line.strip().split()
            dev = Device(host=ip_addr, user=username,
                         passwd=password, port=port)
            bgpDown(dev)

# This function opens a connects to the Juniper device collects
# the hostname and bgp details. When the BGP adjenacy isn't 
# Established, the following details are printed out:
# Hostname, BGP State, Peer ASN, Peer description, Peer Down Time 
def bgpDown(dev):
    try:
        dev.open()
    except ConnectError as conErr:
        print("Cannot connect to device: {0}".format(conErr))
        sys.exit(1)
    except ConnectAuthError as conAuth:
        print("Cannot connect to device: {0}".format(conAuth))
        sys.exit(1)
    except ConnectTimeoutError as conTimeOut:
        print("Cannot connect to device: {0}".format(conAuth))
        sys.exit(1)
    hostname = dev.facts['hostname']
    bgp = bgpSummary(dev).get()
    #Empty list is created
    bgp_down = []
    #for loop with key, value pair (bgp peers, peer detials), that is put into 
    #a dict  
    for neighbor, details in bgp.items():
        bgpDetails = dict(details)
    #from the dict all bgp sessions that are not Established and added to the list
        if bgpDetails['peer-state'] != 'Established':
            bgpDetails['neighbor'] = neighbor  # assumes this is not already in here.
            bgp_down.append(bgpDetails)
    #the un established peers are sorted by ASN and their details looped 
    #and defined as variables, that are printed out 
    for bgpDetails in sorted(bgp_down, key=lambda ele: ele['peer-as']):
            neighbor = bgpDetails['neighbor']
            state = bgpDetails['peer-state']
            asn = bgpDetails['peer-as']
            desc = bgpDetails['description']
            time = bgpDetails['elapsed-time']
            print(hostname, neighbor, state, asn, desc, time)  
    dev.close()

def main():
    openFile()

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Please provide full path to the file with Devices')
        sys.exit(1)
    main()
