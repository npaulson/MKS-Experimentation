import plot_correlation as pltcorr
import plot_dist as pdi
import plot_explained_variance_all as pev
import plot_pc_map as pltmap
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

"""Plot the distances between clusters"""
pdi.pltdist(4)
pdi.pltdist(9)
pdi.pltdist(23)

"""Plot the percentage explained variance"""
pev.variance([0, 10, 0, 110])
pev.variance([0, 150, 98, 100.2])

"""Plot the microstructures in PC space"""
pcA = 0
pcB = 1
pltmap.pltmap(4, pcA, pcB)
pltmap.pltmap(9, pcA, pcB)
pltmap.pltmap(23, pcA, pcB)

# H = 4
# pltmap.pltmap(ns_cal, names_cal, set_id_cal, 'cal', H, pcA, pcB)
# pltmap.pltmap(ns_val, names_val, set_id_val, 'val', H, pcA, pcB)
# H = 9
# pltmap.pltmap(ns_cal, names_cal, set_id_cal, 'cal', H, pcA, pcB)
# pltmap.pltmap(ns_val, names_val, set_id_val, 'val', H, pcA, pcB)
# H = 23
# pltmap.pltmap(ns_cal, names_cal, set_id_cal, 'cal', H, pcA, pcB)
# pltmap.pltmap(ns_val, names_val, set_id_val, 'val', H, pcA, pcB)

"""Plot a dendrogram"""
pd.pltdend(ns_val, set_id_val, names_val, 4)
pd.pltdend(ns_val, set_id_val, names_val, 9)
pd.pltdend(ns_val, set_id_val, names_val, 23)

"""Plot the errors versus number of PCs and polynomial order"""
ppp.pltpcpoly('modulus', 15)
ppp.pltpcpoly('strength', 15)
ppp.pltpcpoly('modulus', 150)
ppp.pltpcpoly('strength', 150)

"""Plot the predicted versus actual values of the property of interest"""
plc.plot_check('modulus', n_pc=2, n_poly=2, H=4)
plc.plot_check('modulus', n_pc=2, n_poly=2, H=9)
plc.plot_check('modulus', n_pc=2, n_poly=2, H=23)

plc.plot_check('strength', n_pc=2, n_poly=2, H=4)
plc.plot_check('strength', n_pc=3, n_poly=2, H=9)
plc.plot_check('strength', n_pc=4, n_poly=2, H=23)

# plt.show()
