"""

radhitya@uwaterloo.ca

Droste effect

References:
    http://www.josleys.com/article_show.php?id=82#ref3
    https://github.com/tcoxon/droste/
"""


import numpy as np
import matplotlib
import matplotlib.pylab as plt

import drostelib.drostehelper as dh    

    
"""
The main function
"""
if __name__ == "__main__":
    
    # load the image
    # there is a possible bug: it only wants .png files
    img_col = matplotlib.image.imread("images/pc_large.png")
    img_col = (img_col * 255).astype(np.uint8)
    height_origin, width_origin, depth = img_col.shape    
    img_droste = np.zeros(img_col.shape, dtype="uint8") 
    
    r1, center_x, center_y = dh.CalculateCenter(img_col)
    r2 = center_y if center_y < center_x else center_x
    # you can modify with something like:
    # r2 = r2 * 0.8
        
    # precompute variables
    log_r1     = np.log(r1)
    r2_over_r1 = r2 / r1
    period     = np.log(r2_over_r1)
    pi2        = np.pi * 2.0
    
    # number of repeats
    repeat_min = -5 # outward repeat
    repeat_max = 10 # inward repeat
               
    # these are for 2nd stage
    alpha = np.arctan(np.log(r2 / r1) / pi2)
    f = np.cos(alpha)
    exp_alpha = np.exp(1j * alpha)
        
    for x_iter in xrange(width_origin):
        
        for y_iter in xrange(height_origin):
            
            xy1 = complex(x_iter - center_x, y_iter - center_y) 
            
            # 1st stage, to polar coordinate
            xy1 = np.log(xy1) - log_r1 
            
            for rep_iter in xrange(repeat_min, repeat_max) :               
                period_rep = period * (rep_iter)
                xy2 = xy1 + complex(period_rep, 0)
                
                # 2nd stage, rotate and shrink
                xy3 = xy2 * f * exp_alpha 
                
                # 3rd stage, exponentiation
                xy4 = np.exp(xy3)  
                
                new_x = np.real(xy4) + center_x
                new_y = np.imag(xy4) + center_y
                
                # somehow my code produces Nan or Inf (why?)
                if not (dh.IsCoordValid(new_x, new_y)):
                    continue            
                
                # the new coordinate should be inside the image
                if(dh.IsInside(new_x, new_y, width_origin, height_origin)):
                    ori_col = img_col[int(new_y)][int(new_x)] 
                    if not(dh.IsMasked(ori_col)):
                        img_droste[y_iter][x_iter] = ori_col
                        break
    
    # print the original and show r1 and r2
    plt.figure(1)
    plt.clf()
    plt.imshow(img_col)
    plt.plot(center_x, center_y,'o', color="blue", markersize=7)
    circle1 = plt.Circle((center_x, center_y), r1, linestyle="dashed", facecolor="none", edgecolor="blue") 
    circle2 = plt.Circle((center_x, center_y), r2, linestyle="dashed", facecolor="none", edgecolor="red") 
    fig = plt.gcf()
    fig.gca().add_artist(circle1)
    fig.gca().add_artist(circle2)
    plt.show()
    
    
    # show the droste image
    plt.figure(2)
    plt.clf()
    plt.imshow(img_droste) 
    #plt.savefig("droste_image.png")
    
    print "Calculation is completed"
    
    
