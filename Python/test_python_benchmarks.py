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
        python_benchmark(1, 36)

    def test_python_benchmark_2(self):
        python_benchmark(2, 48)

    def test_python_benchmark_3(self):
        python_benchmark(3, 75)

    def test_python_benchmark_4(self):
        python_benchmark(4, 26)

    def test_python_benchmark_5(self):
        python_benchmark(5, 119)

    def test_python_benchmark_6(self):
        python_benchmark(6, 27)

    def test_python_benchmark_7(self):
        python_benchmark(7, 205)

    def test_python_benchmark_8(self):
        python_benchmark(8, 821)

    def test_python_benchmark_9(self):
        python_benchmark(9, 1747)

    # TODO cant solve it within a decent time
    # def test_python_benchmark_10(self):
    #     benchmark(10, xx)

    def test_python_benchmark_11(self):
        python_benchmark(11, 100)

    def test_python_benchmark_12(self):
        python_benchmark(12, 115)

    def test_python_benchmark_13(self):
        python_benchmark(13, 52)

    def test_python_benchmark_14(self):
        python_benchmark(14, 34)

    def test_python_benchmark_15(self):
        python_benchmark(15, 70)

    def test_python_benchmark_16(self):
        python_benchmark(16, 70)

    def test_python_benchmark_17(self):
        python_benchmark(17, 53)

    def test_python_benchmark_18(self):
        python_benchmark(18, 53)

    def test_python_benchmark_20(self):
        python_benchmark(20, 43)

    def test_python_benchmark_22(self):
        python_benchmark(22, 115)

    def test_python_benchmark_25(self):
        python_benchmark(25, 120)

    def test_python_benchmark_27(self):
        python_benchmark(27, 169)

    def test_python_benchmark_33(self):
        python_benchmark(33, 333)

    def test_python_benchmark_56(self):
        python_benchmark(56, 39)

    def test_python_benchmark_60(self):
        python_benchmark(60, 65)
