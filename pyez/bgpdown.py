#!/usr/bin/env python
#
#
#$ python3 bgpcheck.py devices
#Hostname: srx1
#10.1.1.3 100 Established 11:25 None
#Hostname: srx3
#10.1.1.1 100 Established 11:28 None

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
    peer-as: peer-as
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
        pprint("Cannot connect to device: {0}".format(conErr))
        sys.exit(1)
    except ConnectAuthError as conAuth:
        pprint("Cannot connect to device: {0}".format(conAuth))
        sys.exit(1)
    except ConnectTimeoutError as conTimeOut:
        pprint("Cannot connect to device: {0}".format(conAuth))
        sys.exit(1)
    hostname = dev.facts['hostname']
    bgp = bgpSummary(dev).get()
    for peer in bgp.items():
        neig = peer[0]
        bgpDetails = dict(peer[1])
        state = bgpDetails['peer-state']
        asn = bgpDetails['peer-as']
        time = bgpDetails['elapsed-time']
        desc = bgpDetails['description']
        if state != 'Established':
            # print(sorted(bgpDetails, key=lambda ele: ele['peer-as']))
            # print(sorted(asn, key=lambda x: x[0]))
            # # print(asn)
            # # # print('Hostname: ' + hostname)
            print(hostname, neig, asn, state, time, desc)      
    # for peer in bgp.items():
    #     neig = peer[0]
    #     state = peer[1][0][1]
    #     asn = peer[1][1][1]
    #     time = peer[1][2][1]
    #     desc = peer[1][3][1]
    #     if state != 'Established':
    #         print('Hostname: ' + hostname)
    #         print(neig, asn, state, time, desc)    
    dev.close()

def main():
    openFile()

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Please provide full path to the file with Devices')
        sys.exit(1)
    main()
