from my_utility_module import isclose


def bigger_or_equal(the_big, the_small, rel_tol=1e-01, abs_tol=0.0):
    c = isclose(the_big, the_small, abs_tol=abs_tol)
    return c or the_big > the_small


def is_between(x, x1, x2, abs_tol=0.0):
    a1 = x1
    a2 = x2
    if bigger_or_equal(x1, x2, abs_tol=abs_tol):
        a1 = x2
        a2 = x1

    c1 = bigger_or_equal(x, a1, abs_tol=abs_tol)
    c2 = bigger_or_equal(a2, x, abs_tol=abs_tol)
    return c1 and c2


