from .base import NodeChunk, Chunk
import typing

class RIFF(NodeChunk):
    def __init__(self, fmt: typing.SupportsBytes):
        NodeChunk.__init__(self, b'RIFF')

        # put the format name before actual data.
        self.reservedbuf = bytes(fmt)

class RIFX(NodeChunk):
    def __init__(self, fmt: typing.SupportsBytes):
        NodeChunk.__init__(self, b'RIFF', bigendian= True)
        
        self.reservedbuf = bytes(fmt)
        
class LIST(RIFF):
    pass
