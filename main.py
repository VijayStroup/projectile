#! /usr/bin/env python3

import airship
import circles
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import plotting
import pidf
import trajectory

# Initialize a pyplot figure and a 3D subplot
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Creating an instance of Cannon so we can control it
cannon = airship.Cannon(1337)

# Target in cylindrical (z, φ, ρ) coordinates relative to cannon
pos_target = (-50, 1.234, 150)

# Wind velocity in cartesian (z, y, x) coordinates
v_wind = (-1.5, -1, 2)

# Testing out the xycircle function
print('Test of xycircle((0, 0, 0), 2, 5) call:')
print(circles.xycircle((0, 0, 0), 2, 5))

# Plotting cannon and targets
plotting.plotsetup(pos_target, ax)

# Calculating trajectory of cannon
traj = trajectory.calctrajectory(cannon, v_wind)
print('\nFirst 5 elements of z traj:\n', traj[0][0:5])
print('\nFirst 5 elements of y traj:\n', traj[1][0:5])
print('\nFirst 5 elements of x traj:\n', traj[2][0:5])

# Plotting the trajectory of the Furby
plotting.plottraj(traj, ax)

# Landing position of Furby
print('\nCalling landingpos(traj, pos_target[0]):\n',
    trajectory.landingpos(traj, pos_target[0]))

# PID iteration
print('\nPID Iteration:', pidf.piditer(np.arange(10), 5, 1, 1.5, 1.5, 1.5))

# PID
errors = pidf.pid(cannon, ax, pos_target, v_wind)
plt.savefig('plots/furby_launches.png')

# Error plot
plt.clf()
plt.plot(errors[0][0], label='phi_error')
plt.plot(errors[0][1], label='rho_error')
plt.title('Phi and Rho Error')
plt.xlabel('Launch Number')
plt.ylabel('Error (unit)')
plt.legend()
plt.savefig('plots/phi_rho_error.png')

# Power plot
plt.clf()
plt.plot(errors[1][0], label='phipower')
plt.plot(errors[1][1], label='velpower')
plt.title('Phipower and Velpower Sent')
plt.xlabel('Launch Number')
plt.ylabel('Power (unit)')
plt.legend()
plt.savefig('plots/phi_vel_power.png')
