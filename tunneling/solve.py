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
tol = 1e-20
cexp = cmath.exp
dot = np.dot
array = np.array
csqrt = cmath.sqrt
identity = np.identity
plt = matplotlib.pyplot


class SolvingProblem:
    # potential variables
    def __init__(self, area: float, start: float, end: float, eff_m: float, thickness: float):
        self.N = 100 + 2
        self.n_V = 44
        self.potential = array([0.3])
        self.reduced_mass = cmath.sqrt(0.511 * eff_m) * 1e+3 / 299792458  # eV ** 0.5 * s / m
        self.reduced_k = self.reduced_mass / hbar
        self.start = start
        self.end = end
        self.area = area
        self.dx = thickness / self.N
        self.temperature = 300. * 8.617343e-5
        self.arr = array([])
        self.Ef = 0

    def main(self, start, end, vlen=False):
        s_time = time.time()
        if vlen:
            bias = vlen
        else:
            bias = np.linspace(start, end, self.n_V)
        queue = [Queue() for _ in range(len(bias))]
        p = [Process(target=self.current, args=(r, output)) for r, output in zip(bias, queue)]
        di = []
        for i in p:
            i.start()
        for i in p:
            i.join()
        for i in queue:
            di.append(i.get())
        fig = plt.figure()
        fig.add_subplot(221)
        for i in bias:
            self.gen_pot(i)
            plt.plot(self.potential, label='{:02f}'.format(i))
        plt.legend()
        fig.add_subplot(222)
        plt.semilogy(bias, abs(np.array(di)))
        fig.add_subplot(223)
        plt.show()
        # print('spended time is %fs' % (time.time() - s_time))
        return bias, np.array(di)

    def current(self, V, result):
        # A/m^2
        self.gen_pot(V)
        constants = 4. * pi * mass * electron / h ** 3 * self.area
        i_tot = 0.
        dn = 0.003
        E_x = self.Ef + 0.6
        Em = 0.6
        if V > 0:
            E_x += V
        else:
            Em -= V
        while E_x > self.Ef - Em:
            i_tot += self.density(E_x, V) * self.tunneling(E_x) * dn
            E_x -= dn
        result.put(constants * i_tot)

    def current_with_barrier(self, V):
        self.gen_pot(V)
        constants = 4. * pi * mass * electron / h ** 3 * self.area
        i_tot = 0.
        dn = 0.003
        E_x = Ef + 0.6
        Em = 0.6
        if V > 0:
            E_x += V
        else:
            Em -= V
        while E_x > self.Ef - Em:
            i_tot += self.density(E_x, V) * self.tunneling(E_x) * dn
            E_x -= dn
        print(constants * i_tot)
        return constants * i_tot

    def main_with_barrier(self, start, vlen=False):
        if vlen:
            bias = vlen
        else:
            bias = np.linspace(-start, start, self.n_V)
        di = []
        for i in bias:
            di.append(self.current_with_barrier(i))
        # print('spended time is %fs' % (time.time() - s_time))
        return bias, np.array(di)

    def density(self, e_x, v):
        a = quad(self.fermi, e_x, np.inf)
        b = quad(self.fermi, e_x + v, np.inf)
        return a[0] - b[0]

    def gen_pot(self, v=0.):
        self.potential = np.linspace(self.start + self.Ef, self.end + self.Ef + v, self.N)
        self.potential.put(0, self.Ef)
        self.potential.put(-1, self.Ef + v)

    def set_temperature(self, t):
        self.temperature = t * 8.617343e-5

    def fermi(self, e=0.):
        """
        fermi() -> fermi-dirac statistics
            Parameters
        ----------
        E : scalar
            energy"""
        if (e - self.Ef) / self.temperature > 700:
            return 0.
        return 1. / (1. + exp((e - self.Ef) / self.temperature))  # eV

    def tunneling(self, E):
        k = [self.reduced_mass * csqrt(2. * (E - v)) / hbar for v in self.potential]
        matrix = identity(2, dtype=np.complex128)
        for n in range(0, self.N - 1):
            try:
                T11 = (k[n] + k[n + 1]) / 2 / k[n] * cexp(-1j * k[n] * self.dx)
                T12 = (k[n] - k[n + 1]) / 2 / k[n] * cexp(-1j * k[n] * self.dx)
                T21 = (k[n] - k[n + 1]) / 2 / k[n] * cexp(1j * k[n] * self.dx)
                T22 = (k[n] + k[n + 1]) / 2 / k[n] * cexp(1j * k[n] * self.dx)
            except ZeroDivisionError:
                print(k[n])
            matrix = dot(matrix, [[T11, T12], [T21, T22]])

        return matrix[0][0].__abs__() ** -2


if __name__ == "__main__":
    pass
