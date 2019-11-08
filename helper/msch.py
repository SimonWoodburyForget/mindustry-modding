""" Mindustry schematics (v0) parser written in Python. """

from pathlib import Path
import zlib
from parsec import string, generate, many, regex, times, none_of
from struct import unpack
from collections import OrderedDict
from base64 import b64decode, b64encode

def get_pos(x, y):
    return x << 0xf | y & 0xffff

def pos_x(pos):
    return pos >> 0xf

def pos_y(pos):
    return pos & 0xffff

def pos_xy(pos):
    return pos_x(pos), pos_y(pos)

header = string(b"msch")
version = string(b"\x00")

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
        out.append((name, pos_xy(pos), config, rotation))
    return out

@generate
def msch_data():
    """ Parses the decompressed msch content. """
    width = yield short
    height = yield short
    tags = yield kv_bytes # dict of tags (ex: name)
    tiles = yield tilesec
    return width, height, tags, tiles

@generate
def msch():
    """ Parses decoded msch. """
    yield header
    yield version
    data = yield everything
    return msch_data.parse(zlib.decompress(data))

def loads(path):
    with open(path, "rb") as f:
        data = f.read()
    return load(data)

def load(data, encoding="utf8"):
    if isinstance(data, str):
        base64header = "bXNjaAB"
        if not data.startswith(base64header):
            raise ValueError(f"String should start with: {base64header}")
        data = bytes(data, encoding)
        data = b64decode(data)

    data = msch.parse(data)
    print(data)

if __name__ == "__main__":
    test = "1572947991821.msch"
    user_data = Path(".local/share/Mindustry/schematics")
    path = Path.home() / user_data / test
    loads(path)

    basic_shard = "bXNjaAB4nD2K2wqAIBiD5ymibnoRn6YnEP1BwUMoBL19FuJ2sbFvUFgYZDaJsLeQrkinN9UJHImsNzlYE7WrIUastuSbnlKx2VJJt+8IQGGKdfO/8J5yrGJSMegLg+YUIA=="

    load(basic_shard)
