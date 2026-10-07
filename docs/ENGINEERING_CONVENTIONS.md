# Engineering conventions

For each calculation, define the system boundary, coordinate direction, known data with units, desired result, and model assumptions. Use SI internally; show conversions before substitution. Write equations in standard LaTeX, with symbols defined beside their first use.

Show the conceptual framework first. For calculus, include differentiation or integration steps and constants or boundary conditions. For vector mechanics, state axes, components, signs, and the force or moment balance. For thermodynamics, identify the system, state variables, property source, phase region, and energy balance before evaluating a state.

Before numerical or iterative work, state the approximation, initial guess if relevant, convergence criterion, tolerances, and failure conditions. Distinguish local solver controls from measured global errors. Carry units through intermediate expressions, and interpret the final answer physically.

Ask learning questions before revealing results: Which quantity should be conserved? What limiting case can check the model? Does the sign make physical sense? What assumption could fail in the experiment?

For future CAD/FEA studies, document geometry, material model, loads, restraints, mesh convergence, and comparison with hand calculations. For fluid mechanics, state flow assumptions and applicable dimensionless groups. Never substitute software output for validation.
