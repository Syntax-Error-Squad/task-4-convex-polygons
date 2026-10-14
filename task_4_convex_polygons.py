class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

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
