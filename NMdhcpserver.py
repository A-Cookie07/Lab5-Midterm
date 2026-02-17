#!/usr/bin/env python3
from netmiko import ConnectHandler
import threading

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
            output = connection.send_command('show cdp entry R5 | include address: ')
            for i in output.split('\n'):
                if 'global' in i:
                    return i
            print("no global address found\n")
            return -1
    except Exception as e:
        print(f"ERROR: {e}")

def connect_R5(host, username, password):
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

    address = get_R5_address(host, username, password)
    address = address.split(" ")[4]

    connect_R5(address, username, password)


    


if __name__ == "__main__":
    main()