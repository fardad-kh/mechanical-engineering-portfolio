# Validation report

Validated on October 7, 2026 with Python, NumPy 2.5.1, SciPy 1.18.0, and Matplotlib 3.11.0 in the available environment. Dependency ranges in requirements.txt are supported installation targets; they are not an exact reproducibility lock or a claim that every combination was tested.

## Measured default displacement errors

| Damping ratio | Maximum absolute numerical–analytical difference (m) |
|---:|---:|
| 0.1 | 1.58e-11 |
| 1.0 | 9.54e-13 |
| 2.0 | 1.06e-11 |

All five test methods passed:

- Analytical agreement and initial conditions for damping ratios 0, 0.1, 1, and 2 (displacement error below 1e-8 m).
- Nonzero initial velocity of -0.25 m/s in all three damped regimes (error below 1e-8 m).
- Nonincreasing damped energy within 1e-10 J per output interval, with integrated dissipation balance residual below 1e-6 J.
- Undamped energy conservation within 1e-8 J.
- Rejection of negative or nonfinite damping ratios.

The complete script ran with a noninteractive plot backend and saved all four PNGs. The displacement comparison was visually inspected. Automated checks do not certify a real device, arbitrary parameter ranges, or near-critical analytical conditioning.

## Changes from the uploads

The original parameter values, solver, damping cases, four plots, and sweep are retained. Execution is guarded so importing the model does not create figures. Output paths are anchored to the script; command-line options allow headless execution and an alternate destination. Analytical formulas now include initial velocity in every regime, and invalid damping ratios are rejected. Both original files are preserved for comparison.
