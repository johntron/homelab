import pprint
import socket

import psutil


def get_ip():
    def interfaces():
        print("Interfaces:")
        iflist = list(psutil.net_if_addrs().keys())
        pprint.pprint(iflist, indent=2)
        return iflist

    def choose_interface():
        ifname = input(f"Which interface has the IP you'd like to use for bootserver? ({iflist[0]}) ").strip()
        return ifname

    def ip(ifname):
        ifaddrs = psutil.net_if_addrs()[ifname]
        address = [addr.address for addr in ifaddrs if addr.family == socket.AF_INET].pop()
        print(f"Got IP {address} from {ifname}")
        return address

    iflist = interfaces()
    ifname = choose_interface()
    return ip(ifname)
