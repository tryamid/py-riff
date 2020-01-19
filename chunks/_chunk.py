"""
RIFF is a object-oriented file-format that uses chunk to label each
data with a meaning and a size. In this API chunks base chunks come
in two flavours — leaf chunk, node chunk.

- Leaf Chunk: has no sub-chunks in it, only raw binary data.
- Node Chunk: has one or more sub-chunks in it.
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

    def __init__(self, id: bytes):
        if not isinstance(id, bytes):
            raise TypeError(f"Identity must be a series of bytes and not {type(id)}.")

        self.id = id
        self.size = 0

    def append(self, data: bytes):
        """Appends a blob of bytes to the underlying buffer."""
        if not isinstance(data, bytes):
            raise TypeError(f"Cannot append {type(data)} to underlying the buffer.")

        self._rawdatbuf+= data
        self.size+= len(data)
    
    def write(self, data: bytes):
        """Overwrites a blob of bytes to the underlying buffer."""
        if not isinstance(data, bytes):
            raise TypeError(f"Cannot write {type(data)} to underlying the buffer.")

        self._rawdatbuf = data
        self.size = len(data)

    def __bytes__(self):
        return (self.id +
                struct.pack('>I', self.size) +
                self._rawdatbuf)
    


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

        list.append(self, chk)

    def extend(self, chks: typing.Iterable[Chunk]):
        """Extends the list by adding chunks to it."""
        for chk in chks:
            if not isinstance(chk, Chunk):
                raise TypeError("Not a valid chunk to append with.")
            
            list.extend(self, chk)

    def insert(self, index, chk: Chunk):
        """Inserts a chunk at an arbitary position in the datablock."""
        if not isinstance(chk, Chunk):
            raise TypeError("Not a valid chunk to insert.")

        list.insert(self, index, chk)

    def __bytes__(self):
        # combines all the chunkdata together.
        if isinstance(self.reservedbuf, bytes):
            Chunk.append(self, self.reservedbuf)
        # concat chunks together.
        Chunk.append(self, functools.reduce(lambda achk, cchk: achk + bytes(cchk), self, b''))
        return Chunk.__bytes__(self)