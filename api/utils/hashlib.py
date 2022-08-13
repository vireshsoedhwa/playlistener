import hashlib


def create_hash_from_file(file):
    try:
        BUF_SIZE = 65536
        md5 = hashlib.md5()
        with open(file, "rb") as f:
            for chunk in iter(lambda: f.read(BUF_SIZE), b""):
                md5.update(chunk)
        return md5.hexdigest()
    except Exception as e:
        raise HashLibError(e)


def create_hash_from_memory(memoryfile):
    try:
        md5 = hashlib.md5()
        md5.update(memoryfile.read())
        return md5.hexdigest()
    except Exception as e:
        raise HashLibError(e)


class HashLibError(Exception):
    def __init__(self, error, message="HashLib Error: "):
        self.message = message
        self.error = error
        super().__init__(self.message)
    def __str__(self):
        return f'{self.message} > {self.error}'
