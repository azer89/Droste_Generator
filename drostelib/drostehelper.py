# -*- coding: utf-8 -*-
"""
Created on Thu Dec 24 12:59:31 2015

@author: azer
"""

import numpy as np


"""
Magenta color as the mask color
"""
transp_color = np.array([255, 0, 255])


"""
Determine whether a color is the mask color
"""
def IsMasked(col):    
    if(col[0] == transp_color[0] and col[1] == transp_color[1] and col[2] == transp_color[2]):
        return True
    return False


"""
Make sure a coordinate is valid
(or is this because a bug in my program?)
"""
def IsCoordValid(x, y):
    # if x is invalid
    if(np.isnan(x) or np.isinf(x)):
        return False            
    # if y is invalid
    if(np.isnan(y) or np.isinf(y)):
        return False
    # the coordinate is valid
    return True


"""
make sure a coordinate is inside the image
"""
def IsInside(x, y, width, height):
    if(x >= 0 and y >= 0 and x < width and y < height):
        return True
    # is inside
    return False


"""
Calculate the center of the mask and the approximate radius
"""
def CalculateCenter(img_col):
    r1 = 0.0
    center_x = 0.0
    center_y = 0.0
    pixel_counter = 0.0   
    
    xs = [] # list of x-coordinates
    ys = [] # list of y-coordinates
    
    height, width, depth = img_col.shape
    
    # sum of the region
    for y_iter in xrange(height):
        for x_iter in xrange(width):
            col = img_col[y_iter][x_iter]
            if(IsMasked(col)):
                center_x += x_iter
                center_y += y_iter
                xs.append(x_iter)
                ys.append(y_iter)                
                pixel_counter += 1.0
                
    # get the center
    center_x /= pixel_counter
    center_y /= pixel_counter
                
    #
    for i in xrange(len(xs)):
        x = xs[i] - center_x
        y = ys[i] - center_y
        r = np.sqrt(x * x + y * y)
        if (r > r1):
            r1 = r
            
    # return the radius and the center
    return r1, center_x, center_y 
