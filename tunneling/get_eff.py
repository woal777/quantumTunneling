import numpy as np
import matplotlib.pyplot as plt
c = 4.036
hbar_c = 1970
mcs = .511e+6

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
mass = k ** 2 / energy * hbar_c ** 2 / mcs
eff_m = dict()
for m, e in zip(mass, energy):
    eff_m[e] = m
print(eff_m)

plt.plot(eff_m.keys(), eff_m.values())
plt.show()