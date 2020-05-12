from mapfw import MapfwBenchmarker
from mstar import Mstar
from test_benchmarks import setup_benchmark
from Cpp.Mstar_cpp import *

# benchmarker = MapfwBenchmarker("42cf6ce8D2A5B954", 4, "M*", "Simple Heuristic", True)
# for problem in benchmarker:
#     graph, v_I, v_W, v_F = setup_benchmark(problem)
#     problem.add_solution(Mstar(graph, v_I, v_W, v_F).solve()[0])

test_queue()

