import hashlib

def create_hash(file):
    BUF_SIZE = 65536
    md5 = hashlib.md5()
    # sha1 = hashlib.sha1()

    with open(file, "rb") as f:
        for chunk in iter(lambda: f.read(BUF_SIZE), b""):
            md5.update(chunk)
    return md5.hexdigest()