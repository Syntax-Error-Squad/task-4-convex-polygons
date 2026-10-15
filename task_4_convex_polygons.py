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
        """Умножает число на вектор.

        Parameters
        ----------
        other : int or float
            Числовой множитель.

        Returns
        -------
        Vector
            Вектор с координатами, умноженными на число.
        """
        return self * other

    def cross_z(self, other):
        """Вычисляет ориентированную длину векторного произведения вдоль оси Z.

        Parameters
        ----------
        other : Vector
            Второй вектор.

        Returns
        -------
        int or float
            Компонента векторного произведения по оси Z. Модуль значения
            равен длине результирующего вектора, а знак задаёт его направление
            вдоль оси Z.
        """
        if not isinstance(other, Vector):
            raise TypeError("other должен быть Vector")
        return self.x * other.y - self.y * other.x


class ConvexPolygon:
    """Представляет выпуклый многоугольник на плоскости."""

    def __init__(self, vertices):
        """Создаёт выпуклый многоугольник из списка вершин.

        Parameters
        ----------
        vertices : list of Point
            Вершины в порядке обхода по часовой стрелке.

        Raises
        ------
        ValueError
            Если из переданных вершин нельзя создать выпуклый многоугольник.
        """
        if not self.is_convex(vertices):
            raise ValueError("Невозможно создать выпуклый многоугольник")

        self.vertices = tuple(vertices)

    @staticmethod
    def is_convex(vertices):
        """Проверяет возможность построения выпуклого многоугольника.

        Parameters
        ----------
        vertices : list of Point
            Проверяемые вершины.

        Returns
        -------
        bool
            False, если вершин меньше трёх, иначе True.
        """
        if len(vertices) < 3:  # noqa: SIM103
            return False

        # Проверка выпуклости (реализация)
        return True

    def perimeter(self):
        """Вычисляет периметр многоугольника.

        Returns
        -------
        float
            Сумма длин всех сторон многоугольника.
        """
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
        """Разбивает выпуклый многоугольник на треугольники.

        Returns
        -------
        list of tuple of Point
            Треугольники в виде троек вершин.
        """
        first = self.vertices[0]

        # Выбираем первую вершину и делим многоугольник на треугольники
        # последовательным обходом.
        return [
            (first, self.vertices[i], self.vertices[i + 1])
            for i in range(1, len(self.vertices) - 1)
        ]

    def area(self):
        """Вычисляет площадь многоугольника через площади треугольников.

        Returns
        -------
        int or float
            Площадь многоугольника.
        """
        # Выбираем треугольники, полученные из triangulate, и считаем их площадь
        # с помощью векторного произведения, далее складываем площади.
        return sum(
            abs((b - a).cross_z(c - a)) / 2
            for a, b, c in self.triangulate()
        )

    @staticmethod
    def _is_inside(point, a, b):
        """Проверяет положение точки относительно ориентированной стороны.

        Parameters
        ----------
        point : Point
            Проверяемая точка.
        a : Point
            Начало стороны.
        b : Point
            Конец стороны.

        Returns
        -------
        bool
            True, если точка лежит справа от стороны или на ней.
        """
        # Направление обхода по часовой стрелке, поэтому знак неположительный, если точка находится внутри
        return (b - a).cross_z(point - a) <= 0

    def contains(self, point):
        """Проверяет принадлежность точки многоугольнику.

        Parameters
        ----------
        point : Point
            Проверяемая точка.

        Returns
        -------
        bool
            True, если точка находится внутри или на границе многоугольника.
        """
        vertices_count = len(self.vertices)

        for i in range(vertices_count):
            a = self.vertices[i]
            b = self.vertices[(i + 1) % vertices_count]

            if not self._is_inside(point, a, b):
                return False

        return True

    @staticmethod
    def _line_intersection(a1, b1, a2, b2):
        """Находит точку пересечения двух прямых.

        Parameters
        ----------
        a1, b1 : Point
            Две точки первой прямой.
        a2, b2 : Point
            Две точки второй прямой.

        Returns
        -------
        Point
            Точка пересечения прямых.

        Raises
        ------
        ValueError
            Если прямые параллельны.
        """
        d1 = b1 - a1
        d2 = b2 - a2

        if d1.cross_z(d2) == 0:
            raise ValueError("Прямые, построенные по точкам, параллельны")

        # https://cp-algorithms.com/geometry/basic-geometry.html#exercises
        t = (a2 - a1).cross_z(d2) / d1.cross_z(d2)
        return a1 + d1 * t

    @staticmethod
    def _clip(vertices, a, b):
        """Отсекает многоугольник ориентированной прямой.

        Parameters
        ----------
        vertices : list of Point
            Вершины отсекаемого многоугольника.
        a : Point
            Начало отсекающей стороны.
        b : Point
            Конец отсекающей стороны.

        Returns
        -------
        list of Point
            Вершины части многоугольника справа от прямой или на ней.
        """
        clipped = []

        previous = vertices[-1]
        previous_inside = ConvexPolygon._is_inside(previous, a, b)

        for current in vertices:
            current_inside = ConvexPolygon._is_inside(current, a, b)

            if previous_inside != current_inside:
                clipped.append(
                    ConvexPolygon._line_intersection(previous, current, a, b)
                )

            if current_inside:
                clipped.append(current)

            previous = current
            previous_inside = current_inside

        return clipped

    def intersection(self, other):
        """Вычисляет пересечение двух выпуклых многоугольников.

        Parameters
        ----------
        other : ConvexPolygon
            Второй многоугольник.

        Returns
        -------
        ConvexPolygon or None
            Пересечение многоугольников или None, если не удалось пересечь.
        """

        # Ссылка на описание алгоритма:
        # https://www.geeksforgeeks.org/dsa/polygon-clipping-sutherland-hodgman-algorithm/
        vertices = list(self.vertices)
        other_vertices_count = len(other.vertices)

        for i in range(other_vertices_count):
            a = other.vertices[i]
            b = other.vertices[(i + 1) % other_vertices_count]

            vertices = self._clip(vertices, a, b)

            if len(vertices) < 3:
                return None

        return ConvexPolygon(vertices)


