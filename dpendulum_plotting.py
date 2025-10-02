import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from constrainthg import TNode

def static_plot_double_pendulum(l_A: float, l_B: float,
                         theta_A: float, theta_B: float):
    """Plot a double pendulum in a given configuration."""
    xA = l_A * np.sin(theta_A)
    yA = -l_A * np.cos(theta_A)

    xB = xA + l_B * np.sin(theta_B)
    yB = yA - l_B * np.cos(theta_B)

    window_width = (l_A + l_B) * 1.1

    # Plot
    plt.figure(figsize=(5,5))
    plt.plot([0, xA], [0, yA], 'o-', lw=2, color="tab:blue")  # first rod
    plt.plot([xA, xB], [yA, yB], 'o-', lw=2, color="tab:orange")  # second rod


    
    plt.xlim(-window_width, window_width)
    plt.ylim(-window_width, window_width)
    plt.gca().set_aspect('equal', adjustable='box')
    plt.title("Driven Double Pendulum")
    plt.show()

def animate_double_pendulum(t: TNode=None, interval=50,
                            theta_As: list=None, theta_Bs: list=None,
                            l_A=1, l_B=1):
    """Animates a double pendulum in a given configuration."""
    if t is not None:
        theta_As = t.values.get('theta_A', [])
        theta_Bs = t.values.get('theta_B', [])
        l_A = t.values.get('l_A', [1.])[0]
        l_B = t.values.get('l_B', [1.])[0]

    window_width = (l_A + l_B) * 1.1

    fig, ax = plt.subplots(figsize=(5,5))
    ax.set_xlim(-window_width, window_width)
    ax.set_ylim(-window_width, window_width)
    ax.set_aspect('equal', adjustable='box')
    ax.set_title("Driven Double Pendulum")

    pendA, = ax.plot([], [], 'o-', lw=2, color="tab:blue")
    pendB, = ax.plot([], [], 'o-', lw=2, color="tab:orange")

    def update(index):
        theta_A, theta_B = theta_As[index], theta_Bs[index]
        xA = l_A * np.sin(theta_A)
        yA = -l_A * np.cos(theta_A)
        xB = xA + l_B * np.sin(theta_B)
        yB = yA - l_B * np.cos(theta_B)

        pendA.set_data([0, xA], [0, yA])
        pendB.set_data([xA, xB], [yA, yB])

        return pendA, pendB

    ani = FuncAnimation(fig, update,
                        frames=min(len(theta_As), len(theta_Bs)),
                        interval=interval,
                        blit=True)
    plt.show()

    return ani
