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


#this function
#1 converts the pcap file into a rdpcap object
#2 goes packet by packet through the obj
#3 if packet is a layer 6 icmp echo request, we further check it
#4compare dest ip with target ip, if a match, return MAC
def scrape_MAC(pcap_file, address):
    print(f"Scraping {pcap_file}...")
    packets = rdpcap(pcap_file)
    for packet in packets:
        if packet.haslayer(ICMPv6EchoRequest):
            if packet[IPv6].dst == address:
                #print(f"{packet[IPv6].src} : {packet[IPv6].dst}")
                #print(f"{packet.src}, :: {packet.dst}")
                return packet.dst

#This runs as a way to test the function on its own
def main():
    pcap_file = input("enter the filename of the pcap\n")
    print(f" scraping R3: {scrape_MAC(pcap_file, '2001:ae86:cafe:1:c803:2dff:fe15:0')}")
    print(f" scraping R2: {scrape_MAC(pcap_file, '2001:ae86:cafe:1:c802:2cff:fed0:0')}")
if __name__ == "__main__":
    main()
