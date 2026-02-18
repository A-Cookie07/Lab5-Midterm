#!/usr/bin/env python3
import validateIPv4
from easysnmp import Session

def main():
    #access_ip = []
    #while len(access_ip) < 5:
        #cur_ip = input(f"Enter access IP for R{len(access_ip)+1} \n")
        #if validateIPv4.isValidAddress(cur_ip):
        #    access_ip.append(cur_ip)
        #else:
        #    print(f"ERROR: Invalid IP address, please check input and try again")
    #access_ip = ['198.51.100.3','198.51.102.11','198.51.102.12','198.51.100.3','198.51.102.1','198.52.100.1']

    #for ip in access_ip:
    #    print(f"ip: {ip}")
    #    session = Session(hostname=ip, community='private', version=2)

    #    ip_address = session.walk('.1.3.6.1.2.1.2.2')
    #    print(ip_address)

    dec_string = '32.1.174.134.202.254.0.1.200.4.45.255.254.81.0.0'
    hex_address = []
    for i in dec_string.split('.'):
        hex_address.append(str(hex(int(i))).split('x')[1])
    print(hex_address)
        


if __name__ == "__main__":
    main()
