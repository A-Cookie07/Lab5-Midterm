#!/usr/bin/env python3
import NMtcpdump
import NMdhcpserver
import NMsnmp
import NMgithub
import validateIPv4
import json

def main():
    # Run the tcpdump function to get the addresses
    pcap_file = input("enter the filename of the pcap\n")
    addr_list = []
    addr_list.append(NMtcpdump.scrape_MAC(pcap_file, addr_list))
    addr_list.append(NMtcpdump.scrape_MAC(pcap_file, addr_list))
    for i in addr_list:
        print(i)

    # Run the dhcp function
    host = input("input ip address of host to get R4 address from:\n")
    username = input ("input username for Router\n")
    password = input ("input password for Router\n")

    address = NMdhcpserver.get_R5_address(host, username, password)
    r2mac,r3mac = NMdhcpserver.get_R3_and_4_address(host, username, password, pcap_file)
    #print(f"r2mac is {r2mac}")
    #print(f"r3mac is {r3mac}")
    NMdhcpserver.connect_R5(address, username, password, r2mac, r3mac)

    # Run the snmp function
    access_ip = []
    while len(access_ip) < 5:
        cur_ip = input(f"Enter access IP for R{len(access_ip)+1} \n")
        if validateIPv4.isValidAddress(cur_ip):
            access_ip.append(cur_ip)
        else:
            print(f"ERROR: Invalid IP address, please check input and try again")

    output_file = input("Enter output file name:\n")

    all_addresses = {}
    all_interfaces = {}

    for ip in access_ip:
        addresses, interfaces = NMsnmp.get_address_and_interface(ip)

    with open(output_file, 'w') as wptr:
        json.dump(all_addresses, wptr, ensure_ascii=False, indent=4)
        json.dump(all_interfaces, wptr, ensure_ascii=False, indent=4)

    NMsnmp.get_cpu_util()

if __name__ == "__main__":
    main()
