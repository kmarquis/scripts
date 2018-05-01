#!/usr/bin/env python
import sys, os, yaml
from devicecred import *
from jnpr.junos import Device
from jnpr.junos.exception import *
from jnpr.junos.factory.factory_loader import FactoryLoader
from pprint import *

yml = '''
---
firewallPolicyTable:
  rpc: get-firewall-policies
  args:
    detail: True
  item: security-context
  key: 
    - context-information/source-zone-name
  view: zonesViews

zonesViews:
  fields:
    sourceZone: context-information/source-zone-name
    destZone: context-information/destination-zone-name
    policies: policyTable

policyTable:
  item: policies/policy-information
  key: policy-name
  view: policyViews

policyViews:
  fields:
    policyName: policy-name
    sourceAdd: source-addresses/source-address/prefixes/address-prefix
    destAdd: destination-addresses/destination-address/prefixes/address-prefix
    appliciation: applications/application/application-name
    action: policy-action/action-type
'''

# Load Table and View definitions via YAML into namespace
globals().update(FactoryLoader().load(yaml.load(yml)))

def openFile():
    with open(sys.argv[1]) as f:
        for line in f:
            ip_addr, port = line.strip().split()
            dev = Device(host=ip_addr, user=username,
                         passwd=password, port=port)
            getFirewallRules(dev)


def getFirewallRules(dev):
    try:
        dev.open()
    except (ConnectError, ConnectAuthError, ConnectTimeoutError) as conErr:
        pprint("Cannot connect to device: {0}".format(conErr))
        sys.exit(1)
    hostname = dev.facts['hostname']
    policy = firewallPolicyTable(dev).get()
    for fromzone, details in policy.items():
        policyZones = dict(details)
        for policies, pdetails in policyZones['policies'].items():
            policyDetails = dict(pdetails)
            srcZone = policyZones['sourceZone']
            destZone = policyZones['destZone']
            polName = policyDetails['policyName']
            srcAdd = policyDetails['sourceAdd']
            dstAdd = policyDetails['destAdd']
            appl = policyDetails['appliciation']
            action = policyDetails['action']
            print(srcZone, destZone, polName, srcAdd, dstAdd, appl, action)
    dev.close()

def main():
    openFile()
    # print(table)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Please provide full path to a ')
        sys.exit(1)
    main()
