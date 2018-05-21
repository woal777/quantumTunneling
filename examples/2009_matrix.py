import numpy as np
import main.solve as sol
import matplotlib.pyplot as plt

arr = np.genfromtxt('/home/jinho/PycharmProjects/quantumTunneling/examples/input/down.dat')

Sol = sol.SolvingProblemArray(4.8e-9, 1, arr, 1)

x, y = Sol.main(0, 0.3)
plt.plot(x, y)
plt.show()