# import plot_correlation as pltcorr
# import plot_dist as pdi
import plot_explained_variance as pev
import plot_pc_map_3d as pltmap3d
import plot_pc_map_cal as pltmap_cal
import plot_pc_map_val as pltmap_val
import plot_dendrogram as pd
import plot_err_v_pc as pevp
import plot_linkage_check_gray as plc
import numpy as np
from constants import const
import matplotlib.pyplot as plt


C = const()

names_cal = C['names_plt_cal']
set_id_cal = C['set_id_cal']
strt_cal = C['strt_cal']
ns_cal = C['ns_cal']
dir_cal = C['dir_cal']

names_val = C['names_plt_val']
set_id_val = C['set_id_val']
strt_val = C['strt_val']
ns_val = C['ns_val']
dir_val = C['dir_val']

Hvec = [6, 15, 41, 90]
# Hvec = [15]

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
pev.variance([.5, 15, 40, 105], Hvec)

"""Plot the microstructures in PC space"""
pcA = 0
pcB = 1
pcC = 2
pltmap_cal.pltmap(15, pcA, pcB)
pltmap_val.pltmap(15, pcA, pcB)
pltmap3d.pltmap(15, pcA, pcB, pcC)

"""Plot a dendrogram"""
pd.pltdend(ns_cal, set_id_cal, names_cal, 15)

"""Plot the errors versus number of PCs and polynomial order"""
pevp.plterr('modulus', 60, 0.6, ['cal'], Hvec)
pevp.plterr('modulus', 60, 0.6, ['LOOCV'], Hvec)
pevp.plterr('modulus', 60, 0.6, ['val'], Hvec)
pevp.plterr('strength', 60, 4, ['cal'], Hvec)
pevp.plterr('strength', 60, 4, ['LOOCV'], Hvec)
pevp.plterr('strength', 60, 4, ['val'], Hvec)

"""Plot the predicted versus actual values of the property of interest"""
plc.plot_check('modulus', n_pc=3, n_poly=2, H=15)
plc.plot_check('strength', n_pc=6, n_poly=2, H=41)

plt.show()
