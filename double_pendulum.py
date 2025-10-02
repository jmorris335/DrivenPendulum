from constrainthg import Hypergraph, Node
import constrainthg.relations as R
import numpy as np

# Nodes
g = Node('g', 9.81, description='gravitataional acceleration (m/s^2)')
step = Node('step', 0.1, description='time step (s)')
time = Node('time', description='current time in simulation (s)')
end_time = Node('end_time', 1.0, description='maximum time in simulation (s)')

thetaA = Node('thetaA', description='angular position (rad)')
thetadotA = Node('omegaA', description='angular velocity (rad/s)')
thetaddotA = Node('alphaA', description='angular acceleration (rad/s^2)')
rA = Node('rA', description='length of tether (m)')
mA = Node('massA', description='mass of bob (kg)')

thetaB = Node('thetaB', description='angular position (rad)')
thetadotB = Node('omegaB', description='angular velocity (rad/s)')
thetaddotB = Node('alphaB', description='angular acceleration (rad/s^2)')
rB = Node('rB', description='length of tether (m)')
mB = Node('massB', description='mass of bob (kg)')

mu = Node('mu', description='mass ratio')


# Relationships
def Rdouble_thetaddotA(thetaA, thetaB, thetadotA, thetadotB, mu, rA, rB, g, **kwargs)-> float:
    '''Equation of motion for angular acceleration (thetaddot).'''
    diff = thetaA - thetaB
    numer = g * (np.sin(thetaB) * np.cos(diff) - mu * np.sin(thetaA))
    numer -= (rB * thetadotB**2 + rA * thetadotA**2 * np.cos(diff)) * np.sin(diff)
    denom = rA * (mu - np.cos(diff)**2)
    thetaddot = numer / denom
    return thetaddot

def Rdouble_thetaddotB(thetaA, thetaB, thetadotA, thetadotB, mu, rA, rB, g, **kwargs)-> float:
    '''Equation of motion for angular acceleration (thetaddot).'''
    diff = thetaA - thetaB
    numer = g * (np.sin(thetaA) * np.cos(diff) - np.sin(thetaB))
    numer += mu * np.sin(diff) + (rB * thetadotA**2 + rA * thetadotB**2 * np.cos(diff))
    denom = rB * (mu - np.cos(diff)**2)
    thetaddot = numer / denom
    return thetaddot

def Rdouble_via(thetaA_i: int, thetaB_i: int, thetadotA_i: int, thetadotB_i: int, **kwargs)-> bool:
    valid = all(thetaA_i == i for i in [thetaB_i, thetadotA_i, thetadotB_i])
    return valid

def Rmu(mA: float, mB: float, **kwargs)-> float:
    '''Equation for mass ratio coefficient.'''
    mu = 1 + (mA / mB)
    return mu

def Reuler(base: float, slope: float, step: float, **kwargs):
    '''First order Eulerian integration.'''
    integrated = base + slope * step
    return integrated

def Reuler_via(base_idx: int, slope_idx: int, **kwargs):
    '''Only valid if the base and slope have the same index.'''
    valid = base_idx == slope_idx - 1
    return valid

## Edges
hg = Hypergraph()
hg.add_edge({'thetaA': thetaA, 'thetaA_i': ('thetaA', 'index'),
             'thetaB': thetaB, 'thetaB_i': ('thetaB', 'index'),
             'thetadotA': thetadotA, 'thetadotA_i': ('thetadotA', 'index'),
             'thetadotB': thetadotB, 'thetadotB_i': ('thetadotB', 'index'),
             'rA': rA, 'rB': rB, 'mu': mu, 'g': g},
             thetaddotA, Rdouble_thetaddotA, via=Rdouble_via, index_offset=1)

hg.add_edge({'base': thetadotA, 'slope': thetaddotA, 'step': step,
             'base_idx': ('base', 'index'), 'slope_idx': ('slope', 'index')}, 
             thetadotA, Reuler, via=Reuler_via)

hg.add_edge({'base': thetaA, 'slope': thetadotA, 'step': step,
             'base_idx': ('base', 'index'), 'slope_idx': ('slope', 'index')}, 
             thetaA, Reuler, via=Reuler_via)

hg.add_edge({'thetaA': thetaA, 'thetaA_i': ('thetaA', 'index'),
             'thetaB': thetaB, 'thetaB_i': ('thetaB', 'index'),
             'thetadotA': thetadotA, 'thetadotA_i': ('thetadotA', 'index'),
             'thetadotB': thetadotB, 'thetadotB_i': ('thetadotB', 'index'),
             'rA': rA, 'rB': rB, 'mu': mu, 'g': g},
             thetaddotB, Rdouble_thetaddotB, via=Rdouble_via, index_offset=1)

hg.add_edge({'base': thetadotB, 'slope': thetaddotB, 'step': step,
             'base_idx': ('base', 'index'), 'slope_idx': ('slope', 'index')}, 
             thetadotB, Reuler, via=Reuler_via)

hg.add_edge({'base': thetaB, 'slope': thetadotB, 'step': step,
             'base_idx': ('base', 'index'), 'slope_idx': ('slope', 'index')}, 
             thetaB, Reuler, via=Reuler_via)

hg.add_edge({'mA': mA, 'mB': mB}, mu, Rmu)

hg.add_edge({'time': time, 'step': step}, time, R.Rsum, index_offset=1)


# Simulation
inputs = {
    time: 0.,
    thetaA: np.pi/4,
    thetadotA: 0,
    rA: 1.,
    mA: 1.,
    thetaB: -np.pi/4,
    thetadotB: 0,
    rB: 1.,
    mB: 1.,
}

hg.add_edge({'out': thetaA, 'idx': ('out', 'index')}, 
            'final_node', R.equal('out'),
             via=R.geq('idx', 20))

t, final_values = hg.solve('final_node', node_values=inputs, to_print=False, search_depth=1000)
print(t)

# import matplotlib.pyplot as plt
# y1 = final_values['thetaA']
# y2 = final_values['thetaB']
# time_vals = [0.0 + step.static_value * i for i in range(len(y1))]

# plt.plot(time_vals[:len(y1)], y1)
# plt.plot(time_vals[:len(y2)], y2)
# plt.show()