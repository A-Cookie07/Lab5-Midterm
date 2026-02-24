#!/usr/bin/env python3
from netmiko import ConnectHandler
import threading
import NMtcpdump

##
# Overview
# This is meant to be ran as a script, not called from a different function
# This process will get login info for ssh,
# Connect to R4 and use the Cisco Discovery Protocol to get the address of R5
# Scrape the MAC address of R2 and R3 from a given pcap file
# Connecty to R5 using netmiko and configure DHCPv4 host reservations and a pool
##

#Note, for this script to run correctly, make sure that R2 and R3 both are configured to request DHCP AND!!! that 
#They are sending their interface as their client ID!!!!

#This function just goes in an gets the R5 ipv6 address from R4 using the Cisco Discovery Process
def get_R5_address(host, username, password):
    R4 = {
                "device_type": "cisco_ios",
                "host": host,
                "username": username,
                "password": password,
                "secret": password
    }
    print(f"devices: {R4}")

    try:
        with ConnectHandler(**R4) as connection:
            #show the current state of the router and enter enable mode
            output = connection.send_command('show cdp entry R5.zaco.com | include address: ')
            for i in output.split('\n'):
                if 'global' in i:
                    return i.split(" ")[4]
            print("no global address found\n")
            print(f"output: {output}")
            return -1
    except Exception as e:
        print(f"ERROR: {e}")

# This function goes in an gets the ipv6 address of an icmpv6 echo request and converts it to a MAC
# using the scrape_MAC function, then returns the mac addrs as a tuple
def get_R3_and_4_address(host, username, password, pcap):
    R4 = {
                "device_type": "cisco_ios",
                "host": host,
                "username": username,
                "password": password,
                "secret": password
    }
    print(f"devices: {R4}")

    try:
        with ConnectHandler(**R4) as connection:
            #show the current state of the router and enter enable mode
            mac_addrs = []
            output = connection.send_command('show cdp entry R2 | include address: ')
            for i in output.split('\n'):
                if 'global' in i:
                    print(f"address is {i.split(' ')[4]}")
                    mac_addr = NMtcpdump.scrape_MAC(pcap , mac_addrs)
                    mac_addrs.append(mac_addr)
            output = connection.send_command('show cdp entry R3 | include address: ')
            for i in output.split('\n'):
                if 'global' in i:
                    print(f"address is {i.split(' ')[4]}")
                    mac_addr = NMtcpdump.scrape_MAC(pcap , mac_addrs)
                    mac_addrs.append(mac_addr)
            if len(mac_addrs) < 2:
                print(f"ERROR: coult not find at least 1 MAC address got {mac_addrs}")
                return -1
            #print(f"MAC addrs = {mac_addrs}")
            return mac_addrs
    except Exception as e:
        print(f"ERROR: {e}")

# This function Connects to R5 and sends a config based on the given mac addresses
def connect_R5(host, username, password, r2mac, r3mac):
    R5 = {
                "device_type": "cisco_ios",
                "ip": host,
                "username": username,
                "password": password,
                "secret": password
    }

    config_r2_list = ['ip dhcp pool CLIENT_R2', 'host 198.51.102.11 255.255.255.0', f"client-identifier 01{r2mac}", 'exit']
    config_r3_list = ['ip dhcp pool CLIENT_R3', 'host 198.51.102.12 255.255.255.0', f"client-identifier 01{r3mac}", 'exit']
    config_r4_scope = ['ip dhcp excluded-address 198.51.102.1 198.51.102.5', 'ip dhcp pool R4_Network', 'network 198.51.102.0 255.255.255.0', 'exit']
    print(f"devices: {R5}")

    try:
        with ConnectHandler(**R5) as connection:
            #show the current state of the router and enter enable mode
            try:
                connection.send_config_set(config_r2_list)
            except Exception as e:
                print(f"could not configure R2: {e}")
            try:
                connection.send_config_set(config_r3_list)
            except Exception as e:
                print(f"could not configure R3: {e}")
            try:
                connection.send_config_set(config_r4_scope)
            except Exception as e:
                print(f"could not configure R4 scope: {e}")

            output = connection.send_command('show ip dhcp binding')
            print(f"output: {output}")

    except Exception as e:
        print(f"ERROR: {e}")


def main():
    host = input("input ip address of host to get R4 address from:\n")
    username = input ("input username for R4\n")
    password = input ("input password for R4\n")
    #host = '198.51.100.3'
    #username = ''
    #password = ''
    pcap_file = input("Enter the pcap file name: \n")

    address = get_R5_address(host, username, password)
    r2mac,r3mac = get_R3_and_4_address(host, username, password, pcap_file)
    print(f"r2mac is {r2mac}")
    print(f"r3mac is {r3mac}")
    connect_R5(address, username, password, r2mac, r3mac)


    


if __name__ == "__main__":
    main()