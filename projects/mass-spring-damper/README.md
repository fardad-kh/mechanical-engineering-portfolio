# Damped mass–spring system: numerical versus analytical

## Start with the physical questions

Before solving: What does $x=0$ mean? Which forces act on the mass? Should mechanical energy remain constant? Which initial conditions determine the response? Predict the qualitative response before looking at the plots.

## Assumptions and scope

- A lumped mass has one translational degree of freedom; downward is positive.
- The spring is linear, the damper is viscous, and $m$, $c$, and $k$ are constant.
- Motion is measured from static equilibrium. Gravity is already balanced by static spring extension and therefore cancels from the perturbation equation.
- No forcing, dry friction, nonlinear stiffness, or structural flexibility is modeled.
- Defaults: $m=1.0\,\mathrm{kg}$, $k=40.0\,\mathrm{N/m}$, $x_0=0.10\,\mathrm{m}$, $v_0=0\,\mathrm{m/s}$; $0\le t\le3\,\mathrm{s}$ sampled at 3000 output points.
- The adaptive numerical solver approximates the continuous trajectory. Output spacing is not its internal integration step. `odeint` uses LSODA, with relative tolerance $10^{-10}$ and absolute tolerance $10^{-12}$ in the SI-valued state components: metres for displacement and metres per second for velocity. These are local controls, not a global accuracy guarantee.

## 1. Force balance and units

With $x$ measured from equilibrium, the restoring and damping forces are $-kx$ and $-c\dot{x}$. Newton's second law gives

$$m\ddot{x}=-c\dot{x}-kx,$$

and hence

$$m\ddot{x}+c\dot{x}+kx=0.$$

Each term has force units:

$$[m\ddot{x}]=\mathrm{kg\,m/s^2}=\mathrm{N},\quad[c\dot{x}]=\mathrm{(N\,s/m)(m/s)}=\mathrm{N},\quad[kx]=\mathrm{(N/m)m}=\mathrm{N}.$$

## 2. Convert to a first-order system

Define $v=\dot{x}$, so

$$\dot{x}=v\quad[\mathrm{m/s}],$$

$$\dot{v}=-\frac{c}{m}v-\frac{k}{m}x\quad[\mathrm{m/s^2}].$$

Since $[c/m]=\mathrm{s^{-1}}$ and $[k/m]=\mathrm{s^{-2}}$, both acceleration terms have the required units. The initial state is $[x_0,v_0]^T$.

## 3. Natural frequency and damping ratio

Divide the force equation by $m$ and compare coefficients:

$$\ddot{x}+2\zeta\omega_n\dot{x}+\omega_n^2x=0,$$

$$\omega_n=\sqrt{k/m}=\sqrt{40\,\mathrm{s^{-2}}}=6.324555\,\mathrm{rad/s},$$

$$\zeta=\frac{c}{2\sqrt{km}},\qquad c=2\zeta\sqrt{km}.$$

Here radians and $\zeta$ are dimensionless. The undamped period is $T_n=2\pi/\omega_n=0.993459\,\mathrm{s}$. Critical damping is $c_{\mathrm{crit}}=12.649111\,\mathrm{N\,s/m}$.

| Case | $\zeta$ | $c$ ($\mathrm{N\,s/m}$) | Default release behavior |
|---|---:|---:|---|
| Underdamped | 0.1 | 1.264911 | Decaying oscillations |
| Critical | 1.0 | 12.649111 | Monotonic return |
| Overdamped | 2.0 | 25.298221 | Slower monotonic return |

## 4. Closed-form displacement

Substitute $x=e^{st}$ to obtain $s^2+2\zeta\omega_ns+\omega_n^2=0$. The roots determine three regimes.

For $0\le\zeta<1$, define $\omega_d=\omega_n\sqrt{1-\zeta^2}$ in $\mathrm{rad/s}$:

$$x=e^{-\zeta\omega_nt}(A\cos\omega_dt+B\sin\omega_dt).$$

At $t=0$, $A=x_0$. Differentiation gives $v_0=-\zeta\omega_nA+\omega_dB$, so

$$x(t)=e^{-\zeta\omega_nt}\left[x_0\cos\omega_dt+\frac{v_0+\zeta\omega_nx_0}{\omega_d}\sin\omega_dt\right].$$

For $\zeta=1$, the repeated root is $s=-\omega_n$:

$$x=(A+Bt)e^{-\omega_nt},\quad A=x_0,\quad v_0=B-\omega_nA,$$

$$x(t)=[x_0+(v_0+\omega_nx_0)t]e^{-\omega_nt}.$$

For $\zeta>1$, let $s_{1,2}=-\omega_n(\zeta\mp\sqrt{\zeta^2-1})$ in $\mathrm{s^{-1}}$:

$$x=Ae^{s_1t}+Be^{s_2t},\quad A+B=x_0,\quad s_1A+s_2B=v_0,$$

$$A=\frac{v_0-s_2x_0}{s_1-s_2},\quad B=\frac{s_1x_0-v_0}{s_1-s_2}.$$

Coefficients multiplying dimensionless exponentials or trigonometric functions carry metres. Critical and overdamped systems have nonoscillatory modes, but initial velocity can cause a zero crossing. “No overshoot” here describes the default release from rest; it is not a universal statement about arbitrary initial states.

## 5. Energy provides an independent physical check

$$E=\tfrac12mv^2+\tfrac12kx^2\quad[\mathrm{J}].$$

Differentiate and substitute the equation of motion:

$$\frac{dE}{dt}=mv\dot{v}+kx\dot{x}=v(m\dot{v}+kx)=-cv^2\le0\quad[\mathrm{W}].$$

The initial energy is $E_0=\tfrac12(40\,\mathrm{N/m})(0.10\,\mathrm{m})^2=0.20\,\mathrm{J}$. With $c=0$, energy should remain constant; with $c>0$, it should decrease within numerical error.

## Outputs and limits

1. `figures/1_displacement.png`: numerical lines versus analytical markers.
2. `figures/2_phase_portrait.png`: displacement ($\mathrm{m}$) versus velocity ($\mathrm{m/s}$).
3. `figures/3_energy.png`: total mechanical energy ($\mathrm{J}$), logarithmic axis.
4. `figures/4_zeta_sweep.png`: six damping ratios.

The script supports general initial velocity in the analytical formulas. Its module-level parameters are intended for a small teaching study; keep $m>0$, $k>0$, and $\zeta\ge0$. Near-critical or extremely large damping can cause cancellation in the direct analytical formulas; those ranges have not been certified. The checked regime set is $\zeta\in\{0,0.1,1,2\}$ with an additional nonzero-velocity check.

Try predicting the effect of doubling mass at fixed stiffness and damping. Does $\omega_n$ increase or decrease? Does keeping $c$ fixed keep $\zeta$ fixed? Derive both answers before rerunning the model.
