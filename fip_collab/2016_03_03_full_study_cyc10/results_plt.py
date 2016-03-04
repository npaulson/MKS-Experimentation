# -*- coding: utf-8 -*-
"""
Created on Wed Oct 01 13:52:33 2014

@author: nhpnp3
"""

import time
import numpy as np
import matplotlib.pyplot as plt
import functions as rr
import h5py
from sklearn.neighbors import KernelDensity


def results(el, ns, set_id, step, typ, comp, newID, traID, nfac):

    """specify the file to write messages to"""
    # wrt_file = 'results_step%s_%s%s_%s.txt' % \
    #            (step, ns, set_id, time.strftime("%Y-%m-%d_h%Hm%M"))

    f = h5py.File("fip_%s%s_s%s.hdf5" % (ns, set_id, step), 'r')

    print f.keys()

    # euler = f.get('euler')[...].reshape(ns, 3, el, el, el)
    traSET = f.get('%s' % traID)[...]
    newSET = f.get('%s' % newID)[...]
    f.close()

    maxindx = np.unravel_index(np.argmax(np.abs(traSET - newSET)),
                               traSET.shape)
    maxresp = traSET[maxindx]
    maxMKS = newSET[maxindx]
    maxdiff = (np.abs(traSET - newSET)[maxindx])

    print '\nindices of max error:'
    print maxindx
    print '\nreference response at max error:'
    print maxresp
    print '\nMKS response at max error:'
    print maxMKS
    print '\nmaximum difference in response:'
    print maxdiff
    # print euler[maxindx[0], :, maxindx[1], maxindx[2], maxindx[3]]

    """VISUALIZATION OF MKS VS. FEM"""

    # pick a slice perpendicular to the x-direction
    # slc = maxindx[1]
    # sn = maxindx[0]

    slc = 0
    sn = 10

    # r_fem_lin = r_fem.reshape(ns*el*el*el)
    # r_mks_lin = r_mks.resape(ns*el*el*el)

    field_std(el, ns, traSET, newSET, euler, typ, comp, sn, slc, 1)
    # hist_std(el, ns, r_fem, r_mks, typ, comp, spr, 2)
    # violin_extreme_val(el, ns, r_fem_lin, r_mks_lin, typ, comp, spr,
    #                    0.99, nfac, 3)
    # hist_extreme_val(el, ns, r_fem, r_mks, typ, comp, spr, 4)
    # hist_extreme_val_2axis(el, ns, r_fem, r_mks, typ, comp, spr, 5)
    # plot_euler(el, ns, euler, sn, slc, 6)

    plt.show()


def field_std(el, ns, traSET, newSET, micr, typ, comp, sn, slc, plotnum):

    """split the typ string for proper plot output"""
    blankloc = typ.find('_')

    if blankloc == -1:
        base = typ
        exp = ''
    else:
        base = typ[:blankloc]
        exp = typ[blankloc+1:]

    """Plot slices of the response"""
    plt.figure(num=plotnum, figsize=[9, 2.7])

    dmin = np.min([newSET[sn, slc, :, :], traSET[sn, slc, :, :]])
    dmax = np.max([newSET[sn, slc, :, :], traSET[sn, slc, :, :]])

    plt.subplot(121)
    ax = plt.imshow(newSET[sn, slc, :, :], origin='lower',
                    interpolation='none', cmap='jet', vmin=dmin, vmax=dmax)
    plt.colorbar(ax)
    plt.title('New Approach $\{%s}_{%s}^{%s}$, slice %s'
              % (base, comp, exp, slc))

    plt.subplot(122)
    ax = plt.imshow(traSET[sn, slc, :, :], origin='lower',
                    interpolation='none', cmap='jet', vmin=dmin, vmax=dmax)
    plt.colorbar(ax)
    plt.title('Standard Approach $\{%s}_{%s}^{%s}$, slice %s'
              % (base, comp, exp, slc))


