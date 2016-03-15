import numpy as np
import db_functions as fn
import constants
import h5py


C = constants.const()

filename = 'log_Xcalc_combine.txt'

f_master = h5py.File("X_parts.hdf5", 'w')

"""load the cosine basis evaluations"""
f_cos = h5py.File("X_parts_cos.hdf5", 'r')

for name in f_cos.keys():
    fn.WP(name, filename)
    tmp = f_cos.get(name)[...]
    f_master.create_dataset(name, data=tmp)
    del tmp

f_cos.close()

"""load the GSH basis evaluations"""

for jobnum in xrange(C['n_jobs_Xcalc']):

    f_gsh = h5py.File("X_parts_GSH_%s.hdf5" % jobnum, 'r')

    for name in f_gsh.keys():
        fn.WP(name, filename)
        tmp = f_gsh.get(name)[...]
        f_master.create_dataset(name, data=tmp)
        del tmp

    f_gsh.close()

f_master.close()
