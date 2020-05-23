from copy import copy

from Cpp.Mstar_pybind import Mstar
from mapfw import MapfwBenchmarker, get_all_benchmarks

benchmarker = MapfwBenchmarker("42cf6ce8D2A5B954", 15, "M*", "Cpp optimal TSP", False)
for problem in benchmarker:
    cpp_waypoints = copy(problem.waypoints)
    for i in range(len(cpp_waypoints)):
        if len(cpp_waypoints[i]) == 0:
            cpp_waypoints[i] = [[-1, -1]]
    problem.add_solution(Mstar(problem.grid, problem.starts, cpp_waypoints, problem.goals).solve()[0])
