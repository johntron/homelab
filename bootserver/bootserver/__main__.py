from bootserver.options import options
from bootserver import serve
from bootserver import prompt
from bootserver import netboot

prompt.choose_address()
if options.command == 'prepare':
    netboot.prepare()
else:
    serve.serve()
