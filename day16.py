
class Data:
    def __init__(self, initial):
        self._data = initial

    def lengthen_to(self, n):
        while len(self._data) < n:
            b = self._data
            b = b[::-1]
            b = ''.join(['1' if c == '0' else '0' for c in b])
            self._data = self._data + '0' + b

    def checksum_to(self, n):
        assert len(self._data) >= n and n % 2 == 0
        checksum = self._data[:n]
        while len(checksum) % 2 == 0:
            pairs = [checksum[2*i:2*i+2] for i in range(len(checksum)//2)]
            checksum = ''
            for pair in pairs:
                if pair == '00' or pair == '11':
                    checksum += '1'
                else:
                    checksum += '0'
        return checksum

d = Data('10111100110001111')
d.lengthen_to(272)
print(d.checksum_to(272))

print('part 2')

d.lengthen_to(35651584)
print(d.checksum_to(35651584))