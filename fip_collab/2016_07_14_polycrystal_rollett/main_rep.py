import alljobs_functions as af
import collect_euler as ce
import collect_spatial as cs
import get_new_space as gns
import transform as tf
from constants import const
import h5py

C = const()

set_id = C['set_id']
dir_micr = C['dir_micr']
logfile = "eulerlog.txt"

# """load the equi and rollx microstructures"""

# af.job_submit(njobs=C['read_njobs'],
#               mem=C['read_mem'],
#               walltime=C['read_walltime'],
#               scriptname=C['read_scriptname'])

# af.job_check(njobs=C['read_njobs'],
#              walltime=C['read_walltime'],
#              scriptname=C['read_scriptname'],
#              logfile=logfile)

# """Rotate the rolled microstructures 90 degrees
# CCW in the X-Z plane, creating rollz microstructures"""

# af.job_submit(njobs=C['rotate_njobs'],
#               mem=C['rotate_mem'],
#               walltime=C['rotate_walltime'],
#               scriptname=C['rotate_scriptname'])

# af.job_check(njobs=C['rotate_njobs'],
#              walltime=C['rotate_walltime'],
#              scriptname=C['rotate_scriptname'],
#              logfile=logfile)

# """load all microstructures into same file"""

# f = h5py.File("euler_L%s.hdf5" % C['H'], 'w')
# f.close()

# ce.collect()

"""Compute GSH coefficients to create microstructure function in real and
fourier space, Compute the periodic statistics for the microstructures"""

af.job_submit(njobs=C['corr_njobs'],
              mem=C['corr_mem'],
              walltime=C['corr_walltime'],
              scriptname=C['corr_scriptname'])

af.job_check(njobs=C['corr_njobs'],
             walltime=C['corr_walltime'],
             scriptname=C['corr_scriptname'],
             logfile=logfile)

# """load all correlations onto the same file"""

# f = h5py.File("spatial_L%s.hdf5" % C['H'], 'w')
# f.close()

# cs.collect()

# """Perform PCA on correlations"""

# pca = gns.new_space(set_id)

# """transform statistics to reduced dimensionality space"""

# f = h5py.File("spatial_reduced_L%s.hdf5" % C['H'], 'w')
# f.close()

# for sid in set_id:
#     tf.transform(sid, pca)
