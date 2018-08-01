from main import analytic as anal
import numpy as np
from matplotlib import pyplot as plt
from main import solve


fig = plt.figure()
fig.add_subplot(211)
x = np.linspace(-1.0, 1.0, 41)
y = [anal.di(3e-9, r, .9, .95, 1) for r in x]
plt.plot(x, y)
y2 = [anal.di(3e-9, r, 1.35, .5, 1) for r in x]
plt.plot(x, y2)
plt.show()