# def hist_extreme_val(el, ns, r_fem, r_mks, typ, comp, spr, plotnum):
#     """
#     The following generates histograms for the top strain
#     value in each MVE for both the MKS and FEM strain fields. The histograms
#     are normalized by the minimum and maximum strain values in the set of
#     extreme values. This normalization is performed to superimpose the FEM and
#     MKS extreme value distributions. This will make it clear if the
#     distributions have the same shape, even if the actual values are different.
#     """

#     fig, ax = plt.subplots(num=plotnum, figsize=[10, 7])

#     # find the min and max of both datasets (in full)
#     fem = np.max(np.abs(r_fem.reshape(ns, el**3)), 1)*100
#     mks = np.max(np.abs(r_mks.reshape(ns, el**3)), 1)*100

#     # select the desired number of bins in the histogram
#     bn = 15

#     # FEM histogram
#     n1, bins, patches = ax.hist(fem,
#                                 bins=bn,
#                                 normed=True,
#                                 histtype='stepfilled',
#                                 fc=[0, 0, .5],
#                                 alpha=0.2)

#     # MKS histogram
#     n2, bins, patches = ax.hist(mks,
#                                 bins=bn,
#                                 normed=True,
#                                 histtype='stepfilled',
#                                 fc=[.5, 0, 0],
#                                 alpha=0.2)

#     smin = np.min(fem)
#     smax = np.max(fem)
#     X_plot = np.linspace(smin, smax, 1000)[:, np.newaxis]

#     bw_silverman = ((4*np.std(fem)**5)/(3*ns))**(1./5.)
#     kde = KernelDensity(kernel='gaussian',
#                         bandwidth=bw_silverman).fit(fem[:, np.newaxis])

#     fem_dens = np.exp(kde.score_samples(X_plot))

#     femp, = ax.plot(X_plot[:, 0],
#                     fem_dens,
#                     linewidth=2,
#                     alpha=0.5,
#                     color=[0., 0., 1.])

#     smin = np.min(mks)
#     smax = np.max(mks)
#     X_plot = np.linspace(smin, smax, 1000)[:, np.newaxis]

#     bw_silverman = ((4*np.std(mks)**5)/(3*ns))**(1./5.)
#     kde = KernelDensity(kernel='gaussian',
#                         bandwidth=bw_silverman).fit(mks[:, np.newaxis])

#     mks_dens = np.exp(kde.score_samples(X_plot))

#     mksp, = ax.plot(X_plot[:, 0],
#                     mks_dens,
#                     linewidth=2,
#                     alpha=0.5,
#                     color=[1., 0., 0.])

#     plt.grid(True)
#     plt.legend([femp, mksp], ["FEM", "MKS"])

#     ax.set_ylim(0, 1.5*np.max([fem_dens, mks_dens]))
#     ax.set_xlabel("%%$\%s_{%s}%s$" % (typ, comp, spr))
#     ax.set_ylabel("Relative Density")
#     plt.title("Maximum $\%s_{%s}%s$ per MVE, FE vs. MKS"
#               % (typ, comp, spr))


# def hist_extreme_val_2axis(el, ns, r_fem, r_mks, typ, comp, spr, plotnum):
#     """
#     The following generates histograms for the top strain
#     value in each MVE for both the MKS and FEM strain fields. The histograms
#     are normalized by the minimum and maximum strain values in the set of
#     extreme values. This normalization is performed to superimpose the FEM and
#     MKS extreme value distributions. This will make it clear if the
#     distributions have the same shape, even if the actual values are different.
#     """

#     fig, ax1 = plt.subplots(num=plotnum, figsize=[10, 7])

#     # define a second x-axis
#     ax2 = ax1.twiny()

#     # find the min and max of both datasets (in full)
#     fem = np.max(np.abs(r_fem.reshape(ns, el**3)), 1)*100
#     mks = np.max(np.abs(r_mks.reshape(ns, el**3)), 1)*100

#     smin = np.min(fem)
#     smax = np.max(fem)
#     X_plot = np.linspace(smin, smax, 1000)[:, np.newaxis]

