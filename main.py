import sys

from Cpp.Mstar_pybind import Mstar
from mapfw import MapfwBenchmarker

if __name__ == "__main__":
    benchmark = int(sys.argv[1])
    debug = sys.argv[2].lower() == 'true' if len(sys.argv) > 2 else True
    unordered = sys.argv[3].lower() == 'true' if len(sys.argv) > 3 else True
    text = "Timon. Unordered: " + str(unordered)
    benchmarker = MapfwBenchmarker("42cf6ce8D2A5B954", benchmark, "M*", text, debug)
    for problem in benchmarker:
        cpp_waypoints = problem.waypoints
        for i in range(len(cpp_waypoints)):
            if len(cpp_waypoints[i]) == 0:
                cpp_waypoints[i] = [[-1, -1]]
        res = Mstar(problem.grid, problem.starts, cpp_waypoints, problem.goals, unordered).solve()
        problem.add_solution(res[0])
