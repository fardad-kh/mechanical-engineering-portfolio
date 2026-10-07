import importlib.util
from pathlib import Path
import unittest
import numpy as np

path = Path(__file__).resolve().parents[1] / 'projects/mass-spring-damper/mass_spring_damper.py'
spec = importlib.util.spec_from_file_location('msd', path)
model = importlib.util.module_from_spec(spec)
spec.loader.exec_module(model)

class PhysicsChecks(unittest.TestCase):
    def test_analytical_agreement_and_initial_conditions(self):
        for zeta in [0.0, 0.1, 1.0, 2.0]:
            with self.subTest(zeta=zeta):
                x, v = model.solve_numeric(zeta)
                self.assertLess(np.max(np.abs(x-model.solve_analytic(zeta))), 1e-8)
                self.assertAlmostEqual(x[0], model.x0)
                self.assertAlmostEqual(v[0], model.v0)

    def test_nonzero_initial_velocity(self):
        original = model.v0
        try:
            model.v0 = -0.25
            for zeta in [0.1, 1.0, 2.0]:
                with self.subTest(zeta=zeta):
                    x, _ = model.solve_numeric(zeta)
                    self.assertLess(np.max(np.abs(x-model.solve_analytic(zeta))), 1e-8)
        finally:
            model.v0 = original

    def test_energy_dissipation(self):
        for zeta in [0.1, 1.0, 2.0]:
            x, v = model.solve_numeric(zeta)
            energy = 0.5*model.m*v**2 + 0.5*model.k*x**2
            self.assertAlmostEqual(energy[0], 0.2)
            self.assertLessEqual(np.max(np.diff(energy)), 1e-10)
            c = 2*zeta*np.sqrt(model.k*model.m)
            dissipation = np.sum(0.5*c*(v[:-1]**2+v[1:]**2)*np.diff(model.t))
            self.assertLess(abs(energy[-1]-energy[0]+dissipation), 1e-6)

    def test_undamped_energy_conservation(self):
        x, v = model.solve_numeric(0)
        energy = 0.5*model.m*v**2 + 0.5*model.k*x**2
        self.assertLess(np.max(np.abs(energy-energy[0])), 1e-8)

    def test_invalid_damping(self):
        for zeta in [-1, float('nan'), float('inf')]:
            for solver in [model.solve_numeric, model.solve_analytic]:
                with self.assertRaises(ValueError):
                    solver(zeta)

if __name__ == '__main__':
    unittest.main()
