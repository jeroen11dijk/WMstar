import matplotlib.pylab as plt
import numpy as np
from mapfw import get_all_benchmarks

Mstar_times_CPP = [7, 8, 2, 7, 153, 2, 24, 24210, 5160, np.nan, 3, 82, 1002, 1, 3, 3, 15550, 38, np.nan, 43, np.nan,
                   1005, 536, np.nan, 648, 24, 334, 5290, np.nan, 5620, np.nan, 1, 2450, 14]
Mstar_inflated_times_CPP = [11, 12, 2, 6, 556, 3, 24, 27770, 472, 244, 4, 133, 2180, 1, 6, 8, 17000, 2, 31040, 58,
                            np.nan, 5, 572, 68000, 119, 24, 52, 53980, 67000, 5830, 23380, 1, 1440, 18]

Mstar_times_Python = [11, 19, 8, 24, 3710, 5, 24, 49540, 11500, np.nan, 2, 1280, 12410, 1, 16, 21, 25730, 5, np.nan,
                      173, np.nan, 5130, np.nan, np.nan, 12390, 117, 11140, 68000, np.nan, 58770, np.nan, 2, 3270, 43]
Mstar_inflated_times_Python = [10, 18, 9, 16, 1160, 7, 20, 48540, 264, 454, 2, 64, 5610, 1, 10, 15, 21110, 3, 27590,
                               168, np.nan, 6, 1380, 113000, 350, 49, 273, 54180, 11250, 29510, np.nan, 2, 3380, 222]

res = []
res_inflated = []
for i in range(len(Mstar_times_CPP)):
    res.append(Mstar_times_Python[i] / Mstar_times_CPP[i])
    res_inflated.append(Mstar_inflated_times_Python[i] / Mstar_inflated_times_CPP[i])

x_axis = sorted(get_all_benchmarks(without=[54, 58, 77, 78]))
ticks = [i for i in range(len(res))]
plt.plot(res, '--bo', color="red")
plt.plot(res_inflated, '--bo', color="green")
plt.xticks(ticks, x_axis)
plt.legend(["Normal", "Inflated"])
plt.xlabel('Benchmark')
plt.ylabel('The factor of the speed up of the C++ implementation')
plt.yscale("log")
plt.show()
