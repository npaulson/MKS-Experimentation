# -*- coding: utf-8 -*-
"""
Created by Noah Paulson 3/22/2015
"""

import numpy as np
import matplotlib.pyplot as plt


def make_hist(el, ns_list, set_id_list, step, comp, typ):
    # the following block is for reading strains.
    # The format is:
    # [# samples, # elements side 1, # elements side 2, # elements side 3]
    resp1 = np.load('%s%s_%s%s_s%s.npy' % (typ, comp, ns_list[0],
                                           set_id_list[0], step))
    resp2 = np.load('%s%s_%s%s_s%s.npy' % (typ, comp, ns_list[1],
                                           set_id_list[1], step))
    resp3 = np.load('%s%s_%s%s_s%s.npy' % (typ, comp, ns_list[2],
                                           set_id_list[2], step))
    resp4 = np.load('%s%s_%s%s_s%s.npy' % (typ, comp, ns_list[3],
                                           set_id_list[3], step))

    # Plot a histogram representing the frequency of strain levels with
    # separate channels for each phase of each type of response.
    plt.figure(num=1, figsize=[12, 5])

    # find the min and max of both datasets (in full)
    dmin = np.amin([np.amin(resp1),
                    np.amin(resp2),
                    np.amin(resp3),
                    np.amin(resp4)])
    dmax = np.amax([np.amax(resp1),
                    np.amax(resp2),
                    np.amax(resp3),
                    np.amax(resp4)])

    resp1L = np.reshape(resp1, ns_list[0]*(el**3))
    resp2L = np.reshape(resp2, ns_list[1]*(el**3))
    resp3L = np.reshape(resp3, ns_list[2]*(el**3))
    resp4L = np.reshape(resp4, ns_list[3]*(el**3))

    # select the desired number of bins in the histogram
    bn = 200
    weight = np.ones_like(resp1L)/(el**3)
    n, bins, patches = plt.hist(resp1L,
                                bins=bn,
                                histtype='step',
                                hold=True,
                                range=(dmin, dmax),
                                weights=weight,
                                color='white')
    bincenters = 0.5*(bins[1:]+bins[:-1])
    resp1L, = plt.plot(bincenters, n, 'k', linestyle='-', lw=0.75)

    weight = np.ones_like(resp2L)/(el**3)
    n, bins, patches = plt.hist(resp2L,
                                bins=bn,
                                histtype='step',
                                hold=True,
                                range=(dmin, dmax),
                                weights=weight,
                                color='white')
    resp2L, = plt.plot(bincenters, n, 'b', linestyle='-', lw=0.75)

    weight = np.ones_like(resp3L)/(el**3)
    n, bins, patches = plt.hist(resp3L,
                                bins=bn,
                                histtype='step',
                                hold=True,
                                range=(dmin, dmax),
                                weights=weight,
                                color='white')
    resp3L, = plt.plot(bincenters, n, 'r', linestyle='-', lw=0.75)
    plt.grid(True)

    weight = np.ones_like(resp4L)/(el**3)
    n, bins, patches = plt.hist(resp4L,
                                bins=bn,
                                histtype='step',
                                hold=True,
                                range=(dmin, dmax),
                                weights=weight,
                                color='white')
    resp4L, = plt.plot(bincenters, n, 'g', linestyle='-', lw=0.75)

    plt.legend([resp1L, resp2L, resp3L, resp4L],
               [set_id_list[0], set_id_list[1], set_id_list[2],
                set_id_list[3]])

    plt.xlabel("$\%s_{%s}$" % (typ, comp))
    plt.ylabel("Count")
    plt.title("$\%s_{%s}$ histograms for $\%s$-Ti textures" % (typ, comp,
                                                               'alpha'))
    plt.ylim([0, 30])

    # plt.savefig("%s%s_histogram.png" % (typ, comp))
    plt.show()

if __name__ == '__main__':
    el = 21
    step = 1
    comp = '22'
    ns_val_list = [390, 22, 44, 399]
    set_id_val_list = ['actual', 'basaltrans', 'trans', 'random']
    make_hist(el, ns_val_list, set_id_val_list, step, comp, 'epsilon')
    make_hist(el, ns_val_list, set_id_val_list, step, comp, 'sigma')
