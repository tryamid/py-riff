"""
RIFF is a object-oriented file-format that uses chunk to label each
data with a meaning and a size. In this API chunks base chunks come
in two flavours — leaf chunk, node chunk.

* Chunk types:
    * Leaf: has no sub-chunks in it, only raw binary data.
    * Node: has one or more sub-chunks in it.
"""

import struct
import typing
import functools

class Chunk(typing.SupportsBytes):
    """
    A RIFF chunk is a blob of data with a identity behalf
    of its meaning. Chunk has a four-byte identity,
    a unsigned 32-bit integer telling the data's size and
    the raw-binary data itself.
    """
    # a series of bytes that contain raw chunk data. 
    _rawdatbuf = b''

    def __init__(self, id: bytes, bigendian= False):
        self.id = id
        self.size = 0
        self.endianness = '<>'[bigendian]

    def append(self, data: bytes):
        """Appends a blob of bytes to the underlying buffer."""
        self._rawdatbuf+= data
        self.size+= len(data)
    
    def write(self, data: bytes):
        """Overwrites with a blob of bytes in the underlying buffer."""
        self._rawdatbuf = data
        self.size = len(data)

    def __bytes__(self):
        return (self.id +
                struct.pack(self.endianness + 'I' , self.size) +
                self._rawdatbuf)

class ChunkEndiannessDifference(Exception):
   """Subchunk differing in endianness from the root chunk."""

class NodeChunk(Chunk, list):
    """
    A variant of a chunk that has one or multiple subchunks in it
    (e.g `RIFF`, `LIST`).
    """
    # a space where a chunk reserves its data before the sub-chunks.
    reservedbuf = None

    def append(self, chk: Chunk):
        """Appends a chunk to the end of the list."""
        if not isinstance(chk, Chunk):
            raise TypeError("Not a valid chunk to append.")
        if chk.endianness != self.endianness:
            raise ChunkEndiannessDifference(f"{chk.id} differs from {self.id}")

        list.append(self, chk)

    def extend(self, chks: typing.Iterable[Chunk]):
        """Extends the list by adding chunks to it."""
        for chk in chks:
            if not isinstance(chk, Chunk):
                raise TypeError("Not a valid chunk to append with.")
            if chk.endianness != self.endianness:
               raise ChunkEndiannessDifference(f"{chk.id} differs from {self.id}")
            
        list.extend(self, chk)

    def insert(self, index, chk: Chunk):
        """Inserts a chunk at an arbitary position in the datablock."""
        if not isinstance(chk, Chunk):
            raise TypeError("Not a valid chunk to insert.")
        if chk.endianness != self.endianness:
            raise ChunkEndiannessDifference(f"{chk.id} differs from {self.id}")

        list.insert(self, index, chk)

    def __bytes__(self):
        # combines all the chunkdata together.
        if isinstance(self.reservedbuf, bytes):
            Chunk.write(self, self.reservedbuf)
        # concat chunks together.
        Chunk.append(self, functools.reduce(lambda achk, cchk: achk + bytes(cchk), self, b''))
        return Chunk.__bytes__(self)
