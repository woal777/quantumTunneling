from main.solve import SolvingProblem, array, hbar
import cmath


class Traps(SolvingProblem):
    # potential variables

    def __init__(self, thickness: float, area: float, start: float, end, eff_m):
        self.N = 50 + 2
        self.potential = array([0.3])
        self.reduced_mass = cmath.sqrt(0.511 * eff_m) * 1e+3 / 299792458  # eV ** 0.5 * s / m
        self.reduced_k = self.reduced_mass / hbar
        self.start = start
        self.end = end
        self.area = area
        self.dx = thickness / self.N
        self.temperature = 300. * 8.617343e-5
        self.arr = array([])

