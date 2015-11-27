'''

complex plane

http://www.josleys.com/article_show.php?id=82#ref3

'''

import numpy as np
import matplotlib.pylab as plt

pi2 = np.pi * 2.0
x = np.arange(0, pi2, 0.05)

'''
r = 10.0
plt.clf()


for i in range(len(x) - 1):
    a1 = x[i]
    a2 = x[i+1]
    print a1, " ", a2
    plt.plot([r * np.sin(a1), r * np.sin(a2)], [r * np.cos(a1), r * np.cos(a2)], 'k-', lw=0.5)
'''

e1 = np.zeros(len(x), dtype="complex")
e2 = np.zeros(len(x), dtype="complex")
r1 = 1.0
r2 = 5.0

for i in range(len(x)):
    theta = x[i]
    e1[i] = r1 * np.exp(1j * theta)
    e2[i] = r2 * np.exp(1j * theta)
    #e1[i] = 1.0j * r2 + r1 * np.exp(1j * theta)
    #e2[i] = 1.0j * r2 + r2 * np.exp(1j * theta)
    
for i in range(len(x)):
    #theta = x[i]
    #e1[i] = np.log(e1[i])
    #e2[i] = np.log(e2[i])    
#    e1[i] = np.log(e1[i] / r1)
#    e2[i] = np.log(e2[i] / r1)
    e1[i] = np.log(e1[i]) - np.log(r1)
    e2[i] = np.log(e2[i]) - np.log(r1)

plt.clf()

for i in range(len(e1)):
    r_val1 = np.real(e1[i])
    i_val1 = np.imag(e1[i])    
    plt.plot(r_val1, i_val1, 'ro')
    
    r_val2 = np.real(e2[i])
    i_val2 = np.imag(e2[i])    
    plt.plot(r_val2, i_val2, 'bo')


plt.axes().set_aspect('equal')
plt.show()
    

