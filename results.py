import os

import numpy as np
import seaborn as sns
import matplotlib.pylab as plt
from mapfw import get_all_benchmarks
from matplotlib.colors import LogNorm

Mstar_cost = [36, 48, 75, 26, 119, 27, 205, 821, 1741, np.nan, 100, 115, 52, 34, 70, 70, 53, 51, np.nan, 43, np.nan, 115, 144, np.nan, 120, 169, 333, 28, 39, np.nan, 65, np.nan, 14, 96, 94]
Mstar_inflated_cost = [36, 48, 75, 26, 119, 27, 205, 821, 1741, 1598, 100, 117, 52, 34, 70, 70, 53, 51, 2921, 43, np.nan, 115, 144, 1551, 120, 169, 333, 28, 39, 850, 65, 1197, 14, 96, 94]

CBS_cost = [36, 48, 75, 26, 119, 27, 205, 821, 1733, 1590, 100, 115, 52, 34, 70, 70, 53, 51, np.nan, 43, 252, 114, 138, 1542, 114, 169, 333, np.nan, np.nan, 824, 65, 1156, 14, 96, 94]
Astar_cost = [36, 48, 75, 26, 119, 27, 205, 821, np.nan, np.nan, 100, 115, 52, 34, 70, 70, 53, 51, np.nan, 43, 252, 114, 138, np.nan, 114, 169, 333, 28, 39, np.nan, 65, np.nan, 14, 96, 94]
MLA_cost = [36, 49, 87, np.nan, 131, 27, 347, 1149, 2264, 2624, 102, 121, 63, 36, 88, 98, 56, 56, 4410, np.nan, 533, 182, 286, 2023, 215, 193, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan]
BCP_cost = [36, 48, 75, 26, 199, 27, np.nan, np.nan, np.nan, 1590, 100, 115, 52, np.nan, 70, 70, 53, 51, np.nan, 43, 252, 114, 138, 1994, 114, 169, 333, 28, 39, 824, 65, 1331, np.nan, np.nan, np.nan]

y_axis = ["M*", "M* inflated", "CBS", "MLA*", "A*+OD+ID", "BCP"]
x_axis = sorted(get_all_benchmarks(without=[54, 58]))

zipper = zip(Mstar_cost, Mstar_inflated_cost, CBS_cost, MLA_cost, Astar_cost, BCP_cost)
data = []
for i in range(len(y_axis)):
    data.append([])
for benchmark in zipper:
    optimal = np.nanmin(benchmark)
    for i in range(len(benchmark)):
        if (benchmark[i] - optimal) == 0:
            data[i].append(1)
        else:
            data[i].append(1 + (benchmark[i] - optimal))


plt.figure(figsize=(len(get_all_benchmarks()), 5))
ax = sns.heatmap(data, xticklabels=x_axis, yticklabels=y_axis, norm=LogNorm(), cmap="magma_r", annot=True, linewidth=0.5)
plt.show()
