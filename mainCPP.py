from mapfw import MapfwBenchmarker


def solve(problem):
    from Cpp.Mstar_pybind import Mstar
    for i in range(len(problem.waypoints)):
        if len(problem.waypoints[i]) == 0:
            problem.waypoints[i] = [[-1, -1]]
    return Mstar(problem.grid, problem.starts, problem.waypoints, problem.goals, True).solve()[0]


if __name__ == '__main__':
    benchmarker = MapfwBenchmarker("42cf6ce8D2A5B954", [67, 68, 69], "M* Inflated", "CPP TSP Dynamic", False, solver=solve, cores=1)
    benchmarker.run()
