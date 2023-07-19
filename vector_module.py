from math import fabs, acos, degrees

from point_module import Point
from data_utility_module import is_between
from my_utility_module import isclose


def closest_point_on_line_param(p, q, x):
    v1 = x - p
    v2 = q - p
    n = v1.dot(v2)
    d = v2.dot(v2)
    return n / d


def closest_point_on_line(p, q, x):
    param = closest_point_on_line_param(p, q, x)
    v = q - p
    s = v.scalar_multiply(param)
    r = p + s
    return r


def closest_point_on_segment(p, q, x):
    param = closest_point_on_line_param(p, q, x)
    if isclose(param, 0, abs_tol=1e-03) or param < 0:
        return p
    elif isclose(param, 1, abs_tol=1e-03) or param > 1:
        return q
    else:
        v = q - p
        s = v.scalar_multiply(param)
        return p + s


def point_between_points(p, q, x, tolerance):
    param = closest_point_on_line_param(p, q, x)
    return (isclose(param, 0, abs_tol=tolerance) or
            isclose(param, 1, abs_tol=tolerance) or
            0 < param < 1
            )

def point_between_points2(p, q, x, tolerance):
    return is_between(x.x,p.x,q.x,abs_tol=tolerance) and is_between(x.y,p.y,q.y,abs_tol=tolerance)

def point_line_distance2(p1, p2, p3):
    d = p1.distance(p2)
    if d == 0:
        return -1

    p = p2 - p1
    n = (p.y * p3.x) - (p.x * p3.y) + (p2.x * p1.y) - (p2.y * p1.x)
    return fabs(n) / d


def point_line_distance(p1, p2, x):
    v1 = p2 - p1
    v2 = x - p1
    n = float(v1.normL2())
    if n == 0:
        return -1
    d = v1.cross_z_magnitude(v2) / n
    return fabs(d)


def are_collinear(a1, a2, x, distance_threshold) :

    d = point_line_distance(a1, a2, x)
    if d <= distance_threshold:
        return True
    else:
        return False


def cos2vector(a, b) :
    r = a.normalize().dot(b.normalize())
    if r>1 and isclose(r,1,abs_tol=0.001):
        return 1
    if r<-1 and isclose(r,-1,abs_tol=0.001):
        return -1
    return r


def get_pi_angle_from_vector(a, b):
    return degrees(acos(cos2vector(a, b)))


def get_angle_of_vector(a, b):
    if a.cross_z_magnitude(b) > 0:
        return get_pi_angle_from_vector(a, b)
    else:
        return 360 - get_pi_angle_from_vector(a, b)


def get_angle(common_point, a, b):
    return get_angle_of_vector(a - common_point, b - common_point)

def get_angle_in_path(common_point, a, b):
    return get_angle_of_vector(a - common_point, b - common_point)


def get_intersection(point_a1, point_a2, point_b1, point_b2, line_intersection):
    x1 = point_a1.x
    x2 = point_a2.x
    x3 = point_b1.x
    x4 = point_b2.x
    y1 = point_a1.y
    y2 = point_a2.y
    y3 = point_b1.y
    y4 = point_b2.y

    e = 0.003

    denominateur = ((x1 - x2) * (y3 - y4)) - ((y1 - y2) * (x3 - x4))
    #print("denominateur",denominateur)
    if fabs(denominateur) > 5:
        if point_a1.distance(point_b1) < e or point_a1.distance(point_b2) < e or point_a2.distance(
            point_b1) < e or point_a2.distance(point_b2) < e:
            return None
        numerateur_a = (x1*y2)-(y1*x2)
        numerateur_b = (x3*y4)-(y3*x4)

        valid = True
        x=((numerateur_a *(x3-x4))-(numerateur_b)*(x1-x2))/denominateur

        precision = Point.e
        if not line_intersection:
            if not is_between(x,x1,x2,abs_tol=precision) or not is_between(x,x3,x4,abs_tol=precision):
                valid = False
        if valid:
            y = ((numerateur_a*(y3-y4))-(numerateur_b*(y1-y2)))/denominateur
        if valid and not line_intersection:
            if not is_between(y,y1,y2,abs_tol=precision) or not is_between(y,y3,y4,abs_tol=precision):
                valid = False
        if valid:
            return Point((x,y,0))
    else:
        return Point((0,0,100))
    return None


def set_point_direction(point_list):
    p1 = point_list[0]
    p2 = point_list[1]
    c = cos2vector(p1-p2,Point((1,0,0)))
    if fabs(c)>0.5:
        Point.direction=0
    else:
        Point.direction=1
