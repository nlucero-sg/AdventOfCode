with open('day6input.txt','r') as f:
    c = zip(*[l.strip() for l in f.readlines()])

message = ''
message_hard = ''
for pos in c:
    message += sorted([( -pos.count(l) , l ) for l in set(pos) ])[0][1]
    message_hard += sorted([( pos.count(l) , l ) for l in set(pos) ])[0][1]

print('message:', message)
print('message_hard:', message_hard)
