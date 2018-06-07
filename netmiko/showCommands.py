#!/usr/bin/env python
import sys
import argparse
import getpass
from huepy import *
from netmiko import ConnectHandler
from netmiko.ssh_exception import AuthenticationException, SSHException
from datetime import datetime

"""This script using Netmiko to run cli commands, creates a new file 
and save the output to newly created file.

Example:
    $ python3 showCommands.py devices commands ospf.txt

Expected Output:
    $ python3 showCommands.py devices commands ospf.txt
    Enter Username: root
    Enter Password:
    [!] You are being connected to localhost
    [+] SSH connectivity with localhost has been established!
    [~] Commands are being collection now
    [+] You are now disconnected from localhost
    [!] You are being connected to localhost
    [+] SSH connectivity with localhost has been established!
    [~] Commands are being collection now
    [+] You are now disconnected from localhost
    [!] You are being connected to localhost
    [-] An Error has occured. Please check Connection to device timed-out: juniper localhost:2202
"""
def openFile():
    username = input("Enter Username: ")
    password = getpass.getpass("Enter Password: ")
    with open(sys.argv[1]) as f:
        for line in f:
            ip_addr, port, platform = line.strip().split()
            dev = { 'device_type': platform, 'username': username, 'password': password, 
            "ip": ip_addr, 'port':port }
            showCommands(dev)

def showCommands(dev):
    output_file = sys.argv[3]
    command_list = []
    with open(sys.argv[2]) as l:
        for newline in l:
            commands = newline.strip().split('\n')
            command_list.extend(commands)
    print(info("You are being connected to {0}".format(dev["ip"])))
    try:
        connect = ConnectHandler(**dev)
        print(good(green("SSH connectivity with {0} has been established!".format(dev["ip"]))))
        print(run(bold("Commands are being collection now")))
        with open(output_file, "a") as i:
            for command in command_list:
                output = connect.send_command(command)
                i.write("\n{2} collected at {0} from {1}".format(datetime.now(), dev["ip"], command))
                i.write(output)
        connect.disconnect()
        print(good(green("You are now disconnected from {0}".format(dev["ip"]))))
    except (AuthenticationException, SSHException, KeyboardInterrupt) as conErr:
        print(bad(lightred("An Error has occured. Please check {0}".format(conErr))))
        sys.exit(1)

def main():
    openFile()

if __name__ == '__main__':
    if len(sys.argv) < 4:
        print(info(lightred('Please provide the following "python3 {0} device_file command_list output_file"'.format(sys.argv[0]))))
        sys.exit(1)
    main()