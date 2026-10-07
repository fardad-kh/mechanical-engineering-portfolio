# Damped Mass-Spring System: Numerical vs Analytical

A single-degree-of-freedom vibration model solved two ways in Python, then compared.

**Governing equation** (x measured from static equilibrium):

    m x'' + c x' + k x = 0

Rewritten as a first-order system and integrated with `scipy.integrate.odeint`:

    dx/dt = v
    dv/dt = -(c/m) v - (k/m) x

The numerical result is checked against the closed-form solution for each damping regime
(damping ratio `zeta = c / (2 sqrt(k m))`):

| Regime | Condition | Behavior |
|---|---|---|
| Underdamped | zeta < 1 | Decaying oscillation at the damped frequency |
| Critically damped | zeta = 1 | Fastest return to equilibrium, no overshoot |
| Overdamped | zeta > 1 | Slow exponential return, no oscillation |

## Run it

    conda create -n engineering python=3.11 numpy scipy matplotlib
    conda activate engineering
    python mass_spring_damper.py

## What it produces (`figures/`)

1. Displacement vs time, numerical (lines) over analytical (dots)
2. Phase portrait (velocity vs displacement)
3. Mechanical energy decay (log scale)
4. Response sweep across damping ratios

## Results

Numerical and analytical solutions agree to within the solver tolerance (see terminal output for max error per case).

## What I learned / next steps

- Why a second-order ODE becomes two first-order ODEs for a numerical solver
- How damping ratio alone determines the response shape
- Next: forced vibration and resonance, then the same model in MATLAB (`ode45`) and a comparison of the two
