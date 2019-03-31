from scipy.interpolate import interp1d
from matplotlib import pyplot as plt
import numpy as np


a = 100
X = np.linspace(-1, 1, 200)
arr = [a * (1 - x ** 2) ** 0.5 for x in X]
arr = np.array(arr)
arr2 = arr * 2
X2 = X * 2
plt.plot(X, arr)
plt.plot(X2, arr2)
plt.show()
