#!/usr/bin/env python
import requests
import json
import napalm
from napalm.exceptions import *

def openFile():
    username = input('Please enter username: ')
    password = getpass.getpass(prompt='Please enter password: ')
    with open(sys.argv[1]) as f:
        for line in f:
            ip_addr, port = line.strip().split()
            dev = Device(host=ip_addr, user=username,
                         passwd=password, port=port)
            peeringChecker(dev)

def peeringChecker(dev):
    try:
        dev.open()
    except NapalmException as conErr:
        print("Cannot connect to device: {0}".format(conErr))
        sys.exit(1)
    bgp = dev.get_bgp_neighbors()
    dev.close()

    # Create a list configured BGP peers
    confPeers = list(bgp['global']['peers'].keys())

    # Define your own ASN
    myASN = '39326'

    #Enter ASN of Peer you want to check against
    peeras = input("Enter Peer ASN: ")

    # Calling peeringdb API to get IX details for your own ASN and 
    # ASN that you want to check against
    myDetails = requests.get('https://www.peeringdb.com/api/netixlan?asn={}'.format(myASN)).json()['data']
    peerDetails = requests.get('https://www.peeringdb.com/api/netixlan?asn={}'.format(peeras)).json()['data']

    # Create an empty list that will store of the peeringdb IX IDs
    # Loop over my asn ix ids then added them to the empty list
    myIXLocations = []
    for myIDs in myDetails:
        ids = myIDs['ix_id']
        myIXLocations.append(ids)

    # Compare the peers peeringdb ix ids with the list myIXLocations
    # If the ids match then print out the following details:
    #   - IX LAN Name
    #   - IX IPv4 Address
    #   - IX IPv6 Address
    #   - If IPv4 & IPv6 address are configured
    for peerIDs in peerDetails:
        if peerIDs['ix_id'] in myIXLocations:
            name = peerIDs['name']
            ipv4 = peerIDs['ipaddr4']
            ipv6 = peerIDs['ipaddr6']
            if ipv4 and ipv6 in confPeers:
                print("{:30} {:20} {:20} {}".format(name, ipv4, ipv6, both))
            elif ipv4 in confPeers:
                print("{:30} {:20} {:20} {}".format(name, ipv4, ipv6, v4Only))
            elif ipv6 in confPeers:
                print("{:30} {:20} {:20} {}".format(name, ipv4, ipv6, v6Only))
            else:
                print("{:30} {:20} {:20} {}".format(name, ipv4, ipv6, neither))
def main():
    openFile()

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Please provide the following: python {} path/to/device_list'.format(sys.argv[0]))
        sys.exit(1)
    main()     
    # v4Only = 'v4 only'
    # v6Only = 'v6 only'
    # both = 'v4 and v6 configured'
    # neither = 'No Peering configured'

    # driver = napalm.get_network_driver('junos')
    # dev = driver(username='root', password='Juniper', hostname='localhost', optional_args={ 'port': '2200' })
    # dev.open()
    # bgp = dev.get_bgp_neighbors()
    # dev.close()

    # # Create a list configured BGP peers
    # confPeers = list(bgp['global']['peers'].keys())

    # # Define your own ASN
    # myASN = '39326'

    # #Enter ASN of Peer you want to check against
    # peeras = input("Enter Peer ASN: ")

    # # Calling peeringdb API to get IX details for your own ASN and 
    # # ASN that you want to check against
    # myDetails = requests.get('https://www.peeringdb.com/api/netixlan?asn={}'.format(myASN)).json()['data']
    # peerDetails = requests.get('https://www.peeringdb.com/api/netixlan?asn={}'.format(peeras)).json()['data']

    # # Create an empty list that will store of the peeringdb IX IDs
    # # Loop over my asn ix ids then added them to the empty list
    # myIXLocations = []
    # for myIDs in myDetails:
    #     ids = myIDs['ix_id']
    #     myIXLocations.append(ids)

    # # Compare the peers peeringdb ix ids with the list myIXLocations
    # # If the ids match then print out the following details:
    # #   - IX LAN Name
    # #   - IX IPv4 Address
    # #   - IX IPv6 Address
    # #   - If IPv4 & IPv6 address are configured
    # for peerIDs in peerDetails:
    #     if peerIDs['ix_id'] in myIXLocations:
    #         name = peerIDs['name']
    #         ipv4 = peerIDs['ipaddr4']
    #         ipv6 = peerIDs['ipaddr6']
    #         if ipv4 and ipv6 in confPeers:
    #             print("{:30} {:20} {:20} {}".format(name, ipv4, ipv6, both))
    #         elif ipv4 in confPeers:
    #             print("{:30} {:20} {:20} {}".format(name, ipv4, ipv6, v4Only))
    #         elif ipv6 in confPeers:
    #             print("{:30} {:20} {:20} {}".format(name, ipv4, ipv6, v6Only))
    #         else:
    #             print("{:30} {:20} {:20} {}".format(name, ipv4, ipv6, neither))