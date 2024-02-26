#!/usr/bin/env python

def is_valid_ip(ip):
    ip_split = ip.split(".")

    if len(ip_split) != 4:
        return False

    for i in ip_split:
        if int(i) < 0 or int(i) > 255:
            return False

    return True

# Alternatywnie
# import socket
# def is_valid_ip(ip):
#     try:
#         socket.inet_pton(socket.AF_INET, ip)
#     except Exception:
#         return False

#     return True

def main():
    ip = input("Enter IP: ")

    if is_valid_ip(ip):
        print("The IP address is correct")
    else:
        print("The IP address is not correct")

if __name__ == "__main__":
    main()