#     bw_silverman = ((4*np.std(fem)**5)/(3*ns))**(1./5.)
#     kde = KernelDensity(kernel='gaussian',
#                         bandwidth=bw_silverman).fit(fem[:, np.newaxis])

#     fem_dens = np.exp(kde.score_samples(X_plot))
#     fem_dens_rel = fem_dens/np.max(fem_dens)

#     femp, = ax1.plot(X_plot[:, 0],
#                      fem_dens_rel,
#                      linewidth=2,
#                      alpha=0.5,
#                      color=[0., 0., 1.])

#     smin = np.min(mks)
#     smax = np.max(mks)
#     X_plot = np.linspace(smin, smax, 1000)[:, np.newaxis]

#     bw_silverman = ((4*np.std(mks)**5)/(3*ns))**(1./5.)
#     kde = KernelDensity(kernel='gaussian',
#                         bandwidth=bw_silverman).fit(mks[:, np.newaxis])

#     mks_dens = np.exp(kde.score_samples(X_plot))
#     mks_dens_rel = mks_dens/np.max(mks_dens)

#     mksp, = ax2.plot(X_plot[:, 0],
#                      mks_dens_rel,
#                      linewidth=2,
#                      alpha=0.5,
#                      color=[1., 0., 0.])

#     plt.grid(True)
#     plt.legend([femp, mksp], ["FEM", "MKS"])

#     # color the labels for the first set of axes blue
#     for tl in ax1.get_xticklabels():
#         tl.set_color('b')
#     # color the labels for the second set of axes red
#     for tl in ax2.get_xticklabels():
#         tl.set_color('r')

#     # set and determine x-limits for first set of axes:
#     mean = np.mean(fem)
#     sdev = np.std(fem)
#     ax_min = mean-4*sdev
#     ax_max = mean+4*sdev
#     ax1.set_xlim(ax_min, ax_max)

#     # set and determine x-limits for second set of axes:
#     mean = np.mean(mks)
#     sdev = np.std(mks)
#     ax_min = mean-4*sdev
#     ax_max = mean+4*sdev
#     ax2.set_xlim(ax_min, ax_max)

#     ax1.set_ylim(0, 1.2)
#     ax1.set_xlabel("%%$\%s_{%s}%s$ FEM" % (typ, comp, spr))
#     ax2.set_xlabel("%%$\%s_{%s}%s$ MKS" % (typ, comp, spr))
#     ax1.set_ylabel("density relative to maximum")
#     plt.title("Maximum $\%s_{%s}%s$ per MVE, FE vs. MKS"
#               % (typ, comp, spr), y=1.08)


# def hist_std(el, ns, r_fem, r_mks, typ, comp, spr, plotnum):

#     fig, ax = plt.subplots(num=plotnum, figsize=[10, 7])

#     fem = r_fem.reshape(ns*el*el*el)[0:-1:400]
#     print fem.size
#     mks = r_mks.reshape(ns*el*el*el)[0:-1:400]

#     smin = np.min(fem)
#     smax = np.max(fem)
#     X_plot = np.linspace(smin, smax, 1000)[:, np.newaxis]

#     bw_silverman = ((4*np.std(fem)**5)/(3*fem.size))**(1./5.)
#     kde = KernelDensity(kernel='gaussian',
#                         bandwidth=bw_silverman).fit(fem[:, np.newaxis])

#     fem_dens = np.exp(kde.score_samples(X_plot))

#     femp, = ax.plot(X_plot[:, 0],
#                     fem_dens,
#                     linewidth=2,
#                     alpha=0.5,
#                     color=[0., 0., 1.])

#     smin = np.min(mks)
#     smax = np.max(mks)
#     X_plot = np.linspace(smin, smax, 1000)[:, np.newaxis]

#     bw_silverman = ((4*np.std(mks)**5)/(3*fem.size))**(1./5.)
#     kde = KernelDensity(kernel='gaussian',
#                         bandwidth=bw_silverman).fit(mks[:, np.newaxis])

#     mks_dens = np.exp(kde.score_samples(X_plot))

