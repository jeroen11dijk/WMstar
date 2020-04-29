import networkx as nx
from matplotlib.pyplot import show, axis

G = nx.grid_2d_graph(4, 4)

v_I = ((0, 0), (0, 1))
v_F = ((2, 3), (0, 3))


def heuristic(u, v):
    return abs((u[0] - v[0])) + abs((u[1] - v[1]))

policy = []
for i in range(len(v_F)):
    opt = {}
    for node in G:
        path = nx.astar_path(G, node, v_F[i], heuristic)
        weight = sum(G[u][v].get('weight', 1) for u, v in zip(path[:-1], path[1:]))
        opt[node] = (path, weight)
    policy.append(opt)

nx.draw_networkx(G)
show()

G = nx.Graph()

G.add_edge('a', 'b')
G.add_edge('a', 'c', weight=0.2)
G.add_edge('c', 'd', weight=0.1)
G.add_edge('c', 'e', weight=0.7)
G.add_edge('c', 'f', weight=0.9)
G.add_edge('a', 'd', weight=0.3)
