# Disinformation Resilience Simulation

These are the simulated model for my papaer:
Modeling Disinformation Resilience: How Social Pressure and Network Dynamics Drive and Sustain the Spread of False Narratives.
Details about the experiments and the paper’s content will be disclosed upon acceptance.

# The structure

```model.py``` The script contains code of one round of diffusion simulation and the required formula

```execution.py``` The script contains the execution of the model and the output of the simulation, assigning the parameters to a single run given the user settings, and calling the simulation.  The functions will be called from ```model.py```.

# Usages

The default run of ```execution.py``` will output the single run result for $w=0.1$, $alpha=0.05$, $b1=3$, $b2=3$, $n_mali_act_1=0$, $n_mali_act_0=0$, $c=0.2$.

For other parameter settings, please modify the params dictionary list at the ```simulate_information_cascade``` function.

