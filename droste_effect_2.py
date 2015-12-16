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


"""
Magenta color as the mask color
"""
transp_color = np.array([255, 0, 255])


"""
Global variables
"""
height_origin = None 
width_origin  = None
depth         = None # RGB channels
origin_x      = None
origin_y      = None


"""
Make sure a coordinate is valid
(or is this because a bug in my program?)
"""
def IsCoordValid(x, y):
    if(np.isnan(x) or np.isinf(x)):
        return False            
    if(np.isnan(y) or np.isinf(y)):
        return False
    return True


"""
make sure a coordinate is inside the image
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
def GetInnerBound(img_col):
    r1 = 0    
    height, width, depth = img_col.shape
    origin_x = width  / 2.0
    origin_y = height / 2.0
    for y_iter in xrange(height):
        for x_iter in xrange(width):
            col = img_col[y_iter][x_iter]
            if(IsMasked(col)): 
                x = x_iter - origin_x
                y = y_iter - origin_y
                r = np.sqrt(x * x + y * y)
                if (r > r1):
                    r1 = r
    return r1
    
def CalculateCenter(img_col):
    r1 = 0.0
    origin_x = 0.0
    origin_y = 0.0
    pixel_counter = 0.0   
    
    xs = []
    ys = []
    
    height, width, depth = img_col.shape
    for y_iter in xrange(height):
        for x_iter in xrange(width):
            col = img_col[y_iter][x_iter]
            if(IsMasked(col)):
                origin_x += x_iter
                origin_y += y_iter
                xs.append(x_iter)
                ys.append(y_iter)                
                pixel_counter += 1.0
                
    origin_x /= pixel_counter
    origin_y /= pixel_counter
                
    for i in xrange(len(xs)):
        x = xs[i] - origin_x
        y = xs[i] - origin_y
        r = np.sqrt(x * x + y * y)
        if (r > r1):
            r1 = r
            
    return r1, origin_x, origin_y        
    

    
"""
The main function
"""
if __name__ == "__main__":
    
    # load the image
    img_col = matplotlib.image.imread("images/dc_clock.png")
    img_col = (img_col * 255).astype(np.uint8)
    height_origin, width_origin, depth = img_col.shape    
    img_droste = np.zeros(img_col.shape, dtype="uint8") 

    #origin_x = width_origin  / 2.0
    #origin_y = height_origin / 2.0
    #r1       = GetInnerBound(img_col)
    r1, origin_x, origin_y = CalculateCenter(img_col)
    r2       = origin_y if origin_y < origin_x else origin_x
    
    
    # adjustment, this is a dirty trick
    #r1 *= 0.8    
    #r1 *= 0.6
    
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
            
            xy1 = complex(x_iter - origin_x, y_iter - origin_y) 
            
            # 1st stage, to polar coordinate
            xy1 = np.log(xy1) - log_r1 
            
            #repeat_array = range(repeat_min, repeat_max)
            #for rep_iter in repeat_array:
            for rep_iter in xrange(repeat_min, repeat_max) :               
                period_rep = period * (rep_iter)
                xy2 = xy1 + complex(period_rep, 0)
                
                # 2nd stage, rotate and shrink
                xy3 = xy2 * f * exp_alpha 
                
                # 3rd stage, exponentiation
                xy4 = np.exp(xy3)  
                
                new_x = np.real(xy4) + origin_x
                new_y = np.imag(xy4) + origin_y
                
                if not (IsCoordValid(new_x, new_y)):
                    continue            
                
                if(IsInside(new_x, new_y, width_origin, height_origin)):
                    ori_col = img_col[int(new_y)][int(new_x)] 
                    if not(IsMasked(ori_col)):
                        img_droste[y_iter][x_iter] = ori_col
                        break
    
    # print the original and show r1 and r2
    plt.figure(1)
    plt.clf()
    plt.imshow(img_col)
    plt.plot(origin_x, origin_y,'x', color="blue", markersize=7)
    circle1 = plt.Circle((origin_x, origin_y), r1, linestyle="dashed", facecolor="none", edgecolor="blue") 
    circle2 = plt.Circle((origin_x, origin_y), r2, linestyle="dashed", facecolor="none", edgecolor="red") 
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
    
    
