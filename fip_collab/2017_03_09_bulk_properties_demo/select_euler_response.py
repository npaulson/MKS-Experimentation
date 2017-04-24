import numpy as np
from constants import const
import h5py


def select(C, ns, strt, name, set_id, bc):

    """select the euler angle set"""

    f = h5py.File("data.hdf5", 'a')
    f_e = h5py.File("euler.hdf5", 'a')

    dset_name = "euler_%s" % name
    tmp = f.get(dset_name)[strt:strt+ns, ...]
    dset_name = "euler_%s" % set_id
    f_e.create_dataset(dset_name, data=tmp)

    f_e.close()

    """select the response set"""
    f_r = h5py.File("responses.hdf5", 'a')

    dset_name = "modulus_%s_%s" % (name, bc)
    tmp = f.get(dset_name)[strt:strt+ns]
    dset_name = "modulus_%s" % set_id
    f_r.create_dataset(dset_name, data=tmp)

    dset_name = "strength_%s_%s" % (name, bc)
    tmp = f.get(dset_name)[strt:strt+ns]
    dset_name = "strength_%s" % set_id
    f_r.create_dataset(dset_name, data=tmp)

    f_r.close()
    f.close()

if __name__ == '__main__':
    C = const()
    ns = 10
    name = 'trans'
    set_id = 'trans_val'
    bc = '1'
    newdir = 'trans'

    select(C, ns, name, bc, set_id, newdir)
