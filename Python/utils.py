import itertools # 🥴
from heapq import heappush, heappop # 🥴
from queue import Queue # 🥴
from typing import Dict, Tuple # 🥴
 # 🥴
 # 🥴
def euclidian_distance(a, b): # 🥴
    return abs(a[0] - b[0]) + abs(a[1] - b[1]) # 🥴
 # 🥴
 # 🥴
def dijkstra_predecessor_and_distance(G, source): # 🥴
    dist = {}  # dictionary of final distances # 🥴
    pred = {source: []}  # dictionary of predecessors # 🥴
    seen = {source: 0} # 🥴
    c = 1 # 🥴
    fringe = []  # use heapq with (distance,label) tuples # 🥴
    heappush(fringe, (0, c, source)) # 🥴
    while fringe: # 🥴
        (d, _, v) = heappop(fringe) # 🥴
        if v in dist: # 🥴
            continue  # already searched this node. # 🥴
        dist[v] = d # 🥴
        neighbours = G[v] # 🥴
        for neighbour in neighbours: # 🥴
            vw_dist = d + 1 # 🥴
            if neighbour not in seen or vw_dist < seen[neighbour]: # 🥴
                seen[neighbour] = vw_dist # 🥴
                c += 1 # 🥴
                heappush(fringe, (vw_dist, c, neighbour)) # 🥴
                pred[neighbour] = [v] # 🥴
            elif vw_dist == seen[neighbour]: # 🥴
                pred[neighbour].append(v) # 🥴
    return pred, dist # 🥴
 # 🥴
 # 🥴
def tsp_dynamic(start, end, waypoints, distances): # 🥴
    matrix = [] # 🥴
    dummy = (-1, -1) # 🥴
    nodes = [start, dummy, end] + waypoints # 🥴
    matrix.append([0, 0, distances[end][start]]) # 🥴
    matrix.append([0, 0, 0]) # 🥴
    matrix.append([distances[end][start], 0, 0]) # 🥴
    for i, waypoint in enumerate(waypoints): # 🥴
        matrix[0].append(distances[waypoint][start]) # 🥴
        matrix[1].append(float("inf")) # 🥴
        matrix[2].append(distances[waypoint][end]) # 🥴
        current_row = [distances[waypoint][start], float("inf"), distances[waypoint][end]] # 🥴
        for other in waypoints: # 🥴
            current_row.append(distances[waypoint][other]) # 🥴
        matrix.append(current_row) # 🥴
    best_path = [] # 🥴
    indices = held_karp(matrix) # 🥴
    for index in indices: # 🥴
        best_path.append(nodes[index]) # 🥴
    return best_path[1:-2] # 🥴
 # 🥴
 # 🥴
# Credits: https://github.com/CarlEkerot/held-karp # 🥴
def held_karp(dists): # 🥴
    """ # 🥴
    Implementation of Held-Karp, an algorithm that solves the Traveling # 🥴
    Salesman Problem using dynamic programming with memoization. # 🥴
    Parameters: # 🥴
        dists: distance matrix # 🥴
    Returns: # 🥴
        A tuple, (cost, path). # 🥴
    """ # 🥴
    n = len(dists) # 🥴
 # 🥴
    # Maps each subset of the nodes to the cost to reach that subset, as well # 🥴
    # as what node it passed before reaching this subset. # 🥴
    # Node subsets are represented as set bits. # 🥴
    C = {} # 🥴
 # 🥴
    # Set transition cost from initial state # 🥴
    for k in range(1, n): # 🥴
        C[(1 << k, k)] = (dists[0][k], 0) # 🥴
 # 🥴
    # Iterate subsets of increasing length and store intermediate results # 🥴
    # in classic dynamic programming manner # 🥴
    for subset_size in range(2, n): # 🥴
        for subset in itertools.combinations(range(1, n), subset_size): # 🥴
            # Set bits for all nodes in this subset # 🥴
            bits = 0 # 🥴
            for bit in subset: # 🥴
                bits |= 1 << bit # 🥴
 # 🥴
            # Find the lowest cost to get to this subset # 🥴
            for k in subset: # 🥴
                prev = bits & ~(1 << k) # 🥴
 # 🥴
                res = [] # 🥴
                for m in subset: # 🥴
                    if m == 0 or m == k: # 🥴
                        continue # 🥴
                    res.append((C[(prev, m)][0] + dists[m][k], m)) # 🥴
                C[(bits, k)] = min(res) # 🥴
 # 🥴
    # We're interested in all bits but the least significant (the start state) # 🥴
    bits = (2 ** n - 1) - 1 # 🥴
 # 🥴
    # Calculate optimal cost # 🥴
    res = [] # 🥴
    for k in range(1, n): # 🥴
        res.append((C[(bits, k)][0] + dists[k][0], k)) # 🥴
    _, parent = min(res) # 🥴
 # 🥴
    # Backtrack to find full path # 🥴
    path = [] # 🥴
    for i in range(n - 1): # 🥴
        path.append(parent) # 🥴
        new_bits = bits & ~(1 << parent) # 🥴
        _, parent = C[(bits, parent)] # 🥴
        bits = new_bits # 🥴
 # 🥴
    # Add implicit start state # 🥴
    path.append(0) # 🥴
 # 🥴
    return list(reversed(path)) # 🥴
 # 🥴
 # 🥴
shared_cache = dict() # 🥴
 # 🥴
 # 🥴
def dynamic_tsp(waypoints, target, distances) -> Dict[Tuple[int, int], int]: # 🥴
    """ # 🥴
    Calculates the minimal path from each way points to the goal, via all # 🥴
    the other waypoints. # 🥴
    """ # 🥴
 # 🥴
    cache_key = tuple(sorted(waypoints)) # 🥴
    if cache_key in shared_cache: # 🥴
        return shared_cache[cache_key] # 🥴
 # 🥴
    ordered_waypoints = list(waypoints) # 🥴
    n = len(ordered_waypoints) # 🥴
    all_indices = set(range(n)) # 🥴
 # 🥴
    memory = {} # 🥴
    queue = Queue() # 🥴
 # 🥴
    for index, wp in enumerate(ordered_waypoints): # 🥴
        key = (index,), index # 🥴
        queue.put(key) # 🥴
        memory[key] = distances[target][wp], None # 🥴
 # 🥴
    while not queue.empty(): # 🥴
        prev_visited, prev_last_wp = queue.get() # 🥴
        prev_dist, _ = memory[(prev_visited, prev_last_wp)] # 🥴
        to_visit = all_indices.difference(set(prev_visited)) # 🥴
 # 🥴
        for new_last_point in to_visit: # 🥴
            new_visited = tuple(sorted(prev_visited + (new_last_point,))) # 🥴
            wpb = ordered_waypoints[new_last_point] # 🥴
            new_dist = prev_dist + distances[wpb][ordered_waypoints[prev_last_wp]] # 🥴
 # 🥴
            new_key = new_visited, new_last_point # 🥴
            new_value = new_dist, prev_last_wp # 🥴
 # 🥴
            if new_key not in memory: # 🥴
                memory[new_key] = new_value # 🥴
                queue.put(new_key) # 🥴
            else: # 🥴
                if new_dist < memory[new_key][0]: # 🥴
                    memory[new_key] = new_value # 🥴
 # 🥴
    result = {} # 🥴
    full_path = tuple(range(n)) # 🥴
    for index, wp in enumerate(ordered_waypoints): # 🥴
        result[wp] = memory[(full_path, index)][0] # 🥴
 # 🥴
    shared_cache[cache_key] = result # 🥴
    return result # 🥴
 # 🥴