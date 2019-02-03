import cmath
from math import pi, exp
from multiprocessing import Process, Queue
from typing import Any, Union, Optional, Tuple

from numpy.core.multiarray import ndarray
from scipy.integrate import quad
import matplotlib.pyplot
import numpy as np

# Variables with simple values
mass = 0.511 * 1e+6 / 299792458 ** 2  # eV * (s / m) ** 2
h = 4.135667662 * 1e-15  # eV * s
hbar = 6.582119514 * 1e-16  # eV * s
electron = 1.602e-19  # C
img = complex(0, 1)
Ef = 0.
tol = 1e-20
cexp = cmath.exp
dot = np.dot
array = np.array
csqrt = cmath.sqrt
identity = np.identity
plt = matplotlib.pyplot


class SolvingProblem:

    potential: Union[ndarray, Tuple[ndarray, Optional[float]]]
    _temperature: Union[float, Any]

    def __init__(self, thickness: float, area: float, phi_i: float, phi_f: float):
        self.N = 52
        self.phi_i = phi_i
        self.phi_f = phi_f
        self._dx = thickness / self.N
        self.set_temperature(300)

    def set_temperature(self, t):
        self._temperature = t * 8.617343e-5

    def density(self, e_x, v):
        a = quad(self.fermi, e_x, np.inf)
        b = quad(self.fermi, e_x - v, np.inf)
        return b[0] - a[0]

    def fermi(self, e=0.):
        """
        fermi() -> fermi-dirac statistics
            Parameters
        ----------
        E : scalar
            energy"""
        if (e - Ef) / self._temperature > 700:
            return 0.
        return 1. / (1. + exp((e - Ef) / self._temperature))  # eV

    def gen_pot(self, v=0.):
        self.potential = np.linspace(self.phi_i + Ef, self.phi_f + Ef + v, self.N)
        self.potential.put(0, Ef)
        self.potential.put(-1, Ef + v)

    def tunneling(self, E):
        k = [csqrt(2. * mass * (E - v)) / hbar for v in self.potential]
        matrix = identity(2, dtype=np.complex128)
        for n in range(0, self.N - 1):
            if k[n].__abs__() < 1e-5:
                continue
            T11 = (k[n] + k[n + 1]) / 2 / k[n] * cexp(-1 * img * k[n] * self.dx)
            T12 = (k[n] - k[n + 1]) / 2 / k[n] * cexp(-1 * img * k[n] * self.dx)
            T21 = (k[n] - k[n + 1]) / 2 / k[n] * cexp(img * k[n] * self.dx)
            T22 = (k[n] + k[n + 1]) / 2 / k[n] * cexp(img * k[n] * self.dx)
            matrix = dot(matrix, [[T11, T12], [T21, T22]])

        return matrix[0][0].__abs__() ** -2


if __name__ is '__main__':
    c = SolvingProblem()

