def is_possible(sides):
    assert isinstance(sides, list) or isinstance(sides, tuple)
    x, y, z = sides
    if x + y <= z or x + z <= y or y + z <= x:
        return False
    return True


with open('day3input.txt', 'r') as f:
    lengths = []
    for l in f.readlines():
        lengths.append((int(l[0:5]), int(l[5:10]), int(l[10:15])))

triangles = []
for i in range(len(lengths)//3):
    triangles.extend(list(zip(*lengths[3*i:3*(i+1)])))

print(len([t for t in triangles if is_possible(t)]))
