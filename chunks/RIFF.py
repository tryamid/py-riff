from ._chunk import NodeChunk, Chunk
import typing

class RIFF(NodeChunk):
    """
    RIFF is parent of all the chunks.
    This is a vitual chunk, who's under all the chunks live.
    """
    def __init__(self, fmt: typing.SupportsBytes):
        NodeChunk.__init__(self, b'RIFF')
        self.reservedbuf = bytes(fmt)