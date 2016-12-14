input = "R3, L5, R2, L2, R1, L3, R1, R3, L4, R3, L1, L1, R1, L3, R2, L3, L2, R1, R1, L1, R4, L1, L4, R3, L2, L2, R1, L1, R5, R4, R2, L5, L2, R5, R5, L2, R3, R1, R1, L3, R1, L4, L4, L190, L5, L2, R4, L5, R4, R5, L4, R1, R2, L5, R50, L2, R1, R73, R1, L2, R191, R2, L4, R1, L5, L5, R5, L3, L5, L4, R4, R5, L4, R4, R4, R5, L2, L5, R3, L4, L4, L5, R2, R2, R2, R4, L3, R4, R5, L3, R5, L2, R3, L1, R2, R2, L3, L1, R5, L3, L5, R2, R4, R1, L1, L5, R3, R2, L3, L4, L5, L1, R3, L5, L2, R2, L3, L4, L1, R1, R4, R2, R2, R4, R2, R2, L3, L3, L4, R4, L4, L4, R1, L4, L4, R1, L2, R5, R2, R3, R3, L2, L5, R3, L3, R5, L2, R3, R2, L4, L3, L1, R2, L2, L3, L5, R3, L1, L3, L4, L3"
input = [i.strip() for i in input.split(',')]


class Person:
    def __init__(self):
        self._dir = complex(0, 1)
        self._pos = complex(0, 0)

    def turn(self, direction):
        if direction.upper() == "L":
            self._dir *= complex(0, 1)
        elif direction.upper() == "R":
            self._dir *= complex(0, -1)
        else:
            raise ValueError("direction must be 'R' or 'L'")

    def walk(self,steps):
        self._pos += steps*self._dir

    def getLocation(self):
        return self._pos.real, self._pos.imag

p = Person()

for instruction in input:
    turn = instruction[0]
    steps = int(instruction[1:])
    p.turn(turn)
    p.walk(steps)

print(p.getLocation())
print(sum([abs(n) for n in p.getLocation()]))



