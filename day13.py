class Node:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Edge:
    def __init__(self, node_1, node_2):
        self.nodes = frozenset([node_1, node_2])


class Map:

    def __init__(self):
        self.nodes = set()
        self.edges = set()

    def add_node(self, node):
        self.nodes.add(node)

    def add_edge(self, edge):
        self.edges.add(edge)

    def get_edges(self, node):
        if node not in self.nodes:
            raise IndexError('{} not in map nodes'.format(node))
        return frozenset([e.nodes for e in self.edges if node in e.nodes])

    def get_neighbors(self, node):
        node_set = set()
        for edge in self.get_edges(node):
            for n in edge:
                node_set.add(n)
        node_set.remove(node)
        return node_set

    def get_node(self, x, y):
        try:
            return [node for node in self.nodes if node.x == x and node.y == y][0]
        except:
            return None

    @staticmethod
    def heuristic_cost_estimate(neighbor, goal):
        return abs(neighbor.x - goal.x) + abs(neighbor.y - goal.y)


class Game:
    def __init__(self, start_node, end_node, map):
        self.map = map
        self.start_node = start_node
        self.end_node = end_node


def a_star(graph, start_node, goal_node):
    closed_set = set()
    open_set = set([start_node])
    came_from = {}

    g_score = dict([(node, 100000) for node in graph.nodes])
    g_score[start_node] = 0
    f_score = dict([(node, 100000) for node in graph.nodes])
    f_score[start_node] = Map.heuristic_cost_estimate(start_node, goal_node)

    while len(open_set) > 0:
        current = min(open_set, key=(lambda key: f_score[key]))
        if current == goal_node:
            return reconstruct_path(came_from, current)

        open_set.remove(current)
        closed_set.add(current)
        for neighbor in graph.get_neighbors(current):
            if neighbor in closed_set:
                continue
            tentative_g_score = g_score[current] + 1
            if neighbor not in open_set:
                open_set.add(neighbor)
            elif tentative_g_score >= g_score[neighbor]:
                continue

            came_from[neighbor] = current
            g_score[neighbor] = tentative_g_score
            f_score[neighbor] = g_score[neighbor] + Map.heuristic_cost_estimate(neighbor, goal_node)

    return -1


def reconstruct_path(came_from, current):
    total_path = [current]
    while current in came_from.keys():
        current = came_from[current]
        total_path.append(current)
    return total_path


def is_open(node, dnum):
    x, y = node.x, node.y
    n = ((x * x) + (3 * x) + (2 * x * y) + y + (y * y)) + dnum
    return sum(int(i) for i in "{0:b}".format(n)) % 2 == 0

def build_game(width, height, dnum, start_tuple, goal_tuple):
    m = Map()
    grid = {}
    for y in range(height):
        grid[y] = {}
        for x in range(width):
            n = Node(x, y)
            if is_open(n, dnum):
                grid[y][x] = n
                m.add_node(n)

    for y in range(height):
        for x in range(width):
            if not (y in grid and x in grid[y]):
                continue
            if y-1 in grid:
                if x in grid[y-1]:
                    m.add_edge(Edge(grid[y][x], grid[y-1][x]))
            if y+1 in grid:
                if x in grid[y+1]:
                    m.add_edge(Edge(grid[y][x], grid[y+1][x]))
            if x-1 in grid[y]:
                m.add_edge(Edge(grid[y][x], grid[y][x-1]))
            if x+1 in grid[y]:
                m.add_edge(Edge(grid[y][x], grid[y][x+1]))
    sx, sy = start_tuple
    gx, gy = goal_tuple
    return Game(m.get_node(sx, sy), m.get_node(gx, gy), m)

g = build_game(10, 10, 10, (1, 1), (7, 4))
a = a_star(g.map, g.start_node, g.end_node)
print(a)
print(len(a)-1)

g2 = build_game(1000,1000,1350, (1, 1), (31, 39))
a2 = a_star(g2.map, g2.start_node, g2.end_node)
print(a2)
print(len(a2)-1)