import re

letters = tuple('abcdefghijklmnopqrstuvwxyz')


def get_data(s):
    sector = re.findall('-(\d+)\[', s)[0]
    name = s[0:s.index(sector)].replace('-', '')
    checksum = re.findall('\[(.*)\]', s)[0]
    orig_name = s[:re.search('-(\d+)\[', s).regs[0][0]]
    return {'name': name, 'checksum': checksum, 'sector': int(sector), 'orig_name': orig_name}


def make_checksum(name):
    return ''.join([x[1] for x in sorted([(-list(name).count(l), l) for l in set(name)])[:5]])


def decode(s, sector):
    def convert_letter(l):
        return ' ' if l == '-' else letters[(letters.index(l) + sector) % len(letters)]
    return ''.join([convert_letter(l) for l in s])


with open('day4input.txt', 'r') as f:
    rooms = [get_data(s.strip()) for s in f.readlines()]

checksum_rooms = tuple(filter(lambda r: r['checksum'] == make_checksum(r['name']), rooms))
print(sum([r['sector'] for r in checksum_rooms]))

decoded = [(r['orig_name'], decode(r['orig_name'], r['sector']), r['sector']) for r in checksum_rooms]
print([i for i in decoded if 'north' in i[-2]])



