# import plot_correlation as pltcorr
import plot_explained_variance as pev
import plot_pc_map_3d as pltmap3d
import plot_pc_map as pltmap
import plot_dendrogram as pd
import plot_err_v_pc as pevp
import plot_linkage_check_gray as plc
import plot_evd as pe
import plot_evd_predicted as pep
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

# Hvec = [6, 15, 41, 90]
Hvec = [6]

# """Plot an autocorrelation"""
# sn = 0
# iA = 1
# iB = 1
# pltcorr.pltcorr(ns_cal[0], set_id_cal[0], sn, iA, iB)

"""Plot the percentage explained variance"""
pev.variance([.5, 15, 40, 105], Hvec)

"""Plot the microstructures in PC space"""
pcA = 0
pcB = 1
pcC = 2
pltmap.pltmap(15, pcA, pcB)
pltmap3d.pltmap(15, pcA, pcB, pcC)

"""Plot a dendrogram"""
pd.pltdend(ns_val, set_id_val, names_val, 15)

"""Plot the errors versus number of PCs and polynomial order"""
pevp.plterr('mu', 60, 5, ['cal'], Hvec)
pevp.plterr('mu', 60, 5, ['LOOCV'], Hvec)
pevp.plterr('mu', 60, 5, ['val'], Hvec)
pevp.plterr('sigma', 60, 5, ['cal'], Hvec)
pevp.plterr('sigma', 60, 5, ['LOOCV'], Hvec)
pevp.plterr('sigma', 60, 5, ['val'], Hvec)

"""Plot the predicted versus actual values of the property of interest"""
plc.plot_check('modulus', n_pc=3, n_poly=2, H=15, erv=1)
plc.plot_check('strength', n_pc=6, n_poly=2, H=15, erv=5)

"""Plot the FIP EVDs versus the predicted FIP EVDs"""
indx = 10
pe.pltevd(set_id_val)
pep.pltevd(set_id_val)

plt.show()
