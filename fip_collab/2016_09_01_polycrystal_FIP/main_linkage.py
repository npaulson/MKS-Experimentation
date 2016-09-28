import vtk_read as vtk
import get_linkage as gl
import get_response as gr
from constants import const
import h5py

C = const()

sid = C['sid']
names = C['names']
sid_split = C['sid_split']
strt = C['strt']
ns = C['ns']
ns_split = C['ns_split']

"""get the data for the linkage"""

f = h5py.File("raw_responses.hdf5", 'w')
f.close()

"""Gather data from vtk files"""
dir_fip = 'fip'

for ii in xrange(len(sid)):
    vtk.read_fip(strt[ii], ns[ii], names[ii], sid[ii],
                 dir_fip)

f = h5py.File("responses.hdf5", 'w')
f.close()

"""get the fitting coefficients for the linkage"""
for ii in xrange(len(sid_split)):
    gr.resp(ns_split[ii], sid_split[ii])

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
