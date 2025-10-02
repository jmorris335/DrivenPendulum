from logging import DEBUG, INFO, WARN

from dpendulum_chg import *

# Set inputs
inputs = {
    time: 0.,
    step: 0.1,
    g: 9.81,

    alpha_A: 0.,
    theta_A: 0.,
    theta_B: np.pi/4,
    omega_B: 0.,

    driven_speed: np.pi/4,
    driven_period: 4,
}

# Optional nodes and edges to debug
debug_nodes = ['alpha_B'] if False else None
debug_edges = ['angular_accel_translating_base_B'] if False else None

# Simulate the CHG
t = chg.solve(
    target=theta_B,
    inputs=inputs,
    min_index=3,
    debug_nodes=debug_nodes,
    debug_edges=debug_edges,
    to_print=True,
    logging_level=WARN,
)

if t is None:
    print("No solutions found")
else:
    print(t)