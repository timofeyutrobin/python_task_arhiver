def get_byte_stream(fileName):
    with open(fileName, 'rb') as f:
        byte = f.read(1)
        while byte:
            yield byte
            byte = f.read(1)
