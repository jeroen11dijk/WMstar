from mapfw import MapfwBenchmarker, get_all_benchmarks
from Python.test_python_benchmarks import setup_benchmark
from Python.mstar import Mstar

def solve(problem):
    from Python.test_python_benchmarks import setup_benchmark
    from Python.mstar import Mstar
    graph, v_I, v_W, v_F = setup_benchmark(problem)
    return Mstar(graph, v_I, v_W, v_F, False).solve()[0]


if __name__ == '__main__':
    benchmarker = MapfwBenchmarker("42cf6ce8D2A5B954", get_all_benchmarks(without=[10, 19, 21, 23, 24, 54, 58, 59, 61]), "M*", "Normal Python", False,
                                   solver=solve,
                                   cores=-1)
    benchmarker.run()

# benchmarker = MapfwBenchmarker("42cf6ce8D2A5B954", 1, "M*", "Normal Python", True, solver=solve, cores=-1)
# for problem in benchmarker:
#     graph, v_I, v_W, v_F = setup_benchmark(problem)
#     res = Mstar(graph, v_I, v_W, v_F, False).solve()[0]
#     problem.add_solution(res)
#     print(res)
