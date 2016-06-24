import get_linkage as gl
import get_poly_response as gpr
import get_single_response as gsr
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

f = h5py.File("responses.hdf5", 'w')
f.close()

bc = 'bc1'

for ii in xrange(len(set_id_cal)-1):
    gpr.resp(ns_cal[ii], strt_cal[ii], names_cal[ii],
             set_id_cal[ii], bc, C['dir_resp'])
for ii in xrange(len(set_id_val)-1):
    gpr.resp(ns_val[ii], strt_val[ii], names_val[ii],
             set_id_val[ii], bc, C['dir_resp'])

gsr.read(strt_cal[-1], ns_cal[-1], set_id_cal[-1])
gsr.read(strt_val[-1], ns_val[-1], set_id_val[-1])

"""create the specified array of linkages and cross validate"""

f = h5py.File("regression_results_L%s.hdf5" % C['H'], 'w')
f.close()

gl.linkage('modulus')
gl.linkage('strength')

"""
NOTES:
* sklearn.decomposition.PCA and scipy.linalg.interpolative.svd
give similar results if you subtract the means of the feature
values from the data matrix prior to SVD
* sklearn.decomposition.PCA does not work for complex values,
scipy.linalg.interpolative.svd does
"""
