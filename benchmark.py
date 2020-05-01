from mapfw import MapfwBenchmarker
from networkx import grid_graph

from mstar import Mstar


def solve(problem):
    graph = grid_graph([len(problem.grid), len(problem.grid[0])])
    for i in range(len(problem.grid)):
        for j in range(len(problem.grid[0])):
            if problem.grid[i][j] == 1:
                graph.remove_node((j, i))
    v_I = tuple(tuple(start) for start in problem.starts)
    v_F = tuple(tuple(target) for target in problem.goals)
    configs = Mstar(graph, v_I, v_F)[0]
    res = []
    for i in range(len(problem.starts)):
        path = []
        for t_config in configs:
            path.append(list(t_config[i]))
        res.append(path)
    return res


benchmarker = MapfwBenchmarker("42cf6ce8D2A5B954", 6, "M*", "Version 1.01 (Without inversing)", False)

for problem in benchmarker:
    problem.add_solution(solve(problem))

benchmarker.submit()
