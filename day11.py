from enum import Enum
from typing import Iterable
from functools import reduce
import itertools

class GameObj:

    def __init__(self, type):
        self.type = type


class Direction(Enum):
    UP = 1
    DOWN = -1


class Generator(GameObj):

    def __eq__(self, other):
        return isinstance(other, Generator) and self.type == other.type

    def __str__(self):
        return '<Generator type="{}">'.format(self.type)

    def __hash__(self):
        return hash('Generator ' + self.type)


class Microchip(GameObj):

    def __eq__(self, other):
        return isinstance(other, Microchip) and self.type == other.type

    def __str__(self):
        return '<Microchip type="{}">'.format(self.type)

    def __hash__(self):
        return hash('Microchip ' + self.type)


class InvalidFloorException(Exception):
    pass


class InvalidGameException(Exception):
    pass


class InvalidGameMoveException(Exception):
    pass


class GameFloor:
    def __init__(self, chips: Iterable[Microchip], gens: Iterable[Generator]):
        self.chips = set(chips)
        self.gens = set(gens)
        if not self.is_valid():
            raise InvalidFloorException

    def __str__(self):
        return str({'microchips': [str(c) for c in self.chips], 'generators': [str(g) for g in self.gens]})

    def __hash__(self):
        return hash(self.items)

    @property
    def items(self):
        return frozenset(list(self.chips) + list(self.gens))

    def is_valid(self) -> bool:
        gen_types = [g.type for g in self.gens]
        for chip in self.chips:
            if self.gens and chip.type not in gen_types:
                return False
        return True

    def remove(self, obj: GameObj):
        assert isinstance(obj, GameObj)
        if isinstance(obj, Generator):
            gens = [g for g in self.gens if obj.type != g.type]
            chips = self.chips
        elif isinstance(obj, Microchip):
            chips = [c for c in self.chips if obj.type != c.type]
            gens = self.gens
        return GameFloor(chips, gens)

    def add(self, obj: GameObj):
        assert isinstance(obj, GameObj)
        if isinstance(obj, Generator):
            gens = list(self.gens) + [obj, ]
            chips = self.chips
        elif isinstance(obj, Microchip):
            chips = list(self.chips) + [obj, ]
            gens = self.gens
        return GameFloor(chips, gens)

    def is_empty(self) -> bool:
        return not (self.chips or self.gens)


class Game:
    def __init__(self, floors: Iterable[GameFloor], elevator_floor=0):
        self.floors = floors
        self.elevator_floor = elevator_floor
        if not self.is_valid():
            raise InvalidGameException

    def __eq__(self, other):
        return self.floors == other.floors and self.elevator_floor == other.elevator_floor

    def __hash__(self):
        return hash(frozenset(list(hash(floor) for floor in self.floors) + [self.elevator_floor]))

    def __str__(self):
        sarr = []
        for i, floor in enumerate(self.floors):
            s = str(floor)
            if i == self.elevator_floor:
                s += ' elevator'
            sarr.append(s)
        return "\n".join(sarr[::-1])

    def is_valid(self) -> bool:
        return all([floor.is_valid() for floor in self.floors])

    def move(self, items: Iterable[GameObj], direction: Direction):
        from_floor = self.elevator_floor
        if len(items) > 2 or (from_floor == len(self.floors) - 1 and direction == Direction.UP) or (
                from_floor == 0 and direction == Direction.DOWN):
            raise InvalidGameMoveException
        try:
            GameFloor([c for c in items if isinstance(c, Microchip)],
                      [g for g in items if isinstance(g, Generator)])
            to_floor = from_floor + 1 if direction == Direction.UP else from_floor - 1
            new_floors = []
            for i, floor in enumerate(self.floors):
                for item in items:
                    floor = floor.remove(item) if i == from_floor else floor
                    floor = floor.add(item) if i == to_floor else floor
                new_floors.append(floor)
            return Game(new_floors, to_floor)
        except InvalidFloorException:
            raise InvalidGameMoveException

    def is_solution(self) -> bool:
        return all([f.is_empty() for f in self.floors[:-1]])

    def transitions(self):
        trans = []
        floor = self.floors[self.elevator_floor]
        for direction in [Direction.UP, Direction.DOWN]:
            for item_set in itertools.combinations(list(floor.items) + [None, ], 2):
                item_set = [item for item in item_set if item]
                try:
                    trans.append(self.move(item_set, direction))
                except InvalidGameMoveException:
                    pass
        return trans

    def equivalent_games(self):
        games = [self,]
        types = list(set([i.type for floor in self.floors for i in floor.items]))
        perms = list(itertools.permutations(types, len(types)))[1:]
        dicts = []
        for p in perms:
            dict = {}
            for i in range(len(types)):
                dict[types[i]] = p[i]
            dicts.append(dict)
        for d in dicts:
            new_floors = []
            for floor in self.floors:
                chips = [Microchip(d[c.type]) for c in floor.chips]
                gens = [Generator(d[g.type]) for g in floor.gens]
                new_floors.append(GameFloor(chips, gens))
            games.append(Game(new_floors, self.elevator_floor))
        return games

with open('day11input.txt', 'r') as f:
    floors = []
    for l in f.readlines():
        l = l.strip().replace(',', '').replace('.', '').split(' a ')
        print(l)
        if len(l) == 1:
            floors.append(GameFloor([], []))
        else:
            gens, chips = [], []
            for item in l[1:]:
                pos = item.find(' gen')
                if pos > 0:
                    class_name = item[:pos]
                    gens.append(Generator(class_name))
                pos = item.find('-comp')
                if pos > 0:
                    class_name = item[:pos]
                    chips.append(Microchip(class_name))
            floors.append(GameFloor(chips, gens))

moves = 0
games = [Game(floors), ]
cached_games = set()
while not any([g.is_solution() for g in games]):
    cached_games = set(list(cached_games) + [hash(g) for g in games])
    print(games[0])
    new_games = []
    for g in games:
        cached_games = set(list(cached_games) + [hash(e) for e in g.equivalent_games()])
        new_games += [game for game in g.transitions() if hash(game) not in cached_games]
    games = new_games
    moves += 1
    print('moves: {}, games: {}'.format(moves, len(games)))
