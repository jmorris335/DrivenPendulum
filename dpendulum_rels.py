'''
Name: dpendulum_rels.py
Author: John Morris, jhmmrs@clemson.edu, ORCID: 0009-0005-6571-1959
Date: 2 Oct 2025
Purpose: Relationships for driven double pendulum CHG
Rights: MIT License
'''

import constrainthg.relations as R

import numpy as np

def Rsimple_angular_accel(g: float, l: float, theta: float, *ar, **kw)-> float:
    """Calculates angular acceleration of an simple, undamped pendulum."""
    alpha = -g / l * np.sin(theta)
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
    alpha = -xddot * np.cos(theta) - np.sin(theta) * (yddot + g)
    return alpha

def Rdriven_velocity(time: float, period: float, speed: float, 
                     *ar, **kw)-> float:
    """Calculates time-varying angular velocity of a driven pendlum."""
    swung_prop = (time % period) / period
    if swung_prop < 0.25 or swung_prop > 0.75:
        velocity = speed
    else:
        velocity = -speed
    return velocity

def Reuler(base: float, slope: float, step: float, *ar, **kw)-> float:
    """First order Eulerian integration."""
    integrated = base + slope * step
    return integrated

def Reuler_via(base: int, slope: int, *ar, **kw)-> bool:
    """Valid if the base and slope have the same index or are constant."""
    return R.Rsame(base, slope)

def Rdifferentiate(y2, y1, step, *ar, **kw)-> float:
    """Differentiates y with respect to a constant step."""
    diff = (y2 - y1) / step
    return diff

def Rdifferentiate_via(y2, y1, *ar, **kw)-> bool:
    """Valid if the two values are one index apart."""
    return y2 == y1 + 1