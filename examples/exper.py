try:
    from main import solve, analytic
except ImportError:
    import main.solve
    import main.analytic as analytic

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
    d = 10.e-9  # m
    # area = 10e-9 * 2 * pi * 1e+6
    area = 1e+3 * pi * 50e-6 ** 2
    start = 1.
    offset = .5
    # up
    #s = solve.SolvingProblem(d, area, .9 + offset, .95 + offset, 1)
    #s.set_temperature(10)
    #x, y = s.main(-start, start)
    x = np.linspace(-start, start)
    y = [analytic.di(d, r, .9 + offset, .95 + offset, 1) for r in x]
    plt.plot(x, y, 'g')

    # down
    #s = solve.SolvingProblem(d, area, 1.35 + offset, .5 + offset, 1)
    #s.set_temperature(10)
    #x, y = s.main(-start, start)
    x = np.linspace(-start, start)
    y = [analytic.di(d, r, .9 + offset, .95 + offset, 1) for r in x]
    plt.plot(x, y)

    plt.show()
