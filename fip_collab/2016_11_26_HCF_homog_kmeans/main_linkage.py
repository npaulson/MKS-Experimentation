import vtk_read as vtk
import get_linkage as gl
# import get_linkage_w_var as gl
import sub_sample as ss
import get_response as gr
from constants import const
import h5py

C = const()

sid = C['sid']
names = C['names']
strt = C['strt']
ns = C['ns']

# """get the data for the linkage"""

# f = h5py.File("raw_responses.hdf5", 'w')
# f.close()

# """Gather data from vtk files"""
# dir_fip = 'fip'

# for ii in xrange(len(sid)):
#     vtk.read_fip(strt[ii], ns[ii], names[ii], sid[ii],
#                  dir_fip)

f = h5py.File("responses.hdf5", 'w')
f.close()

for ii in xrange(len(sid)):
    gr.resp(ns[ii], sid[ii])


f = h5py.File("sample_L%s.hdf5" % C['H'], 'w')
f.close()

"""subsample the clusters and identify gamma distribution parameters
for the sampled areas"""
for ii in xrange(len(sid)):
    ss.sample(ns[ii], sid[ii])

"""create the specified array of linkages and cross validate"""
f = h5py.File("regression_results_L%s.hdf5" % C['H'], 'w')
f.close()

par = 'mu'
gl.linkage(par)

par = 'sigma'
gl.linkage(par)

"""
NOTES:
* sklearn.decomposition.PCA and scipy.linalg.interpolative.svd
give similar results if you subtract the means of the feature
values from the data matrix prior to SVD
* sklearn.decomposition.PCA does not work for complex values,
scipy.linalg.interpolative.svd does
"""
