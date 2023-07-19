from math import fabs, isinf


def get_from_set(s):
    if len(s) == 0:
        return None
    for e in s:
        return e


def get_n_from_set(n, s):
    if len(s) == 0:
        return None
    l = []
    for e in s:
        l.append(e)
        if len(l) == n:
            return l



def isclose(a, b,abs_tol=0.001):
    return fabs(b - a) <= abs_tol


def same_space(segment_1, segment_2, threshold):
    p_1_1 = segment_1[0]
    p_1_2 = segment_1[1]
    p_2_1 = segment_2[0]
    p_2_2 = segment_2[1]

    if p_1_1.xe > p_2_1.xe + threshold and p_1_2.xe > p_2_1.xe + threshold and p_1_1.xe > p_2_2.xe + threshold and p_1_2.xe > p_2_2.xe + threshold:
        return False

    if p_1_1.xe < p_2_1.xe - threshold and p_1_2.xe < p_2_1.xe - threshold and p_1_1.xe < p_2_2.xe - threshold and p_1_2.xe < p_2_2.xe - threshold:
        return False

    if p_1_1.ye > p_2_1.ye + threshold and p_1_2.ye > p_2_1.ye + threshold and p_1_1.ye > p_2_2.ye + threshold and p_1_2.ye > p_2_2.ye + threshold:
        return False

    if p_1_1.ye < p_2_1.ye - threshold and p_1_2.ye < p_2_1.ye - threshold and p_1_1.ye < p_2_2.ye - threshold and p_1_2.ye < p_2_2.ye - threshold:
        return False

    return True

def same_space_point(segment_1, point, threshold):
    p_1_1 = segment_1[0]
    p_1_2 = segment_1[1]

    if p_1_1.xe > point.xe + threshold and p_1_2.xe > point.xe + threshold:
        return False

    if p_1_1.xe < point.xe - threshold and p_1_2.xe < point.xe - threshold:
        return False

    if p_1_1.ye > point.ye + threshold and p_1_2.ye > point.ye + threshold:
        return False

    if p_1_1.ye < point.ye - threshold and p_1_2.ye < point.ye - threshold:
        return False

    return True
