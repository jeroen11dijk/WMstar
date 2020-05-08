import math

from mapfw import MapfwBenchmarker
from networkx import grid_graph

from mstar import Mstar


def main(G, v_I, v_W, v_F, min_cost):
    res = Mstar(G, v_I, v_W, v_F).solve()
    if res[1] < min_cost:
        print(res[1])
    assert res[1] < min_cost or math.isclose(res[1], min_cost)
    paths = res[0]
    for i in range(len(v_I)):
        assert v_I[i] in paths[i][0] or list(v_I[i]) == paths[i][0]
    for i in range(len(v_W)):
        if len(v_W[i]) > 0:
            for waypoint in v_W[i]:
                assert list(waypoint) in paths[i]
    for i in range(len(v_F)):
        assert v_F[i] == paths[i][-1] or list(v_F[i]) == paths[i][-1]


def benchmark(i, min_cost):
    benchmarker = MapfwBenchmarker("42cf6ce8D2A5B954", i, "M*", "Test", True)
    for problem in benchmarker:
        graph, v_I, v_W, v_F = setup_benchmark(problem)
        main(graph, v_I, v_W, v_F, min_cost)


def setup_benchmark(problem):
    graph = grid_graph([len(problem.grid), len(problem.grid[0])])
    for i in range(len(problem.grid)):
        for j in range(len(problem.grid[0])):
            if problem.grid[i][j] == 1:
                graph.remove_node((j, i))
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
    return graph, v_I, v_W, v_F


class TestBenchmarks:
    def test_benchmark_1(self):
        benchmark(1, 26)

    def test_benchmark_2(self):
        benchmark(2, 38)

    def test_benchmark_3(self):
        benchmark(3, 73)

    def test_benchmark_4(self):
        benchmark(4, 17)

    def test_benchmark_5(self):
        benchmark(5, 110)

    def test_benchmark_6(self):
        benchmark(6, 21)

    # TODO one agent doesnt work yet
    # def test_benchmark_7(self):
    #     benchmark(7, xx)

    # TODO one agent doesnt work yet
    # def test_benchmark_8(self):
    #     benchmark(8, xx)

    def test_benchmark_9(self):
        benchmark(9, 2677)

    # TODO cant solve it within a decent time
    # def test_benchmark_10(self):
    #     benchmark(10, xx)

    def test_benchmark_11(self):
        benchmark(11, 110)

    def test_benchmark_12(self):
        benchmark(12, 110)

    def test_benchmark_13(self):
        benchmark(13, 43)

    # TODO one agent doesnt work yet
    # def test_benchmark_14(self):
    #     benchmark(14, xx)

    def test_benchmark_15(self):
        benchmark(15, 76)

    def test_benchmark_16(self):
        benchmark(16, 76)

    def test_benchmark_17(self):
        benchmark(17, 41)
