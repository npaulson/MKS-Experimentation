# -*- coding: utf-8 -*-
import numpy as np
import gsh_hex_tri_L0_16 as gsh
import h5py


def get_M(C, ns, set_id):

    """get the euler angle files"""
    f = h5py.File("euler.hdf5", 'a')
    euler = f.get('euler_%s' % set_id)[...]
    f.close()

    mf = np.zeros([ns, C['H'], C['el']**3], dtype='float64')

    indxvec = gsh.gsh_basis_info()

    c = 0
    for h in xrange(C['H']):
        tmp = gsh.gsh_eval(euler.swapaxes(1, 2), [h])
        tmp = np.squeeze(tmp)

        if indxvec[h, 1] < 0:
            mf[:, c, :] = tmp.imag/(2.*indxvec[h, 0]+1.)
        else:
            mf[:, c, :] = tmp.real/(2.*indxvec[h, 0]+1.)
        c += 1

    mf = mf.reshape([ns, C['H'], C['el'], C['el'], C['el']])

    # MICROSTRUCTURE FUNCTIONS IN FREQUENCY SPACE

    M = np.fft.fftn(mf, axes=[2, 3, 4])
    del mf

    f = h5py.File("spatial_L%s.hdf5" % C['H'], 'a')
    f.create_dataset('M_%s' % set_id, data=M)
    f.close()
