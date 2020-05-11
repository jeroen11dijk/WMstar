from heapq import heappush, heappop
from itertools import count


def dijkstra_predecessor_and_distance(G, source):
    dist = {}  # dictionary of final distances
    pred = {source: []}  # dictionary of predecessors
    seen = {source: 0}
    c = count()
    fringe = []  # use heapq with (distance,label) tuples
    heappush(fringe, (0, next(c), source))
    while fringe:
        (d, _, v) = heappop(fringe)
        if v in dist:
            continue  # already searched this node.
        dist[v] = d
        neighbours = G[v]
        for neighbour in neighbours:
            vw_dist = dist[v] + 1
            if neighbour in dist:
                if vw_dist < dist[neighbour]:
                    raise ValueError('Contradictory paths found:',
                                     'negative weights?')
            elif neighbour not in seen or vw_dist < seen[neighbour]:
                seen[neighbour] = vw_dist
                heappush(fringe, (vw_dist, next(c), neighbour))
                pred[neighbour] = [v]
            elif vw_dist == seen[neighbour]:
                pred[neighbour].append(v)
    return pred, dist