#     mksp, = ax.plot(X_plot[:, 0],
#                     mks_dens,
#                     linewidth=2,
#                     alpha=0.5,
#                     color=[1., 0., 0.])

#     plt.grid(True)

#     plt.legend([femp, mksp], ['FEM', 'MKS'])

#     plt.xlabel('$\%s_{%s}^%s$' % (typ, comp, spr))
#     plt.ylabel('Frequency')
#     plt.title('Frequency comparison MKS with FE results')


# def plot_euler(el, ns, euler, sn, slc, plotnum):

#     plt.figure(num=plotnum, figsize=[12, 2.7])

#     plt.subplot(131)
#     ax = plt.imshow(euler[sn, 0, slc, :, :],
#                     origin='lower',
#                     interpolation='none',
#                     cmap='jet')
#     plt.colorbar(ax)
#     plt.title('Slice %s, $\phi_1$' % slc)

#     plt.subplot(132)
#     ax = plt.imshow(euler[sn, 1, slc, :, :],
#                     origin='lower',
#                     interpolation='none',
#                     cmap='jet')
#     plt.colorbar(ax)
#     plt.title('$\Phi$')

#     plt.subplot(133)
#     ax = plt.imshow(euler[sn, 2, slc, :, :],
#                     origin='lower',
#                     interpolation='none',
#                     cmap='jet')
#     plt.colorbar(ax)
#     plt.title('$\phi_2$')


# def violin_extreme_val(el, ns, r_fem_lin, r_mks_lin, typ, comp, spr,
#                        percentile, nfac, plotnum):

#     error = ((r_fem_lin - r_mks_lin)/nfac)*100

#     sort_list = np.argsort(r_fem_lin)

#     e_sort = r_fem_lin[sort_list[np.round(percentile*len(error)):]]

#     err_sort = error[sort_list[np.round(percentile*len(error)):]]

#     # select the desired number of bins in the histogram
#     bn = 10

#     # number of error values per bin in the violin plot
#     num_per_bin = np.floor(len(e_sort)/bn)

#     error_in_bin_list = []
#     bin_labels = []

#     for ii in xrange(bn):

#         if ii != bn-1:
#             error_in_bin = err_sort[ii*num_per_bin:(ii+1)*num_per_bin-1]
#             ep_in_bin = e_sort[ii*num_per_bin:(ii+1)*num_per_bin-1]
#         else:
#             error_in_bin = err_sort[ii*num_per_bin:]
#             ep_in_bin = e_sort[ii*num_per_bin:]

#         print len(ep_in_bin)

#         error_in_bin_list.append(error_in_bin)

#         label_cur = str(np.round(100*ep_in_bin[0], 4)) + '% - ' + \
#             str(np.round(100*ep_in_bin[-1], 4)) + '%'
#         bin_labels.append(label_cur)

#     plt.figure(num=3, figsize=[12, 7])

#     ax = plt.subplot(111)

#     x = np.arange(1, bn + 1)

#     ax.violinplot(dataset=error_in_bin_list, showextrema=False,
#                   showmedians=False, showmeans=False)

#     ax.set_xticks(x)
#     ax.set_xticklabels(bin_labels, rotation='vertical')

#     plt.xlabel("bin centers, $\%s_{%s}^%s$" % (typ, comp, spr))
#     plt.ylabel("% error")
#     plt.title("Error Histogram, $\%s_{%s}^%s$" % (typ, comp, spr))
#     plt.grid(True)
#     plt.tight_layout(pad=0.1)
#     plt.ylim([1.25*np.min(err_sort), 1.25*np.max(err_sort)])


if __name__ == '__main__':
    el = 21
    ns = 100
    set_id = 'val'
    step = 5

    # """parameters to plot strain field"""
    # typ = 'epsilon_t'
    # comp = '11'
    # newID = 'rmks'
    # traID = 'r'
    # nfac = 0.00747

    """parameters to plot fips"""
    typ = 'fip'
    comp = ''
    newID = 'fip'
    traID = 'fipmks'
    nfac = 1.0

    results(el, ns, set_id, step, typ, comp, newID, traID, nfac)
