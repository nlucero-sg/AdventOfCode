# Disc #1 has 13 positions; at time=0, it is at position 11.
# Disc #2 has 5 positions; at time=0, it is at position 0.
# Disc #3 has 17 positions; at time=0, it is at position 11.
# Disc #4 has 3 positions; at time=0, it is at position 0.
# Disc #5 has 7 positions; at time=0, it is at position 2.
# Disc #6 has 19 positions; at time=0, it is at position 17.

class Disk:

    def __init__(self, positions, initial_position, depth):
        self.positions = positions
        self.initial_position = initial_position
        self.depth = depth

    def pos_at_t(self, t):
        return (self.initial_position + t) % self.positions

    def aligns_for_drop_at_t(self, t):
        return self.pos_at_t(t+self.depth) == 0

class DiskSet:

    def __init__(self, disks=None):
        if disks is None:
            disks = []
        self.disks = disks

    def add_disk(self, disk):
        self.disks.append(disk)

    def solution_at_t(self, t):
        return all([d.aligns_for_drop_at_t(t) for d in self.disks])

td1 = Disk(13, 11, 1)
if td1.pos_at_t(5) == (11 + 5) % 13:
    print('pass postion test')

td2 = Disk(13, 10, 2)
tds = DiskSet([td1, td2])
if tds.solution_at_t(1):
    print('pass solution test')

ds = DiskSet()
ds.add_disk(Disk(13, 11, 1))
ds.add_disk(Disk(5, 0, 2))
ds.add_disk(Disk(17, 11, 3))
ds.add_disk(Disk(3, 0, 4))
ds.add_disk(Disk(7, 2, 5))
ds.add_disk(Disk(19, 17, 6))

for t in range(1000000):
    print(t)
    if ds.solution_at_t(t):
        print('solution!')
        break

#scenario 2

ds.add_disk(Disk(11, 0, 7))

for t in range(10000000):
    if ds.solution_at_t(t):
        print(t)
        print('solution!')
        break