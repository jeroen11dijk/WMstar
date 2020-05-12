from mapfw import MapfwBenchmarker
import Mstar_cpp
from mstar import Mstar
from test_benchmarks import setup_benchmark

benchmarker = MapfwBenchmarker("42cf6ce8D2A5B954", 17, "M*", "Simple Heuristic", True)
for problem in benchmarker:
    graph, v_I, v_W, v_F = setup_benchmark(problem)
    problem.add_solution(Mstar(graph, v_I, v_W, v_F).solve()[0])


dictionary = {"A": 0, "B": 0, "C": 0}

print(Mstar_cpp.NietJeroen(dictionary, "A"))
print(Mstar_cpp.NietJeroen(dictionary, "HELLO"))