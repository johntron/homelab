import threading

from time import sleep

from pypxe import tftp

from .options import options


def serve():
    tftp_server = tftp.TFTPD(
        netboot_directory=options.static,
        mode_verbose=True,
        mode_debug=True,
        # port=args.TFTP_PORT,
        ip=options.address
    )
    tftpd = threading.Thread(target=tftp_server.listen)
    tftpd.daemon = True
    tftpd.start()
    while tftpd.is_alive():
        sleep(1)
