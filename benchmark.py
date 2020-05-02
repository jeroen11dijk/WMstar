from mapfw import MapfwBenchmarker
from networkx import grid_graph

from mstar import Mstar


def solve(problem):
    # Create a networkx graph
    graph = grid_graph([len(problem.grid), len(problem.grid[0])])
    for i in range(len(problem.grid)):
        for j in range(len(problem.grid[0])):
            if problem.grid[i][j] == 1:
                graph.remove_node((j, i))
    # Create V_I and v_F
    v_I = tuple(tuple(start) for start in problem.starts)
    v_W = tuple(tuple(waypoint) for waypoint in problem.waypoints)
    v_F = tuple(tuple(target) for target in problem.goals)
    # Run the algorithm
    configs = Mstar(graph, v_I, v_W, v_F)[0]
    # Convert to the accepted format
    res = []
    for i in range(len(problem.starts)):
        res.append([list(config[i]) for config in configs])
    return res


benchmarker = MapfwBenchmarker("42cf6ce8D2A5B954", 3, "M*", "Version 0.1 for 1 waypoint", True)


for problem in benchmarker:
    print(problem.waypoints)
    print(solve(problem))
    problem.add_solution(solve(problem))
