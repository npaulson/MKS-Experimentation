import numpy as np
from constants import const
import h5py
import sys


def getcorrslc(set_id, iA):

    C = const()

    f = h5py.File("euler_L%s.hdf5" % C['H'], 'r')
    dset_name = 'euler_%s' % set_id
    print dset_name
    euler_raw = f.get(dset_name)[:, 0].reshape(C['el'], C['el'], C['el'])
    f.close()

    f = h5py.File("spatial_L%s.hdf5" % C['H'], 'r')
    dset_name = 'ff_%s' % set_id
    print dset_name
    corr_raw = f.get(dset_name)[...]
    corr_raw = corr_raw[iA, ...]
    f.close()

    corr_centered = np.fft.fftshift(corr_raw)

    f = h5py.File('slice.hdf5', 'w')
    f.create_dataset('euler', data=euler_raw[:, 0, :])
    slc = np.int16(np.floor(C['vmax']/2.))
    f.create_dataset('corr', data=corr_centered[:, slc, :])
    f.create_dataset('set_id', data=set_id)
    f.create_dataset('iA', data=iA)
    f.close


if __name__ == '__main__':
    set_id = sys.argv[1]
    iA = sys.argv[2]
    getcorrslc(set_id, iA)
