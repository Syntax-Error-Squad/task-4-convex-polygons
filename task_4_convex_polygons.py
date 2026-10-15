import math
from numbers import Real


class Point:
    """Представляет точку на плоскости."""

    def __init__(self, x, y):
        """Создаёт точку с заданными координатами.

        Parameters
        ----------
        x : int or float
            Координата точки по оси X.
        y : int or float
            Координата точки по оси Y.
        """
        self.x = x
        self.y = y

    def __sub__(self, other):
        """Вычитает одну точку из другой.

        Parameters
        ----------
        other : Point
            Вычитаемая точка.

        Returns
        -------
        Vector
            Вектор, направленный от other к текущей точке.
        """
        if not isinstance(other, Point):
            return NotImplemented
        return Vector(self.x - other.x, self.y - other.y)

    def __add__(self, vector):
        """Перемещает точку на заданный вектор.

        Parameters
        ----------
        vector : Vector
            Вектор перемещения.

        Returns
        -------
        Point
            Новая точка, полученная после перемещения.
        """
        if not isinstance(vector, Vector):
            return NotImplemented
        return Point(self.x + vector.x, self.y + vector.y)


class Vector:
    """Представляет вектор на плоскости."""

    def __init__(self, x, y):
        """Создаёт вектор с заданными координатами.

        Parameters
        ----------
        x : int or float
            Координата вектора по оси X.
        y : int or float
            Координата вектора по оси Y.
        """
        self.x = x
        self.y = y

    def length(self):
        """Вычисляет длину вектора.

        Returns
        -------
        float
            Евклидова длина вектора.
        """
        return math.hypot(self.x, self.y)

    def __add__(self, other):
        """Складывает два вектора.

        Parameters
        ----------
        other : Vector
            Второе слагаемое.

        Returns
        -------
        Vector
            Сумма векторов.
        """
        if not isinstance(other, Vector):
            return NotImplemented
        return Vector(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        """Вычитает один вектор из другого.

        Parameters
        ----------
        other : Vector
            Вычитаемый вектор.

        Returns
        -------
        Vector
            Разность векторов.
        """
        if not isinstance(other, Vector):
            return NotImplemented
        return Vector(self.x - other.x, self.y - other.y)

    def __mul__(self, other):
        """Умножает вектор на число или вычисляет скалярное произведение.

        Parameters
        ----------
        other : int, float or Vector
            Числовой множитель или второй вектор.

        Returns
        -------
        Vector or int or float
            Вектор при умножении на число либо скалярное произведение
            при умножении на другой вектор.
        """
        if isinstance(other, Vector):
            return self.x * other.x + self.y * other.y
        if isinstance(other, Real):
            return Vector(self.x * other, self.y * other)
        return NotImplemented

    def __rmul__(self, other):
        return self * other

    def cross(self, other):
        """Вычисляет векторное произведение двух векторов на плоскости.

        Parameters
        ----------
        other : Vector
            Второй вектор.

        Returns
        -------
        int or float
            Псевдоскалярное произведение векторов. Его знак определяет
            направление поворота от текущего вектора к вектору other.
        """
        if not isinstance(other, Vector):
            raise TypeError("other должен быть Vector")
        return self.x * other.y - self.y * other.x


class ConvexPolygon:
    """Представляет выпуклый многоугольник на плоскости."""

    def __init__(self, vertices):
        if not self.is_convex(vertices):
            raise ValueError("Невозможно создать выпуклый многоугольник")

        self.vertices = tuple(vertices)

    @staticmethod
    def is_convex(vertices):
        if len(vertices) < 3:  # noqa: SIM103
            return False

        # Проверка выпуклости будет добавлена позже.
        return True

    def perimeter(self):
        perimeter = 0
        vertices_count = len(self.vertices)

        for i in range(vertices_count):
            current_point = self.vertices[i]
            next_point = self.vertices[(i + 1) % vertices_count]

            # Разность соседних точек задаёт вектор стороны.
            # Для последней точки следующей становится первая, замыкая контур.
            perimeter += (next_point - current_point).length()

        return perimeter

    def triangulate(self):
        ...

    def area(self):
        ...

    def contains(self, point):
        ...

    def intersection(self, other):
        ...
