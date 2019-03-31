try:
    from tunneling import solve, analytic
except ImportError:
    import tunneling.solve
    import tunneling.analytic as analytic

from cmath import exp, sqrt, sinh, pi
import matplotlib.pyplot as plt
import numpy as np

c = 3e+8  # m/s
m0 = 0.5109989461e+6 / (c ** 2)  # ev / c ** 2
h_ = 6.582119514e-16  # ev s
e = 1.602e-19  # C


def di(v, p1, p2, mr):
    m = mr * m0
    C = - (4 * e * m) / (9 * pi ** 2 * h_ ** 3)
    alpha = (4 * d * (2 * m) ** .5) / (3 * h_ * (p1 + v - p2))
    term_sinh: complex = 1.5 * alpha * (sqrt(p2 - v / 2) - sqrt(p1 + v / 2)) * v / 2
    term_exp: complex = alpha * (sqrt(p2 - v / 2) ** 3 - sqrt(p1 + v / 2) ** 3)
    term_reciprocal: complex = (alpha ** 2 * (sqrt(p2 - v / 2) - sqrt(p1 + v / 2)) ** 2)
    return (C * exp(term_exp.real).real * sinh(term_sinh.real).real / term_reciprocal.real).real


def fn(v, p1, p2, mr):
    m = mr * m0
    E = - v / (e * d) + (p2 - p1) / (e * d)
    C = e ** 3 * m0 / (16 * pi ** 2 * h_ * m)
    p = p2
    if v > 0:
        C = C
    else:
        C = -C
    return (C * E ** 2 / p * exp(-4 * (2 * m) ** 0.5 * p ** 1.5 / (3 * h_ * e * E))).real


if __name__ == "__main__":
    fig = plt.figure()
    # area = 10e-9 * 2 * pi * 1e+6
    area = 1e+1 * pi * 50e-6 ** 2 * 4e+4
    start = 1.
    d = 5.e-9  # m
    diff = -1.5e-9
    mr = .8
    vlen = list(np.linspace(-1., 1., 30))
    temp = 300
    # up
    s = solve.SolvingProblem(d, area, 1.55, 1.4, mr)
    s.set_temperature(temp)
    x, y = s.main(-start, start, vlen=vlen)
    # x = np.linspace(-start, start)
    # y = [analytic.di(d, r, .9 + offset, .95 + offset, 1) for r in x]
    plt.semilogy(x, abs(y), 'g')

    # down
    s = solve.SolvingProblem(d + diff, area, 2.35, 1.35, mr)
    s.set_temperature(temp)
    x, y2 = s.main(-start, start, vlen=vlen)
    print(y[1] / y[0], y2[1] / y2[0])
    print(y[0] / y2[0], y[1] / y2[1])
    # x = np.linspace(-start, start)
    # y = [analytic.di(d, r, 1.35 + offset, .5 + offset, 1) for r in x]
    plt.semilogy(x, abs(y2))
    plt.show()
