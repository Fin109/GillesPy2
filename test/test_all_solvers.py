import unittest
import numpy as np

import gillespy2
from example_models import Example, Oregonator
from gillespy2.core.results import Results, Trajectory
from gillespy2.solvers.cpp.ssa_c_solver import SSACSolver
from gillespy2.solvers.cpp.variable_ssa_c_solver import VariableSSACSolver
from gillespy2.solvers.numpy.basic_ode_solver import BasicODESolver
from gillespy2.solvers.numpy.ssa_solver import NumPySSASolver
from gillespy2.solvers.numpy.basic_tau_leaping_solver import BasicTauLeapingSolver
from gillespy2.solvers.numpy.basic_tau_hybrid_solver import BasicTauHybridSolver


class TestAllSolvers(unittest.TestCase):

    solvers = [SSACSolver, VariableSSACSolver, BasicODESolver, 
                NumPySSASolver, BasicTauLeapingSolver, BasicTauHybridSolver]

    model = Example()
    for sp in model.listOfSpecies.values():
        sp.mode = 'discrete'
    results = {}
    labeled_results = {}
    labeled_results_more_trajectories = {}

    for solver in solvers:
        labeled_results[solver] = model.run(solver=solver, number_of_trajectories=1,seed=1)
        labeled_results_more_trajectories[solver] = model.run(solver=solver, number_of_trajectories=2)

    def test_instantiated(self):
        for solver in self.solvers:
            self.model.run(solver=solver())

    def test_to_array(self):
        for solver in self.solvers:
            print(self.labeled_results[solver].to_array(),type(self.labeled_results[solver].to_array()[0]))
            self.assertTrue(isinstance(self.labeled_results[solver].to_array(), np.ndarray))

    def test_return_type_show_labels(self):
        for solver in self.solvers:
            self.assertTrue(isinstance(self.labeled_results[solver], Results))
            self.assertTrue(isinstance(self.labeled_results[solver]['Sp'], np.ndarray))
            self.assertTrue(isinstance(self.labeled_results[solver]['Sp'][0], np.float))

            self.assertTrue(isinstance(self.labeled_results[solver][0], Trajectory))

            self.assertTrue(isinstance(self.labeled_results_more_trajectories[solver], Results))
            self.assertTrue(isinstance(self.labeled_results_more_trajectories[solver][0], Trajectory))
            self.assertTrue(isinstance(self.labeled_results_more_trajectories[solver][0]['Sp'], np.ndarray))
            self.assertTrue(isinstance(self.labeled_results_more_trajectories[solver][0]['Sp'][0], np.float))


    def test_random_seed(self):
        for solver in self.solvers:
            same_results = self.model.run(solver=solver, seed=1)
            compare_results = self.model.run(solver=solver,seed=1)
            self.assertTrue(np.array_equal(same_results.to_array(), compare_results.to_array()))
            if solver.name == 'BasicODESolver': continue
            diff_results = self.model.run(solver=solver, seed=2)
            self.assertFalse(np.array_equal(diff_results.to_array(),same_results.to_array()))
    
    def test_extraneous_args(self):
        for solver in self.solvers:
            with self.assertLogs(level='WARN'):
                model = Example()
                results = model.run(solver=solver, nonsense='ABC')

    def test_timeout(self):
        for solver in self.solvers:
            with self.assertLogs(level='WARN'):
                model = Oregonator()
                model.timespan(np.linspace(0, 1000000, 101))
                results = model.run(solver=solver, timeout=1)

if __name__ == '__main__':
    unittest.main()
