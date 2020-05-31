from mapfw import MapfwBenchmarker


def solve(problem):
    from Python.test_python_benchmarks import setup_benchmark
    from Python.mstar import Mstar
    graph, v_I, v_W, v_F = setup_benchmark(problem)
    return Mstar(graph, v_I, v_W, v_F, True).solve()[0]


benchmarks = [31, 32, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51]

if __name__ == '__main__':
    for i in range(9):
        benchmarker = MapfwBenchmarker("42cf6ce8D2A5B954", benchmarks, "M*", "Python inflated", False, solver=solve,
                                       cores=-1, timeout=60000)
        benchmarker.run()
