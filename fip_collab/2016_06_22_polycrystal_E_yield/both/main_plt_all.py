import plot_correlation as pltcorr
import plot_dist as pdi
import plot_explained_variance_all as pev
import plot_pc_map_3d as pltmap
import plot_dendrogram as pd
import plot_pc_vs_poly_all as ppp
import plot_linkage_check as plc
import numpy as np
from constants import const
import matplotlib.pyplot as plt


C = const()

names_cal = C['names_cal']
set_id_cal = C['set_id_cal']
strt_cal = C['strt_cal']
ns_cal = C['ns_cal']
dir_cal = C['dir_cal']

names_val = C['names_val']
set_id_val = C['set_id_val']
strt_val = C['strt_val']
ns_val = C['ns_val']
dir_val = C['dir_val']

# """Plot an autocorrelation"""
# sn = 0
# iA = 1
# iB = 1
# pltcorr.pltcorr(ns_cal[0], set_id_cal[0], sn, iA, iB)

# """Plot the distances between clusters"""
# pdi.pltdist(4)
# pdi.pltdist(9)
# pdi.pltdist(23)

"""Plot the percentage explained variance"""
pev.variance([0, 40, 0, 105])

"""Plot the microstructures in PC space"""
pcA = 0
pcB = 1
pcC = 2
pltmap.pltmap(4, pcA, pcB, pcC)
pltmap.pltmap(9, pcA, pcB, pcC)
pltmap.pltmap(23, pcA, pcB, pcC)

"""Plot a dendrogram"""
pd.pltdend(ns_val, set_id_val, names_val, 4)
pd.pltdend(ns_val, set_id_val, names_val, 9)
pd.pltdend(ns_val, set_id_val, names_val, 23)

"""Plot the errors versus number of PCs and polynomial order"""
ppp.pltpcpoly('modulus', 150)
ppp.pltpcpoly('strength', 150)

"""Plot the predicted versus actual values of the property of interest"""
plc.plot_check('modulus', n_pc=30, n_poly=2, H=4)
plc.plot_check('modulus', n_pc=30, n_poly=2, H=9)
plc.plot_check('modulus', n_pc=30, n_poly=2, H=23)

plc.plot_check('strength', n_pc=30, n_poly=2, H=4)
plc.plot_check('strength', n_pc=30, n_poly=2, H=9)
plc.plot_check('strength', n_pc=30, n_poly=2, H=23)

plt.show()
