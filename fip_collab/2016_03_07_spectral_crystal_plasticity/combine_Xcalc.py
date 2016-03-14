import h5py
import numpy as np


"""initialize important variables"""
n_jobs = 40  # number of jobs submitted

f_master = h5py.File("X_parts.hdf5", 'w')

"""load the cosine basis evaluations"""
f_cos = h5py.File("X_parts_cos.hdf5", 'r')

for name in f_cos.keys():
    tmp = f_cos.get(name)[...]
    f_master.create_dataset(name, data=tmp)
    del tmp

f_cos.close()

"""load the GSH basis evaluations"""

for jobnum in xrange(n_jobs):

    f_gsh = h5py.File("X_parts_GSH_%s.hdf5" % jobnum, 'r')

    for name in f_gsh.keys():
        tmp = f_gsh.get(name)[...]
        f_master.create_dataset(name, data=tmp)
        del tmp

    f_gsh.close()

f_master.close()
