from main.analytic import *
import matplotlib.pyplot as plt
import numpy as np


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
