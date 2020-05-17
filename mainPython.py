from mapfw import MapfwBenchmarker

from Python.mstar import Mstar
from Python.test_python_benchmarks import setup_benchmark

benchmarker = MapfwBenchmarker("42cf6ce8D2A5B954", 20, "M*", "Python greedy TSP", True)
for problem in benchmarker:
    graph, v_I, v_W, v_F = setup_benchmark(problem)
    problem.add_solution(Mstar(graph, v_I, v_W, v_F).solve()[0])
