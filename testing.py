from mapfw import MapfwBenchmarker
import Mstar_cpp
from mstar import Mstar
from test_benchmarks import setup_benchmark

# benchmarker = MapfwBenchmarker("42cf6ce8D2A5B954", 17, "M*", "Simple Heuristic", True)
# for problem in benchmarker:
#     graph, v_I, v_W, v_F = setup_benchmark(problem)
#     problem.add_solution(Mstar(graph, v_I, v_W, v_F).solve()[0])


a = Mstar_cpp.Jeroen(1)
print(a)