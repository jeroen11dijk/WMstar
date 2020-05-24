import math
from copy import copy

from Cpp.Mstar_pybind import Mstar
from mapfw import MapfwBenchmarker


def cpp_test(G, v_I, v_W, v_F, min_cost):
    res = Mstar(G, v_I, v_W, v_F).solve()
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


def cpp_benchmark(i, min_cost):
    benchmarker = MapfwBenchmarker("42cf6ce8D2A5B954", i, "M*", "Test", True)
    for problem in benchmarker:
        cpp_waypoints = copy(problem.waypoints)
        for i in range(len(cpp_waypoints)):
            if len(cpp_waypoints[i]) == 0:
                cpp_waypoints[i] = [[-1, -1]]
        cpp_test(problem.grid, problem.starts, cpp_waypoints, problem.goals, min_cost)


class TestBenchmarks:
    def test_cpp_benchmark_1(self):
        cpp_benchmark(1, 26)

    def test_cpp_benchmark_2(self):
        cpp_benchmark(2, 46)

    def test_cpp_benchmark_3(self):
        cpp_benchmark(3, 73)

    def test_cpp_benchmark_4(self):
        cpp_benchmark(4, 23)

    def test_cpp_benchmark_5(self):
        cpp_benchmark(5, 116)

    def test_cpp_benchmark_6(self):
        cpp_benchmark(6, 25)

    def test_cpp_benchmark_7(self):
        cpp_benchmark(7, 204)

    def test_cpp_benchmark_8(self):
        cpp_benchmark(8, 821)

    def test_cpp_benchmark_9(self):
        cpp_benchmark(9, 1744)

    # TODO cant solve it within a decent time
    # def test_cpp_benchmark_10(self):
    #     cpp_benchmark(10, xx)

    def test_cpp_benchmark_11(self):
        cpp_benchmark(11, 98)

    def test_cpp_benchmark_12(self):
        cpp_benchmark(12, 112)

    def test_cpp_benchmark_13(self):
        cpp_benchmark(13, 47)

    def test_cpp_benchmark_14(self):
        cpp_benchmark(14, 33)

    def test_cpp_benchmark_15(self):
        cpp_benchmark(15, 68)

    def test_cpp_benchmark_16(self):
        cpp_benchmark(16, 68)

    def test_cpp_benchmark_17(self):
        cpp_benchmark(17, 49)

    def test_cpp_benchmark_18(self):
        cpp_benchmark(18, 50)

    def test_cpp_benchmark_20(self):
        cpp_benchmark(20, 39)

    def test_cpp_benchmark_22(self):
        cpp_benchmark(22, 109)

    def test_cpp_benchmark_25(self):
        cpp_benchmark(25, 116)

    def test_cpp_benchmark_27(self):
        cpp_benchmark(27, 159)

    def test_cpp_benchmark_33(self):
        cpp_benchmark(33, 328)

    def test_cpp_benchmark_56(self):
        cpp_benchmark(56, 23)
