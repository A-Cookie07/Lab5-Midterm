#!/usr/bin/env python3
from scapy.all import *
from scapy.layers.inet6 import IPv6, ICMPv6EchoRequest, ICMPv6EchoReply

def scrape_MAC(pcap_file, address):
    print(f"Scraping {pcap_file}...")
    packets = rdpcap(pcap_file)
    for packet in packets:
        if packet.haslayer(ICMPv6EchoRequest):
            if packet[IPv6].dst == address:
                print(f"{packet[IPv6].src} : {packet[IPv6].dst}")
                print(f"{packet.src}, :: {packet.dst}")
                return packet.dst
def main():
    pcap_file = input("enter the filename of the pcap\n")
    scrape_MAC(pcap_file, '2001:ae86:cafe:1:c803:6cff:fe8b:0')
    scrape_MAC(pcap_file, '2001:ae86:cafe:1:c802:6cff:fe6c:0')
if __name__ == "__main__":
    main()
