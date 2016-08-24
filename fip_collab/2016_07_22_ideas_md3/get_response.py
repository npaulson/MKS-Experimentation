import numpy as np
from constants import const
import os
import h5py


def resp(C, ns, strt, name, set_id, bc, newdir):

    f = h5py.File("responses_all.hdf5", 'a')

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


if __name__ == '__main__':
    C = const()
    ns = 10
    name = 'trans'
    set_id = 'trans_val'
    bc = '1'
    newdir = 'trans'

    resp(C, ns, name, bc, set_id, newdir)
