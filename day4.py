import re

def get_data(s):
    sector = re.findall('-(\d+)\[', s)[0]
    name = s[0:s.index(sector)].replace('-', '')
    checksum = re.findall('\[(.*)\]', s)[0]
    return name, checksum, int(sector)


def make_checksum(name):
    return ''.join([x[1] for x in sorted([(-list(name).count(l), l) for l in set(name)])[:5]])


with open('day4input.txt', 'r') as f:
    rooms = [get_data(s.strip()) for s in f.readlines()]

print(sum([r[-1] for r in rooms if r[1] == make_checksum(r[0])]))
