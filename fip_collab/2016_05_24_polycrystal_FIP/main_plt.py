import plot_correlation as pltcorr
import plot_pc_map as pltmap
import plot_linkage_check as plc
import plot_explained_variance as pev
import plot_pc_vs_poly as pltpcpoly
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

par = 'c2'

# """Plot an autocorrelation"""
# sn = 0
# iA = 1
# iB = 1
# pltcorr.pltcorr(ns_cal[0], set_id_cal[0], sn, iA, iB)

"""Plot the percentage explained variance"""
pev.variance()

"""Plot the microstructures in PC space"""
pcA = 0
pcB = 1
pltmap.pltmap(ns_val, set_id_val, pcA, pcB)

"""Plot the error in predicitons of calibration and validation data
versus number of PCs and polynomial order"""
pltpcpoly.pltpcpoly(par)

"""Plot the predicted versus actual values of the property of interest"""
plc.plot_check(ns_val, names_val, par)

"""Plot the FIP EVDs versus the predicted FIP EVDs"""
pe.pltevd(set_id_val)

plt.show()
