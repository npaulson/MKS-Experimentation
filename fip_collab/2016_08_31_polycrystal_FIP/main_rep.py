import vtk_read as vtk
import correlate as corr
import get_new_space as gns
import transform as tf
from constants import const
import get_M
import h5py

C = const()

sid_cal = C['sid_cal']
names_cal = C['names_cal']
names_cal_alt = C['names_cal_alt']
sid_cal = C['sid_cal']
strt_cal = C['strt_cal']
ns_cal = C['ns_cal']

sid_val = C['sid_val']
names_val = C['names_val']
names_val_alt = C['names_val_alt']
sid_val = C['sid_val']
strt_val = C['strt_val']
ns_val = C['ns_val']

# f = h5py.File("euler.hdf5", 'w')
# f.close()

# """Gather data from vtk files"""
# for ii in xrange(len(sid_cal)):
#     vtk.read_euler(strt_cal[ii], ns_cal[ii], names_cal_alt[ii], sid_cal[ii],
#                    'euler', 0)
# for ii in xrange(len(sid_val)):
#     vtk.read_euler(strt_val[ii], ns_val[ii], names_val_alt[ii], sid_val[ii],
#                    'euler', 0)

f = h5py.File("spatial_L%s.hdf5" % C['H'], 'w')
f.close()

"""Compute GSH coefficients to create microstructure function in real and
fourier space"""

for ii in xrange(len(sid_cal)):
    get_M.get_M(ns_cal[ii], sid_cal[ii])
for ii in xrange(len(sid_val)):
    get_M.get_M(ns_val[ii], sid_val[ii])

"""Compute the periodic statistics for the microstructures"""
for ii in xrange(len(sid_cal)):
    corr.correlate(ns_cal[ii], sid_cal[ii])
for ii in xrange(len(sid_val)):
    corr.correlate(ns_val[ii], sid_val[ii])

"""Perform PCA on correlations"""
pca = gns.new_space(ns_cal, sid_cal)

"""transform statistics to reduced dimensionality space"""
f = h5py.File("spatial_reduced_L%s.hdf5" % C['H'], 'w')
f.close()

for ii in xrange(len(sid_cal)):
    tf.transform(ns_cal[ii], sid_cal[ii], pca)
for ii in xrange(len(sid_val)):
    tf.transform(ns_val[ii], sid_val[ii], pca)
