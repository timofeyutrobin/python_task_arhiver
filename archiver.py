import os
import struct
import read
from huffmantree.huffmantree import HuffmanTree


class Archiver:
    FLOAT_LENGTH = 4

    def __init__(self, file_name):
        file_exists = os.path.isfile(file_name)
        if file_exists:
            self.inFileName = file_name
            self.inFileSize = os.path.getsize(file_name)
            self.outFileName = file_name + '.huffmanized'

            # will be created in encode method
            self.outFile = None
        else:
            raise FileNotFoundError
        self.probabilities = {}

    def encode_file(self):
        byte_stream = read.get_byte_stream(self.inFileName)
        frequencies = self._get_bytes_frequencies(byte_stream)
        self.probabilities = {
            f: frequencies[f] / self.inFileSize for f in frequencies
        }

        huffman_tree = HuffmanTree(self.probabilities)

        self.outFile = open(self.outFileName, 'w+b')
        self.write_dict_to_file()

    def write_dict_to_file(self):
        # dict stored at the beginning of the file
        # as a pair (byte, float)
        dict_len = len(self.probabilities) * (1 + self.FLOAT_LENGTH)
        dict_chunk = struct.pack('h', dict_len)

        for byte in self.probabilities:
            dict_chunk += bytes([byte])
            dict_chunk += struct.pack('f', self.probabilities[byte])

        self.outFile.write(dict_chunk)

    @staticmethod
    def _get_bytes_frequencies(byte_stream):
            frequencies = {}
            for byte in byte_stream:
                frequencies[byte] = frequencies.get(byte, 0) + 1
            return frequencies
