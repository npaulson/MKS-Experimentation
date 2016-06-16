import plot_correlation as pltcorr
import plot_explained_variance as pev
import plot_pc_map as pltmap
import plot_dendrogram as pd
import plot_pc_vs_poly_alt as pltpcpoly
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

bc = 'bc1'
prop = 'yield'

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

"""Plot a dendrogram"""
pd.pltdend(ns_val, set_id_val, names_val)

# """Plot the error in predicitons of calibration and validation data
# versus number of PCs and polynomial order"""
# pltpcpoly.pltpcpoly(prop, bc)

# """Plot the predicted versus actual values of the property of interest"""
# plc.plot_check(ns_val, names_val, prop, bc)

plt.show()
