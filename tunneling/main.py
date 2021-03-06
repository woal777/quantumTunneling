import multiprocessing
from math import exp
from joblib import Parallel, delayed
import numpy as np
from cmath import exp as cexp
import matplotlib.pyplot as plt
from scipy.integrate import quad


class Current:

    def __init__(self, pot):
        self.h = 4.135667662e-15  # eV * s
        mass = 0.511 * 1e+6 / 299792458 ** 2  # eV * (s / m) ** 2
        self.e = 1.602e-19  # C
        self.m = mass * .15
        self.hbar = self.h / (2 * np.pi)
        self.v = pot
        self.v_tmp = self.v
        self.dx = 1e-10
        self.temperature = 300 * 8.617343e-5

    def fermi(self, e=0.):
        """
        fermi() -> fermi-dirac statistics
            Parameters
        ----------
        E : scalar
            energy"""
        if (e / self.temperature) > 100:
            return 0
        else:
            return 1. / (1. + exp(e / self.temperature))  # eV

    def gen_pot(self, v):
        self.v = self.v_tmp + np.linspace(0, -v, len(self.v))
        if abs(v) < 0.1:
            plt.step(range(len(self.v)), self.v, label=v)

    def density(self, e_x, v):
        a = quad(self.fermi, e_x, np.inf)
        b = quad(self.fermi, e_x + v, np.inf)
        return a[0] - b[0]

    def transmission(self, energy):
        k = np.sqrt(2 * self.m * (energy - self.v)) / self.hbar * self.dx
        matrix = np.identity(2, dtype=np.complex)
        for n in range(0, len(self.v) - 1):
            if k[n] == 0:
                continue
            t = np.zeros((2, 2), dtype=np.complex)
            t[0, 0] = (k[n] + k[n + 1]) / 2 / k[n] * cexp(-1j * k[n])
            t[0, 1] = (k[n] - k[n + 1]) / 2 / k[n] * cexp(-1j * k[n])
            t[1, 0] = (k[n] - k[n + 1]) / 2 / k[n] * cexp(1j * k[n])
            t[1, 1] = (k[n] + k[n + 1]) / 2 / k[n] * cexp(1j * k[n])
            matrix = np.dot(matrix, t)
        return matrix[0][0].__abs__() ** -2

    def current(self, volt):
        # A/m^2
        self.gen_pot(volt)
        constants = 4. * np.pi * self.m * self.e / self.h ** 3
        e_m = 1.2
        if volt < 0:
            e_m -= volt
        x = np.linspace(0, e_m, 500)
        de = x[1] - x[0]
        num_cores = multiprocessing.cpu_count()

        def di(e_x):
            return self.density(e_x, volt) * self.transmission(e_x + 0j) * de

        y = Parallel(n_jobs=num_cores)(delayed(di)(i) for i in x)
        i_tot = sum(y)
        return constants * i_tot


if __name__ == '__main__':
    c = Current(np.array([0, *np.linspace(1, 1, 10), *np.linspace(1, 1, 10), 0]))
    '''
    for i in [1, 3, 7]:
        c.dx = i * 1.3e-10
        x = np.linspace(1e-19, 2, 5222)
        y = [c.transmission(r + 0j) for r in x]
        plt.legend()
    plt.show()'''
    fig = plt.figure()
    fig.add_subplot(211)
    x = np.linspace(-1.5, 1.5, 32)
    y = [abs(c.current(r)) for r in x]
    plt.legend()
    fig.add_subplot(212)
    plt.semilogy(x, y)
    plt.show()
