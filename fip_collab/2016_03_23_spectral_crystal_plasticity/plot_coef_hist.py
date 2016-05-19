# -*- coding: utf-8 -*-
import h5py
import numpy as np
import matplotlib.pyplot as plt
from gsh_cub_tri_L0_40 import gsh_basis_info


if __name__ == '__main__':

    lvl0 = 10
    lvl1 = 24
    lvl2 = 28

    tmp = gsh_basis_info()[:, 0]

    n_p = np.sum(tmp <= lvl2)
    n_tot = n_p*60

    lvec = np.zeros((n_tot,))

    for ii in xrange(n_p):
        lvec[ii*60:(ii+1)*60] = tmp[ii]

    print "lvec: %s" % str(lvec)

    set0 = lvec <= lvl0
    print "set0.sum(): %s" % set0.sum()
    set1 = (lvec > lvl0)*(lvec <= lvl1)
    print "set1.sum(): %s" % set1.sum()
    set2 = (lvec > lvl1)*(lvec <= lvl2)
    print "set2.sum(): %s" % set2.sum()

    tmp = set0.sum() + set1.sum() + set2.sum()
    print "set0.sum()+set1.sum()+set2.sum(): %s" % tmp

    tmp = np.sum(lvec <= lvl2)
    print "# indices <= than max l: %s" % tmp

    f = h5py.File('coef_40.hdf5', 'r')
    coef = f.get('coef')[:n_tot, 0]
    f.close()

    coef_mag = np.abs(coef)
    # coef_mag = np.log(np.abs(coef))

    indxv = np.arange(n_p*60)

    arg = np.argsort(coef_mag)[::-1]

    set0_s = set0[arg]
    set1_s = set1[arg]
    set2_s = set2[arg]

    coef_mag_s = coef_mag[arg]

    coef_0 = coef_mag_s[set0_s]
    coef_1 = coef_mag_s[set1_s]
    coef_2 = coef_mag_s[set2_s]

    indxv_0 = indxv[set0_s]
    indxv_1 = indxv[set1_s]
    indxv_2 = indxv[set2_s]

    bar_width = 1.00
    opacity = 0.7

    n_plt = 5000

    plt.bar(indxv_0[:n_plt], coef_0[:n_plt], bar_width,
            alpha=opacity,
            color='g',
            linewidth=0,
            log=True,
            label='0 < l <= %s' % lvl0)

    plt.bar(indxv_1[:n_plt], coef_1[:n_plt], bar_width,
            alpha=opacity,
            color='y',
            linewidth=0,
            log=True,
            label='%s < l <= %s' % (lvl0, lvl1))

    plt.bar(indxv_2[:n_plt], coef_2[:n_plt], bar_width,
            alpha=opacity,
            color='r',
            linewidth=0,
            log=True,
            label='%s < l <= %s' % (lvl1, lvl2))

    plt.legend()

    plt.xlabel("sorted coefficients")
    plt.ylabel("|coefficient|")

    plt.show()
