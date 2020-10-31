#! /usr/bin/env python3
"""NAME
    ariship

DESCRIPTION
    A module for controling your airships' various cannons.

CLASSES
    Cannon

NOTES
    See the Cannon docstring
"""


import numpy as np


class Cannon():
    """
    Attributes
    ----------
    phi : float
        The azimuthal angle the cannon's barrel.
    theta : float
        The zenith angle the cannon's barrel.
    vel : float
        The velocity of an object as it leaves the barrel of the cannon.
    adjt : float
        The time it takes for the cannon to adjust.

    Notes
    -----
    Manually 

    This class can be used to take control of one of the airships'
    cannons. Do NOT use this unless you are authorised, or the fate of
    humanity depends on it. (Cannons are very dangerous)

    Examples
    --------
    >>> import airship
    >>> cannon = airship.Cannon(1234)
    >>> # "cannon" controls cannon number 1234

    """

    def __init__(self, serialnum):
        """
        Parameters
        ----------
        serialnum : int
            serial number of the cannon you would like to take control of

        """

        # set some attributes of the cannon
        self.num   = serialnum/100000
        self.phi   = 0
        self.theta = np.pi/4
        self.vel   = 20
        self.adjt  = .05

    def adjust(self, phipower, velpower):
        """Adjusts the cannon.

        This method adjusts azimuthal angle of the cannon, as well as a
        mechanism which determines the velocity of things launched from the
        cannon. The cannon's vel and phi attributes will be updated after
        phipower and velpower are sent to their respective systems.

        Parameters
        ----------
        phipower : float
            A float giving the amount of power to send to the motor
            controlling the azimuthal angle of the cannon's barrel.

        velpower : float
            A float giving the amount of power to send to the motor
            controling the velocity of objects launched.

        Returns
        -------
        None

        Examples
        --------
        >>> import airship
        >>> cannon = airship.Cannon(1234)
        >>> # print some of cannon's attributes before adjusting
        >>> print(cannon.phi)
        0
        >>> print(cannon.theta)
        0.7853981633974483
        >>> print(cannon.vel)
        20
        >>> cannon.adjust(2, 25)
        >>> # print the same attributes after adjusting
        >>> print(cannon.phi)
        1.9678528192
        >>> # cannon.theta should be unchanged
        >>> print(cannon.theta)
        0.7853981633974483
        >>> print(cannon.vel)
        22.732094751167295
        """

        # simulates a semi-random response to input in the phi motor
        dphi      = self.num**2 * phipower**5 - self.num * phipower**3 \
                    + phipower + self.num * 5
        self.phi += dphi

        if np.abs(dphi) > 2 * np.pi:

            # warns the user if the cannon begins to spin uncontrolably
            print("WARNING: phi motor rotated by mor than 2*pi in one time step")

        velpower /= 8

        # simulates a semi-random response to input in the vel motor
        self.vel += self.num**2 * velpower**5 - self.num * velpower**3 \
                    + velpower - 5 * self.num

        if self.vel < 0:
            self.vel = 0

        # If you made it here, you may have realised that this
        # function doesn't really control a cannon on an airship!!
        # Alas, the Furby apocalypse was fabricated to teach you to
        # code. Also, this function doesn't really take self.adjt
        # seconds to adjust, just pretend it does...
        return
