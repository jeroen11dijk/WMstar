import matplotlib.pylab as plt
import numpy as np
import seaborn as sns
from mapfw import get_all_benchmarks
from matplotlib.colors import LogNorm

Mstar_times = [7, 8, 2, 7, 153, 2, 24, 24210, 5160, np.nan, 3, 82, 1002, 1, 3, 3, 15550, 38, np.nan, 43, np.nan, 1005,
               536, np.nan, 648, 24, 334, 82000, 5290, np.nan, 5620, np.nan, 1, 2450, 14]
Mstar_inflated_times = [11, 12, 2, 6, 556, 3, 24, 27770, 472, 244, 4, 133, 2180, 1, 6, 8, 17000, 2, 31040, 58,
                       np.nan, 5, 572, 68000, 119, 24, 52, 96000, 53980, 67000, 5830, 23380, 1, 1440, 18]

CBS_times = [1, 34, 7, 118, 1770, 11, 33, 118000, 171000, 33490, 12, 299, 31, 1, 64, 41, 4950, 7, np.nan, 941, 1680, 30,
             277, 406000, 1220, 63, 483, np.nan, np.nan, 98000, 7520, 3501000, 11, 1092, 372]
Astar_times = [3, 58, 11, 42, 27610, 17, 103, 90000, np.nan, np.nan, 25, 3590, 2040, 3, 77, 54, 112000, 18, np.nan, 210,
               7030, 88, 857, np.nan, 4280, 92, 11990, 13760, 516, np.nan, 1980, np.nan, 7, 6660, 154]
MLA_times = [1, 1, 6, np.nan, 53, 1, 35, 134, 228, 385, 7, 12, 2, 1, 13, 17, 8, 3, 861, np.nan, 20, 23, 45, 244, 14, 9,
             27, np.nan, np.nan, 104, np.nan, 246, np.nan, 6, np.nan]
BCP_times = [11, 172, 13, 45, 341, 28, np.nan, np.nan, np.nan, 30940, 17, 49, 30, np.nan, 30, 27, 385, 24, np.nan, 15,
             38, 9, 922, 1460, 494, 14, 2320, 8710, 67, 2549000, 247, 653000, 12, 599, 6930]

y_axis = ["WM*", "inflated WM*", "CBS", "MLA*", "A*+OD+ID", "BCP"]
x_axis = sorted(get_all_benchmarks(without=[54, 58, 77, 78]))

zipper = zip(Mstar_times, Mstar_inflated_times, CBS_times, MLA_times, Astar_times, BCP_times)
data = []
remove = []
for i in range(len(y_axis)):
    data.append([])
for i, benchmark in enumerate(zipper):
    optimal = np.nanmin(benchmark)
    if all(val == optimal or np.isnan(val) for val in benchmark):
        remove.append(i)
    else:
        for i in range(len(benchmark)):
            if (benchmark[i] - optimal) == 0:
                data[i].append(1)
            else:
                data[i].append(1 + (benchmark[i] - optimal))
for index in reversed(remove):
    x_axis.pop(index)

sns.set(font_scale=2)
plt.figure(figsize=(2 * len(x_axis), 1.5 * len(y_axis)))
ax = sns.heatmap(data, xticklabels=x_axis, yticklabels=y_axis, norm=LogNorm(), cmap="magma_r", annot=True,
                 linewidth=0.5)
plt.tight_layout()
plt.savefig(fname="times")
