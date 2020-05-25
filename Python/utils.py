import itertools
import math
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
    print(graph[start])
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


def tsp_dynamic(start, end, waypoints, distances):
    matrix = []
    nodes = [start, (-1, -1), end] + waypoints
    matrix.append([0, 0, distances[-1][start]] + [distances[i][start] for i in range(len(waypoints))])
    matrix.append([0, 0, 0] + len(waypoints) * [math.inf])
    matrix.append([distances[-1][start], 0, 0] + [distances[i][end] for i in range(len(waypoints))])
    for index, waypoint in enumerate(waypoints):
        matrix.append([distances[index][start], math.inf, distances[-1][waypoint]] + [distances[i][waypoint] for i in
                                                                                      range(len(waypoints))])
    indices = held_karp(matrix)
    best_path = []
    for index in indices:
        best_path.append(nodes[index])
    return best_path[1:-2]


# Credits: https://github.com/CarlEkerot/held-karp
def held_karp(dists):
    """
    Implementation of Held-Karp, an algorithm that solves the Traveling
    Salesman Problem using dynamic programming with memoization.
    Parameters:
        dists: distance matrix
    Returns:
        A tuple, (cost, path).
    """
    n = len(dists)

    # Maps each subset of the nodes to the cost to reach that subset, as well
    # as what node it passed before reaching this subset.
    # Node subsets are represented as set bits.
    C = {}

    # Set transition cost from initial state
    for k in range(1, n):
        C[(1 << k, k)] = (dists[0][k], 0)

    # Iterate subsets of increasing length and store intermediate results
    # in classic dynamic programming manner
    for subset_size in range(2, n):
        for subset in itertools.combinations(range(1, n), subset_size):
            # Set bits for all nodes in this subset
            bits = 0
            for bit in subset:
                bits |= 1 << bit

            # Find the lowest cost to get to this subset
            for k in subset:
                prev = bits & ~(1 << k)

                res = []
                for m in subset:
                    if m == 0 or m == k:
                        continue
                    res.append((C[(prev, m)][0] + dists[m][k], m))
                C[(bits, k)] = min(res)

    # We're interested in all bits but the least significant (the start state)
    bits = (2 ** n - 1) - 1

    # Calculate optimal cost
    res = []
    for k in range(1, n):
        res.append((C[(bits, k)][0] + dists[k][0], k))
    _, parent = min(res)

    # Backtrack to find full path
    path = []
    for i in range(n - 1):
        path.append(parent)
        new_bits = bits & ~(1 << parent)
        _, parent = C[(bits, parent)]
        bits = new_bits

    # Add implicit start state
    path.append(0)

    return list(reversed(path))


def phi(v_l, v_k):
    seen = set()
    double = []
    edges = {}
    for i in range(len(v_k)):
        edges[v_k[i]] = v_l[i]
    for i, val in enumerate(v_l):
        if val in seen or val != v_k[i] and val in edges and edges[val] == v_k[i]:
            double.append(val)
        else:
            seen.add(val)
    double = set(double)
    return [i for i, val in enumerate(v_l) if val in double]