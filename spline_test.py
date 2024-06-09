from scipy.interpolate import CubicSpline
import matplotlib.pyplot as plt
import numpy as np


y = [0,-0.07,-0.041, 0.088, -0.08, -0.05, 0.07, 0.004, -0.26, 0.07, -1.4, -0.9, -1.14, -0.4, 0.008, -0.06, -0.03, -0.004, 0.03, 0.05, -0.015]
x = np.linspace(0,10,len(y))


cs = CubicSpline(x,y)

plt.figure()
plt.plot(x,y)
plt.plot(x,cs(x), '--')
plt.show()

