from heapq import heappush, heappop


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


def tsp(start, end, waypoints, distances):
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
