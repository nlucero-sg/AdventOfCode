import re

with open('day9input.txt', 'r') as f:
    instr = f.readline().strip()

count = 0
while instr:
    m = re.search(r"\((\d+)x(\d+)\)", instr)
    if m:
        b, e = m.span()
        letters, times = [int(element) for element in m.groups()]
        count += b
        count += letters * times
        instr = instr[e + letters:]
    else:
        count += len(instr)
        instr = instr[len(instr):]

print(count)
