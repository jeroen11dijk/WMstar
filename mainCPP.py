from copy import copy

from Mstar_cpp import Mstar_cpp
from mapfw import MapfwBenchmarker

benchmarker = MapfwBenchmarker("42cf6ce8D2A5B954", 17, "M*", "Cpp limited neighbours", True)
for problem in benchmarker:
    cpp_waypoints = copy(problem.waypoints)
    for i in range(len(cpp_waypoints)):
        if len(cpp_waypoints[i]) == 0:
            cpp_waypoints[i] = [[-1, -1]]
    problem.add_solution(Mstar_cpp(problem.grid, problem.starts, cpp_waypoints, problem.goals).solve()[0])
