import sve_gen as gen
import correlate as corr
import plot_correlation as pltcorr
import pca_on_correlations as pcaC
import sve_plot_pc as pltPC
import numpy as np
import time


ns_cal = [10, 2, 50, 200]
set_id_cal = ['random', 'delta', 'inclusion', 'bicrystal']

el = 21
step = 0

wrt_file = 'log_%s.txt' % (time.strftime("%Y-%m-%d_h%Hm%M"))

"""
The tensorID determines the type of tensor data read from the .vtk file
if tensorID == 0, we read the stress tensor
if tensorID == 1, we read the strain tensor
if tensorID == 2, we read the plastic strain tensor
"""

"""Generate microstructures"""

gen.rand(el, ns_cal[0], set_id_cal[0], step, wrt_file)

gen.delta(el, ns_cal[1], set_id_cal[1], step, wrt_file)

gen.inclusion(el, ns_cal[2], set_id_cal[2], step, wrt_file)

gen.bicrystal(el, ns_cal[3], set_id_cal[3], step, wrt_file)

"""Compute the periodic statistics for the microstructures"""
for ii in xrange(len(set_id_cal)):
    corr.correlate(el, ns_cal[ii], set_id_cal[ii], step, wrt_file)

"""Plot an autocorrelation"""
sn = 0
pltcorr.pltcorr(el, ns_cal[2], set_id_cal[2], step, sn)

"""Perform PCA on autocorrelations"""
pcaC.doPCA(el, ns_cal, set_id_cal, step, wrt_file)

"""Plot the microstructures in PC space"""
pcA = 0
pcB = 1
pltPC.pltPC(el, ns_cal, set_id_cal, step, pcA, pcB)