def run_tests():
    """Запускает основные проверки классов точки, вектора и многоугольника."""
    def show_result(name, result, expected):
        print(f"{name}: результат = {result}, ожидается = {expected}")

    def point_coordinates(point):
        return point.x, point.y

    triangle = ConvexPolygon([
        Point(0, 0),
        Point(0, 3),
        Point(4, 0),
    ])

    show_result("Периметр треугольника", triangle.perimeter(), 12)
    show_result("Площадь треугольника", triangle.area(), 6)
    show_result("Количество треугольников", len(triangle.triangulate()), 1)
    show_result("Точка (1, 1) внутри", triangle.contains(Point(1, 1)), True)
    show_result("Точка (4, 4) внутри", triangle.contains(Point(4, 4)), False)

    pentagon = ConvexPolygon([
        Point(0, 0),
        Point(0, 2),
        Point(2, 4),
        Point(4, 2),
        Point(4, 0),
    ])
    pentagon_triangles = [
        [point_coordinates(point) for point in triangle]
        for triangle in pentagon.triangulate()
    ]
    expected_triangles = [
        [(0, 0), (0, 2), (2, 4)],
        [(0, 0), (2, 4), (4, 2)],
        [(0, 0), (4, 2), (4, 0)],
    ]
    show_result("Триангуляция пятиугольника", pentagon_triangles,
                expected_triangles)

    first = ConvexPolygon([
        Point(0, 0),
        Point(0, 3),
        Point(3, 3),
        Point(3, 0),
    ])
    second = ConvexPolygon([
        Point(2, 1),
        Point(2, 4),
        Point(4, 4),
        Point(4, 1),
    ])

    intersection = first.intersection(second)
    show_result("Пересечение существует", intersection is not None, True)

    if intersection is not None:
        intersection_points = [
            point_coordinates(point) for point in intersection.vertices
        ]
        expected_points = [
            (2, 1),
            (2, 3),
            (3, 3),
            (3, 1),
        ]
        show_result("Вершины пересечения", intersection_points,
                    expected_points)
        show_result("Площадь пересечения", intersection.area(), 2)
        show_result("Периметр пересечения", intersection.perimeter(), 6)


if __name__ == "__main__":
    run_tests()
