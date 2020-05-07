import math
import time

import networkx as nx
from mapfw import MapfwBenchmarker
from networkx import grid_graph

from mstar import Mstar


def test(G, v_I, v_W, v_F, time_budget, min_cost):
    start = time.time()
    res = Mstar(G, v_I, v_W, v_F)
    assert time.time() - start < time_budget
    print(res[1])
    assert res[1] < min_cost or math.isclose(res[1], min_cost)
    paths = res[0]
    for i in range(len(v_I)):
        assert v_I[i] in paths[i][0] or list(v_I[i]) == paths[i][0]
    for i in range(len(v_W)):
        if len(v_W[i]) > 0:
            for waypoint in v_W[i]:
                assert any(waypoint in config for config in paths[i])
    for i in range(len(v_F)):
        assert v_F[i] == paths[i][-1] or list(v_F[i]) == paths[i][-1]


def benchmark(i, time_budget, min_cost):
    benchmarker = MapfwBenchmarker("42cf6ce8D2A5B954", i, "M*", "Test", True)
    for problem in benchmarker:
        graph, v_I, v_W, v_F = setup_benchmark(problem)
        test(graph, v_I, v_W, v_F, time_budget, min_cost)


def setup_benchmark(problem):
    graph = grid_graph([len(problem.grid), len(problem.grid[0])])
    for i in range(len(problem.grid)):
        for j in range(len(problem.grid[0])):
            if problem.grid[i][j] == 1:
                graph.remove_node((j, i))
    # Create V_I and v_F
    v_I = tuple(tuple(start) for start in problem.starts)
    v_W = []
    for waypoint in problem.waypoints:
        if len(waypoint) > 0:
            v_W.append(tuple(tuple(waypoint[0])))
        else:
            v_W.append(())
    v_F = tuple(tuple(target) for target in problem.goals)
    return graph, v_I, v_W, v_F


def run_all_tests():

    benchmark(1, 0.02, 50)
    benchmark(2, 0.02, 38)
    benchmark(3, 0.02, 76)
    benchmark(4, 0.02, 17)
    benchmark(6, 0.02, 21)
    benchmark(17, 9, 41)

    print("All tests have passed!")


run_all_tests()

# benchmarker = MapfwBenchmarker("42cf6ce8D2A5B954", 17, "M*", "Version 1.2", True)
# for problem in benchmarker:
#     graph, v_I, v_W, v_F = setup_benchmark(problem)
#     solution = Mstar(graph, v_I, v_W, v_F)
#     print(solution)
#     problem.add_solution(solution[0])
