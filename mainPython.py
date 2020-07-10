from mapfw import MapfwBenchmarker, get_all_benchmarks


def solve(problem):
    from Python.test_python_benchmarks import setup_benchmark
    from Python.mstar import Mstar
    graph, v_I, v_W, v_F = setup_benchmark(problem)
    res = Mstar(graph, v_I, v_W, v_F, ordered=True).solve()[0]
    return res


if __name__ == '__main__':
    benchmarker = MapfwBenchmarker("42cf6ce8D2A5B954", get_all_benchmarks(without=[10, 19, 21, 23, 24, 54, 58, 59, 61]), "WM*", "Python Ordered", False,
                                   solver=solve, cores=1)
    benchmarker.run()
