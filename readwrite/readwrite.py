import os


class File:
    def __init__(self, file_path, mode):
        self._file = open(file_path, mode)
        self._size = os.path.getsize(file_path)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._file.close()

    @property
    def file_size(self):
        return self._size


class Reader(File):
    def __init__(self, file_path):
        file_exist = os.path.isfile(file_path)
        if not file_exist:
            raise FileNotFoundError
        super().__init__(file_path, 'rb')

    def get_chunk_stream(self, chunk_size=4096):
        chunk = self._file.read(chunk_size)
        while chunk:
            yield chunk
            chunk = self._file.read(chunk_size)

    def get_byte_stream(self):
        # read file in chunks for better performance
        for chunk in self.get_chunk_stream():
            for byte in chunk:
                yield byte

    def read(self, count):
        return self._file.read(count)

    def read_last_byte(self):
        self._file.seek(-1, 2)
        byte = self._file.read(1)
        self._file.seek(0)

        return byte


class Writer(File):
    def __init__(self, file_path):
        file_exist = os.path.isfile(file_path)
        if file_exist:
            raise FileExistsError
        super().__init__(file_path, 'w+b')

    def write_bits(self, bit_string):
        self._file.write(self._to_bytes(bit_string))

    def write(self, byte_string):
        self._file.write(byte_string)

    @staticmethod
    def _to_bytes(bit_string):
        bytes_count = (len(bit_string) + 7) // 8
        return int(bit_string, 2).to_bytes(bytes_count, 'big')
