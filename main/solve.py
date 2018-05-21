import cmath
import time
from math import pi, exp
from multiprocessing import Process, Queue
from scipy.integrate import quad
import matplotlib.pyplot
import numpy as np

# Variables with simple values
mass = 0.511 * 1e+6 / 299792458 ** 2  # eV * (s / m) ** 2
h = 4.135667662 * 1e-15  # eV * s
hbar = 6.582119514 * 1e-16  # eV * s
electron = 1.602e-19  # C
img = complex(0, 1)
Ef = 7.
tol = 1e-20
cexp = cmath.exp
dot = np.dot
array = np.array
csqrt = cmath.sqrt
identity = np.identity
plt = matplotlib.pyplot


class SolvingProblem:
    # potential variables

    def __init__(self, thickness: float, area: float, start: float, end, eff_m):
        self.N = 500
        self.potential = array([0.3])
        self.reduced_mass = cmath.sqrt(0.511 * eff_m) * 1e+3 / 299792458  # eV ** 0.5 * s / m
        self.reduced_k = self.reduced_mass / hbar
        self.start = start
        self.end = end
        self.area = area
        self.dx = thickness / self.N
        self.temperature = 300. * 8.617343e-5
        self.arr = array([])

    def main(self, start, end):
        s_time = time.time()
        n_V = 22
        queue = [Queue() for _ in range(n_V)]
        bias = np.linspace(start, end, n_V)
        p = [Process(target=self.current, args=(r, output)) for r, output in zip(bias, queue)]
        di = []
        for i in p:
            i.start()
        for i in p:
            i.join()
        for i in queue:
            di.append(i.get())
        print('spended time is %fs' % (time.time() - s_time))
        return bias, np.array(di)

    def current(self, V, result):
        self.gen_pot(self.start, self.end + V, V)
        constants = 4. * pi * mass * electron / h ** 3 * self.area
        i_tot = 0.
        dn = 0.003
        E_x = Ef + 0.6
        Em = 0.6
        if V > 0:
            E_x += V
        else:
            Em -= V
        while E_x > Ef - Em:
            i_tot += self.density(E_x, V) * self.tunneling(E_x) * dn
            E_x -= dn
        result.put(constants * i_tot)

    def density(self, e_x, v):
        a = quad(self.fermi, e_x, np.inf)
        b = quad(self.fermi, e_x - v, np.inf)
        return b[0] - a[0]

    def gen_pot(self, start=0., end=1., v=0.):
        self.potential = np.linspace(start + Ef, end + Ef, self.N + 2)
        self.potential.put(0, 0)
        self.potential.put(-1, v)

    def set_temperature(self, t):
        self.temperature = t * 8.617343e-5

    def fermi(self, e=0.):
        """
        fermi() -> fermi-dirac statistics
            Parameters
        ----------
        E : scalar
            energy"""
        if (e - Ef) / self.temperature > 700:
            return 0.
        return 1. / (1. + exp((e - Ef) / self.temperature))  # eV

    def tunneling(self, E):
        k = [self.reduced_mass * csqrt(2. * (E - v)) / hbar for v in self.potential]
        matrix = identity(2, dtype=np.complex128)
        for n in range(0, self.N + 1):
            if k[n].__abs__() < 1e-5:
                continue
            T11 = (k[n] + k[n + 1]) / 2 / k[n] * cexp(-1 * img * k[n] * self.dx)
            T12 = (k[n] - k[n + 1]) / 2 / k[n] * cexp(-1 * img * k[n] * self.dx)
            T21 = (k[n] - k[n + 1]) / 2 / k[n] * cexp(img * k[n] * self.dx)
            T22 = (k[n] + k[n + 1]) / 2 / k[n] * cexp(img * k[n] * self.dx)
            matrix = dot(matrix, [[T11, T12], [T21, T22]])

        return matrix[0][0].__abs__() ** -2


class SolvingProblemArray(SolvingProblem):

    def __init__(self, thickness: float, area: float, arr, eff_m):
        SolvingProblem.__init__(self, thickness, area, start=0, end=None, eff_m=eff_m)
        self.N = len(arr) - 1
        self.potential = array([0.3])
        self.reduced_mass = cmath.sqrt(0.511 * eff_m) * 1e+3 / 299792458  # eV ** 0.5 * s / m
        self.area = area
        self.dx = thickness / self.N
        self.temperature = 300. * 8.617343e-5
        self.arr = arr

    def current(self, v, result):
        self.gen_pot(v)
        constants = 4. * pi * mass * electron / h ** 3 * self.area
        i_tot = 0.
        dn = 0.003
        E_x = Ef + 0.6
        Em = 0.6
        if v > 0:
            E_x += v
        else:
            Em -= v
        while E_x > Ef - Em:
            i_tot += self.density(E_x, v) * self.tunneling(E_x) * dn
            E_x -= dn
        result.put(constants * i_tot)

    def gen_pot(self, start=0., end=1., v=0.):
        self.potential = np.zeros(self.N * 100 + 2)
        for i in range(len(self.arr) - 1):
            self.potential[100 * i + 1: 100 * (i + 1) + 1] = np.linspace(self.arr[i] + Ef, self.arr[i + 1] + Ef, 100)
        self.potential += np.linspace(0, v, self.N * 100 + 2)
        self.potential.put(0, 0)
        self.potential.put(-1, v)


if __name__ == "__main__":
    pass