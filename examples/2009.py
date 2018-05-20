try:
    from main import solve
except ImportError:
    import main.solve

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
    d = 4.8e-9  # m
    #area = 10e-9 * 2 * pi * 1e+6
    area = 1
    # up
    fig.add_subplot(221)
    s = solve.SolvingProblem(d, area, 0.24, 1.52, 1.)
    s.set_temperature(10)
    x, y = s.main(-0.3, .3)
    plt.plot(x, y, 'g')

    # down
    fig.add_subplot(222)
    s = solve.SolvingProblem(d, area, 0.48, .96, 1.)
    s.set_temperature(10)
    x, y = s.main(-0.3, .3)
    plt.plot(x, y, 'g')

    # up
    fig.add_subplot(224)
    x = np.linspace(-.3, .3, 30)
    y = np.array([di(v, 0.24, 1.52, 1) * area for v in x])
    plt.plot(-x, -y)
    fig.add_subplot(221)
    plt.plot(-x, -y)

    # down
    fig.add_subplot(224)
    x = np.linspace(-.3, .3, 30)
    y = np.array([di(v, .48, .96, 1) * area for v in x])
    plt.plot(-x, -y)
    fig.add_subplot(222)
    plt.plot(-x, -y)

    plt.show()
