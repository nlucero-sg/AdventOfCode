import hashlib
import re


def md5(s):
    m = hashlib.md5()
    m.update(s.encode())
    return m.hexdigest()

class KeyStore:

    _three_pattern = re.compile(r'(\S)(\1)(\1)')

    def __init__(self, salt):
        self.salt = salt
        self._index = 0
        self._current_hash = md5(self.salt+str(self._index))
        self._next_hashes = [md5(self.salt+str(i)) for i in range(1, 1001)]
        self.keys = []

    def _advance(self):
        self._index += 1
        self._current_hash = md5(self.salt+str(self._index))
        self._next_hashes = self._next_hashes[1:] + [md5(self.salt+str(1000+self._index))]

    def generate_keys(self, n):
        n_keys = len(self.keys)
        while len(self.keys) < n_keys + n:
            if self._current_is_key():
                self.keys.append(Key(self._index, self._current_hash))
            self._advance()

    def _current_is_key(self):
        m = re.search(KeyStore._three_pattern, self._current_hash)
        if m:
            c = m.groups()[0]
            _five_pattern = re.compile("["+c+"]{5}")
            for n in self._next_hashes:
                if re.search(_five_pattern,n):
                    return True
        return False

class Key:

    def __init__(self, index, keyval):
        self.index, self.keyval = index, keyval

    def __str__(self):
        return "Key: {}, Value: {}".format(self.index, self.keyval)

ks = KeyStore('zpqevtbw')
ks.generate_keys(64)
count = 1
for k in ks.keys:
    print(count, k)
    count += 1
print(len(ks.keys))
