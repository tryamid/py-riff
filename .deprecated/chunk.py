raise DeprecationWarning("This module was initally made for testing, but now abandoned in favour of the newer module.")

"""
RIFF is a object-oriented file-format that uses chunk to label each
data with a meaning and a size. Chunks come in two flavours -
*leaf chunk*, *node chunk*.

Leaf Chunk: a chunk that has no sub-chunks in it, only raw binary data.
Node Chunk: a chunk that one or more sub-chunks in it.
"""

import struct

class Chunk(bytearray):
    """
    A RIFF chunk is a blob of data with a identity behalf
    of its meaning. Chunk has a four-byte identity,
    a unsigned 32-bit integer telling the data's size and
    the raw-binary data itself.
    """
    # size of the raw data contained inside a chunk.
    _size: int = 0

    def __init__(self, id: bytes):
        bytearray.__init__(self, 8)
        self[0:4] = id

    def append(self, data: int):
        """Appends series of bytes to end of the datablock."""
        bytearray.append(self, data)
        self._size+= 1
        self[4:8] = struct.pack('>I', self._size)

    def insert(self, index, data: int):
        """Inserts a specific bytevalue at an arbitary postion in datablock."""
        bytearray.insert(self, index+8, data)
        if index <= self._size:
            self._size+= 1
            self[4:8] = struct.pack('>I', self._size)


class NodeChunk(Chunk):
    """
    A variant of a chunk that has one or multiple subchunks in it
    (e.g `RIFF`, `LIST`).
    """
    # list of chunks to be put in
    _chunks = []

    def append(self, chk: Chunk):
        """Appends a chunk to the end of the list."""
        if not isinstance(chk, Chunk):
            raise TypeError("Not a valid chunk to append.")

        self._chunks.append(chk)
        for dat in chk:
            Chunk.append(self, dat)

    def insert(self, index, chk: Chunk):
        """Inserts a chunk at an arbitary position in the datablock."""
        if not isinstance(chk, Chunk):
            raise TypeError("Not a valid chunk to insert.")

        self._chunks.insert(index, chk)
        _curdatoff = 0
        for _chk in self._chunks:
            for dat, datoff in enumerate(_chk):
                Chunk.insert(self, _curdatoff + datoff, dat)
                _curdatoff+= 1