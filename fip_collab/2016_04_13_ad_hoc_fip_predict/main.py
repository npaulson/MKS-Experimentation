import vtk_read as vtk
import get_neighbors as gn
import get_response as gr
import get_new_space as gns
import get_linkage as gl
import transform as tf
import time
import get_M
import h5py


ns_cal = 2
set_id_cal = 'cal'
dir_cal = 'cal'

ns_val = 2
set_id_val = 'val'
dir_val = 'val'


L = 4
H = 15
el = 21
step = 1

wrt_file = 'log_%s.txt' % (time.strftime("%Y-%m-%d_h%Hm%M"))

f = h5py.File("spatial.hdf5", 'w')
f.close()

"""
The tensorID determines the type of tensor data read from the .vtk file
if tensorID == 0, we read the stress tensor
if tensorID == 1, we read the strain tensor
if tensorID == 2, we read the plastic strain tensor
"""

"""Gather data from vtk files"""
vtk.read_euler(el, ns_cal, set_id_cal,
               step, dir_cal, wrt_file, 1)
vtk.read_euler(el, ns_val, set_id_val,
               step, dir_val, wrt_file, 1)

"""Compute GSH coefficients to create microstructure function"""
get_M.get_M(el, H, ns_cal, set_id_cal, step, wrt_file)
get_M.get_M(el, H, ns_val, set_id_val, step, wrt_file)

"""Generate the local microstructure information"""
gn.neighbors(el, ns_cal, H, set_id_cal, step, wrt_file)
gn.neighbors(el, ns_val, H, set_id_val, step, wrt_file)

"""Perform PCA on correlations"""
gns.new_space(el, ns_cal, H, set_id_cal, step, wrt_file)

"""transform statistics to reduced dimensionality space"""
tf.transform(el, ns_cal, H, set_id_cal, step, wrt_file)
tf.transform(el, ns_val, H, set_id_val, step, wrt_file)

# """get the data for the linkage"""
# f = h5py.File("responses.hdf5", 'w')
# f.close()

# f = h5py.File("linkage.hdf5", 'w')
# f.close()

# for ii in xrange(len(set_id_cal)):
#     gr.Eeff(el, ns_cal[ii], set_id_cal[ii], step, dir_cal[ii], wrt_file)
#     gr.Eeff(el, ns_val[ii], set_id_val[ii], step, dir_val[ii], wrt_file)
#     # gr.FIP(el, ns_cal[ii], set_id_cal[ii], step, dir_cal[ii], wrt_file)
#     # gr.FIP(el, ns_val[ii], set_id_val[ii], step, dir_val[ii], wrt_file)

# """create the specified array of linkages and cross validate"""

# gl.linkage(el, ns_cal, ns_val, set_id_cal, set_id_val, 'Eeff', wrt_file)

"""
NOTES:
* sklearn.decomposition.PCA and scipy.linalg.interpolative.svd
give similar results if you subtract the means of the feature
values from the data matrix prior to SVD
* sklearn.decomposition.PCA does not work for complex values,
scipy.linalg.interpolative.svd does
"""
