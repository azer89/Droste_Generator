'''

complex plane

'''

import numpy as np
import matplotlib.pylab as plt

pi2 = np.pi * 2.0
x = np.arange(0, pi2, 0.05)

r = 10.0
plt.clf()

'''
for i in range(len(x) - 1):
    a1 = x[i]
    a2 = x[i+1]
    print a1, " ", a2
    plt.plot([r * np.sin(a1), r * np.sin(a2)], [r * np.cos(a1), r * np.cos(a2)], 'k-', lw=0.5)
'''

plt.axes().set_aspect('equal')
plt.show()
    

