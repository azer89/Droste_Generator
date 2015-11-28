"""
Droste effect

References:
    http://www.josleys.com/article_show.php?id=82#ref3
    https://github.com/tcoxon/droste/blob/master/droste.c
"""

import numpy as np
import matplotlib
import matplotlib.pylab as plt

img_col = matplotlib.image.imread("image067.jpg")
height, width, depth = img_col.shape

img_droste = np.zeros(img_col.shape) 


repeat_min = -2
repeat_max = 10
r1 = 100.0
r2 = 300.0

pi2 = np.pi * 2.0

log_r1 = np.log(r1)
r2_over_r1 = r2 / r1
period = np.log(r2_over_r1)
origin_x = width/2.0;
origin_y = height/2.0

alpha = np.arctan(np.log(r2 / r1) / pi2)
f = np.cos(alpha)
exp_alpha = np.exp(1j * alpha)

for y_iter in range(height):
    for x_iter in range(width):
        #print x_iter, " - ", y_iter        
        
        coord1 = complex(x_iter - origin_x, y_iter - origin_y)
        
        coord1 = np.log(coord1) - log_r1
        
        for rep_iter in range(repeat_min, repeat_max):
            #print rep_iter
            coord2 = coord1
            
            coord2 += complex(rep_iter * period ,0)
            
            coord2 = coord2 * f * exp_alpha
            
            coord2 = np.exp(coord2)
            
            coord2 += complex(origin_x, origin_y)
            
            new_x = np.real(coord2)
            new_y = np.imag(coord2)
            
            if(np.isnan(new_x) or np.isinf(new_x)):
                continue
            
            if(np.isnan(new_y) or np.isinf(new_y)):
                continue
            
            print new_x, "- ", new_y
            
            new_x = int(new_x)
            new_y = int(new_y)
            #print new_x, " ", new_y
            
            if(new_x >= 0 and new_x < width and new_y >= 0 and new_y < height):
                #print "yooow"
                #print new_x, "- ", new_y
                img_droste[y_iter][x_iter] = img_col[new_y][new_x]
                break
            #else:
            #    print new_x, "- ", new_y
                
            
        
        #img_droste[y_iter][x_iter] = img_col[y_iter][x_iter]





plt.figure(0)
plt.clf()
plt.imshow(img_droste) 
