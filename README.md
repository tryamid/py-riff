[![PyPI version](https://badge.fury.io/py/py-riff.svg)](https://badge.fury.io/py/py-riff)

OOP based [**RIFF** encoding][1] implementation in pure *Python*. Chunks can be decoded by the pre-packaged [`chunks`][2] module in
the Python standard library.

### Ideology
For the ease of use the API distinguishes chunks into two variants — *Node Chunk*, *Leaf Chunk*.

| Chunk Type |                     Description                     |
|------------|-----------------------------------------------------|
|    Leaf    |       has no subchunks, only raw binary data.       |
|    Node    | has one or more subchunks (optionally binary data). |

#### Built in Chunks
Some built-in chunks exist because these chunks are most commonly seen in **RIFF** based files.

| Chunk ID | Description |
|----------|-------------|
| `RIFF`   | exists as a parent of all chunks and to identify as RIFF bitstream. |
| `RIFX`   | derived version of the `RIFF` chunks which uses big-endian. |
| `LIST`   | chunk used to extend RIFF based files addtional formats. |

[1]: https://en.wikipedia.org/wiki/Resource_Interchange_File_Format
[2]: https://docs.python.org/3/library/chunk.html
