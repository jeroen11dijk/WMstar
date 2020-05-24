import math

from mapfw import MapfwBenchmarker

from Python.mstar import Mstar


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


def python_benchmark(i, min_cost):
    benchmarker = MapfwBenchmarker("42cf6ce8D2A5B954", i, "M*", "Test", True)
    for problem in benchmarker:
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
    def test_python_benchmark_1(self):
        python_benchmark(1, 26)

    def test_python_benchmark_2(self):
        python_benchmark(2, 46)

    def test_python_benchmark_3(self):
        python_benchmark(3, 73)

    def test_python_benchmark_4(self):
        python_benchmark(4, 23)

    def test_python_benchmark_5(self):
        python_benchmark(5, 116)

    def test_python_benchmark_6(self):
        python_benchmark(6, 25)

    def test_python_benchmark_7(self):
        python_benchmark(7, 204)

    def test_python_benchmark_8(self):
        python_benchmark(8, 821)

    def test_python_benchmark_9(self):
        python_benchmark(9, 1744)

    # TODO cant solve it within a decent time
    # def test_python_benchmark_10(self):
    #     benchmark(10, xx)

    def test_python_benchmark_11(self):
        python_benchmark(11, 98)

    def test_python_benchmark_12(self):
        python_benchmark(12, 112)

    def test_python_benchmark_13(self):
        python_benchmark(13, 47)

    def test_python_benchmark_14(self):
        python_benchmark(14, 33)

    def test_python_benchmark_15(self):
        python_benchmark(15, 68)

    def test_python_benchmark_16(self):
        python_benchmark(16, 68)

    def test_python_benchmark_17(self):
        python_benchmark(17, 49)

    def test_python_benchmark_18(self):
        python_benchmark(18, 50)

    def test_python_benchmark_20(self):
        python_benchmark(20, 39)

    def test_python_benchmark_22(self):
        python_benchmark(22, 109)

    def test_python_benchmark_25(self):
        python_benchmark(25, 116)

    def test_python_benchmark_27(self):
        python_benchmark(27, 159)

    def test_python_benchmark_33(self):
        python_benchmark(33, 328)

    def test_python_benchmark_56(self):
        python_benchmark(56, 328)
