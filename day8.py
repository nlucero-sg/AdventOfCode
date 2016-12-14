import re

class Screen:
    def __init__(self, width, height, off_fill, on_fill):
        self._width = width
        self._height = height
        self._pixels = []
        self._off_fill = off_fill
        self._on_fill = on_fill
        for y in range(height):
            self._pixels.append([off_fill for x in range(width)])

    def _set_pixel(self, x, y, value):
        self._pixels[y][x] = value

    def _get_pixel(self, x, y):
        return self._pixels[y][x]

    def __str__(self):
        s_arr = []
        for y in range(self._height):
            s_arr.append(''.join([str(self._pixels[y][x]) for x in range(self._width)]))
        return "\n".join(s_arr)

    def rect(self, x, y):
        for i in range(x):
            for j in range(y):
                self._set_pixel(i, j, self._on_fill)

    def _rotate(self, rc, a, b):
        assert rc in ('row', 'column')
        if rc == 'row':
            y = a
            b = b % self._width
            row = [self._get_pixel(x, y) for x in range(self._width)]
            new_row = row[-b:] + row[:-b]
            for x in range(self._width):
                self._set_pixel(x, y, new_row[x])
        else:
            x = a
            b = b % self._height
            col = [self._get_pixel(x, y) for y in range(self._height)]
            new_col = col[-b:] + col[:-b]
            for y in range(self._height):
                self._set_pixel(x, y, new_col[y])

    def rotate_row(self, a, b):
        return self._rotate('row', a, b)

    def rotate_col(self, a, b):
        return self._rotate('column', a, b)

    def count_pixels(self, val=None):
        if not val:
            val = self._on_fill
        c = 0
        for x in range(self._width):
            for y in range(self._height):
                if self._get_pixel(x, y) == val:
                    c += 1
        return c

    def apply_input(self, s):
        m = re.search(r"rect (\d+)x(\d+)", s)
        if m:
            x, y = m.groups()
            self.rect(int(x), int(y))
        m = re.search(r"rotate (\w+).*=(\d+) by (\d+)", s)
        if m:
            rc, a, b = m.groups()
            self._rotate(rc, int(a), int(b))


with open('day8input.txt','r') as f:
    s = Screen(50, 6, ' ', '#')
    print(s)
    print("\n")
    for l in f.readlines():
        s.apply_input(l.strip())
        print(l + "\n")
        print(s)


print("\n")

print(s.count_pixels())


