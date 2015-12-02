
"""
Droste Visualization
"""

import numpy as np
import matplotlib
import matplotlib.pylab as plt

"""
Magenta color as the mask color
"""
transp_color = np.array([255, 0, 255])

"""
Global variables
"""
height = None 
width  = None 
depth  = None
origin_x = None
origin_y = None


"""
Make sure a corrdinate is valid
"""
def IsCoordValid(x, y):
    if(np.isnan(x) or np.isinf(x)):
        return False                
    if(np.isnan(y) or np.isinf(y)):
        return False    
    return True


"""
Is inside the image
"""
def IsInside(x, y, width, height):
    if(x >= 0 and y >= 0 and x < width and y < height):
        return True
    return False

"""
Determine whether a color is the mask color
"""
def IsMasked(col):    
    if(col[0] == transp_color[0] and col[1] == transp_color[1] and col[2] == transp_color[2]):
        return True
    return False

"""
Obtain the inner radius
"""
def GetMaskBound(img_col):
    r1 = 0    
    height, width, depth = img_col.shape
    origin_x   = width  / 2.0
    origin_y   = height / 2.0
    for y_iter in range(height):
        for x_iter in range(width):
            col = img_col[y_iter][x_iter]
            if(IsMasked(col)): 
                x = x_iter - origin_x
                y = y_iter - origin_y
                r = np.sqrt(x * x + y * y)
                if (r > r1):
                    r1 = r
    return r1
    
    
"""
The main function
"""
if __name__ == "__main__":
    # load the image

    img_col = matplotlib.image.imread("circles.png")
    img_col = (img_col * 255).astype(np.uint8)
    height, width, depth = img_col.shape    
    img_droste = np.zeros(img_col.shape, dtype="uint8") 

    origin_x = width  / 2.0
    origin_y = height / 2.0
    r1       = GetMaskBound(img_col)
    r2       = origin_y if origin_y < origin_x else origin_x
    
    
    log_r1     = np.log(r1)
    r2_over_r1 = r2 / r1
    period     = np.log(r2_over_r1)
    pi2        = np.pi * 2.0
    
    repeat_min = -1 # outward repeat
    repeat_max = 3 # inward repeat
           
    
    alpha = np.arctan(np.log(r2 / r1) / pi2)
    f = np.cos(alpha)
    exp_alpha = np.exp(1j * alpha)
        
    plt.figure(1)
    plt.clf()
    for x_iter in range(width):
        for y_iter in range(height): 

            xy1 = complex(x_iter - origin_x, y_iter - origin_y) 
            #xy1 = complex(x_iter, y_iter)            
            
             # 1st transform
            xy1 = np.log(xy1) - log_r1             
            
            repeat_array = range(repeat_min, repeat_max)
            for rep_iter in repeat_array:
                period_rep = period * (rep_iter)
                xy2 = xy1 + complex(period_rep, 0)            
            

                
                #2nd transform
                xy3 = xy2 * f * exp_alpha 
#    
#                #3rd transform            
                xy4 = np.exp(xy3)
                
                new_x = np.real(xy4)
                new_y = np.imag(xy4)            
                
                if not (IsCoordValid(new_x, new_y)):
                    continue            
                ori_col = img_col[x_iter][y_iter]             
                plt.plot(new_x, new_y, "^", color=(ori_col[0] / 255.0, ori_col[1] / 255.0, ori_col[2] / 255.0))
                
    plt.show()
                
    
    # print the original
    plt.figure(2)
    plt.clf()
    plt.imshow(img_col)
    circle1 = plt.Circle((origin_x, origin_y), r1, linestyle="dashed", facecolor="none", edgecolor="blue") 
    circle2 = plt.Circle((origin_x, origin_y), r2, linestyle="dashed", facecolor="none", edgecolor="red") 
    fig = plt.gcf()
    fig.gca().add_artist(circle1)
    fig.gca().add_artist(circle2)
    plt.show()
    
    """
    # show the droste image
    plt.figure(2)
    plt.clf()
    plt.imshow(img_droste) 
    plt.savefig("droste_image.png")
        
    print "Calculation is completed"
    """
    