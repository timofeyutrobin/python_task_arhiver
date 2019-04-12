import os
import struct
from readwrite.readwrite import Reader, Writer
from huffmantree.huffmantree import HuffmanTree

BYTES_IN_FLOAT = 4
FILE_EXTENSION = '.huff'
PRECISION = 6


def encode_file(file_name):
    # Сперва подсчитываются частоты и относительные частоты байт в файле.
    # Затем создается дерево Хаффмана,
    # из которого можно получить соответствующие коды.
    with Reader(file_name) as reader:
        frequencies = _get_bytes_frequencies(reader)

        file_size = reader.file_size
        probabilities = {
            f: round(frequencies[f]/file_size, PRECISION) for f in frequencies
        }

    huffman_tree = HuffmanTree(probabilities)

    out_file_name = file_name + FILE_EXTENSION
    offset = _get_first_byte_offset(frequencies, huffman_tree)
    with Reader(file_name) as reader, Writer(out_file_name) as writer:
        writer.write(struct.pack('b', offset))

        _write_probabilities_to_file(writer, probabilities)
        _write_codes_to_file(reader, writer, huffman_tree, offset)
    return out_file_name


def _get_bytes_frequencies(reader):
    frequencies = {}
    for byte in reader.get_byte_stream():
        frequencies[byte] = frequencies.get(byte, 0) + 1

    return frequencies


def _get_first_byte_offset(frequencies, huffman_tree):
    # Поскольку коды Хаффмана имеют переменную длину,
    # может получиться так, что длина закодированной строки не будет кратна 8.
    # Нам нужно знать, на сколько бит нужно сдвинуть последовательность кодов,
    # чтобы при распаковке закончить чтение ровно в конце байта
    # Считаем длину закодированной строки и берем остаток от деления на 8
    length = 0
    for byte in frequencies:
        length += frequencies[byte] * len(huffman_tree.get_code(byte))
    offset = 8 - (length % 8)

    return offset


def _write_probabilities_to_file(file, dic):
    # Чтобы декодировать файл нужно сперва построить дерево,
    # поэтому в выходной файл нужно записать словарь относительных частот.
    # Он храниться как множество пар (byte, float)
    # Перед словарем записывается его длина
    dict_len = len(dic)

    dict_chunk = struct.pack('h', dict_len)
    for byte in dic:
        dict_chunk += bytes([byte])
        dict_chunk += struct.pack('f', dic[byte])

    file.write(dict_chunk)


def _write_codes_to_file(reader, writer, huffman_tree, offset):
    bits = ''
    first = True
    for chunk in reader.get_chunk_stream():
        if first:
            bits += _to_huffman_code(chunk, huffman_tree, offset)
            first = False
        else:
            bits += _to_huffman_code(chunk, huffman_tree)
        remainder = len(bits) % 8
        rest = ''
        if remainder:
            rest = bits[-remainder:]
            bits = bits[:-remainder]

        writer.write_bits(bits)
        bits = rest


def _to_huffman_code(chunk, huffman_tree, offset=0):
    huffman_string = '0' * offset
    for byte in chunk:
        byte_code = huffman_tree.get_code(byte)
        huffman_string += byte_code
    return huffman_string


def decode_file(file_name, out_file_name=None):
    if out_file_name is None:
        out_file_name = _get_original_file_name(file_name)

    with Reader(file_name) as reader, Writer(out_file_name) as writer:
        # Первый байт - количество бит, которые нужно прочитать в последнем байте
        first_byte_offset = struct.unpack('b', reader.read(1))[0]

        # Далее читаем словарь
        probabilities = _read_probabilities_from_file(reader)

        # Из прочитанного словаря можем построить дерево
        huffman_tree = HuffmanTree(probabilities)

        first = True
        for chunk in reader.get_chunk_stream():
            if first:
                bit_string = _to_bits(chunk, first_byte_offset)
                first = False
            else:
                bit_string = _to_bits(chunk)

            original_bytes = _get_original_bytes(bit_string, huffman_tree)
            writer.write(original_bytes)


def _get_original_file_name(file_name: str):
    name, extension = os.path.splitext(file_name)
    if extension != FILE_EXTENSION:
        raise AttributeError(
            'Wrong file extension, this archiver works with .huff extension'
        )
    return name


def _read_probabilities_from_file(file):
    probabilities = {}
    dict_len = struct.unpack('h', file.read(2))[0]
    for i in range(dict_len):
        byte = ord(file.read(1))
        probability = struct.unpack('f', file.read(4))[0]
        probability = round(probability, PRECISION)
        probabilities[byte] = probability
    return probabilities


def _to_bits(chunk, offset=0):
    bits = []
    for byte in chunk:
        byte_bits = []
        for i in range(8):
            bit = (byte >> i) & 1
            byte_bits.append(bit)
        byte_bits.reverse()
        bits += byte_bits
        byte_bits.clear()
    return bits[offset:]


def _get_original_bytes(bit_string, huffman_tree):
    original_bytes = bytearray()
    for bit in bit_string:
        byte = huffman_tree.search(bit)
        if byte is not None:
            original_bytes.append(byte)
    return original_bytes
