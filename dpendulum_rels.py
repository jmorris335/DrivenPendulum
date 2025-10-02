'''
Name: dpendulum_rels.py
Author: John Morris
Date: 2 Oct 2025
Purpose: Relationships for driven double pendulum CHG
Rights: MIT License
'''

import constrainthg.relations as R

import numpy as np

def Rsimple_angular_accel(g: float, l: float, theta: float, *ar, **kw)-> float:
    """Calculates angular acceleration of an simple, undamped pendulum."""
    alpha = g / l * np.sin(theta)
    return alpha

def Rhorizontal_accel(alpha: float, omega: float, theta: float,
                      *ar, **kw)-> float:
    """Calculates horizontal acceleration of a pendulum's base when 
    attached to another pendulum. Assumes equivalent bob masses and 
    pendulum radii."""
    xddot = alpha * np.cos(theta) - omega**2 * np.sin(theta)
    return xddot

def Rvertical_accel(alpha: float, omega: float, theta: float,
                    *ar, **kw)-> float:
    """Calculates vertical acceleration of a pendulum's base when 
    attached to another pendulum. Assumes equivalent bob masses and 
    pendulum."""
    yddot = alpha * np.sin(theta) + omega**2 * np.cos(theta)
    return yddot

def Raccel_translating_base(xddot: float, yddot: float, theta: float, g: float,
                            *ar, **kw)-> float:
    """Calculates the angular acceleration of an undamped pendulum whose
    base is freely translating with a given acceleration. Assumes
    equivalent bob masses and pendulum radii."""
    alpha = -xddot * np.cos(theta) - np.sin(yddot + g)
    return alpha

def Rdriven_velocity(time: float, period: float, speed: float, 
                     *ar, **kw)-> float:
    """Calculates time-varying angular velocity of a driven pendlum."""
    swung_prop = (time % period) / period
    velocity = speed * (-1 if swung_prop > 0.5 else 1)
    return velocity

def Reuler(base: float, slope: float, step: float, **kwargs):
    """First order Eulerian integration."""
    integrated = base + slope * step
    return integrated

def Reuler_via(base: int, slope: int, **kwargs):
    '''Valid if the base and slope have the same index or are constant.'''
    return R.Rsame(base, slope)