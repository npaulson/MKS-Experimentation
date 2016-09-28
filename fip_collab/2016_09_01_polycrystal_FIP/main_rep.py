import vtk_read as vtk
import correlate as corr
import get_new_space as gns
import transform as tf
from constants import const
import get_M
import h5py

C = const()

sid = C['sid']
names = C['names']
strt = C['strt']
ns = C['ns']

# f = h5py.File("euler.hdf5", 'w')
# f.close()

# """Gather data from vtk files"""
# for ii in xrange(len(sid)):
#     vtk.read_euler(strt[ii], ns[ii], names[ii], sid[ii],
#                    'euler', 0)

f = h5py.File("spatial_L%s.hdf5" % C['H'], 'w')
f.close()

"""Compute GSH coefficients to create microstructure function in real and
fourier space"""

for ii in xrange(len(sid)):
    get_M.get_M(ns[ii], sid[ii])

"""Compute the periodic statistics for the microstructures"""
for ii in xrange(len(sid)):
    corr.correlate(ns[ii], sid[ii])

"""Perform PCA on correlations"""
pca = gns.new_space(ns, sid)

"""transform statistics to reduced dimensionality space"""
f = h5py.File("spatial_reduced_L%s.hdf5" % C['H'], 'w')
f.close()

for ii in xrange(len(sid)):
    tf.transform(ns[ii], sid[ii], pca)
