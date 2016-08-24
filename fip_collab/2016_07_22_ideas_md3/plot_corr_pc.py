import numpy as np
import matplotlib.pyplot as plt
import h5py
from constants import const


def pltcorrpc(C, set_id, sn, iA):

    """Plot slices of the response"""
    plt.figure(figsize=[16, 6])

    f = h5py.File("spatial_L%s.hdf5" % C['H'], 'r')
    tmp = f.get('ff_%s' % set_id)[sn, iA, ...]
    f.close()

    corr = tmp

    # slc = 0
    slc = np.int16(np.floor(C['vmax']/2.))

    plt.subplot(241)
    ax = plt.imshow(np.fft.fftshift(corr[slc, :, :]), origin='lower',
                    interpolation='none', cmap='viridis')
    plt.colorbar(ax)
    plt.title('ff: %s, %s' % (C['cmat'][iA, 0], C['cmat'][iA, 1]))

    f = h5py.File("pca_data_L%s.hdf5" % C['H'], 'r')
    tmp = f.get('mean')[...]
    tmp = tmp.reshape((C['cmax'], C['el'], C['el'], C['el']))
    mean = tmp[iA, ...]

    plt.subplot(245)
    ax = plt.imshow(np.fft.fftshift(mean[slc, :, :]), origin='lower',
                    interpolation='none', cmap='viridis')
    plt.colorbar(ax)
    plt.title('PCA mean')

    tmp = f.get('components')[...]
    tmp = tmp.reshape((C['n_pc_tot'], C['cmax'], C['el'], C['el'], C['el']))
    tmp = tmp[:, iA, ...]

    pc1 = tmp[0, ...]
    pc2 = tmp[1, ...]
    pc3 = tmp[2, ...]

    # pc4 = tmp[3, ...]
    # pc5 = tmp[4, ...]
    # pc6 = tmp[5, ...]
    # pc7 = tmp[6, ...]
    # pc8 = tmp[7, ...]
    # pc9 = tmp[8, ...]
    # pc10 = tmp[9, ...]

    plt.subplot(246)
    ax = plt.imshow(np.fft.fftshift(pc1[slc, :, :]), origin='lower',
                    interpolation='none', cmap='viridis')
    plt.colorbar(ax)
    plt.title('PC 1')

    plt.subplot(247)
    ax = plt.imshow(np.fft.fftshift(pc2[slc, :, :]), origin='lower',
                    interpolation='none', cmap='viridis')
    plt.colorbar(ax)
    plt.title('PC 2')

    plt.subplot(248)
    ax = plt.imshow(np.fft.fftshift(pc3[slc, :, :]), origin='lower',
                    interpolation='none', cmap='viridis')
    plt.colorbar(ax)
    plt.title('PC 3')

    f.close()

    f = h5py.File("spatial_reduced_L%s.hdf5" % C['H'], 'r')
    ff_coef = f.get('reduced_%s' % set_id)[...]
    f.close()

    print ff_coef[sn, :]

    # corr_1pc = mean + ff_coef[sn, 0]*pc1

    # plt.subplot(242)
    # ax = plt.imshow(corr_1pc[slc, :, :], origin='lower',
    #                 interpolation='none', cmap='viridis')
    # plt.colorbar(ax)
    # plt.title('ff with 1 PC')

    # corr_2pc = corr_1pc + ff_coef[sn, 1]*pc2

    # plt.subplot(243)
    # ax = plt.imshow(corr_2pc[slc, :, :], origin='lower',
    #                 interpolation='none', cmap='viridis')
    # plt.colorbar(ax)
    # plt.title('ff with 2 PCs')

    corr_10pc = mean
    for ii in xrange(C['n_pc_tot']):
        corr_10pc += ff_coef[sn, ii]*tmp[ii, ...]

    plt.subplot(244)
    ax = plt.imshow(np.fft.fftshift(corr_10pc[slc, :, :]), origin='lower',
                    interpolation='none', cmap='viridis')
    plt.colorbar(ax)
    plt.title('ff with 10 PCs')


if __name__ == '__main__':
    C = const()
    set_id = 'Ra_cal'
    sn = 0
    iA = 6

    pltcorrpc(C, set_id, sn, iA)
    plt.show()
