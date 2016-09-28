# import plot_correlation as pltcorr
import plot_explained_variance as pev
import plot_pc_map_3d as pltmap3d
import plot_pc_map as pltmap
import plot_dendrogram as pd
import plot_err_v_pc as pevp
import plot_linkage_check as plc
import plot_evd as pe
import plot_evd_predicted as pep
from constants import const
import matplotlib.pyplot as plt


C = const()

names_cal = C['names_cal_split']
sid_cal = C['sid_cal_split']
ns_cal = C['ns_cal_split']

names_val = C['names_val_split']
sid_val = C['sid_val_split']
ns_val = C['ns_cal_split']

# Hvec = [6, 15, 41, 90]
Hvec = [6]
H = 15
deg = 2

# """Plot an autocorrelation"""
# sn = 0
# iA = 1
# iB = 1
# pltcorr.pltcorr(ns_cal[0], sid_cal[0], sn, iA, iB)

"""Plot the percentage explained variance"""
pev.variance([.5, 15, 40, 105], Hvec)

"""Plot the microstructures in PC space"""
pcA = 0
pcB = 1
pcC = 2
pltmap.pltmap(H, pcA, pcB)
pltmap3d.pltmap(H, pcA, pcB, pcC)

"""Plot a dendrogram"""

pd.pltdend(ns_cal+ns_val, sid_cal+sid_val, names_cal+names_val, H)

"""Plot the errors versus number of PCs and polynomial order"""
emax = 100
pevp.plterr('mu', emax, deg, ['cal'], Hvec)
pevp.plterr('mu', emax, deg, ['LOOCV'], Hvec)
pevp.plterr('mu', emax, deg, ['val'], Hvec)
pevp.plterr('sigma', emax, deg, ['cal'], Hvec)
pevp.plterr('sigma', emax, deg, ['LOOCV'], Hvec)
pevp.plterr('sigma', emax, deg, ['val'], Hvec)

"""Plot the predicted versus actual values of the property of interest"""
indx1 = plc.plot_check('mu', n_pc=2, n_poly=3, H=H, erv=10)
indx2 = plc.plot_check('sigma', n_pc=2, n_poly=3, H=H, erv=10)

"""Plot the FIP EVDs versus the predicted FIP EVDs"""
pe.pltevd(H)
pep.pltevd(indx1, indx2, H)

plt.show()
