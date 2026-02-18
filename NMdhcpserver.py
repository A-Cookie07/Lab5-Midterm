#!/usr/bin/env python3
from netmiko import ConnectHandler
import threading
import NMtcpdump

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
                    mac_addr = NMtcpdump.scrape_MAC(pcap , (i.split(' ')[4]).lower())
                    mac_addrs.append(mac_addr)
            output = connection.send_command('show cdp entry R3 | include address: ')
            for i in output.split('\n'):
                if 'global' in i:
                    print(f"address is {i.split(' ')[4]}")
                    mac_addr = NMtcpdump.scrape_MAC(pcap , (i.split(' ')[4]).lower())
                    mac_addrs.append(mac_addr)
            if len(mac_addrs) < 2:
                print(f"ERROR: coult not find at least 1 MAC address got {mac_addrs}")
                return -1
            return mac_addrs
    except Exception as e:
        print(f"ERROR: {e}")

def connect_R5(host, username, password, r2mac, r3mac):
    R5 = {
                "device_type": "cisco_ios",
                "ip": host,
                "username": username,
                "password": password,
                "secret": password
    }
    print(f"devices: {R5}")

    try:
        with ConnectHandler(**R5) as connection:
            #show the current state of the router and enter enable mode
            output = connection.send_command('show ipv6 int br')
            print(output)
    except Exception as e:
        print(f"ERROR: {e}")


def main():
    #host = input("input ip address of host to get R4 address from:\n")
    #username = input ("input username for R4\n")
    #password = input ("input password for R4\n")
    host = '198.51.100.3'
    username = 'zaco6003'
    password = 'cisco'
    pcap_file = input("Enter the pcap file name: \n")

    address = get_R5_address(host, username, password)
    r2mac,r3mac = get_R3_and_4_address(host, username, password, pcap_file)
    print(f"r3mac is {r3mac}")
    connect_R5(address, username, password, r2mac, r3mac)


    


if __name__ == "__main__":
    main()