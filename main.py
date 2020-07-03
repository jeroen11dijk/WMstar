import multiprocessing
from typing import List

import click
from mapfw import MapfwBenchmarker
from mapfw.problem import Problem


def solve(problem, ordered=False, inflated=False):
    from Python.test_python_benchmarks import setup_benchmark
    from Python.mstar import Mstar
    graph, v_I, v_W, v_F = setup_benchmark(problem)
    res = Mstar(graph, v_I, v_W, v_F, ordered=ordered, inflated=inflated).solve()[0]
    return res


@click.command()
@click.argument('benchmarks', required=True, nargs=-1, type=int)
@click.option('--name', '-n',
              type=str,
              help="Name of the algorithm version, can be left empty to "
                   "generate based on options.")
@click.option('--inflated', '-i', is_flag=True, default=False,
              help="Inflate the heuristic by 1.1")
@click.option('--cores', '-c',
              type=click.IntRange(1, multiprocessing.cpu_count()),
              default=1,
              help="Number of cores to use concurrently, "
                   "requires more than one benchmark "
                   "or a progressive benchmark.")
@click.option('--debug', '-d', is_flag=True, default=True,
              help="Run benchmark(s) as debug attempt.")
@click.option('--unordered', '-u', is_flag=True, default=True,
              help="Unordered variant where the order of the waypoint visits doesnt matter")
@click.option('--official', '-o', is_flag=True, default=False,
              help="Indicate this is an officially timed run on the "
                   "TU Delft server. Will append '(TU)' to the version.")
def main(benchmarks, name, inflated, unordered, cores, debug, official):
    if inflated:
        algorithm = "M* Inflated"
    else:
        algorithm = "M*"
    if not name:
        name = "Python"
        if not unordered:
            name += " Ordered"
        if official:
            name += " (TU)"

    def prepped_solver(problem: Problem) -> List:
        return solve(problem, inflated=inflated, ordered=not unordered)

    benchmarker = MapfwBenchmarker("42cf6ce8D2A5B954", benchmarks, algorithm, "Python Ordered", debug,
                                   solver=prepped_solver, cores=cores)
    benchmarker.run()


if __name__ == '__main__':
    main()
