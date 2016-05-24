import plot_correlation as pltcorr
import plot_pc_map as pltmap
import plot_response as pr
import plot_linkage_check as plc
import explained_variance as ev
import plot_pc_vs_poly as pltpcpoly
import numpy as np
from constants import const


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

# """Plot the percentage explained variance"""
# ns_tot = np.sum(ns_cal)
# ev.variance(ns_tot)

"""Plot the microstructures in PC space"""
pcA = 0
pcB = 1
pltmap.pltmap(ns_val, set_id_val, pcA, pcB)

# """Plot the response versus a PC dimension"""
# pcA = 0
# pr.pltresponse(ns_val, set_id_val, prop, bc, pcA)

# """Plot the error in predicitons of calibration and validation data
# versus number of PCs and polynomial order"""
# pltpcpoly.pltpcpoly(prop, bc)

"""Plot the predicted versus actual values of the property of interest"""
plc.plot_check(ns_val, names_val, prop, bc)
