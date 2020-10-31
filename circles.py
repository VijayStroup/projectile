#! /usr/bin/env python3

import numpy as np

def xycircle(center, rad, res=100):
    """Helper function that will be used later to generate circles in
    the 3D plot which will represent the cannon and target’s 
    (Krakatoa’s) positions in your plot
    
    Parameters
    ----------
    center: touple
        This is the center of the circle passed in as a touple
        containing the coordinates in a (z, y, x) fashion.
    rad: int
        This is the radius of the circle
    res: int
        This is the amount of points that make up the circle.

    References
    ----------
    From homework 7, we had to draw circles in plots so I recycled some
    code from this homework. This is the part that I used:
    theta = np.linspace(0, 2*np.pi, 200)
    center = (150,150)
    radius = 100
    x = center[0] + radius * np.cos(theta)
    y = center[1] + radius * np.sin(theta)

    Examples
    --------
    >>>circles.xycircle((0, 0, 0), 2, 5)
    [[ 0.0000000e+00  0.0000000e+00  2.0000000e+00]
     [ 0.0000000e+00  2.0000000e+00  1.2246468e-16]
     [ 0.0000000e+00  2.4492936e-16 -2.0000000e+00]
     [ 0.0000000e+00 -2.0000000e+00 -3.6739404e-16]
     [ 0.0000000e+00 -4.8985872e-16  2.0000000e+00]]
    """
    
    theta = np.linspace(0, 2*np.pi, res)
    x = center[2] + rad * np.cos(theta)
    y = center[1] + rad * np.sin(theta)
    z = center[0]
    circle = np.zeros(3 * res).reshape(res,3)
    circle[:,2] = x
    circle[:,1] = y
    circle[:,0] = z

    return circle
