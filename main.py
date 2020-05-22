import sys
from mapfw import MapfwBenchmarker

from Python.mstar import Mstar
from Python.test_python_benchmarks import setup_benchmark


if __name__ == "__main__":
    benchmark = int(sys.argv[1])
    debug = sys.argv[2].lower() == 'true' if len(sys.argv) > 2 else True
    unordered = sys.argv[3].lower() == 'true' if len(sys.argv) > 3 else True
    optimal = sys.argv[4].lower() == 'true' if len(sys.argv) > 4 else True
    text = "Timon. Unordered: " + str(unordered) + ". Optimal: " + str(optimal)
    benchmarker = MapfwBenchmarker("42cf6ce8D2A5B954", benchmark, "M*", text, debug)
    for problem in benchmarker:
        graph, v_I, v_W, v_F = setup_benchmark(problem)
        problem.add_solution(Mstar(graph, v_I, v_W, v_F, unordered, optimal).solve()[0])