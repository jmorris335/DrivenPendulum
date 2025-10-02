'''
Name: dpendulum_chg.py
Author: John Morris, jhmmrs@clemson.edu, ORCID: 0009-0005-6571-1959
Date: 2 Oct 2025
Purpose: CHG system model for driven double pendulum
Rights: MIT License
'''

from constrainthg import Hypergraph, Node
import constrainthg.relations as R

from dpendulum_rels import *

chg = Hypergraph(no_weights=True)

# NODES
## Environment Parameters
g = chg.add_node(Node('g', units='m/s^2'))
time = chg.add_node(Node('time', units='s'))
step = chg.add_node(Node('step', units='s'))

## Physical Parameters
l_A = chg.add_node(Node('l_A', units='m'))
l_B = chg.add_node(Node('l_B', units='m'))

## Rotational Dynamics
theta_A = chg.add_node(Node('theta_A', units='rad'))
omega_A = chg.add_node(Node('omega_A', units='rad/s'))
alpha_A = chg.add_node(Node('alpha_A', units='rad/s^2'))

theta_B = chg.add_node(Node('theta_B', units='rad'))
omega_B = chg.add_node(Node('omega_B', units='rad/s'))
alpha_B = chg.add_node(Node('alpha_B', units='rad/s^2'))

driven_speed = chg.add_node(Node('driven_speed', units='rad/s'))
driven_period = chg.add_node(Node('driven_period', units='s'))

## Translational Dynamics for Bottom Pendulum (B)
x_B = chg.add_node(Node('x_B', units='m'))
xdot_B = chg.add_node(Node('xdot_B', units='m/s'))
xddot_B = chg.add_node(Node('xddot_B', units='m/s^2'))

y_B = chg.add_node(Node('y_B', units='m'))
ydot_B = chg.add_node(Node('ydot_B', units='m/s'))
yddot_B = chg.add_node(Node('yddot_B', units='m/s^2'))

# RELATIONSHIPS
# chg.add_edge(
#     {'g': g,
#      'l': l_A,
#      'theta': theta_A},
#     target=alpha_A,
#     rel=Rsimple_angular_accel,
#     disposable=['theta'],
#     label='simple_pend_A',
# )
# chg.add_edge(
#     {'g': g,
#      'l': l_B,
#      'theta': theta_B},
#     target=alpha_B,
#     rel=Rsimple_angular_accel,
#     disposable=['theta'],
#     label='simple_pend_B',
# )
chg.add_edge(
    {'alpha': alpha_A,
     'omega': omega_A,
     'theta': theta_A},
    target=xddot_B,
    rel=Rhorizontal_accel,
    index_via=lambda omega, theta, alpha, **kw : R.Rsame(omega, theta, alpha),
    disposable=['alpha', 'omega', 'theta'],
    label='horizontal_accel_B',
)
chg.add_edge(
    {'alpha': alpha_A,
     'omega': omega_A,
     'theta': theta_A},
    target=yddot_B,
    rel=Rvertical_accel,
    index_via=lambda omega, theta, alpha, **kw : R.Rsame(omega, theta, alpha),
    disposable=['alpha', 'omega', 'theta'],
    label='vertical_accel_B',
)
chg.add_edge(
    {'xddot': xddot_B,
     'yddot': yddot_B,
     'theta': theta_B,
     'g': g},
    target=alpha_B,
    rel=Raccel_translating_base,
    index_via=lambda xddot, yddot, theta, **kw : R.Rsame(xddot, yddot, theta),
    disposable=['xddot', 'yddot', 'theta'],
    label='angular_accel_translating_base_B'
)
chg.add_edge(
    {'time': time,
     'period': driven_period,
     "speed": driven_speed},
    target=omega_A,
    rel=Rdriven_velocity,
    disposable=['time'],
    label='driven_velocity_A',
)
chg.add_edge(omega_A, 'prev_omega_A', R.Rfirst)
chg.add_edge(
    {'y2': omega_A,
     'y1': 'prev_omega_A',
     'step': step},
    target=alpha_A,
    rel=Rdifferentiate,
    index_via=Rdifferentiate_via,
    disposable=['y2', 'y1'],
    label='differentiate_omega_A->alpha_A'
)
# chg.add_edge(
#     {'base': omega_A,
#      'slope': alpha_A,
#      'step': step},
#     target=omega_A,
#     rel=Reuler,
#     index_via=Reuler_via,
#     disposable=['base', 'slope'],
#     index_offset=1,
#     label='integrating_omega_A',
# )
chg.add_edge(
    {'base': theta_A,
     'slope': omega_A,
     'step': step},
    target=theta_A,
    rel=Reuler,
    index_via=Reuler_via,
    disposable=['base', 'slope'],
    index_offset=1,
    label='integrating_omega_A->theta_A',
)
chg.add_edge(
    {'base': omega_B,
     'slope': alpha_B,
     'step': step},
    target=omega_B,
    rel=Reuler,
    index_via=Reuler_via,
    disposable=['base', 'slope'],
    index_offset=1,
    label='integrating_alpha_B->omega_B',
)
chg.add_edge(
    {'base': theta_B,
     'slope': omega_B,
     'step': step},
    target=theta_B,
    rel=Reuler,
    index_via=Reuler_via,
    disposable=['base', 'slope'],
    index_offset=1,
    label='integrating_omega_B->theta_B',
)
chg.add_edge({step, time}, time, R.Rsum, index_offset=1)
