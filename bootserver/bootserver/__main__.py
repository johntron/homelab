import pprint

from bootserver import prompt, cloudinit, inventory, ipxe, server
from bootserver.options import options


def run():
    prompt.choose_address()
    if options.command == 'prepare':
        ipxe.prepare()
        cloudinit.prepare()
    elif options.command == 'inventory':
        print(pprint.pprint(inventory.all_nodes()))
    else:
        server.serve()


if "__main__" == __name__:
    run()
