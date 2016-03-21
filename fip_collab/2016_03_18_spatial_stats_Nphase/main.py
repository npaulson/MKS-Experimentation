import sve_gen as gen
import get_M as gm
import correlate as corr
import plot_correlation as pltcorr
import pca_on_correlations as pcaC
import sve_plot_pc as pltPC
import numpy as np
import time


ns_cal = [10, 40, 40]
set_id_cal = ['incl1', 'bicrystal_orthog', 'bicrystal']

# ns_cal = [30, 30, 30]
# set_id_cal = ['xrod', 'yrod', 'zrod']

# ns_cal = [30, 30, 30]
# set_id_cal = ['incl1', 'incl2', 'incl3']

el = 21
H = 4
step = 0

wrt_file = 'log_%s.txt' % (time.strftime("%Y-%m-%d_h%Hm%M"))

"""
The tensorID determines the type of tensor data read from the .vtk file
if tensorID == 0, we read the stress tensor
if tensorID == 1, we read the strain tensor
if tensorID == 2, we read the plastic strain tensor
"""

"""Generate microstructures"""

# gen.delta(el, ns_cal[0], H, set_id_cal[0], step, wrt_file)

vfrac = [.075, .125]
gen.inclusion_red(el, ns_cal[0], H, set_id_cal[0], step, wrt_file, vfrac)
# vfrac = [.100, .100]
# gen.inclusion_red(el, ns_cal[1], H, set_id_cal[1], step, wrt_file, vfrac)
# vfrac = [.125, .075]
# gen.inclusion_red(el, ns_cal[2], H, set_id_cal[2], step, wrt_file, vfrac)

gen.bicrystal_orthog(el, ns_cal[1], H, set_id_cal[1], step, wrt_file)
gen.bicrystal(el, ns_cal[2], H, set_id_cal[2], step, wrt_file)

# raxis = 0
# gen.rod(el, ns_cal[0], H, set_id_cal[0], step, wrt_file, raxis)
# raxis = 1
# gen.rod(el, ns_cal[1], H, set_id_cal[1], step, wrt_file, raxis)
# raxis = 2
# gen.rod(el, ns_cal[2], H, set_id_cal[2], step, wrt_file, raxis)

"""Generate the fourier space microstructure functions"""

for ii in xrange(len(set_id_cal)):
    gm.get_M(el, ns_cal[ii], H, set_id_cal[ii], step, wrt_file)

"""Compute the periodic statistics for the microstructures"""
for ii in xrange(len(set_id_cal)):
    corr.correlate(el, ns_cal[ii], H, set_id_cal[ii], step, wrt_file)

"""Plot an autocorrelation"""
sn = 0
iA = 0
iB = 0
pltcorr.pltcorr(el, ns_cal[2], set_id_cal[2], step, sn, iA, iB)

"""Perform PCA on autocorrelations"""
pcaC.doPCA(el, ns_cal, H, set_id_cal, step, wrt_file)

"""Plot the microstructures in PC space"""
pcA = 0
pcB = 1
pltPC.pltPC(el, ns_cal, set_id_cal, step, pcA, pcB)
