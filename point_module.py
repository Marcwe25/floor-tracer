from math import fabs

from my_utility_module import isclose


class Point(object):
    direction = 0
    e = 3
    re = 3

    def __init__(self, pos, material_id=1):
        self._x = float(pos[0])
        self._y = float(pos[1])
        self._z = float(pos[2])
        self.__material_id = material_id
        self.xe = int(self.x / Point.e)
        self.ye = int(self.y / Point.e)
        self.ze = int(self.z / Point.e)
        self.angle = None

    def same(self, other_point):
        return self.xe == other_point.xe and self.ye == other_point.ye

    # get x coordinate
    @property
    def x(self):
        return self._x

    # set x coordinate
    @x.setter
    def x(self, x):
        self._x = x
        self.xe = int(self.x / Point.e)

    # get y coordinate
    @property
    def y(self):
        return self._y

    # set y coordinate
    @y.setter
    def y(self, y):
        self._y = y
        self.ye = int(self.y / Point.e)

    # get y coordinate
    @property
    def z(self):
        return self._z

    # set y coordinate
    @z.setter
    def z(self, z):
        self._z = z
        self.ze = int(self.z / Point.e)

    # get current position
    def get_position(self):
        return self._x, self._y, self._z

    def set_position(self, new_coordinate):
        self.x = new_coordinate[0]
        self.y = new_coordinate[1]
        self.z = new_coordinate[2]

    # change x & y coordinates by p & q
    def move_by(self, p, q):
        self.x += p
        self.y += q

    # overload + operator
    def __add__(self, point_ov):
        return Point((self._x + point_ov._x, self._y + point_ov._y, self._z + point_ov._z))

    # overload - operator
    def __sub__(self, point_ov):
        return Point((self._x - point_ov._x, self._y - point_ov._y, self._z - point_ov._z))

    # overload < (less than) operator
    def __lt__(self, point_ov):
        if Point.direction == 0:
            return self.x < point_ov.x
        else:
            return self.y < point_ov.y

    # overload > (greater than) operator
    def __gt__(self, point_ov):
        if Point.direction == 0:
            return self.x > point_ov.x
        else:
            return self.y > point_ov.y

    # overload <= (less than or equal to) operator
    def __le__(self, point_ov):
        if Point.direction == 0:
            if isclose(self.x, point_ov.x, abs_tol=Point.e):
                return True
            return self.x < point_ov.x
        else:
            if isclose(self.y, point_ov.y, abs_tol=Point.e):
                return True
            return self.y < point_ov.y

    # overload >= (greater than or equal to) operator
    def __ge__(self, point_ov):
        if Point.direction == 0:
            if isclose(self.x, point_ov.x, abs_tol=Point.e):
                return True
            return self.x >= point_ov.x
        else:
            if isclose(self.y, point_ov.y, abs_tol=Point.e):
                return True
            return self.y >= point_ov.y

    def same_exact_position(self,point_other, precision=0.001):
        if isclose(self.x,point_other.x,abs_tol=precision):
            if isclose(self.y,point_other.y,precision):
                return True
        return False

    # overload == (equal to) operator
    def __eq__(self, point_other):
        if point_other is None:
            return False
        if not isinstance(point_other, Point):
            return False
        if abs(self.xe - point_other.xe) < 2:
            if abs(self.ye - point_other.ye) < 2:
                if self.distance(point_other) < self.re:
                    return True
        return False

    def __ne__(self, point_ov):
        if point_ov is None:
            return True
        if not isinstance(point_ov, Point):
            return True
        if abs(self.xe - point_ov.xe) < 2:
            if abs(self.ye - point_ov.ye) < 2:
                if self.distance(point_ov) < self.re:
                    return False
        return True

    def __hash__(self):
        return 1

    def __str__(self):
        return "[" + str(self.x) + "," + str(self.y) + "," + str(self.z) + "]"

    def __repr__(self):
        return "P3(" + str(self.x) + "," + str(self.y) + ")"

    # dot product
    def dot(self, other):
        return (self._x * other._x) + (self._y * other._y)

    # cross product
    def cross_z_magnitude(self, other):
        return (self._x * other._y) - self._y * other._x

    def normL1(self):
        return fabs(self._x) + fabs(self._y)

    def normL2(self):
        return (self._x ** 2 + self._y ** 2) ** 0.5

    def normalize(self):
        m = self.normL2()
        r = self.scalar_multiply(1 / m)
        return r

    def distance(self, other):
        #print("distance x",self._x,other._x)
        return ((other._x - self._x) ** 2 + (other._y - self._y) ** 2) ** 0.5

    def scalar_multiply(self, a):
        return Point((self._x * a, self._y * a, self._z * a))
