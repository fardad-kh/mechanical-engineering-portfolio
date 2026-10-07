"""
Damped Mass-Spring System: Numerical vs Analytical Solution
Author: Fardad Khondakar

Model (x measured from static equilibrium, down is positive):
    m*x'' + c*x' + k*x = 0

Rewritten as two first-order ODEs for the solver:
    dx/dt = v
    dv/dt = -(c/m)*v - (k/m)*x

Useful quantities:
    wn   = sqrt(k/m)              natural frequency (rad/s)
    zeta = c / (2*sqrt(k*m))      damping ratio (dimensionless)
    wd   = wn*sqrt(1 - zeta^2)    damped frequency (only if zeta < 1)

Run:  python mass_spring_damper.py
"""

import argparse
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint

# ---------------------------------------------------------------- parameters
m = 1.0            # mass (kg)
k = 40.0           # spring stiffness (N/m)
x0, v0 = 0.10, 0.0 # pulled down 0.10 m, released from rest
t = np.linspace(0, 3, 3000)  # time grid (s)

wn = np.sqrt(k / m)

# three damping regimes, defined by damping ratio zeta
cases = {
    "Underdamped (zeta=0.1)":       0.1,
    "Critically damped (zeta=1.0)": 1.0,
    "Overdamped (zeta=2.0)":        2.0,
}
colors = ["tab:blue", "tab:green", "tab:red"]


# ------------------------------------------------------------ numerical ODE
def make_rhs(c):
    def rhs(state, t):
        x, v = state
        return [v, -(c / m) * v - (k / m) * x]
    return rhs


def solve_numeric(zeta):
    if not np.isfinite(zeta) or zeta < 0:
        raise ValueError("Damping ratio must be finite and nonnegative.")
    c = 2 * zeta * np.sqrt(k * m)
    sol = odeint(make_rhs(c), [x0, v0], t, rtol=1e-10, atol=1e-12)
    return sol[:, 0], sol[:, 1]


# -------------------------------------------------------- analytical (general initial velocity)
def solve_analytic(zeta):
    if not np.isfinite(zeta) or zeta < 0:
        raise ValueError("Damping ratio must be finite and nonnegative.")
    if zeta < 1:      # underdamped: decaying cosine
        wd = wn * np.sqrt(1 - zeta**2)
        return np.exp(-zeta * wn * t) * (
            x0 * np.cos(wd * t) + ((v0 + zeta * wn * x0) / wd) * np.sin(wd * t))
    if zeta == 1:     # critical: fastest return with no overshoot
        return (x0 + (v0 + wn * x0) * t) * np.exp(-wn * t)
    # overdamped: two real decaying exponentials
    s1 = -wn * (zeta - np.sqrt(zeta**2 - 1))
    s2 = -wn * (zeta + np.sqrt(zeta**2 - 1))
    return ((v0 - s2 * x0) * np.exp(s1 * t) + (s1 * x0 - v0) * np.exp(s2 * t)) / (s1 - s2)


def main(output_dir=None, show=True):
    """Generate the four original comparisons; quantities use SI units."""
    output_dir = Path(output_dir) if output_dir else Path(__file__).parent / "figures"
    
    output_dir.mkdir(parents=True, exist_ok=True)
    results = {}
    print(f"m = {m} kg, k = {k} N/m, wn = {wn:.3f} rad/s, "
          f"undamped period = {2*np.pi/wn:.3f} s\n")
    
    for (name, zeta) in cases.items():
        x_num, v_num = solve_numeric(zeta)
        x_ana = solve_analytic(zeta)
        err = np.max(np.abs(x_num - x_ana))
        results[name] = (x_num, v_num, x_ana)
        print(f"{name:32s} max |numeric - analytic| = {err:.2e} m")
    
    # ------------------------------------------- figure 1: displacement vs time
    fig, ax = plt.subplots(figsize=(9, 5))
    for (name, _), col in zip(cases.items(), colors):
        x_num, _, x_ana = results[name]
        ax.plot(t, x_num, color=col, lw=2, label=f"{name} - numerical")
        ax.plot(t[::120], x_ana[::120], "o", color=col, ms=5,
                label=f"{name} - analytical")
    ax.axhline(0, color="k", lw=0.8, ls="--", alpha=0.4)
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Displacement from equilibrium (m)")
    ax.set_title("Damped mass-spring: numerical (lines) vs analytical (dots)")
    ax.legend(fontsize=7, ncol=1)
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    fig.savefig(output_dir / "1_displacement.png", dpi=200)
    
    # ------------------------------------------------ figure 2: phase portrait
    fig, ax = plt.subplots(figsize=(6, 6))
    for (name, _), col in zip(cases.items(), colors):
        x_num, v_num, _ = results[name]
        ax.plot(x_num, v_num, color=col, lw=2, label=name)
        ax.plot(x_num[0], v_num[0], "ko")
    ax.set_xlabel("Displacement x (m)")
    ax.set_ylabel("Velocity v (m/s)")
    ax.set_title("Phase portrait (black dot = start)")
    ax.legend(fontsize=8)
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    fig.savefig(output_dir / "2_phase_portrait.png", dpi=200)
    
    # ----------------------------------------------- figure 3: energy decay
    fig, ax = plt.subplots(figsize=(9, 5))
    for (name, _), col in zip(cases.items(), colors):
        x_num, v_num, _ = results[name]
        E = 0.5 * m * v_num**2 + 0.5 * k * x_num**2
        ax.semilogy(t, E, color=col, lw=2, label=name)
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Total mechanical energy (J)")
    ax.set_title("Energy dissipated by damping (log scale)")
    ax.legend(fontsize=8)
    ax.grid(True, alpha=0.3, which="both")
    fig.tight_layout()
    fig.savefig(output_dir / "3_energy.png", dpi=200)
    
    # ------------------------------------ figure 4: parameter sweep over zeta
    fig, ax = plt.subplots(figsize=(9, 5))
    for z in [0.05, 0.2, 0.5, 0.8, 1.0, 1.5]:
        x_num, _ = solve_numeric(z)
        ax.plot(t, x_num, lw=1.8, label=f"zeta = {z}")
    ax.axhline(0, color="k", lw=0.8, ls="--", alpha=0.4)
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Displacement (m)")
    ax.set_title("Effect of damping ratio on response")
    ax.legend(fontsize=8)
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    fig.savefig(output_dir / "4_zeta_sweep.png", dpi=200)
    
    print(f"\nSaved 4 figures to {output_dir}")
    if show:
        plt.show()
    else:
        plt.close("all")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--no-show", action="store_true", help="Save figures without opening windows")
    parser.add_argument("--output-dir", type=Path, help="Override figure destination")
    args = parser.parse_args()
    main(args.output_dir, show=not args.no_show)
