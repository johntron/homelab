import pprint

from bootserver import prompt, cloudinit, netboot, inventory
from bootserver import serve
from bootserver.options import options


def run():
    prompt.choose_address()
    if options.command == 'prepare':
        netboot.prepare()
        cloudinit.prepare()
    elif options.command == 'inventory':
        print(pprint.pprint(inventory.all_nodes()))
    else:
        serve.serve()


if "__main__" == __name__:
    run()
