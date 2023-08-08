from bootserver import prompt, cloudinit, netboot
from bootserver import serve
from bootserver.options import options


def run():
    prompt.choose_address()
    if options.command == 'prepare':
        netboot.prepare()
        cloudinit.prepare()
    else:
        serve.serve()


if "__main__" == __name__:
    run()
