from copy import copy

from mapfw import MapfwBenchmarker


def solve(problem):
    from Python.test_python_benchmarks import setup_benchmark
    from Python.mstar import Mstar
    graph, v_I, v_W, v_F = setup_benchmark(problem)
    return Mstar(graph, v_I, v_W, v_F, True).solve()[0]


# if __name__ == '__main__':
#     benchmarker = MapfwBenchmarker("42cf6ce8D2A5B954", 1, "M*", "Python TSP dynamic", True, solver=solve,
#                                    cores=-1, timeout=60000)
#     benchmarker.run()

benchmarker = MapfwBenchmarker("42cf6ce8D2A5B954", 2, "M*", "Python OD", True, solver=solve, cores=-1)
for problem in benchmarker:
    res = solve(problem)
    print(res)
    # problem.add_solution(res)