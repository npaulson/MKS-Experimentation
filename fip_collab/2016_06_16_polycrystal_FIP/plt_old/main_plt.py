import plot_correlation as pc
import plot_explained_variance as pev
import plot_dendrogram as pd
import plot_pc_map as pltmap
import plot_pc_vs_poly as ppp
import plot_pc_vs_poly_LOOCV as pppL
import plot_linkage_check as plc
import plot_evd as pe
from constants import const
import matplotlib.pyplot as plt


C = const()

names_cal = C['names_cal']
set_id_cal = C['set_id_cal']
strt_cal = C['strt_cal']
ns_cal = C['ns_cal']

names_val = C['names_val']
set_id_val = C['set_id_val']
strt_val = C['strt_val']
ns_val = C['ns_val']

# """Plot an autocorrelation"""
# sn = 0
# iA = 1
# iB = 1
# pc.pltcorr(ns_cal[0], set_id_cal[0], sn, iA, iB)

"""Plot the percentage explained variance"""
pev.variance()

"""Plot the microstructures in PC space"""
pcA = 0
pcB = 1
pltmap.pltmap(ns_val, set_id_val, pcA, pcB)

"""Plot a dendrogram"""
pd.pltdend(ns_val, set_id_val, names_val)

"""Plot the error in predicitons of calibration and validation data
versus number of PCs and polynomial order"""
ppp.pltpcpoly('mu', 5)
ppp.pltpcpoly('sigma', 6)

"""Plot the LOOCV error in calibration data
versus number of PCs and polynomial order"""
pppL.pltpcpoly('mu', 7)
pppL.pltpcpoly('sigma', 8)

"""Plot the predicted versus actual values of the property of interest"""
n_poly = 2
indx = plc.plot_check(ns_val, names_val, 'mu', n_poly, 9)
indx = plc.plot_check(ns_val, names_val, 'sigma', n_poly, 10)

"""Plot the FIP EVDs versus the predicted FIP EVDs"""
pe.pltevd(set_id_val, indx, 11)

plt.show()
