#! /usr/bin/env python3

import circles
import matplotlib.pyplot as plt
import numpy as np

def plotsetup(pos_target, ax, rad_cannon=8, radii_target=(3, 7, 15)):
    """This function plots the the cannon and target and sets the
    appropriate z, y, and x limits on the plot
    
    Parameters
    ----------
    pos_target: touple
        This is the center of the circle passed in as a touple
        containing the coordinates in a (z, φ, ρ) fashion.
    ax: class
        Setup of plot from main:
        ax = fig.add_subplot(111, projection='3d')
    rad_cannon: int
        This is the radius of the cannon.
    radii_target: touple
        This is the radius of each target. There may be more or less
        than 3 targets so be careful not to restrict the code to only
        3 targets.

    References
    ----------
    Changing from cylindrical to Cartesian coordinates:
        z = z
        y = ρsin(φ) 
        x = ρcos(φ)

    matplotplotlib axis limiting:
        https://matplotlib.org/api/_as_gen/matplotlib.axes.Axes.set_xlim.html

    """

    # Converting cylindrical to cartesian coordinates
    z = pos_target[0] # z = z
    y = pos_target[2] * np.sin(pos_target[1]) # y = ρsin(φ)
    x = pos_target[2] * np.cos(pos_target[1]) # x = ρcos(φ)

    # Setting the limits of the plot by ± the maximum of the absolute
    # value of z and ρ coordinates of the target
    if pos_target[0] > pos_target[2]:
        limit = pos_target[0]
    else:
        limit = pos_target[2]

    ax.set_zlim(-limit, limit)
    ax.set_ylim(-limit, limit)
    ax.set_xlim(-limit, limit)  

    # Plotting cannon of radius rad_cannon around center of ax
    cannon = circles.xycircle((0, 0, 0), rad_cannon)
    ax.plot(cannon[:,2], cannon[:,1], cannon[:,0], label='cannon')

    # Plotting targets of radius radii_target assuming that there may
    # be more or less than 3 targets
    for radius in radii_target:
        target = circles.xycircle((z, y, x), radius)
        ax.plot(target[:,2], target[:,1], target[:,0], label='target')

    plt.title('Plot Setup')
    plt.legend()
    plt.savefig('plots/plotsetup.png')

def plottraj(traj, ax):
    """This function plots the the trajectory of a Furby
    
    Parameters
    ----------
    traj: touple
        This is an touple of positions at a certain time calculated in
        trajectory.py. This touple holds the components of those
        positions in (z, y, x)
    ax: class
        Setup of plot from main:
        ax = fig.add_subplot(111, projection='3d')

    """

    ax.plot(traj[2], traj[1], traj[0], label='trajectory')
    plt.title('Plot Trajectory')
    plt.legend()
    plt.savefig('plots/trajectory.png')
