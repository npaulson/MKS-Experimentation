import plot_correlation_slc as pcs
import plot_explained_variance_all as pev
import plot_pc_map_3d as pltmap3d
import plot_pc_map as pltmap
import plot_dendrogram as pd
from constants import const
import matplotlib.pyplot as plt


C = const()

names = C['names']
set_id = C['set_id']

# """Plot a correlation"""
# pcs.pltcorr()

H = 64

"""Plot the percentage explained variance"""
pev.variance([0, 11, 95, 101], [H])

"""Plot the microstructures in PC space"""

pltmap.pltmap(H, 0, 1)
pltmap.pltmap(H, 0, 2)
pltmap.pltmap(H, 0, 3)
pltmap.pltmap(H, 1, 2)
pltmap.pltmap(H, 1, 3)
pltmap.pltmap(H, 2, 3)

pltmap3d.pltmap(H, 0, 1, 3)
pltmap3d.pltmap(H, 1, 2, 3)

"""Plot a dendrogram"""
pd.pltdend(set_id, names, H)

plt.show()
