#! /usr/bin/env python3

import numpy as np

def calctrajectory(cannon, v_wind, time=10, steps=1000, k=.003):
    """This function calculates the trajectory of a Furby. There are
    two methods in which we can calculate the trajectory, one with
    wind, the other without wind. For this, we will be using without
    wind for the sake of simplicity.
    
    Parameters
    ----------
    cannon: object instance
        This is an instance of the Cannon class found in airship.py
    v_wind: touple
        This is the wind velocity in cartesian (z, y, x) coordinates.
        For calculating the trajectory without wind, we will not be
        utilizing this
    time: int
        This is the amount of time the Furby will be in the air
    steps: int
        This is the amount of points we want each component to have. 
        This will be utilized by using numpy linspace to make an even
        amount of steps from 0 to time
    k: float
        This is the Furby's mass. For calculating the trajectory
        without wind, we will not be utilizing this

    References
    ----------
    For finding the inital velocity, we need to get the components of a
    vector in Cartesian coordinates. To do this, we can use the
    following formulae:
    vz = vcos(θ) | vy = vsin(θ)sin(φ) | vx = vsin(θ)cos(φ)

    Once we have the velocity in Cartesian, we can then substitute
    those values in to find the final position in each component:
    z(t) = z(0) + vzt − .5gt^2 | y(t) = y(0) + vyt | x(t) = x(0) + vxt

    Examples
    --------
    >>>traj = trajectory.calctrajectory(cannon, v_wind)
    >>>print('\nFirst 5 elements of z traj:\n', traj[0][0:5])
    >>>print('\nFirst 5 elements of y traj:\n', traj[1][0:5])
    >>>print('\nFirst 5 elements of x traj:\n', traj[2][0:5])
    First 5 elements of z traj:
     [0.         0.14107194 0.28116191 0.42026992 0.55839597]

    First 5 elements of y traj:
     [0. 0. 0. 0. 0.]

    First 5 elements of x traj:
     [0.         0.14156292 0.28312584 0.42468876 0.56625168]

    """

    # constants
    g = 9.8                         # gravitational acceleration
    theta = cannon.theta            # theta attribute of cannon
    phi = cannon.phi                # phi attribute of cannon
    vel = cannon.vel                # velocity attribute of cannon
    t = np.linspace(0, time, steps) # time spaced evenly from 0 to time in
                                    # n number of steps

    # Inital velocity
    vz = vel * np.cos(theta)               # vz = vcos(Θ)
    vy = vel * np.sin(theta) * np.sin(phi) # vy = vsin(Θ)sin(φ)
    vx = vel * np.sin(theta) * np.cos(phi) # vx = vsin(Θ)cos(φ)

    # Final position of Furby after time seconds
    zt = (vz * t) - (.5 * g * t**2) # z(t) = z(0) + vt - .5gt^2
    yt = vy * t                     # y(t) = y(0) + vt
    xt = vx * t                     # x(t) = x(0) + vt

    return (zt, yt, xt)

def landingpos(traj, z_target):
    """This function takes an array of positions, traj, and the z
    component of the target's position, z_target, and returns the
    azimuthal angle of the landing position and the distance in the xy
    plane from the cannon to the location where the Furby first goes
    below z_target level
    
    Parameters
    ----------
    traj: touple
        This is a touple of the trajectory of the Furby calculated from
        the function above, calctrajectory, where the return is in a
        order of (zt, yt, xt)
    z_target: int
        This is the z position of the target

    References
    ----------
    For calculating the distance in the xy plane of the Furby from the
    cannon:
        ρ = 􏰁x2 + y2

    For calculating the azimuthal angle φ between -π and π:
        https://docs.scipy.org/doc/numpy/reference/generated/numpy.arctan2.html

    For finding the index in which the Furby first goes below z_target:
        https://docs.scipy.org/doc/numpy/reference/generated/numpy.where.html

    Examples
    --------
    >>>trajectory.landingpos(traj, pos_target[0]))
    (0.0, 70.07364498245065)

    """

    zpos = traj[0]
    ypos = traj[1]
    xpos = traj[2]

    # Finding the index in which the Furby first goes below z_target
    posi = np.where(z_target < zpos)[0][-1] + 1

    # Distance in the xy plane of the Furby from the cannon
    p = np.sqrt(xpos[posi-1]**2 + ypos[posi-1]**2)

    # φ is measured from the positive x-axis and goes counter-clockwise
    # (looking down) about the z axis
    azimuthal = np.arctan2(ypos[posi-1], xpos[posi-1])

    return (azimuthal, p)
