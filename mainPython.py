from mapfw import MapfwBenchmarker, get_all_benchmarks

from Python.mstar import Mstar
from Python.test_python_benchmarks import setup_benchmark

# benchmarks = [1, 2, 3, 4, 5, 6, 7, 9, 11, 12, 13, 14, 15, 16, 17, 18, 20, 22, 25]
# for benchmark in benchmarks:
benchmarker = MapfwBenchmarker("42cf6ce8D2A5B954", 33, "M*", "Python Dynamic TSP", True)
for problem in benchmarker:
    graph, v_I, v_W, v_F = setup_benchmark(problem)
    problem.add_solution(Mstar(graph, v_I, v_W, v_F).solve()[0])
