import numpy as np
import functions as rr
from constants import const
import os
import h5py
import time


def resp(ns, strt, name, set_id, bc, newdir):

    start = time.time()

    C = const()

    f = h5py.File("responses.hdf5", 'a')

    # nwd = os.getcwd() + '\\' + newdir
    nwd = os.getcwd() + '/' + newdir  # for unix
    os.chdir(nwd)

    fname = "%s_%s.txt" % (name, bc)
    tmp = np.loadtxt(fname)

    dset_name = "strength_%s" % set_id
    f.create_dataset(dset_name, data=tmp[strt:strt+ns, 2])
    dset_name = "modulus_%s" % set_id
    f.create_dataset(dset_name, data=tmp[strt:strt+ns, 5])

    # return to the original directory
    os.chdir('..')

    f.close()

    end = time.time()
    timeE = np.round((end - start), 3)

    msg = 'responses read from .txt file for %s_%s: %s seconds' \
          % (name, bc, timeE)
    rr.WP(msg, C['wrt_file'])


if __name__ == '__main__':
    ns = 10
    name = 'trans'
    set_id = 'trans_val'
    bc = '1'
    newdir = 'trans'

    resp(ns, name, bc, set_id, newdir)
