import os
import pathlib

from py3tftp import file_io
from py3tftp.protocols import TFTPServerProtocol

from bootserver.options import options


class FileReader(file_io.FileReader):
    def __init__(self, fname, chunk_size=0, mode=None):
        self._f = None
        self.fname = pathlib.Path(options.static) / os.fsdecode(fname)
        self.chunk_size = chunk_size
        self._f = self._open_file()
        self.finished = False
        if mode:
            print(f"Ignoring mode {mode.decode('utf-8')}")
        print(f"Reading {self.fname}")


class TFTPProtocol(TFTPServerProtocol):
    def select_file_handler(self, packet):
        if packet.is_wrq():
            raise NotImplementedError("Writing is not supported")
        else:
            return lambda filename, opts: FileReader(filename, opts, packet.mode)
