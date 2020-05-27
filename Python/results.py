import numpy as np
import seaborn as sns
import matplotlib.pylab as plt
from mapfw import get_all_benchmarks
from matplotlib.colors import LogNorm


uniform_data = np.random.rand(5, len(get_all_benchmarks()))
plt.figure(figsize=(len(get_all_benchmarks()), 5))
ax = sns.heatmap(uniform_data, xticklabels=get_all_benchmarks(), cmap="viridis", norm=LogNorm(), annot=True, linewidth=0.5)
plt.show()