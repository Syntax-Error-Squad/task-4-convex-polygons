import math
from numbers import Real

EPS = 1e-9


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

    def __repr__(self):
        """Возвращает строковое представление точки."""
        return f"Point({self.x}, {self.y})"

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
            Вершины в порядке обхода по часовой или против часовой стрелки.

        Raises
        ------
        ValueError
            Если из переданных вершин нельзя создать выпуклый многоугольник.
        """
        vertices = list(vertices)
        if not self.is_convex(vertices):
            raise ValueError("Невозможно создать выпуклый многоугольник")

        # Остальные методы рассчитаны на обход по часовой стрелке,
        # поэтому вершины, заданные против часовой, разворачиваются.
        if self._signed_area(vertices) > 0:
            vertices.reverse()

        self.vertices = tuple(vertices)

    @staticmethod
    def _signed_area(vertices):
        """Вычисляет ориентированную площадь многоугольника.

        Parameters
        ----------
        vertices : list of Point
            Вершины многоугольника.

        Returns
        -------
        float
            Положительное значение при обходе против часовой стрелки,
            отрицательное при обходе по часовой.
        """
        first = vertices[0]
        return sum(
            (vertices[i] - first).cross_z(vertices[i + 1] - first)
            for i in range(1, len(vertices) - 1)
        ) / 2

    @staticmethod
    def _segments_cross(a1, a2, b1, b2):
        """Проверяет, пересекаются ли два отрезка во внутренней точке.

        Касание концами и наложение отрезков на одной прямой
        пересечением не считаются.

        Parameters
        ----------
        a1, a2 : Point
            Концы первого отрезка.
        b1, b2 : Point
            Концы второго отрезка.

        Returns
        -------
        bool
            True, если отрезки пересекаются.
        """
        d1 = (a2 - a1).cross_z(b1 - a1)
        d2 = (a2 - a1).cross_z(b2 - a1)
        d3 = (b2 - b1).cross_z(a1 - b1)
        d4 = (b2 - b1).cross_z(a2 - b1)

        # Отрезки пересекаются, если концы каждого лежат строго
        # по разные стороны от прямой, содержащей другой.
        a_splits_b = (d1 > EPS and d2 < -EPS) or (d1 < -EPS and d2 > EPS)
        b_splits_a = (d3 > EPS and d4 < -EPS) or (d3 < -EPS and d4 > EPS)
        return a_splits_b and b_splits_a

    @staticmethod
    def is_convex(vertices):
        """Проверяет, задают ли вершины выпуклый многоугольник.

        Многоугольник выпуклый, если:
        1. все ненулевые повороты имеют одинаковое направление
           (все по часовой стрелке или все против);
        2. хотя бы один поворот ненулевой, то есть вершины
           не лежат на одной прямой;
        3. никакие несмежные стороны не пересекаются.

        Parameters
        ----------
        vertices : list of Point
            Вершины в порядке обхода по часовой или против часовой стрелки.

        Returns
        -------
        bool
            True, если вершины задают выпуклый многоугольник.
        """
        n = len(vertices)
        if n < 3:
            return False

        # 1-2. Все повороты в одну сторону и хотя бы один ненулевой.
        sign = None
        for i in range(n):
            p1 = vertices[i]
            p2 = vertices[(i + 1) % n]
            p3 = vertices[(i + 2) % n]

            cross = (p2 - p1).cross_z(p3 - p2)
            if abs(cross) < EPS:
                continue

            current_positive = cross > 0
            if sign is None:
                sign = current_positive
            elif current_positive != sign:
                return False

        if sign is None:
            return False

        # 3. Несмежные стороны не пересекаются (отсекает звёзды).
        for i in range(n):
            a1 = vertices[i]
            a2 = vertices[(i + 1) % n]

            for j in range(i + 2, n):
                if (j + 1) % n == i:
                    continue

                b1 = vertices[j]
                b2 = vertices[(j + 1) % n]

                if ConvexPolygon._segments_cross(a1, a2, b1, b2):
                    return False

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
        # Вершины хранятся по часовой стрелке, поэтому для точки внутри
        # знак векторного произведения неположительный.
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

        if abs(d1.cross_z(d2)) < EPS:
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

        try:
            return ConvexPolygon(vertices)
        except ValueError:
            return None


def run_tests():
    """Запускает основные проверки классов точки, вектора и многоугольника."""
    def show_result(name, result, expected):
        print(f"{name}: результат = {result}, ожидается = {expected}")

    def point_coordinates(point):
        return point.x, point.y

    print("Проверка is_convex")
    print()
    good_triangle = [Point(0,0), Point(0,3), Point(4,0)]
    print(f"Правильный треугольник: {ConvexPolygon.is_convex(good_triangle)}, ожидается: True")
    ccw_triangle = [Point(0,0), Point(4,0), Point(0,3)]
    print(f"Против часовой стрелки: {ConvexPolygon.is_convex(ccw_triangle)}, ожидается: True")
    star_trek_badge = [Point(0,0), Point(0,4), Point(1,2), Point(4,0)]
    print(f"Невыпуклая фигура: {ConvexPolygon.is_convex(star_trek_badge)}, ожидается: False")
    too_short = [Point(0,0), Point(1,1)]
    print(f"Меньше 3 вершин: {ConvexPolygon.is_convex(too_short)}, ожидается: False")
    collinear = [Point(0,0), Point(1,1), Point(2,2)]
    print(f"Точки на одной прямой: {ConvexPolygon.is_convex(collinear)}, ожидается: False")
    asymmetric_star = [Point(0,0), Point(2,3), Point(4,0), Point(2,0), Point(4,2)]
    print(f"Звезда (самопересечение): {ConvexPolygon.is_convex(asymmetric_star)}, ожидается: False")
    print()

    ccw_square = ConvexPolygon([Point(0,0), Point(2,0), Point(2,2), Point(0,2)])
    show_result("Квадрат против часовой: точка (1, 1) внутри",
                ccw_square.contains(Point(1, 1)), True)
    show_result("Квадрат против часовой: площадь", ccw_square.area(), 4)
    print()
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
