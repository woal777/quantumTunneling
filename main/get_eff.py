import numpy as np
import matplotlib.pyplot as plt

c = 5.03
hbar_c = 1970
mcs = .511e+6

fig = plt.figure(1)
arr = np.genfromtxt('input')
arr = arr.transpose()
arr[0, :] -= arr[0, 0]
arr[1, :] -= arr[1, -1]
arr = np.abs(arr)
arr = arr[:, np.where(arr[0, :] == np.amax(arr[0, :]))[0][0]:]
'''eV'''
energy = arr[1, :]
'''1 / Ang'''
k = arr[0, :] / (2 * np.pi) * c
fig.add_subplot(211)
plt.plot(energy, k)
mass = k ** 2 / energy * hbar_c ** 2 / mcs
fig.add_subplot(212)
plt.plot(energy, mass)
plt.show()
