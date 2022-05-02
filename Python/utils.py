from heapq import heappush, heappop
from queue import Queue
from typing import Dict, Tuple


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


def dynamic_tsp(waypoints, target, distances, cache) -> Dict[Tuple[int, int], int]:
    """
    Calculates the minimal path from each way point to the goal, via all
    the other waypoints.
    """
    cache_key = tuple(sorted(waypoints) + [target])
    if cache_key in cache:
        return cache[cache_key]

    ordered_waypoints = list(waypoints)
    n = len(ordered_waypoints)
    all_indices = set(range(n))

    memory = {}
    queue = Queue()

    for index, wp in enumerate(ordered_waypoints):
        key = (index,), index
        queue.put(key)
        memory[key] = distances[target][wp], None

    while not queue.empty():
        prev_visited, prev_last_wp = queue.get()
        prev_dist, _ = memory[(prev_visited, prev_last_wp)]
        to_visit = all_indices.difference(set(prev_visited))

        for new_last_point in to_visit:
            new_visited = tuple(sorted(prev_visited + (new_last_point,)))
            wpb = ordered_waypoints[new_last_point]
            new_dist = prev_dist + distances[wpb][ordered_waypoints[prev_last_wp]]

            new_key = new_visited, new_last_point
            new_value = new_dist, prev_last_wp

            if new_key not in memory:
                memory[new_key] = new_value
                queue.put(new_key)
            else:
                if new_dist < memory[new_key][0]:
                    memory[new_key] = new_value

    result = {}
    full_path = tuple(range(n))
    for index, wp in enumerate(ordered_waypoints):
        result[wp] = memory[(full_path, index)][0]

    cache[cache_key] = result
    return result


def phi(v_l, v_k):
    res = set()
    for a1 in range(len(v_k)):
        for a2 in range(min(a1, len(v_l))):
            if v_l[a1] == v_l[a2]:
                res.add(a1)
                res.add(a2)
            elif v_k[a1] == v_l[a2] and v_l[a1] == v_k[a2]:
                res.add(a1)
                res.add(a2)
    return len(res) > 0, res


def issubset(a, b):
    for s in a:
        for os in b:
            if s.issubset(os):
                break
        else:
            return False
    return True
