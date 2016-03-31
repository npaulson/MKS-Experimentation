import vtk_read as vtk
# import sve_gen as gen
import correlate as corr
import plot_correlation as pltcorr
import sve_plot_pc as pltPC
# import explained_variance as ev
# import numpy as np
import dim_reduce
import time
import get_M
import h5py


# ns_cal = [10]
# set_id_cal = ['bicrystal']

# ns_cal = [10, 10, 10, 10]
# set_id_cal = ['randomD3D', 'delta', 'inclusion', 'bicrystal']

# ns_D3D = [10]
# set_id_D3D = ['randomD3D']
# dir_D3D = ['randomD3D']

ns_cal = [10, 10, 10, 10]
set_id_cal = ['randomD3D', 'transverseD3D', 'basaltransD3D', 'actualD3D']
dir_cal = ['randomD3D', 'transverseD3D', 'basaltransD3D', 'actualD3D']

ns_D3D = [10, 10, 10, 10]
set_id_D3D = ['randomD3D', 'transverseD3D', 'basaltransD3D', 'actualD3D']
dir_D3D = ['randomD3D', 'transverseD3D', 'basaltransD3D', 'actualD3D']

L = 4
H = 15
el = 21
step = 6

wrt_file = 'log_%s.txt' % (time.strftime("%Y-%m-%d_h%Hm%M"))

# f = h5py.File("spatial_stats.hdf5", 'w')
# f.close()

# """
# The tensorID determines the type of tensor data read from the .vtk file
# if tensorID == 0, we read the stress tensor
# if tensorID == 1, we read the strain tensor
# if tensorID == 2, we read the plastic strain tensor
# """

# """Gather data from calibration vtk files"""
# for ii in xrange(len(set_id_D3D)):
#     vtk.read_euler(el, ns_D3D[ii], set_id_D3D[ii],
#                    step, dir_D3D[ii], wrt_file, 1)

# # gen.delta(el, ns_cal[1], set_id_cal[1], step, wrt_file)

# # vfrac = np.array([.1, .05])
# # gen.inclusion(el, ns_cal[2], set_id_cal[2], step, wrt_file, vfrac)

# # gen.bicrystal(el, ns_cal[0], set_id_cal[0], step, wrt_file)

# """Compute GSH coefficients to create microstructure function in real and
# fourier space"""
# for ii in xrange(len(set_id_cal)):
#     get_M.get_M(el, H, ns_cal[ii], set_id_cal[ii], step, wrt_file)

# """Compute the periodic statistics for the microstructures"""
# for ii in xrange(len(set_id_cal)):
#     corr.correlate(el, ns_cal[ii], H, set_id_cal[ii], step, wrt_file)

# """Perform PCA on correlations"""
# dim_reduce.reduce(el, ns_cal, H, set_id_cal, step, wrt_file)

# """Plot an autocorrelation"""
# sn = 0
# iA = 1
# iB = 1
# pltcorr.pltcorr(el, ns_cal[0], set_id_cal[0], step, sn, iA, iB)

# """Plot the percentage explained variance"""
# ns_tot = np.sum(ns_cal)
# ev.variance(el, ns_tot, step)

"""Plot the microstructures in PC space"""
pcA = 4
pcB = 2
pltPC.pltPC(el, ns_cal, set_id_cal, step, pcA, pcB)

"""
NOTES:
* sklearn.decomposition.PCA and scipy.linalg.interpolative.svd
give similar results if you subtract the means of the feature
values from the data matrix prior to SVD
* sklearn.decomposition.PCA does not work for complex values,
scipy.linalg.interpolative.svd does
"""
