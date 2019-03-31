import numpy as np
import tunneling.solve as sol
import matplotlib.pyplot as plt

arr = np.genfromtxt('/home/jinho/PycharmProjects/quantumTunneling/examples/input/down.dat')
arr = np.linspace(arr[0], arr[-1], 6)

Sol = sol.SolvingProblemArray(4.8e-9, 1, arr, 1)

fig = plt.figure()
x, y = Sol.main(-0.3, 0.3)
fig.add_subplot(211)
plt.plot(x, y)

Sol2 = sol.SolvingProblem(4.8e-9, 1, arr[0], arr[-1], 1)
x, y = Sol2.main(-0.3, 0.3)
fig.add_subplot(212)
plt.plot(x, y)

plt.show()
