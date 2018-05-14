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
    a = input('2009? or 2015?\n')
    if a == '09':
        d = 4.8e-9  # m
        # up
        x = np.linspace(-.3, .3, 30)
        area = 0.5e-6 ** 2
        dimension = 1e+6
        y = [-di(v, 0.24, 1.52, 1) * area * dimension for v in x]
        plt.plot(-x, y)

        # down
        y = [-di(v, 0.48, .96, 1) * area * dimension for v in x]
        plt.plot(-x, y)
        plt.xlim((-.3, .3))
        plt.show()

    elif a == '15':
        d = 4.6e-9  # m
        start = -0.5
        end = -start
        dimension = 1e-4
        # W
        x = np.linspace(start, end, 31)
        yW = [(di(v, 0.2, 1.45, .22) + fn(v, 0.2, 1.45, .22) * .24) * dimension for v in x]

        # Co
        yC = [(di(v, 0.2, 1.67, .20) + fn(v, 0.2, 1.67, .20) * .19) * dimension for v in x]

        # Ni
        yN = [(di(v, 0.2, 2.05, .20) + fn(v, 0.2, 2.05, .20) * .14) * dimension for v in x]

        yI = [(di(v, 0.2, 2.84, .16) + fn(v, 0.2, 2.84, .16) * .07) * dimension for v in x]
        plt.plot(x, yW, x, yC, x, yN, x, yI)
        tot = np.array((x, yW, yC, yN, yI)).transpose()
        np.savetxt('15.dat', tot)
        plt.xlim((start, end))
        plt.show()

    elif a == '14':
        d = 3e-9  # m
        start = -0.1
        end = -start
        eff_m = 1
        area = 2e-12
        dimension = 1e+9
        x = np.linspace(start, end, 30)
        y = [-di(v, 0.3, 0.61, eff_m) * area * dimension for v in x]

        # down
        y2 = [-di(v, 0.37, .76, eff_m) * area * dimension for v in x]
        plt.plot(-x, y, -x, y2)
        tot = np.array((-x, y, y2)).transpose()
        np.savetxt('14.dat', tot)
        plt.show()

    elif a == '14au':
        d = 3e-9  # m
        start = -0.2
        end = -start
        eff_m = 1
        area = 2e-12
        dimension = 1e+9
        x = np.linspace(start, end, 30)
        y = [-di(v, 0.26, 0.78, eff_m) * area * dimension for v in x]

        # down
        y2 = [-di(v, 0.24, .92, eff_m) * area * dimension for v in x]
        plt.plot(-x, y, -x, y2)
        tot = np.array((-x, y, y2)).transpose()
        np.savetxt('14au.dat', tot)
        plt.show()
