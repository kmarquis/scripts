#!/usr/bin/env python
import requests
import json
import napalm

if __name__ == '__main__':
    
    v4Only = 'v4 only'
    v6Only = 'v6 only'
    both = 'v4 and v6 configured'
    neither = 'No Peering configured'

    driver = napalm.get_network_driver('junos')
    dev = driver(username='root', password='Juniper', hostname='localhost', optional_args={ 'port': '2222' })
    dev.open()
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