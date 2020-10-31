#! /usr/bin/env python3

import airship
import matplotlib.pyplot as plt
import numpy as np
import trajectory as traj

def piditer(error, i, dt, kp, ki, kd):
    """This function takes in an array of errors at each time step, a
    current time step index, a time step length, and PID k values and
    returns a PID output value ui
    
    Parameters
    ----------
    error: array
        This is an array of errors
    i: int
        This is the index at which to access the array of errors
    dt: int
        This is the time step length
    kp: float
        This is the proportional gain
    ki: float
        This is the integral gain
    kd: float
        This is the derivative gain

    References
    ----------
    For calculating the PID:
        ui = Pi + Ii + Di where i is the index

    For summing values in an array, np.sum was utilized:
        https://docs.scipy.org/doc/numpy/reference/generated/numpy.sum.html

    Examples
    --------
    >>>print('\nPID Iteration:', piditer(np.arange(10), 5, 1, 1.5, 1.5, 1.5)):
    PID Iteration: 31.5

    """

    # proportional term: Pi = Kpei
    P = kp * error[i]

    # integral term: Ii = Kidt∑ej
    I = ki * dt * np.sum([ele for ele in error if ele <= error[i]])

    # derivative term: Di = Kd (ei-e(i-1) / dt)
    if i != 0:
        D = kd * ((error[i] - error[i-1]) / dt)
    else:
        D = 0

    U = P + I + D

    return U

def pid(cannon, ax, pos_target, v_wind=np.zeros(3), steps=50,
    k_phi=(1.7,1.5,.00125), k_rho=(.25,1.5,.005)):
    """This function acts as a proportional-integral-derivative
    controller for the cannon.
    
    Parameters
    ----------
    cannon: object instance
        This is an instance of the Cannon class found in airship.py
    ax: class
        Setup of plot from main:
        ax = fig.add_subplot(111, projection='3d')
    pos_target: touple
        This is the center of the circle passed in as a touple
        containing the coordinates in a (z, φ, ρ) fashion.
    v_wind: touple
        This is the wind velocity in cartesian (z, y, x) coordinates.
        For calculating the trajectory without wind, we will not be
        utilizing this
    steps: int
        This is the amount of points we want each component to have. 
        This will be utilized by using numpy linspace to make an even
        amount of steps from 0 to time
    k_phi: touple
        This is the PID gains ordered in (kp,ki,kd) order
    k_rho: touple
        This is the PID gains in rho

    Examples
    --------
    >>>errors = pidf.pid(cannon, ax, pos_target, v_wind)
    >>>print(errors)
    (array([[ 1.23400000e+00, -8.91713604e-01,  6.20928620e-01,
        -5.02740626e-01,  4.05043549e-01, -2.95431213e-01, ...

    """

    # Creation of the two arrays to be returned
    error_vals = np.zeros(2*steps).reshape(2,steps)
    pwr_sigs = np.zeros(2*steps).reshape(2,steps)

    i = 0
    for step in range(steps):
        trajectory = traj.calctrajectory(cannon, v_wind)
        ax.plot(trajectory[2], trajectory[1], trajectory[0], 
            color=plt.cm.viridis(i/steps))
        landingpos = traj.landingpos(trajectory, pos_target[0])

        phi_error = pos_target[1] - landingpos[0]
        rho_error = pos_target[2] - landingpos[1]
        # if error > π: -2π | if error < π: +2π
        if phi_error > np.pi:
            phi_error -= 2*np.pi
        elif phi_error < -np.pi:
            phi_error += 2*np.pi
        error_vals[0,i] = phi_error
        error_vals[1,i] = rho_error

        phipower = piditer(error_vals[0], i, cannon.adjt, k_phi[0], k_phi[1], 
            k_phi[2])
        velpower = piditer(error_vals[1], i, cannon.adjt, k_rho[0], k_rho[1], 
            k_rho[2])
        pwr_sigs[0,i] = phipower
        pwr_sigs[1,i] = velpower

        i += 1

        cannon.adjust(phipower, velpower)

    return (error_vals, pwr_sigs)
