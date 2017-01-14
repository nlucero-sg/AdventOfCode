import re

class Game:

    def __init__(self, inst):
        self.a, self.b, self.c, self.d = 0, 0, 0, 0
        self.pointer = 0
        self.inst = inst
        self.halted = False

    def cpy(self, i, reg):
        if isinstance(i, str):
            i = self.get(i)
        self.set(reg, i)
        self.pointer += 1

    def inc(self, reg):
        self.set(reg, self.get(reg) + 1)
        self.pointer += 1

    def dec(self, reg):
        self.set(reg, self.get(reg)-1)
        self.pointer += 1


    def get(self, char):
        assert isinstance(char, str)
        if char == 'a':
            return self.a
        if char == 'b':
            return self.b
        if char == 'c':
            return self.c
        if char == 'd':
            return self.d
        else:
            raise KeyError("{} is not a valid register".format(char))

    def set(self, char, i):
        assert isinstance(char, str)
        if char == 'a':
            self.a = i
        elif char == 'b':
            self.b = i
        elif char == 'c':
            self.c = i
        elif char == 'd':
            self.d = i
        else:
            raise KeyError("{} is not a valid register".format(char))

    def jnz(self, x, y):
        if isinstance(x, str):
            x = self.get(x)
        if x:
            pointer = self.pointer + y
            if pointer >= len(self.inst):
                self.halt()
            elif pointer < 0:
                pointer = 0
            else:
                self.pointer = pointer
        else:
            self.pointer += 1

    def halt(self):
        print("Program halted with (a, b, c, d) == ({}, {}, {}, {})".format(self.a, self.b, self.c, self.d))
        self.halted = True

    def get_instruction(self):
        try:
            return self.inst[self.pointer]
        except IndexError:
            self.halt()
            return ''

    def __str__(self):
        return str((self.a,self.b,self.c,self.d))


re_copy = re.compile(r"cpy (\S+) (\S+)")
re_jnz = re.compile(r"jnz (\S+) (\S+)")
re_inc = re.compile(r"inc (\S+)")
re_dec = re.compile(r"dec (\S+)")

with open('day11input.txt', 'r') as f:
    instr = [r.strip() for r in f.readlines()]

g = Game(instr)

while not g.halted:
    inst = g.get_instruction()
    m = re.match(re_copy, inst)
    if m:
        i, reg = m.groups(0)
        try:
            i = int(i)
        except:
            pass
        g.cpy(i, reg)
    m = re.match(re_jnz, inst)
    if m:
        x, y = m.groups(0)
        y = int(y)
        try:
            x = int(x)
        except:
            pass
        g.jnz(x, y)
    m = re.match(re_inc, inst)
    if m:
        reg = m.groups(0)[0]
        g.inc(reg)
    m = re.match(re_dec, inst)
    if m:
        reg = m.groups(0)[0]
        g.dec(reg)



