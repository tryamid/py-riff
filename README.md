OOP based [**RIFF** encoding][1] implementation in pure *Python*. These chunks can be decoded by the pre-packaged [`chunks`][2] module in
the Python standard library.

### Ideology
For the ease of use the API distinguishes chunks into two variants — *Node Chunk*, *Leaf Chunk*.

| Chunk Type |                     Description                     |
|------------|-----------------------------------------------------|
|    Leaf    |       has no subchunks, only raw binary data.       |
|    Node    | has one or more subchunks (optionally binary data). |


[1]: https://en.wikipedia.org/wiki/Resource_Interchange_File_Format
[2]: https://docs.python.org/3/library/chunk.html
