with open('day6input.txt','r') as f:
    c = zip(*[l.strip() for l in f.readlines()])

message = ''
for pos in c:
    message += sorted([( -pos.count(l) , l ) for l in set(pos) ])[0][1]

print(message)
