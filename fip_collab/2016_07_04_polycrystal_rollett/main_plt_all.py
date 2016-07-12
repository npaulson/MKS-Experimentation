import plot_correlation_slc as pcs
import plot_dist as pdi
import plot_explained_variance_all as pev
import plot_pc_map_3d as pltmap3d
import plot_pc_map as pltmap
import plot_dendrogram as pd
import plot_pc_vs_poly_all as ppp
import plot_linkage_check as plc
import numpy as np
from constants import const
import matplotlib.pyplot as plt


C = const()

names = C['names']
set_id = C['set_id']

"""Plot a correlation"""
pcs.pltcorr()

"""Plot the distances between clusters"""
# pdi.pltdist(4)
# pdi.pltdist(9)
# pdi.pltdist(23)

"""Plot the percentage explained variance"""
pev.variance([0, 11, 90, 101])

"""Plot the microstructures in PC space"""
pcA = 0
pcB = 1
pcC = 2
pltmap.pltmap(15, pcA, pcB)
pltmap3d.pltmap(15, pcA, pcB, pcC)


"""Plot a dendrogram"""
pd.pltdend(set_id, names, 15)

# """Plot the errors versus number of PCs and polynomial order"""
# ppp.pltpcpoly('modulus', 15)
# ppp.pltpcpoly('strength', 15)

# """Plot the predicted versus actual values of the property of interest"""
# plc.plot_check('modulus', n_pc=2, n_poly=2, H=9)
# plc.plot_check('strength', n_pc=3, n_poly=2, H=9)

plt.show()
