import get_euler as ge
import correlate as corr
import get_new_space as gns
import transform as tf
from constants import const
import get_M
import h5py

C = const()

set_id = C['set_id']
names = C['names']
dir_micr = C['dir_micr']

# f = h5py.File("spatial_L%s.hdf5" % C['H'], 'w')
# f.close()

# """Gather euler angles and phase ids from txt files"""
# for sid in set_id:
#     ge.read_euler(sid, dir_micr)

# """Compute GSH coefficients to create microstructure function in real and
# fourier space"""
# for sid in set_id:
#     get_M.get_M(sid)

# """Compute the periodic statistics for the microstructures"""
# for sid in set_id:
#     corr.correlate(sid)

"""Perform PCA on correlations"""
pca = gns.new_space(set_id)

"""transform statistics to reduced dimensionality space"""
f = h5py.File("spatial_reduced_L%s.hdf5" % C['H'], 'w')
f.close()

for sid in set_id:
    tf.transform(sid, pca)
