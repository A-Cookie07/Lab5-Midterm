#!/usr/bin/env python3
from scapy.all import *
from scapy.layers.inet6 import IPv6, ICMPv6EchoRequest, ICMPv6EchoReply

###
# Overview
# This function takes a given pcap file and an ipv6 address,
# and returns the MAC address of the device associated with
# The given ipv6 address.  
#
# In its current state, it is used to find the MAC address of 2 specific 
# devices, and the plan is to grab these automatically in another function
# then call this function to return the MAC address for that functions use
###

##I figured this is a common enough task that someone already has a solution.
##Here is a script I found on Stack Overflow
##https://stackoverflow.com/questions/37140846/how-to-convert-ipv6-link-local-address-to-mac-address-in-python

def ipv62mac(ipv6):
    # remove subnet info if given
    subnetIndex = ipv6.find("/")
    if subnetIndex != -1:
        ipv6 = ipv6[:subnetIndex]

    ipv6Parts = ipv6.split(":")
    macParts = []
    for ipv6Part in ipv6Parts[-4:]:
        while len(ipv6Part) < 4:
            ipv6Part = "0" + ipv6Part
        macParts.append(ipv6Part[:2])
        macParts.append(ipv6Part[-2:])

    # modify parts to match MAC value
    macParts[0] = "%02x" % (int(macParts[0], 16) ^ 2)
    del macParts[4]
    del macParts[3]

    return ":".join(macParts)
    


#this function
#1 converts the pcap file into a rdpcap object
#2 goes packet by packet through the obj
#3 if packet is a layer 6 icmp echo request, we further check it
#4compare dest ip with target ip, if a match, return MAC
def scrape_MAC(pcap_file, addr_list):
    print(f"Scraping {pcap_file}...")
    packets = rdpcap(pcap_file)
    for packet in packets:
        if packet.haslayer(ICMPv6EchoRequest):
            mac_addr = ipv62mac(packet[IPv6].dst)
            if not (mac_addr in addr_list):
                #print(f"{packet[IPv6].src} : {packet[IPv6].dst}")
                #print(f"{packet.src}, :: {packet.dst}")
                #print(new_mac)
                return mac_addr

#This runs as a way to test the function on its own
def main():
    pcap_file = input("enter the filename of the pcap\n")
    addr_list = []
    addr_list.append(scrape_MAC(pcap_file, addr_list))
    addr_list.append(scrape_MAC(pcap_file, addr_list))
    for i in addr_list:
        print(i)
if __name__ == "__main__":
    main()
