from mapfw import MapfwBenchmarker
from matplotlib.pyplot import show
from networkx import grid_graph, draw_networkx

from mstar import Mstar


# Problem 1 has a grid of 28x26 yet the width and height are given as 27x26

def solve(problem):
    graph = grid_graph([28, problem.height])
    for i in range(len(problem.grid)):
        for j in range(len(problem.grid[0])):
            if problem.grid[i][j] == 1:
                graph.remove_node((i, j))
    v_I = []
    for start in problem.starts:
        v_I.append((start[1], start[0]))
    v_I = tuple(v_I)
    v_F = []
    for target in problem.goals:
        v_F.append((target[1], target[0]))
    v_F = tuple(v_F)
    configs = Mstar(graph, v_I, v_F)[0]
    res = []
    for i in range(len(problem.starts)):
        path = []
        for t_config in configs:
            path.append(list(t_config[i]))
        res.append(path)
    """
    Now paths looks like:

    paths = [path agent 1, path agent 2, ..]
    path agent 1 = [pos agent 1 at time 0, pos agent 1 at time 1, .., pos agent 1 at finishing time]
    pos = [x coordinate, y coordinate]
    """

    return res


benchmarker = MapfwBenchmarker("42cf6ce8D2A5B954", 1, "M*", "Version 1", False)
for problem in benchmarker:
    solve(problem)