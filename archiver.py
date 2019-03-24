import read
from huffmantree.huffmantree import HuffmanTree


def get_bytes_frequencies(byteStream):
    frequencies = {}
    for byte in byteStream:
        frequencies[byte] = frequencies.get(byte, 0) + 1
    return frequencies


def encode_file(fileName):
    pass
