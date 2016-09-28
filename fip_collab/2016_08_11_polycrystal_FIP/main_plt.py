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

names_cal = C['names_cal']
set_id_cal = C['set_id_cal']
ns_cal = C['ns_cal']

names_val = C['names_val']
set_id_val = C['set_id_val']
ns_val = C['ns_val']

# Hvec = [6, 15, 41, 90]
Hvec = [6, 15]
H = 15

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
pltmap.pltmap(H, pcA, pcB)
pltmap3d.pltmap(H, pcA, pcB, pcC)

"""Plot a dendrogram"""

pd.pltdend(ns_cal+ns_val, set_id_cal+set_id_val, names_cal+names_val, 6)

"""Plot the errors versus number of PCs and polynomial order"""
Emax = 100
pevp.plterr('mu', 10, Emax, ['cal'], Hvec)
pevp.plterr('mu', 10, Emax, ['LOOCV'], Hvec)
pevp.plterr('mu', 10, Emax, ['val'], Hvec)
pevp.plterr('sigma', 10, Emax, ['cal'], Hvec)
pevp.plterr('sigma', 10, Emax, ['LOOCV'], Hvec)
pevp.plterr('sigma', 10, Emax, ['val'], Hvec)

"""Plot the predicted versus actual values of the property of interest"""
indx1 = plc.plot_check('mu', n_pc=1, n_poly=2, H=H, erv=10)
indx2 = plc.plot_check('sigma', n_pc=1, n_poly=2, H=H, erv=10)

"""Plot the FIP EVDs versus the predicted FIP EVDs"""
pe.pltevd(H)
pep.pltevd(indx1, indx2, H)

plt.show()
