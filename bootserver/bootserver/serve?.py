import pprint
import socket
import threading
from time import sleep

import psutil as psutil
from pypxe import tftp

def serve(ip):
    tftp_server = tftp.TFTPD(
        netboot_directory='bootserver',
        mode_verbose=True,
        mode_debug=True,
        # port=args.TFTP_PORT,
        ip=ip
    )
    tftpd = threading.Thread(target=tftp_server.listen)
    tftpd.daemon = True
    tftpd.start()
    while tftpd.is_alive():
        sleep(1)

def get_ip():
    def interfaces():
        print("Interfaces:")
        iflist = list(psutil.net_if_addrs().keys())
        pprint.pprint(iflist, indent=3)
        return iflist

    def choose_interface():
        ifname = input(f"Which interface has the IP you'd like to use for bootserver? ({iflist[1]}) ").strip()
        return ifname

    def ip(ifname):
        ifaddrs = psutil.net_if_addrs()[ifname]
        address = [addr.address for addr in ifaddrs if addr.family == socket.AF_INET].pop()
        print(f"Got IP {address} from {ifname}")
        return address

    iflist = interfaces()
    ifname = choose_interface()
    return ip(ifname)

ip = get_ip()
serve(ip)