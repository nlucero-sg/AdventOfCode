import hashlib as h

password = ''
count = 0
input = 'ojvtpuvg'

while len(password) < 8:
    m = h.md5()
    m.update((input + str(count)).encode())
    d = m.hexdigest()
    if d[0:5] == '00000':
        password += d[5]
    count += 1

print(password)