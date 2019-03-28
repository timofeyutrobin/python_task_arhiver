def get_byte_stream(fileName):
    with open(fileName, 'rb') as file:
        byte = file.read(1)
        while byte:
            yield byte
            byte = file.read(1)
