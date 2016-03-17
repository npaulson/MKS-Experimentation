import vtk_read as vtk
import euler_to_gsh as e2g
import correlate as corr
import plot_correlation as pltcorr
# import pca_on_correlations as pcaC
# import plot_SVE_pc as pltPC
import time


# ns_cal = [10, 10, 10]
# set_id_cal = ['random', 'transverse', 'basaltrans']
# dir_cal = ['random', 'transverse', 'basaltrans']
ns_cal = [5]
set_id_cal = ['random']
dir_cal = ['random']

L = 4
H = 15
el = 21
step = 0

wrt_file = 'log_%s.txt' % (time.strftime("%Y-%m-%d_h%Hm%M"))

"""
The tensorID determines the type of tensor data read from the .vtk file
if tensorID == 0, we read the stress tensor
if tensorID == 1, we read the strain tensor
if tensorID == 2, we read the plastic strain tensor
"""

"""Gather data from calibration vtk files"""
for ii in xrange(len(set_id_cal)):
    vtk.read_euler(el, ns_cal[ii], set_id_cal[ii],
                   step, dir_cal[ii], wrt_file, 0)

"""Compute GSH coefficients to create microstructure function in real and
fourier space"""
for ii in xrange(len(set_id_cal)):
    e2g.euler_to_gsh(el, H, ns_cal[ii], set_id_cal[ii], step,
                     wrt_file)

"""Compute the periodic autocorrelations for the microstructures"""
for ii in xrange(len(set_id_cal)):
    corr.correlate(el, ns_cal[ii], H, set_id_cal[ii], step, wrt_file)

"""Plot an autocorrelation"""
sn = 0
iA = 1
iB = 1
pltcorr.pltcorr(el, ns_cal[0], set_id_cal[0], step, sn, iA, iB)

# """Perform PCA on autocorrelations"""
# pcaC.doPCA(el, H, ns_cal, set_id_cal, step, wrt_file)

# """Plot the microstructures in PC space"""
# pcA = 0
# pcB = 1
# pltPC.pltPC(el, ns_cal, set_id_cal, step, pcA, pcB)
