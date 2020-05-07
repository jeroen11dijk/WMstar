from mapfw import MapfwBenchmarker
from networkx import single_target_shortest_path

from mstar import Mstar
from test_benchmarks import setup_benchmark

benchmarker = MapfwBenchmarker("42cf6ce8D2A5B954", 4, "M*", "Test", True)
for problem in benchmarker:
    graph, v_I, v_W, v_F = setup_benchmark(problem)
    problem.add_solution(Mstar(graph, v_I, v_W, v_F)[0])
    start = v_I[0]
    goal = v_F[0]
    policies = single_target_shortest_path(graph, goal)
    for policy in policies:
        if len(policies[policy]) > 1:
            policies[policy].pop(0)
    print(start, goal)
    print(policies[goal])
    print(len(policies[start]))
