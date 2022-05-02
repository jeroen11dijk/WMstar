from Python.mstar import Mstar


def convert_graph(graph):
    grap_new = {}
    height = len(graph)
    width = len(graph[0])
    for i in range(len(graph)):
        for j in range(len(graph[0])):
            if graph[i][j] == 0:
                current = (j, i)
                neighbours = []
                if i != 0 and graph[i - 1][j] == 0:
                    neighbours.append((j, i - 1))
                if j != 0 and graph[i][j - 1] == 0:
                    neighbours.append((j - 1, i))
                if i != height - 1 and graph[i + 1][j] == 0:
                    neighbours.append((j, i + 1))
                if j != width - 1 and graph[i][j + 1] == 0:
                    neighbours.append((j + 1, i))
                grap_new[current] = neighbours
    return grap_new


if __name__ == '__main__':
    n_agents = 2
    problem_graph = [[0, 0, 0, 0, 0, 0, 0],
                     [0, 1, 0, 1, 0, 1, 0],
                     [0, 1, 0, 1, 0, 1, 0],
                     [0, 1, 0, 1, 0, 1, 0],
                     [0, 1, 0, 1, 0, 1, 0],
                     [0, 1, 0, 1, 0, 1, 0],
                     [0, 1, 0, 1, 0, 1, 0],
                     [0, 1, 0, 1, 0, 1, 0],
                     [0, 0, 0, 0, 0, 0, 0]]
    start = ((6, 0), (0, 0))
    waypoints = tuple([()] * n_agents)
    end = ((0, 4), (0, 8))
    graph = convert_graph(problem_graph)
    res = Mstar(graph, start, waypoints, end).solve()[0]
    print(res)
