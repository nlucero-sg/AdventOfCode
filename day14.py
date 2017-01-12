import hashlib


def md5(s):
    m = hashlib.md5()
    m.update(s.encode())
    return m.hexdigest()

class KeyStore:

    def __init__(self, salt):
        self.salt = salt
        self.index = 0
        self.current_hash = md5(salt+str(self.index))
        self.next_hashes = [md5(salt+str(i)) for i in range(1, 1001)]
        self.keys = []


class Key:

    def __init__(self, index, keyval):
        self.index, self.keyval = index, keyval

print(k.current_hash, k.next_hashes[0], len(k.next_hashes))