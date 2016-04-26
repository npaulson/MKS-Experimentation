import plot_correlation as pltcorr
import sve_plot_pc as pltPC
import plot_effective_stiffness as pem
import plot_linkage_check as plc
import explained_variance as ev
import numpy as np
import time


ns_cal = [30, 30, 30, 30, 30, 30, 30, 30]
set_id_cal = ['actual', 'basaltrans',
              'dice', 'doubledonut',
              'innerdonut', 'outerdonut',
              'random', 'trans']
dir_cal = ['actual', 'basaltrans',
           'dice', 'doubledonut',
           'innerdonut', 'outerdonut',
           'random', 'trans']


L = 4
H = 15
el = 21
step = 1

wrt_file = 'log_%s.txt' % (time.strftime("%Y-%m-%d_h%Hm%M"))

"""Plot an autocorrelation"""
sn = 0
iA = 1
iB = 1
pltcorr.pltcorr(el, ns_cal[0], set_id_cal[0], step, sn, iA, iB)

"""Plot the percentage explained variance"""
ns_tot = np.sum(ns_cal)
ev.variance(el, ns_tot, step)

"""Plot the microstructures in PC space"""
pcA = 0
pcB = 1
pltPC.pltPC(el, ns_cal, set_id_cal, pcA, pcB)

# """Plot the effective stiffness versus a PC dimension"""
# pcA = 1
# pem.plt_stiffness(el, ns_cal, set_id_cal, step, pcA)

# """Plot the predicted versus actual values of the property of interest"""
# pcA = 1
# plc.plot_check(el, ns_val, set_id_val, 'Eeff')
