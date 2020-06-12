from mapfw import MapfwBenchmarker

def solve(problem):
    from Python.test_python_benchmarks import setup_benchmark
    from Python.mstar import Mstar
    graph, v_I, v_W, v_F = setup_benchmark(problem)
    return Mstar(graph, v_I, v_W, v_F, False).solve()[0]


if __name__ == '__main__':
    benchmarker = MapfwBenchmarker("42cf6ce8D2A5B954", 1, "M*", "Python (TU)", True,
                                   solver=solve,
                                   cores=3)
    benchmarker.run()
