from copy import copy

from mapfw import MapfwBenchmarker
from mstar import Mstar
from test_benchmarks import setup_benchmark
from Cpp.Mstar_cpp import Mstar_cpp


# benchmarker = MapfwBenchmarker("42cf6ce8D2A5B954", 17, "M*", "Python edge conflicts", True)
# for problem in benchmarker:
#     # PYTHON
#     graph, v_I, v_W, v_F = setup_benchmark(problem)
#     problem.add_solution(Mstar(graph, v_I, v_W, v_F).solve()[0])

benchmarker = MapfwBenchmarker("42cf6ce8D2A5B954", 1, "M*", "Cpp edge conflicts", True)
for problem in benchmarker:
    cpp_waypoints = copy(problem.waypoints)
    for i in range(len(cpp_waypoints)):
        if len(cpp_waypoints[i]) == 0:
            cpp_waypoints[i] = [[-1, -1]]
    problem.add_solution(Mstar_cpp(problem.grid, problem.starts, cpp_waypoints, problem.goals).solve()[0])
