class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __sub__(self, other):
        ...

    def __add__(self, vector):
        ...


class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def length(self):
        ...

    def __add__(self, other):
        ...

    def __sub__(self, other):
        ...

    def __mul__(self, other):
        ...

    def cross(self, other):
        ...


class ConvexPolygon:
    def __init__(self, vertices):
        self.vertices = vertices

    def is_convex(self):
        ...

    def area(self):
        ...

    def perimeter(self):
        ...

    def contains(self, point):
        ...

    def intersection(self, other):
        ...

    def triangulate(self):
        ...
