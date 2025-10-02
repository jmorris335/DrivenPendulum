from logging import DEBUG, INFO, WARN

from dpendulum_chg import *
from dpendulum_plotting import animate_double_pendulum

# Set inputs
inputs = {
    time: 0.,
    step: 0.01,
    g: 9.81,

    alpha_A: 0.,
    theta_A: 0.,
    omega_B: 0.,
    theta_B: -np.pi/4,

    driven_speed: 1.5,
    driven_period: 4,
}

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