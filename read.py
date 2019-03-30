def get_byte_stream(file_name):
    chunks = get_chunk_stream(file_name)
    for chunk in chunks:
        for byte in chunk:
            yield byte


def get_chunk_stream(file_name, chunk_size=4096):
    with open(file_name, 'rb') as file:
        chunk = file.read(chunk_size)
        while chunk:
            yield chunk
            chunk = file.read(chunk_size)
