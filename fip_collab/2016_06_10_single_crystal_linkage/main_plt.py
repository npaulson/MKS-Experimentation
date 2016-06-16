# import plot_correlation as pltcorr
import plot_pc_map as pltmap
import plot_linkage_check as plc
import plot_explained_variance as pev
import plot_pc_vs_poly as pltpcpoly
import numpy as np
from constants import const
import matplotlib.pyplot as plt


C = const()

names_cal = C['names_cal']
set_id_cal = C['set_id_cal']
# strt_cal = C['strt_cal']
ns_cal = C['ns_cal']
dir_cal = C['dir_cal']

names_val = C['names_val']
set_id_val = C['set_id_val']
# strt_val = C['strt_val']
ns_val = C['ns_val']
dir_val = C['dir_val']


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
pltmap.pltmap(ns_cal, set_id_cal, pcA, pcB)

"""plot the error metrics"""
pltpcpoly.pltpcpoly("modulus", 4)
pltpcpoly.pltpcpoly("strength", 5)

"""Plot the predicted versus actual values of the property of interest"""
n_poly = 2
plc.plot_check(ns_val, names_val, "modulus", n_poly, 6)
n_poly = 2
plc.plot_check(ns_val, names_val, "strength", n_poly, 7)

plt.show()
