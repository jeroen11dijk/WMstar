import math
from copy import copy

from Mstar_cpp import Mstar_cpp
from mapfw import MapfwBenchmarker

from mstar import Mstar


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


def cpp_test(G, v_I, v_W, v_F, min_cost):
    res = Mstar_cpp(G, v_I, v_W, v_F).solve()
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


def benchmark(i, min_cost):
    benchmarker = MapfwBenchmarker("42cf6ce8D2A5B954", i, "M*", "Test", True)
    for problem in benchmarker:
        cpp_waypoints = copy(problem.waypoints)
        for i in range(len(cpp_waypoints)):
            if len(cpp_waypoints[i]) == 0:
                cpp_waypoints[i] = [[-1, -1]]
        cpp_test(problem.grid, problem.starts, cpp_waypoints, problem.goals, min_cost)
        graph, v_I, v_W, v_F = setup_benchmark(problem)
        python_test(graph, v_I, v_W, v_F, min_cost)


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


class TestBenchmarks:
    def test_benchmark_1(self):
        benchmark(1, 26)

    def test_benchmark_2(self):
        benchmark(2, 46)

    def test_benchmark_3(self):
        benchmark(3, 73)

    def test_benchmark_4(self):
        benchmark(4, 23)

    def test_benchmark_5(self):
        benchmark(5, 116)

    def test_benchmark_6(self):
        benchmark(6, 25)

    def test_benchmark_7(self):
        benchmark(7, 278)

    def test_benchmark_8(self):
        benchmark(8, 1576)

    def test_benchmark_9(self):
        benchmark(9, 2438)

    # TODO cant solve it within a decent time
    # def test_benchmark_10(self):
    #     benchmark(10, xx)

    def test_benchmark_11(self):
        benchmark(11, 100)

    def test_benchmark_12(self):
        benchmark(12, 112)

    def test_benchmark_13(self):
        benchmark(13, 47)

    def test_benchmark_14(self):
        benchmark(14, 72)

    def test_benchmark_15(self):
        benchmark(15, 72)

    def test_benchmark_16(self):
        benchmark(16, 68)

    def test_benchmark_17(self):
        benchmark(17, 49)

    def test_benchmark_18(self):
        benchmark(18, 55)
