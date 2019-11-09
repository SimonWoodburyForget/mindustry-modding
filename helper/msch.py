""" Mindustry schematics (v0) parser written in Python. 

Note: this can do plenty of invalid things, if you insert data manually
although the game wont really care about it, as it doesn't manual inputs.
For example, in the example below, you'll see a 3x3 block, inserted into 
a 1x1 schematic.

This package uses a custom version of parsec.py fixed for byte parsing:
- https://github.com/SimonWoodburyForget/parsec.py
"""

from pathlib import Path
import zlib
from parsec import string, generate, many, regex, times, none_of
from struct import unpack, pack
from collections import OrderedDict, namedtuple
from base64 import b64decode, b64encode

def get_pos(x, y):
    return x << 0xf | y & 0xffff

def pos_x(pos):
    return pos >> 0xf

def pos_y(pos):
    return pos & 0xffff

def pos_xy(pos):
    return pos_x(pos), pos_y(pos)

class Schematic(namedtuple("Schematic", "name pos config rotation")):
    pass

class Schematics(namedtuple("Schematics", "width height tags tiles")):
    pass 

HEADER = b"msch"
VERSION = b"\x00"

########################################
## Reader
########################################

header = string(HEADER)
version = string(VERSION)

everything = regex(b"(?s).*") # don't forget newlines

byte = regex(b"(?s).")
char = byte.parsecmap(lambda x: unpack("b", x)[0])
short = regex(b"(?s).{2}").parsecmap(lambda x: unpack(">h", x)[0])
intp = regex(b"(?s).{4}").parsecmap(lambda x: unpack(">i", x)[0])
nbytes = lambda x: times(byte, x).parsecmap(lambda x: b"".join(x))

@generate
def utf8_bytes():
    """ Parses utf8 string, prefixed with length. """
    length = yield short
    name = yield nbytes(length)
    return name.decode("utf8")

@generate
def kv_bytes():
    """ Parses list of key values. """
    kv = {}
    n = yield char
    for _ in range(0, n):
        key = yield utf8_bytes
        val = yield utf8_bytes
        kv[key] = val
    return kv

@generate
def ordset_bytes():
    """ Parses an order set of bytes.
    (returns OrderedDict with None values) """
    names = OrderedDict()
    n = yield char
    for _ in range(0, n):
        name = yield utf8_bytes
        names[name] = None
    return names

@generate
def tilesec():
    """ Parses block+tile section. """
    blocks = yield ordset_bytes
    n = yield intp
    out = []
    for _ in range(0, n):
        idx = yield char
        name = next((x for i, x in enumerate(blocks) if i == idx))
        pos = yield intp
        config = yield intp
        rotation = yield char
        out.append(Schematic(name, pos_xy(pos), config, rotation))
    return out

@generate
def msch_data():
    """ Parses the decompressed msch content. """
    width = yield short
    height = yield short
    tags = yield kv_bytes # dict of tags (ex: name)
    tiles = yield tilesec
    return Schematics(width, height, tags, tiles)

@generate
def msch():
    """ Parses decoded msch. """
    yield header
    yield version
    data = yield everything
    return msch_data.parse(zlib.decompress(data))

def loads(path):
    """ Loads a binary `.msch` formatted file at a path. """
    with open(path, "rb") as f:
        data = f.read()
    return load(data)

def load(data, encoding="utf8"):
    """ Loads a base64 encoded schematic `str` object, 
    or a non-base65 encoded `bytes` object; returns a 
    Schematics object containing a Schematic, and it's 
    metadata, like width, height and tags."""
    if isinstance(data, str):
        base64header = "bXNjaAB"
        if not data.startswith(base64header):
            raise ValueError(f"String should start with: {base64header}")
        data = bytes(data, encoding)
        data = b64decode(data)

    if isinstance(data, bytes):
        data = msch.parse(data)
        return data
    else:
        raise ValueError(f"Unknown or unsupported type: {type(data)}")

########################################
## Writer
########################################

def pack_utf8(string):
    b = bytes(string, "utf8")
    bl = pack(">h", len(b))
    return bl + b

def pack_content(data):
    out = pack(">hh", data.width, data.height)

    out += pack("b", len(data.tags))
    for k, v in data.tags.items():
        out += pack_utf8(k)
        out += pack_utf8(v)

    blocks = OrderedDict()
    out += pack("b", len(set(x.name for x in data.tiles)))
    for i, k in enumerate(set(x.name for x in data.tiles)):
        blocks[k] = None
        out += pack_utf8(k)

    out += pack(">i", len(data.tiles))
    for v in data.tiles:
        out += pack("b", next((i for i, x in enumerate(blocks) if x == v.name)))
        out += pack(">i", get_pos(*v.pos))
        out += pack(">i", v.config)
        out += pack("b", v.rotation)    
    return out

def dump(data, encode=False):
    bdata = pack_content(data)
    zdata = zlib.compress(bdata)
    data = HEADER + VERSION + zdata
    if encode:
        return str(b64encode(data), "utf8")
    else:
        return data
    
if __name__ == "__main__":
    test = "1572947991821.msch"
    user_data = Path(".local/share/Mindustry/schematics")
    path = Path.home() / user_data / test
    loads(path)

    basic_shard = "bXNjaAB4nD2K2wqAIBiD5ymibnoRn6YnEP1BwUMoBL19FuJ2sbFvUFgYZDaJsLeQrkinN9UJHImsNzlYE7WrIUastuSbnlKx2VJJt+8IQGGKdfO/8J5yrGJSMegLg+YUIA=="
    basic_shard_obj = load(basic_shard)
    assert len(basic_shard_obj.tiles) == 5

    data = dump(basic_shard_obj)
    assert dump(load(data)) == data # ...may randomly fail?
    
    print(dump(Schematics(
        1, 1, {"name": "Core Block"}, [Schematic("core-shard", (0, 0), 0, 0)]
    ), True))

    ##########################################
    # vault replaced with core-nucleus example
    ##########################################
    #
    # schematic with vault at place of core
    print(load("bXNjaAB4nGPgZuBmZGDJS8xNZWALSS0uUXBkZuDOSSxOLdJNKcrMyWFgLUsszSlhECjILweK5eWnpOrmJBalpzIwMLAxMDACIQQwMnBCaVYgBAEmoAJGiBBQDqaOE6oOAMywEOk="))
    #
    # rename `vault` with `core-nucleus`
    print(dump(Schematics(width=11, height=11, tags={'name': 'Test A'}, tiles=[Schematic(name='laser-drill', pos=(2, 1), config=0, rotation=0), Schematic(name='laser-drill', pos=(2, 9), config=0, rotation=0), Schematic(name='core-nucleus', pos=(10, 5), config=0, rotation=0), Schematic(name='power-node-large', pos=(12, 1), config=0, rotation=1), Schematic(name='laser-drill', pos=(18, 1), config=0, rotation=0), Schematic(name='laser-drill', pos=(18, 9), config=0, rotation=0)]), True))
    #
    # no repositioning is required, even though
    # the vault is smaller then the core.

    
