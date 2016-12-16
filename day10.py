import re


class Actor():
    def receive(self, val):
        pass


class Bot(Actor):
    def __init__(self, key, high=None, low=None):
        self.set_high(high)
        self.set_low(low)
        self.key = key
        self.vals = []

    def receive(self, val):
        self.vals.append(val)
        if len(self.vals) == 2 and self.high and self.low:
            self.high.receive(max(self.vals))
            self.low.receive(min(self.vals))
            print(self.key, sorted(self.vals))
            self.vals = []

    def set_high(self, high):
        assert high is None or isinstance(high, Actor)
        self.high = high

    def set_low(self, low):
        assert low is None or isinstance(low, Actor)
        self.low = low


class Output(Actor):
    def __init__(self, key):
        self.vals = []
        self.key = key

    def receive(self, val):
        self.vals.append(val)


bots = {}
outputs = {}
with open('day10input.txt', 'r') as f:
    for l in sorted(f.readlines()):
        m = re.match(r"value (.*) goes to bot (.*)", l.strip())
        if m:
            val, key = m.groups()
            ret = bots[key].receive(int(val))
            if ret:
                print(key, ret)
        m = re.match(r"bot (.*) gives low to (.*) (.*) and high to bot (.*)", l.strip())
        if m:
            b1, bo, a2, b3 = m.groups()
            if b3 not in bots:
                bots[b3] = Bot(b3)
            if bo == 'bot':
                if a2 not in bots:
                    bots[a2] = Bot(a2)
            else:
                if a2 not in outputs:
                    outputs[a2] = Output(a2)
            if b1 in bots:
                if bo == 'bot':
                    bots[b1].set_low(bots[a2])
                else:
                    bots[b1].set_low(outputs[a2])
                bots[b1].set_high(bots[b3])
            else:
                if b3 not in bots:
                    bots[b3] = Bot(b3)
                if a2 not in bots:
                    bots[a2] = Bot(a2)
                bots[b1] = Bot(b1, bots[b3], bots[a2])
