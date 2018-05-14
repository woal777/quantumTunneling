try:
    from quantum_mach import solve2
except ImportError:
    import solve2
import matplotlib.pyplot as plt

if __name__ == "__main__":
    for i in range(len(self.arr) - 1):
        self.potential[100 * i + 1: 100 * (i + 1) + 1] = np.linspace(self.arr[i] + Ef, self.arr[i + 1] + Ef, 100)

    s = solve2.SolvingProblemArray(4.8e-09, 1, [1, 0, 0, 1, 1], 1.)
    x, y = s.main(0, 1.3)
    plt.plot(x, y)
    plt.show()
