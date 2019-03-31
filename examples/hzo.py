from tunneling import analytic
from numpy import linspace


x = linspace(0, .2, 10)
y = [analytic.simmon_low(2.33, r, 2.8e-9) for r in x]
print(x, y)