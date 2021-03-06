import vtk_read as vtk
import get_linkage as gl
import get_response as gr
from constants import const
import h5py

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

"""get the data for the linkage"""

# f = h5py.File("raw_responses.hdf5", 'w')
# f.close()

# """Gather data from vtk files"""
# for ii in xrange(len(set_id_cal)):
#     vtk.read_fip(strt_cal[ii], ns_cal[ii], set_id_cal[ii],
#                  dir_cal[ii])
# for ii in xrange(len(set_id_val)):
#     vtk.read_fip(strt_val[ii], ns_val[ii], set_id_val[ii],
#                  dir_val[ii])

f = h5py.File("responses.hdf5", 'w')
f.close()

"""get the fitting coefficients for the linkage"""
for ii in xrange(len(set_id_cal)):
    gr.resp(ns_cal[ii], set_id_cal[ii])
for ii in xrange(len(set_id_val)):
    gr.resp(ns_val[ii], set_id_val[ii])

"""create the specified array of linkages and cross validate"""

f = h5py.File("regression_results.hdf5", 'w')
f.close()

par = 'c0'
gl.linkage(par)

par = 'c1'
gl.linkage(par)

par = 'c2'
gl.linkage(par)

par = 'c3'
gl.linkage(par)

par = 'c4'
gl.linkage(par)


"""
NOTES:
* sklearn.decomposition.PCA and scipy.linalg.interpolative.svd
give similar results if you subtract the means of the feature
values from the data matrix prior to SVD
* sklearn.decomposition.PCA does not work for complex values,
scipy.linalg.interpolative.svd does
"""
