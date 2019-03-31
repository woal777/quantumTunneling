try:
    from tunneling import solve
except ImportError:
    import tunneling.solve

from tunneling import analytic
from cmath import exp, sqrt, sinh, pi, log
import matplotlib.pyplot as plt
import numpy as np

c = 3e+8  # m/s
m0 = 0.5109989461e+6 / (c ** 2)  # ev / c ** 2
h_ = 6.582119514e-16  # ev s
e = 1.602e-19  # C


def di(thickness, v, p1, p2, mr):
    m = mr * m0
    C = - (4 * e * m) / (9 * pi ** 2 * h_ ** 3)
    alpha = (4 * thickness * (2 * m) ** .5) / (3 * h_ * (p1 + v - p2))
    term_sinh: complex = 1.5 * alpha * (sqrt(p2 - v / 2) - sqrt(p1 + v / 2)) * v / 2
    term_exp: complex = alpha * (sqrt(p2 - v / 2) ** 3 - sqrt(p1 + v / 2) ** 3)
    term_reciprocal: complex = (alpha ** 2 * (sqrt(p2 - v / 2) - sqrt(p1 + v / 2)) ** 2)
    return (C * exp(term_exp) * sinh(term_sinh) / term_reciprocal).real


def fn(thickness, v, p1, p2, mr):
    E = v / thickness + (p2 - p1) / thickness
    C = 2.2 * e / (16 * pi ** 2 * h_)
    p = p2
    if v > 0:
        C = C
    else:
        C = -C
    try:
        return (exp(log(C * E ** 2 / p) - 4 * (2 * m0 * mr) ** 0.5 * p ** 1.5 / (3 * h_ * E))).real
    except OverflowError:
        print((3 * h_ * e * E), v)
        return 0


if __name__ == "__main__":
    fig = plt.figure()
    d = 4.8e-9  # m
    # area = 10e-9 * 2 * pi * 1e+6
    start = -.31
    end = -start
    area = 0.5 * 1.3 * 0.5 * 1.5 * 1e-12 * 1e+6
    # up
    eff_m = 0.13
    fig.add_subplot(221)
    s = solve.SolvingProblem(d, area, 0.24, 1.52, eff_m)
    s.set_temperature(300)
    arr = np.genfromtxt('2009_raw_down')
    x, y = arr[:,0], arr[:,1]
    plt.plot(x, y)
    x, y = s.main(start, end)
    plt.plot(x, y, 'g')
    fig.add_subplot(223)
    plt.plot(x, y)

    # down
    fig.add_subplot(222)
    s = solve.SolvingProblem(d, area, 0.48, .96, eff_m)
    s.set_temperature(300)
    arr = np.genfromtxt('2009_raw_up')
    x, y = arr[:,0], arr[:,1]
    plt.plot(x, y)
    x, y = s.main(start, end)
    plt.plot(x, y, 'g')
    fig.add_subplot(223)
    plt.plot(x, y)
    plt.show()

'''
    # up
    x = np.linspace(start, end, 30)
    y = np.array([di(d, v, 0.24, 1.52, eff_m) * area for v in x])
    fig.add_subplot(221)
    plt.plot(-x, -y)
    fig.add_subplot(224)
    plt.plot(-x, -y)

    # down
    x = np.linspace(start, end, 30)
    y = np.array([di(d, v, .48, .96, eff_m) * area for v in x])
    fig.add_subplot(222)
    plt.plot(-x, -y)
    fig.add_subplot(224)
    plt.plot(-x, -y)
'''