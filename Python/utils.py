from heapq import heappush, heappop
import itertools
from collections import deque

def euclidian_distance(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def dijkstra_predecessor_and_distance(G, source):
    dist = {}  # dictionary of final distances
    pred = {source: []}  # dictionary of predecessors
    seen = {source: 0}
    c = 1
    fringe = []  # use heapq with (distance,label) tuples
    heappush(fringe, (0, c, source))
    while fringe:
        (d, _, v) = heappop(fringe)
        if v in dist:
            continue  # already searched this node.
        dist[v] = d
        neighbours = G[v]
        for neighbour in neighbours:
            vw_dist = d + 1
            if neighbour not in seen or vw_dist < seen[neighbour]:
                seen[neighbour] = vw_dist
                c += 1
                heappush(fringe, (vw_dist, c, neighbour))
                pred[neighbour] = [v]
            elif vw_dist == seen[neighbour]:
                pred[neighbour].append(v)
    return pred, dist


def tsp_greedy(start, end, waypoints, distances):
    graph = {}
    graph[start] = [(distances[i][start], waypoints[i]) for i in range(len(waypoints))] + [(distances[-1][start], end),
                                                                                           (0, (-1, -1))]
    graph[start].sort()
    graph[end] = [(distances[i][end], waypoints[i]) for i in range(len(waypoints))] + [(distances[-1][start], start),
                                                                                       (0, (-1, -1))]
    graph[end].sort()
    graph[(-1, -1)] = [(0, start), (0, end)]
    for index, waypoint in enumerate(waypoints):
        graph[waypoint] = [(distances[i][waypoint], waypoints[i]) for i in range(len(waypoints))] + [
            (distances[index][start], start), (distances[-1][waypoint], end)]
        graph[waypoint].sort()
    # Greedy
    n_nodes = len(waypoints) + 3
    visited = []
    visited.append(end)
    current = end
    while len(visited) < n_nodes:
        index = 0
        while graph[current][index][1] in visited:
            if start == end == graph[current][index][1] and visited.count(start) < 2:
                break
            index += 1
        next = graph[current][index][1]
        visited.append(next)
        current = next
    return visited[3:]


def tsp(start, end, waypoints, distances):
    graph = {}
    graph[start] = {waypoints[i]: distances[i][start] for i in range(len(waypoints))}
    graph[end] = {waypoints[i]: distances[i][end] for i in range(len(waypoints))}
    for index, waypoint in enumerate(waypoints):
        graph[waypoint] = {waypoints[i]: distances[i][waypoint] for i in range(len(waypoints))}
        graph[waypoint][start] = distances[index][start]
        graph[waypoint][end] = distances[-1][waypoint]
    # Optimal
    best_path = None
    best_cost = float('inf')
    for path in itertools.permutations(waypoints):
        path = list(path)
        path.insert(0, start)
        path.append(end)
        path_cost = 0
        for i in range(len(path) - 1):
            current = path[i]
            next = path[i + 1]
            path_cost += graph[current][next]
        if path_cost < best_cost:
            best_path = path
            best_cost = path_cost
    return best_path[1:-1]
