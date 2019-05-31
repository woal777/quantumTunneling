import tunneling.solve as solve
import numpy as np
import cmath
import matplotlib.pyplot as plt


class SolvingProblemArray(solve.SolvingProblem):

    def __init__(self, thickness: float, area: float, arr, eff_m, start: float = 0, end=0):
        super().__init__(thickness, area, start, end, eff_m)
        self.dense = 30
        self.N = (len(arr) - 1) * self.dense + 2
        self.potential = np.array([0.3])
        self.reduced_mass = cmath.sqrt(0.511 * eff_m) * 1e+3 / 299792458  # eV ** 0.5 * s / m
        self.area = area
        self.dx = thickness / self.N
        self.arr = arr

    def gen_pot(self, v=0.):
        self.potential = np.zeros(self.N)
        for i in range(len(self.arr) - 1):
            self.potential[self.dense * i + 1: self.dense * (i + 1) + 1] \
                = np.linspace(self.arr[i] + self.Ef, self.arr[i + 1] + self.Ef, self.dense)
        self.potential += np.linspace(0, v, self.N)
        self.potential.put(0, self.Ef)
        self.potential.put(-1, self.Ef + v)
#        plt.show()
