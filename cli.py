from logging import DEBUG, INFO, WARN

from dpendulum_chg import *
from dpendulum_plotting import animate_double_pendulum

# Set inputs
inputs = dict(
    time=0.,            #s
    step=0.02,          #s
    g=9.81,             #m/s^2

    alpha_A=0.,         #rad/s^2
    theta_A=0.,         #rad
    omega_B=0.,         #rad/s
    theta_B=-0.3,       #rad

    driven_speed=1.2,   #rad/s
    driven_period=2,    #s
)

# Optional nodes and edges to debug
debug_nodes = ['alpha_B'] if False else None
debug_edges = ['angular_accel_translating_base_B'] if False else None

# Simulate the CHG
t = chg.solve(
    target=theta_B,
    inputs=inputs,
    min_index=1000,
    debug_nodes=debug_nodes,
    debug_edges=debug_edges,
    to_print=False,
    logging_level=INFO,
)

if t is None:
    print("No solutions found")
else:
    print(t)


# Animation
animate_double_pendulum(t, interval=10)