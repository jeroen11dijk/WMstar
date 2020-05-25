import math

import pytest
from mapfw import MapfwBenchmarker, get_all_benchmarks

from Python.mstar import Mstar

min_cost = {1: 36, 2: 48, 3: 75, 4: 26, 5: 119, 6: 27, 7: 205, 8: 821, 9: 1747, 10: 1590, 11: 110, 12: 115, 13: 52,
            14: 34, 15: 70, 16: 70, 17: 53, 18: 53, 19: 4410, 20: 43, 21: 252, 22: 115, 23: 144, 24: 1542, 25: 120,
            27: 169, 33: 333, 54: 0, 55: 28, 56: 39, 58: 0, 59: 824, 60: 65, 61: 1156, 62: 14, 64: 96}


def python_test(G, v_I, v_W, v_F, min_cost):
    res = Mstar(G, v_I, v_W, v_F).solve()
    if res[1] < min_cost:
        print(res[1])
    assert res[1] < min_cost or math.isclose(res[1], min_cost)
    paths = res[0]
    for i in range(len(v_I)):
        assert list(v_I[i]) == paths[i][0]
    for i in range(len(v_W)):
        if len(v_W[i]) > 0:
            for waypoint in v_W[i]:
                assert list(waypoint) in paths[i]
    for i in range(len(v_F)):
        assert list(v_F[i]) == paths[i][-1]


def setup_benchmark(problem):
    grap_new = {}
    for i in range(problem.height):
        for j in range(problem.width):
            if problem.grid[i][j] == 0:
                current = (j, i)
                neighbours = []
                if i != 0 and problem.grid[i - 1][j] == 0:
                    neighbours.append((j, i - 1))
                if j != 0 and problem.grid[i][j - 1] == 0:
                    neighbours.append((j - 1, i))
                if i != problem.height - 1 and problem.grid[i + 1][j] == 0:
                    neighbours.append((j, i + 1))
                if j != problem.width - 1 and problem.grid[i][j + 1] == 0:
                    neighbours.append((j + 1, i))
                grap_new[current] = neighbours
    # Create V_I and v_F
    v_I = tuple(tuple(start) for start in problem.starts)
    v_W = []
    for agent_waypoints in problem.waypoints:
        if len(agent_waypoints) > 0:
            v_W_i = []
            for waypoint in agent_waypoints:
                v_W_i.append(tuple(tuple(waypoint)))
            v_W.append(v_W_i)
        else:
            v_W.append(())
    v_W = tuple(v_W)
    v_F = tuple(tuple(target) for target in problem.goals)
    return grap_new, v_I, v_W, v_F


@pytest.mark.parametrize("test_id", get_all_benchmarks(without=[10, 19, 21, 23, 24, 54, 58, 59, 61]))
def test_python_benchmark(test_id):
    benchmarker = MapfwBenchmarker("42cf6ce8D2A5B954", test_id, "M*", "Test", True)
    for problem in benchmarker:
        graph, v_I, v_W, v_F = setup_benchmark(problem)
        python_test(graph, v_I, v_W, v_F, min_cost[test_id])
