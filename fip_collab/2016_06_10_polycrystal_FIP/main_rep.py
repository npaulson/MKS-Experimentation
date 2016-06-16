import vtk_read as vtk
import correlate as corr
import get_new_space as gns
import transform as tf
from constants import const
import get_M
import h5py

C = const()

names_cal = C['names_cal']
set_id_cal = C['set_id_cal']
strt_cal = C['strt_cal']
ns_cal = C['ns_cal']

names_val = C['names_val']
set_id_val = C['set_id_val']
strt_val = C['strt_val']
ns_val = C['ns_val']

f = h5py.File("spatial.hdf5", 'w')
f.close()

"""Gather data from vtk files"""

dir_euler = "euler"
for ii in xrange(len(set_id_cal)):
    vtk.read_euler(strt_cal[ii], ns_cal[ii], names_cal[ii], set_id_cal[ii],
                   dir_euler, 0)
for ii in xrange(len(set_id_val)):
    vtk.read_euler(strt_val[ii], ns_val[ii], names_val[ii], set_id_val[ii],
                   dir_euler, 0)

"""Compute GSH coefficients to create microstructure function in real and
fourier space"""

for ii in xrange(len(set_id_cal)):
    get_M.get_M(ns_cal[ii], set_id_cal[ii])
for ii in xrange(len(set_id_val)):
    get_M.get_M(ns_val[ii], set_id_val[ii])

"""Compute the periodic statistics for the microstructures"""
for ii in xrange(len(set_id_cal)):
    corr.correlate(ns_cal[ii], set_id_cal[ii])
for ii in xrange(len(set_id_val)):
    corr.correlate(ns_val[ii], set_id_val[ii])

"""Perform PCA on correlations"""
pca = gns.new_space(ns_cal, set_id_cal)

"""transform statistics to reduced dimensionality space"""
f = h5py.File("spatial_reduced.hdf5", 'w')
f.close()

for ii in xrange(len(set_id_cal)):
    tf.transform(ns_cal[ii], set_id_cal[ii], pca)
for ii in xrange(len(set_id_val)):
    tf.transform(ns_val[ii], set_id_val[ii], pca)
