import pprint
import socket

import psutil

from .options import options


def choose_address():
    def interfaces():
        print("Interfaces:")
        iflist = list(psutil.net_if_addrs().keys())
        pprint.pprint(iflist, indent=2)
        return iflist

    def choose_interface():
        ifname = input(f"Which interface has the IP you'd like to use for bootserver? ({iflist[0]}) ").strip()
        return ifname

    def address(ifname):
        ifaddrs = psutil.net_if_addrs()[ifname]
        address = [addr.address for addr in ifaddrs if addr.family == socket.AF_INET].pop()
        print(f"Got IP {address} from {ifname}")
        return address

    if options.address:
        print(f"Using {options.address} for bootserver")
        return
    iflist = interfaces()
    ifname = choose_interface()
    options.address = address(ifname)
