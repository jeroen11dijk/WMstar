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


def tsp_dynamic(start, end, waypoints, distances):
    matrix = []
    dummy = (-1, -1)
    nodes = [start, dummy, end] + waypoints
    matrix.append([0, 0, distances[end][start]])
    matrix.append([0, 0, 0])
    matrix.append([distances[end][start], 0, 0])
    for i, waypoint in enumerate(waypoints):
        matrix[0].append(distances[waypoint][start])
        matrix[1].append(float("inf"))
        matrix[2].append(distances[waypoint][end])
        current_row = [distances[waypoint][start], float("inf"), distances[waypoint][end]]
        for other in waypoints:
            current_row.append(distances[waypoint][other])
        matrix.append(current_row)
    best_path = []
    indices = held_karp(matrix)
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


def disjoint(set_list):
    result = []
    for s in set_list:
        for elem in s:
            for output_set in result:
                if elem in output_set:
                    output_set.update(s)
                    break
            else:
                continue
            break
        else:
            result.append(s)
    return result


def isSubset(config, collisions):
    for collision_set in collisions:
        if len(config.collisions) == 0:
            return False
        for config_collision_set in config.collisions:
            if collision_set.issubset(config_collision_set):
                break
            return False
    return True
