"""
RIFF chunk is the parent of all the chunks. It always
stays the top of all the chunks.
"""
import _chunk

class RIFF(_chunk.NodeChunk):
    def __init__(self):
        _chunk.NodeChunk.__init__(self, b'RIFF')