"""
Droste effect

References:
    http://www.josleys.com/article_show.php?id=82#ref3
    https://github.com/tcoxon/droste/
"""

#import sys
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

    img_col = matplotlib.image.imread("reza.png")
    img_col = (img_col * 255).astype(np.uint8)
    height, width, depth = img_col.shape    
    img_droste = np.zeros(img_col.shape, dtype="uint8") 

    origin_x = width  / 2.0
    origin_y = height / 2.0
    r1       = GetMaskBound(img_col)
    r2       = origin_y if origin_y < origin_x else origin_x
    
    # adjustment
    #r1 *= 0.8    
    r1 *= 1.2
    
    log_r1     = np.log(r1)
    r2_over_r1 = r2 / r1
    period     = np.log(r2_over_r1)
    pi2        = np.pi * 2.0
    
    repeat_min = -5 # outward repeat
    repeat_max = 10 # inward repeat
           
    
    alpha = np.arctan(np.log(r2 / r1) / pi2)
    f = np.cos(alpha)
    exp_alpha = np.exp(1j * alpha)
        
    for x_iter in range(width):
        for y_iter in range(height):        
            #img_droste[y_iter][x_iter] = transp_color
            
            xy1 = complex(x_iter - origin_x, y_iter - origin_y) 
            xy1 = np.log(xy1) - log_r1 # 1st transform
            
            repeat_array = range(repeat_min, repeat_max)
            for rep_iter in repeat_array:
                period_rep = period * rep_iter
                xy2 = xy1 + complex(period_rep, 0)
                
                # 2nd transform
                xy3 = xy2 * f * exp_alpha   
                #xy3 = complex(np.real(xy2)*cosacosa - np.imag(xy2)*cosasina, np.imag(xy2)*cosacosa + np.real(xy2)*cosasina)
                
                # 3rd transform
                xy4 = np.exp(xy3) 
                #exp_x = np.exp(np.real(xy3) + log_r1)
                #xy4 = complex(np.cos(np.imag(xy3)) * exp_x, np.sin(np.imag(xy3)) * exp_x)                 
                
                """
                xy4 += complex(origin_x, origin_y)                
                new_x = np.real(xy4)
                new_y = np.imag(xy4)
                """
                #xy4 += complex(origin_x, origin_y)                
                new_x = np.real(xy4) + origin_x
                new_y = np.imag(xy4) + origin_y
                
                """
                if(np.isnan(new_x) or np.isinf(new_x)):
                    continue
                
                if(np.isnan(new_y) or np.isinf(new_y)):
                    continue
                """
                if not (IsCoordValid(new_x, new_y)):
                    continue
                
                new_x = int(new_x)
                new_y = int(new_y)                
                
                if(IsInside(new_x, new_y, width, height)):
                    ori_col = img_col[new_y][new_x] 
                    if not(IsMasked(ori_col)):
                        img_droste[y_iter][x_iter] = ori_col
                        break
    
    plt.figure(1)
    plt.clf()
    plt.imshow(img_col)
    circle1 = plt.Circle((origin_x, origin_y), r1, linestyle="dashed", facecolor="none", edgecolor="blue") 
    circle2 = plt.Circle((origin_x, origin_y), r2, linestyle="dashed", facecolor="none", edgecolor="red") 
    fig = plt.gcf()
    fig.gca().add_artist(circle1)
    fig.gca().add_artist(circle2)
    plt.show()
    
    plt.figure(2)
    plt.clf()
    plt.imshow(img_droste) 
    
    print "Calculation is completed"
