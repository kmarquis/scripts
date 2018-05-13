#!/usr/bin/env python
import sys
import getpass
from huepy import *
from jnpr.junos import Device
from jnpr.junos.utils.config import * 
from jnpr.junos.exception import *
from jnpr.junos.factory.factory_loader import FactoryLoader

def loginDetails():
    comment = input("Please provide a reason or reference: ")
    host = sys.argv[0]
    username = input(" Enter Usename: ")
    password =  getpass.getpass("Enter password: ")
    port = '22'
    dev = Device(host=host, user=username, passwd=password, port=port)
    configDevice(dev)

def configDevice(dev):
    blockAddress = sys.argv[1]
    try:
        dev.open()
    except ConnectError as conErr:
        print(bad(f"Cannot connect the device: {conErr}"))
        sys.exit(1)
    cu = Config(dev, mode='exclusive')
    print(info("The following config will be applied: "))
    try:
        cu.load(f"set routing-options static route {blockAddress} discard tag 6666", format='set', merge=True)
        if cu.diff() is None:
            print(info("No change is needed, exiting script :) "))
            sys.exit(1)
        else:
            print(cu.diff())
            print(que("Does this look good for a commit check?"))
            askForCheck = input("Commit Check? (yes/no) ")
            if askForCheck == "yes":
                try:
                    if cu.commit_check() == True:
                        print(info("Check has passed, change will be commited now"))
                        cu.commit(comment=f"Committed using {sys.argv[0]} script")
                        print(good(lightgreen("Commit has been completed, config has been applied")))
                except CommitError as commiterr:
                    cu.rollback(rb_id=0)
                    print(bad(f"The commit check has failed {commiterr}. Conifg has been rolled back"))
            else:
                cu.rollback(rb_id=0)
                print(info(lightred("Commit has been cancelled, no change has been made")))    
    except RpcError as rpcerr:
        print(bad(f"An Error had occurred {rpcerr}"))
    dev.close()

def main():
    loginDetails()

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(info(lightred(f'Please provide the following "python3 {sys.argv[0]} route/netmask"')))
        sys.exit(1)
    main() 