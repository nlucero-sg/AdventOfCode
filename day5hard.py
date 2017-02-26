import hashlib as h

count = 0
input = 'ojvtpuvg'

password = list('--------')

while '-' in password:
    m = h.md5()
    m.update((input + str(count)).encode())
    d = m.hexdigest()
    if d[0:5] == '00000':
        try:
            pos = int(d[5])
            if password[pos] == '-':
                password[int(d[5])] = d[6]
                print(password)
        except:
            print('Error:', d[5])
    count += 1

print('Password:', ''.join(password))