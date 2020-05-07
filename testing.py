from mapfw import MapfwBenchmarker
from networkx import single_source_dijkstra_path, dijkstra_predecessor_and_distance
import cProfile
from mstar import Mstar
from test_benchmarks import setup_benchmark

benchmarker = MapfwBenchmarker("42cf6ce8D2A5B954", 1, "M*", "Test", True)
for problem in benchmarker:
    graph, v_I, v_W, v_F = setup_benchmark(problem)
    # cProfile.run('Mstar(graph, v_I, v_W, v_F)')
    problem.add_solution(Mstar(graph, v_I, v_W, v_F)[0])
