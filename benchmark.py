from mapfw import MapfwBenchmarker
from matplotlib.pyplot import show
from networkx import grid_graph, draw_networkx
import cProfile

from mstar import Mstar


# Problem 1 has a grid of 28x26 yet the width and height are given as 27x26

def solve(problem):
    graph = grid_graph([len(problem.grid), len(problem.grid[0])])
    for i in range(len(problem.grid)):
        for j in range(len(problem.grid[0])):
            if problem.grid[i][j] == 1:
                graph.remove_node((j, i))
    v_I = []
    for start in problem.starts:
        v_I.append((start[0], start[1]))
    v_I = tuple(v_I)
    v_F = []
    for target in problem.goals:
        v_F.append((target[0], target[1]))
    v_F = tuple(v_F)
    configs = Mstar(graph, v_I, v_F)[0]
    res = []
    for i in range(len(problem.starts)):
        path = []
        for t_config in configs:
            path.append(list(t_config))
        res.append(path)
    return res


benchmarker = MapfwBenchmarker("42cf6ce8D2A5B954", 6, "M*", "Version 1 (Without inversing)", True)

for problem in benchmarker:
    problem.add_solution(solve(problem))

# benchmarker.submit()