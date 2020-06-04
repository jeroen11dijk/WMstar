import math

import pytest
from Cpp.Mstar_pybind import Mstar
from mapfw import MapfwBenchmarker, get_all_benchmarks

min_cost = {1: 36, 2: 48, 3: 75, 4: 26, 5: 119, 6: 27, 7: 205, 8: 821, 9: 1747, 10: 1590, 11: 110, 12: 115, 13: 52,
            14: 34, 15: 70, 16: 70, 17: 53, 18: 53, 19: 4410, 20: 43, 21: 252, 22: 115, 23: 144, 24: 1542, 25: 120,
            27: 169, 33: 333, 54: 0, 55: 28, 56: 39, 58: 0, 59: 824, 60: 65, 61: 1156, 62: 14, 64: 96, 66: 94, 77: 100,
            78: 20}


def cpp_test(G, v_I, v_W, v_F, min_cost):
    res = Mstar(G, v_I, v_W, v_F, False).solve()
    if res[1] < min_cost:
        print(res[1])
    assert res[1] < min_cost or math.isclose(res[1], min_cost)
    paths = res[0]
    for i in range(len(v_I)):
        assert v_I[i] == list(paths[i][0])
    for i in range(len(v_W)):
        if len(v_W[i]) > 0:
            for waypoint in v_W[i]:
                if waypoint != [-1, -1]:
                    assert tuple(waypoint) in paths[i]
    for i in range(len(v_F)):
        assert v_F[i] == list(paths[i][-1])


@pytest.mark.parametrize("test_id", get_all_benchmarks(without=[10, 19, 21, 23, 24, 54, 58, 59, 61]))
def test_cpp_benchmark(test_id):
    benchmarker = MapfwBenchmarker("42cf6ce8D2A5B954", test_id, "M*", "Test", True)
    for problem in benchmarker:
        cpp_waypoints = problem.waypoints
        for i in range(len(cpp_waypoints)):
            if len(cpp_waypoints[i]) == 0:
                cpp_waypoints[i] = [[-1, -1]]
        cpp_test(problem.grid, problem.starts, cpp_waypoints, problem.goals, min_cost[test_id])
