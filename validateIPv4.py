#!/usr/bin/env python3
import argparse
import re

###
# Overview
# This module is only for the purpose of checking that a passed in string is a valid IP address
# This means it is not only in the form of [0-255].[0-255].[0-255].[0-255]
# but also not reserved for multicast, loopback, link-local, or broadcast
###


##Note, to check validity I received help from https://www.geeksforgeeks.org/python/python-program-to-validate-an-ip-address/
#This chunk just grabs an address as an input if the module is run directly
def ArgParseHelper():
    parser = argparse.ArgumentParser(description="Returns if IPv4 address is valid or not")
    parser.add_argument("address", action='store', help="The address you wish to validate")
    parser.add_argument("--version", action='version', version='%(progs)s 1.0')
    args = parser.parse_args()
    return(args)

#this chunk actually checks the input
#this goes through 2 rounds of checking, with the first being a regex to ensure it is in a certain range
#and the second ensuring it is not one of the reserved values that still qualifies as a valid address
def isValidAddress(address):
    ##Basically what this huge reges does in ensure that the IP is [0-223].[0-255].[0-255].[0-255]
    regex = "^((22[0-3]|2[0-1][0-9]|1[0-9][0-9]|[1-9]?[0-9])\.)((25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\.){2}(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])$"
    if(re.search(regex, address)):
        ##Weed out 169.254 and 127 addresses
        ##Because these are in the middle of our valid IP range, we just set up a second screen for them
        restricted = "^(?!(169.254)|(127)).*$"
        if re.search(restricted, address):
            print("Valid IP Address")
            return True
        else:
            print("Invalid IP Address")
            return False
    else:
        print("Invalid IP address")
        return False

def main():
    args = ArgParseHelper()
    isValidAddress(args.address)
    return 0

if __name__ == "__main__":
    main()
