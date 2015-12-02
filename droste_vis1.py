"""
Droste effect

References:
    http://www.josleys.com/article_show.php?id=82#ref3
    https://github.com/tcoxon/droste/blob/master/droste.c
"""

import numpy as np
import matplotlib
import matplotlib.pylab as plt

#image is taken from 
# http://www.josleys.com/article_show.php?id=82#ref3
#img_col = matplotlib.image.imread("image067.jpg")
img_col = matplotlib.image.imread("feel.png")
height, width, depth = img_col.shape


plt.figure(0)
plt.clf()
plt.imshow(img_col) 

pi2 = np.pi * 2.0
x = np.arange(0, pi2, 0.05)

r1 = 1.0
r2 = 5.0

log_r1 = np.log(r1)
r2_over_r1 = r2 / r1
period = np.log(r2_over_r1)
origin_x = width/2.0;
origin_y = height/2.0

z1 = np.zeros(len(x), dtype="complex")
z2 = np.zeros(len(x), dtype="complex")

for i in range(len(x)):
    theta = x[i]
    z1[i] = r1 * np.exp(1j * theta)
    z2[i] = r2 * np.exp(1j * theta)
    
    
#plt.clf()
#
#for i in range(len(z1)):
#    r_val1 = np.real(z1[i])
#    i_val1 = np.imag(z1[i])    
#    plt.plot(r_val1, i_val1, 'ro')
#    
#    r_val2 = np.real(z2[i])
#    i_val2 = np.imag(z2[i])    
#    plt.plot(r_val2, i_val2, 'bo')
    

# Transform z into logarithmic polar coordinates
"""
for i in range(len(x)):
    x1 = np.real(z1[i])
    y1 = np.imag(z1[i])
    z1[i] = complex(np.log(np.sqrt(x1 * x1 + y1 * y1 )) - log_r1,  np.arctan2(y1, x1))
    
    x2 = np.real(z2[i])
    y2 = np.imag(z2[i])
    z2[i] = complex(np.log(np.sqrt(x2 * x2 + y2 * y2 )) - log_r1,  np.arctan2(y2, x2))
"""
for i in range(len(x)):
    z1[i] = np.log(z1[i]) - log_r1
    z2[i] = np.log(z2[i]) - log_r1

# rotate and shrunk
alpha = np.arctan(np.log(r2 / r1) / pi2)
f = np.cos(alpha)
exp_alpha = np.exp(1j * alpha)
for i in range(len(x)):
    z1[i] = z1[i] * f * exp_alpha 
    z2[i] = z2[i] * f * exp_alpha 
    
# exponentiation
for i in range(len(x)):
#    x1 = np.real(z1[i])
#    y1 = np.imag(z1[i])
#    e_x1 = np.exp(x1 + log_r1)
#    z1[i] = complex(np.cos(y1) * e_x1, np.sin(y1) * e_x1)
#    
#    x2 = np.real(z2[i])
#    y2 = np.imag(z2[i])
#    e_x2 = np.exp(x2 + log_r1);
#    z2[i] = complex(np.cos(y2) * e_x2, np.sin(y2) * e_x2)
    z1[i] = np.exp(z1[i])
    z2[i] = np.exp(z2[i])    
    

plt.figure(1)
plt.clf()

plt.plot([-5, 5], [0, 0], 'r-', lw=0.5)
plt.plot([0, 0], [-5, 5], 'r-', lw=0.5)

for i in range(len(z1)):
    r_val1 = np.real(z1[i])
    i_val1 = np.imag(z1[i])    
    plt.plot(r_val1, i_val1, 'ro')
    
    r_val2 = np.real(z2[i])
    i_val2 = np.imag(z2[i])    
    plt.plot(r_val2, i_val2, 'bo')


plt.axes().set_aspect('equal')
plt.show()
