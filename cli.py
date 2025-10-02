from logging import DEBUG, INFO, WARN

from dpendulum_chg import *
from dpendulum_plotting import animate_double_pendulum

# Set inputs
inputs = {
    time: 0.,
    step: 0.02,
    g: 9.81,

    alpha_A: 0.,
    theta_A: 0.,
    omega_B: 0.,
    theta_B: -np.pi/8,


    driven_speed: np.pi/3,
    driven_period: 2,
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
    logging_level=DEBUG+2,
    search_depth=10000,
)

if t is None:
    print("No solutions found")
else:
    print(t)

# Animation
animate_double_pendulum(t, interval=30)