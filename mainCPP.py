from mapfw import MapfwBenchmarker


def solve(problem):
    from Cpp.Mstar_pybind import Mstar
    for i in range(len(problem.waypoints)):
        if len(problem.waypoints[i]) == 0:
            problem.waypoints[i] = [[-1, -1]]
    return Mstar(problem.grid, problem.starts, problem.waypoints, problem.goals, False).solve()


benchmarks = [31, 32, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51]

if __name__ == '__main__':
    benchmarker = MapfwBenchmarker("42cf6ce8D2A5B954", 2, "M*", "CPP inflated", True, solver=solve, cores=-1)
    benchmarker.run()
