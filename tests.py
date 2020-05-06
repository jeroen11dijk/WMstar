import math
import time

import networkx as nx
from mapfw import MapfwBenchmarker
from networkx import grid_graph

from mstar import Mstar


def test(G, v_I, v_W, v_F, weigh_cost, time_budget, min_cost):
    start = time.time()
    res = Mstar(G, v_I, v_W, v_F, weigh_cost)
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
        test(graph, v_I, v_W, v_F, 1, time_budget, min_cost)


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
    G = nx.Graph()

    G.add_edge('a', 'b')
    G.add_edge('a', 'c', weight=0.4)
    G.add_edge('c', 'd', weight=0.1)
    G.add_edge('c', 'e', weight=0.7)
    G.add_edge('c', 'f', weight=0.9)
    G.add_edge('a', 'd', weight=0.3)
    G.add_edge('b', 'f', weight=0.2)
    G.add_edge('g', 'e', weight=0.7)
    G.add_edge('g', 'a', weight=0.5)
    G.add_edge('c', 'h', weight=0.1)
    G.add_edge('h', 'd', weight=0.6)
    G.add_edge('i', 'a', weight=0.3)
    G.add_edge('i', 'c', weight=0.9)
    G.add_edge('j', 'c', weight=0.1)
    G.add_edge('h', 'k', weight=0.6)
    G.add_edge('a', 'k', weight=0.7)
    G.add_edge('b', 'h', weight=0.4)
    G.add_edge('l', 'a', weight=0.1)
    G.add_edge('l', 'h', weight=0.3)
    G.add_edge('m', 'c', weight=0.8)
    G.add_edge('m', 'f', weight=0.3)
    G.add_edge('n', 'g', weight=0.7)
    G.add_edge('n', 'h', weight=0.9)
    G.add_edge('n', 'a', weight=0.5)
    G.add_edge('o', 'a', weight=0.3)
    G.add_edge('o', 'b', weight=0.1)
    G.add_edge('o', 'k', weight=0.2)
    G.add_edge('o', 'n', weight=0.9)

    v_I1 = ('j', 'm', 'b', 'a', 'c', 'f')
    v_W1 = ((), (), (), (), (), ())
    v_F1 = ('l', 'b', 'h', 'j', 'g', 'o')

    v_I2 = ('m', 'k', 'j', 'd')
    v_W2 = ('c', 'a', 'l', 'b')
    v_F2 = ('f', 'b', 'j', 'c')

    v_I3 = ('m', 'k')
    v_W3 = ((), 'a')
    v_F3 = ('f', 'b')

    # test(G, v_I1, v_W1, v_F1, 0, 4.2, 3.2)
    test(G, v_I2, v_W2, v_F2, 0, 0.1, 4.5)
    test(G, v_I3, v_W3, v_F3, 0, 0.01, 1.2)

    benchmark(1, 0.02, 50)
    benchmark(2, 0.02, 38)
    benchmark(3, 0.02, 76)
    benchmark(4, 0.02, 17)
    benchmark(6, 0.02, 20)

    print("All tests have passed!")


# run_all_tests()

benchmarker = MapfwBenchmarker("42cf6ce8D2A5B954", 4, "M*", "Version 1.2", True)
for problem in benchmarker:
    graph, v_I, v_W, v_F = setup_benchmark(problem)
    solution = Mstar(graph, v_I, v_W, v_F, 1)
    print(solution)
    problem.add_solution(solution[0])
