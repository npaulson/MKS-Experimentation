import vtk_read as vtk
import correlate as corr
import get_response as gr
import get_new_space as gns
import get_linkage as gl
import transform as tf
import time
import get_M
import h5py


ns_cal = [20, 20, 20, 20]
set_id_cal = ['randomD3D_cal', 'transverseD3D_cal',
              'basaltransD3D_cal', 'actualD3D_cal']
dir_cal = ['randomD3D_cal', 'transverseD3D_cal',
           'basaltransD3D_cal', 'actualD3D_cal']

ns_val = [10, 10, 10, 10]
set_id_val = ['randomD3D_val', 'transverseD3D_val',
              'basaltransD3D_val', 'actualD3D_val']
dir_val = ['randomD3D_val', 'transverseD3D_val',
           'basaltransD3D_val', 'actualD3D_val']

# ns_cal = [60]
# set_id_cal = ['randomD3D_cal']
# dir_cal = ['randomD3D_cal']

# ns_val = [40]
# set_id_val = ['randomD3D_val']
# dir_val = ['randomD3D_val']


H = 4
el = 21
step = 1
n_pc_tot = 20

wrt_file = 'log_%s.txt' % (time.strftime("%Y-%m-%d_h%Hm%M"))

f = h5py.File("spatial_stats.hdf5", 'w')
f.close()

"""
The tensorID determines the type of tensor data read from the .vtk file
if tensorID == 0, we read the stress tensor
if tensorID == 1, we read the strain tensor
if tensorID == 2, we read the plastic strain tensor
"""

"""Gather data from vtk files"""
for ii in xrange(len(set_id_cal)):
    vtk.read_euler(el, ns_cal[ii], set_id_cal[ii],
                   step, dir_cal[ii], wrt_file, 1)
    vtk.read_euler(el, ns_val[ii], set_id_val[ii],
                   step, dir_val[ii], wrt_file, 1)

"""get the data for the linkage"""

f = h5py.File("responses.hdf5", 'w')
f.close()
f = h5py.File("responses_for_linkage.hdf5", 'w')
f.close()

for ii in xrange(len(set_id_cal)):
    # gr.Eeff(el, ns_cal[ii], set_id_cal[ii], step, dir_cal[ii], wrt_file)
    # gr.Eeff(el, ns_val[ii], set_id_val[ii], step, dir_val[ii], wrt_file)
    gr.FIP(el, ns_cal[ii], set_id_cal[ii], step, dir_cal[ii], wrt_file)
    gr.FIP(el, ns_val[ii], set_id_val[ii], step, dir_val[ii], wrt_file)

"""Compute GSH coefficients to create microstructure function in real and
fourier space"""

for ii in xrange(len(set_id_cal)):
    get_M.get_M(el, H, ns_cal[ii], set_id_cal[ii], step, wrt_file)
    get_M.get_M(el, H, ns_val[ii], set_id_val[ii], step, wrt_file)

"""Compute the periodic statistics for the microstructures"""
for ii in xrange(len(set_id_cal)):
    corr.correlate(el, ns_cal[ii], H, set_id_cal[ii], step, wrt_file)
    corr.correlate(el, ns_val[ii], H, set_id_val[ii], step, wrt_file)

"""Perform PCA on correlations"""
pca = gns.new_space(el, ns_cal, H, set_id_cal, step, n_pc_tot, wrt_file)

"""transform statistics to reduced dimensionality space"""
f = h5py.File("sve_reduced.hdf5", 'w')
f.close()

for ii in xrange(len(set_id_cal)):
    tf.transform(el, ns_cal[ii], H, set_id_cal[ii], step, pca, wrt_file)
    tf.transform(el, ns_val[ii], H, set_id_val[ii], step, pca, wrt_file)

"""create the specified array of linkages and cross validate"""

gl.linkage(el, ns_cal, ns_val, set_id_cal,
           set_id_val, 'fip', n_pc_tot, wrt_file)

"""
NOTES:
* sklearn.decomposition.PCA and scipy.linalg.interpolative.svd
give similar results if you subtract the means of the feature
values from the data matrix prior to SVD
* sklearn.decomposition.PCA does not work for complex values,
scipy.linalg.interpolative.svd does
"""
