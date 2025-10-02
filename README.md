# Driven Double Pendulum Model
This repository contains a CHG model for a driven, double pendulum, primarily used for demonstration purposes.

![drivenpendulum](https://github.com/user-attachments/assets/41bb6179-28b2-4c4c-bd18-62e374f9f730)


## Running the package
### Installation
This package is built on [ConstraintHg](https://constrainthg.readthedocs.io/en/latest/index.html), which is available on the Python Package Index. You can install this using PIP after creating a virtual environment:

```
pip install constrainthg
```

### Setup
After that, you can execute the model via the caller interface (`cli.py`). That script allows you to set the inputs and setup the pendulum simulation.

The model has 8 different functions found in `depndulum_rels.py`. These map between the XX variables in the system, forming XX edges, as given in `dpendulum_chg.py`.

To simulat the model, you have to provide several inputs. The most common set of inputs is:

```python
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
```

### Simulation
These can then be passed to ConstraintHg to form a simulation. To do this, call:

```python
t = chg.solve(<target>, inputs)
```

where `<target>` is the Node you want to simulate.

### Animation
You can also animate the simulation by calling the `animate_double_pendulum` function in `dpendulum_plotting.py`. The primary argument for this function is the output (`t`) from `chg.solve()`. This output contains the values of all the solved variables in the simulation path. As long as the simulation path contained all the angular positions for the two pendulums, you should be able to pass this node to the function to produce an animation similar to the one at the top.

## Licensing
For questions, comments, or help, check out the [discussion board](https://github.com/jmorris335/ConstraintHg/discussions) for ConstraintHg.
Author: [John Morris](https://orcid.org/0009-0005-6571-1959)
License: MIT License
