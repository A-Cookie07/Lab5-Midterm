#!/usr/bin/env python3
import validateIPv4
from easysnmp import Session
import time
import matplotlib.pyplot as plt
import json

def get_if_status(status):
    if status == "1":
        return "up"
    else: 
        return "down"

def dec_to_hex(dec_string):
    hex_address = ""
    add_colon = False
    for i in dec_string.split('.'):
        # Note this isnt really a byte, but the idea is its going by every 2 hex digits, 
        # and I don't know the word for that
        cur_byte = str(hex(int(i))).split('x')[1]
        if len(cur_byte) < 2:
            cur_byte = '0'+cur_byte
        hex_address += cur_byte

        if (add_colon):
            hex_address += ':'
            add_colon = False
        else:
            add_colon = True
    if len(hex_address) > 39:
        hex_address = hex_address[:-(len(hex_address)-39)]
    return str(hex_address)

def main():
    #access_ip = []
    #while len(access_ip) < 5:
    #    cur_ip = input(f"Enter access IP for R{len(access_ip)+1} \n")
    #    if validateIPv4.isValidAddress(cur_ip):
    #        access_ip.append(cur_ip)
    #    else:
    #        print(f"ERROR: Invalid IP address, please check input and try again")
    access_ip = ['198.51.100.3','198.51.102.11','198.51.102.12','198.51.100.3','198.51.102.1','198.52.100.1']
    #access_ip = ['198.51.100.3']

    output_file = input("Enter output file name:\n")

    all_addresses = {}
    all_interfaces = {}

    for ip in access_ip:
        print(f"ip: {ip}")
        addresses = {}
        interfaces = {}
        session = Session(hostname=ip, community='private', version=2)

        cur_hostname = session.get('.1.3.6.1.2.1.1.5.0')
        print(f"hostname: {cur_hostname.value}")

        ip_address_list = session.walk('.1.3.6.1.2.1.2.2.1.2')
        for address in ip_address_list:
            ip_addr = str(address.oid.split("3.6.1.2.1.2.2.1.2")[1])

            #print(address.value)
            #print(ip_addr[1:])
            addresses[ip_addr[1:]] = {"name":address.value, "ips":[] }
            interfaces[ip_addr[1:]] = {"name":address.value, "status":""}

        ip_address_list = session.walk('.1.3.6.1.2.1.2.2.1.7')
        for address in ip_address_list:
            ip_addr = str(address.oid.split("3.6.1.2.1.2.2.1.7")[1])

            #print(f"value:{address.value}")
            #print(f"interface is {ip_addr[1:]}")
            interfaces[ip_addr[1:]]["status"] = get_if_status(address.value)
            

        ip_address_list = session.walk('.1.3.6.1.2.1.4.34.1.3')
        for address in ip_address_list:
            oid_addr = str(address.oid.split("3.6.1.2.1.4.34.1.3")[1:])
            oid_addr = oid_addr.split(".")[3:]
            ip_addr = ""
            for i in oid_addr:
                ip_addr += f"{i}."
            ip_addr = ip_addr[:-3]

            if ip_addr.count(".") > 3:
                ip_addr = dec_to_hex(ip_addr)

            #print(str(ip_addr))
            #print(address.value)
            addresses[address.value]['ips'].append(ip_addr)

        #ip_address_list = session.walk('.1.3.6.1.2.1.4.34.1.7')
        #for address in ip_address_list:
        #    oid_addr = str(address.oid.split("3.6.1.2.1.4.34.1.7")[1:])
        #    oid_addr = oid_addr.split(".")[3:]
        #    ip_addr = ""
        #    for i in oid_addr:
        #        ip_addr += f"{i}."
        #    ip_addr = ip_addr[:-3]

        #    if ip_addr.count(".") > 3:
        #        ip_addr = dec_to_hex(ip_addr)

        #    print(str(ip_addr))
        #    print(address.value)


        #ip_address_list = session.walk('.1.3.6.1.2.1.4.20.1')
        #for address in ip_address_list:
        #    print(address.oid)
        #    print(address.value)

        all_addresses[cur_hostname.value] = addresses
        all_interfaces[cur_hostname.value] = interfaces

    #print(all_addresses)
    #print(all_interfaces)
    with open(output_file, 'w') as wptr:
        json.dump(all_addresses, wptr, ensure_ascii=False, indent=4)
        json.dump(all_interfaces, wptr, ensure_ascii=False, indent=4)

        
    util = []
    session = Session(hostname='198.52.100.1', community='private', version=2)
    for i in range(0,24):
        cpu_util = session.get('.1.3.6.1.4.1.9.9.109.1.1.1.1.6.1')
        util.append(int(cpu_util.value))
        #print(f"CPU util: {cpu_util.value}")
        time.sleep(5)
        
    plt.plot(util)
    plt.ylabel("Utilization")
    plt.xlabel("Time")
    plt.title("CPU Utilization in 5 second intervals")

    plt.savefig('utilization.png', bbox_inches='tight')
    plt.show()


    #dec_string = '32.1.174.134.202.254.0.1.200.4.45.255.254.81.0.0'
    #print(dec_to_hex(dec_string))
    #dec_string = '254.128.0.0.0.0.0.0.200.4.45.255.254.81.0.0.18.0.0.3'
    #print(dec_to_hex(dec_string))
    

if __name__ == "__main__":
    main()
