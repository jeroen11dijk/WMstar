from mapfw import MapfwBenchmarker
from mstar import Mstar
from test_benchmarks import setup_benchmark
from Cpp.Mstar_cpp import *

benchmarker = MapfwBenchmarker("42cf6ce8D2A5B954", 5, "M*", "Python edge conflicts", True)
for problem in benchmarker:
    for i in range(len(problem.waypoints)):
        if len(problem.waypoints[i]) == 0:
            problem.waypoints[i] = [[-1, -1]]
    # PYTHON
    graph, v_I, v_W, v_F = setup_benchmark(problem)
    problem.add_solution(Mstar(graph, v_I, v_W, v_F).solve()[0])
    # # problem.add_solution(Mstar_cpp(problem.grid, problem.starts, problem.waypoints, problem.goals).solve()[0])
    # print(Mstar_cpp(problem.grid, problem.starts, problem.waypoints, problem.goals).solve())


# test_queue()
