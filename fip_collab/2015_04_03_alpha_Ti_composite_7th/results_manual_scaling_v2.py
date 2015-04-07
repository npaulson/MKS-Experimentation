# -*- coding: utf-8 -*-
"""
Created on Wed Oct 01 13:52:33 2014

@author: nhpnp3
"""

import numpy as np
import matplotlib.pyplot as plt
import functions as rr
import tables as tb
from sklearn.neighbors import KernelDensity


def results(el, ns, set_id, typ, comp, spr, wrt_file):

    if spr == 'p':
        spr_ = "_p"
        sprup = "^p"
    else:
        spr_ = spr
        sprup = ""

    # open reference HDF5 file
    base = tb.open_file("ref_%s%s.h5" % (ns, set_id), mode="r")
    # assign data to array
    group = base.get_node('/%s%s' % (typ, spr_))
    r_mks = group.r_mks[...]
    r_fem = group.r_fem[...]
    micr = base.root.msf.pre_micr[...]
    # close the HDF5 file
    base.close()

    maxindx = np.unravel_index(np.argmax(np.abs(r_fem - r_mks)), r_fem.shape)
    maxresp = r_fem[maxindx]
    maxMKS = r_mks[maxindx]
    maxdiff = (np.abs(r_fem - r_mks)[maxindx])

    print '\nindices of max error:'
    print maxindx
    print '\nreference response at max error:'
    print maxresp
    print '\nMKS response at max error:'
    print maxMKS
    print '\nmaximum difference in response:'
    print maxdiff
    print micr[maxindx[0], :, maxindx[1], maxindx[2], maxindx[3]]

    # VISUALIZATION OF MKS VS. FEM

    # pick a slice perpendicular to the x-direction
    # slc = maxindx[1]
    # sn = maxindx[0]

    slc = 0
    sn = 200

    r_fem_lin = r_fem.reshape(ns*el*el*el)
    r_mks_lin = r_mks.reshape(ns*el*el*el)

    # field_std(el, ns, r_fem, r_mks, micr, typ, comp, sprup, sn, slc, 1)
    # hist_std(el, ns, r_fem, r_mks, micr, typ, comp, sprup, 2)
    # violin_extreme_val(el, ns, r_fem_lin, r_mks_lin, typ, comp, sprup,
    #                    0.99, nfac, 3)
    hist_extreme_val(el, ns, r_fem, r_mks, typ, comp, sprup, 4)
    # hist_extreme_val_2axis(el, ns, r_fem, r_mks, typ, comp, sprup, 5)
    hist_extreme_val_2axis_alt(el, ns, r_fem, r_mks, typ, comp, sprup, 6)
    # error_calc(el, ns, r_fem, r_mks, typ, comp, spr, nfac, wrt_file)

    plt.show()


def error_calc(el, ns, r_fem, r_mks, typ, comp, spr, nfac, wrt_file):

    # MEAN ABSOLUTE STRAIN ERROR (MASE)
    max_diff_all = np.zeros(ns)
    for sn in xrange(ns):
        max_diff_all[sn] = np.amax(abs(r_fem[sn, ...]-r_mks[sn, ...]))

    # DIFFERENCE MEASURES
    mean_diff_meas = np.mean(abs(r_fem-r_mks))/nfac
    mean_max_diff_meas = np.mean(max_diff_all)/nfac
    max_diff_meas_all = np.amax(abs(r_fem-r_mks))/nfac

    msg = 'Mean voxel difference over all microstructures'\
        ' (divided by mean von-Mises meas), %s_%s%s: %s%%' \
        % (typ, spr, comp, mean_diff_meas*100)
    rr.WP(msg, wrt_file)
    msg = 'Average Maximum voxel difference per microstructure'\
        ' (divided by mean von-Mises meas), %s_%s%s: %s%%' \
        % (typ, spr, comp, mean_max_diff_meas*100)
    rr.WP(msg, wrt_file)
    msg = 'Maximum voxel difference in all microstructures '\
        '(divided by mean von-Mises meas), %s_%s%s: %s%%' \
        % (typ, spr, comp, max_diff_meas_all*100)
    rr.WP(msg, wrt_file)

    # STANDARD STATISTICS
    msg = 'Average, %s_%s%s, FEM: %s' % (typ, spr, comp, np.mean(r_fem))
    rr.WP(msg, wrt_file)
    msg = 'Average, %s_%s%s, MKS: %s' % (typ, spr, comp, np.mean(r_mks))
    rr.WP(msg, wrt_file)
    msg = 'Standard deviation, %s_%s%s, FEM: %s' \
        % (typ, spr, comp, np.std(r_fem))
    rr.WP(msg, wrt_file)
    msg = 'Standard deviation, %s_%s%s, MKS: %s' \
        % (typ, spr, comp, np.std(r_mks))
    rr.WP(msg, wrt_file)

    r_fem_min = np.mean(np.amin(r_fem.reshape([el**3, ns]), axis=0))
    r_mks_min = np.mean(np.amin(r_mks.reshape([el**3, ns]), axis=0))

    r_fem_max = np.mean(np.amax(r_fem.reshape([el**3, ns]), axis=0))
    r_mks_max = np.mean(np.amax(r_mks.reshape([el**3, ns]), axis=0))

    msg = 'Mean minimum, %s_%s%s, FEM: %s' % (typ, spr, comp, r_fem_min)
    rr.WP(msg, wrt_file)
    msg = 'Mean minimum, %s_%s%s, MKS: %s' % (typ, spr, comp, r_mks_min)
    rr.WP(msg, wrt_file)
    msg = 'Mean maximum, %s_%s%s, FEM: %s' % (typ, spr, comp, r_fem_max)
    rr.WP(msg, wrt_file)
    msg = 'Mean maximum, %s_%s%s, MKS: %s' % (typ, spr, comp, r_mks_max)
    rr.WP(msg, wrt_file)


def field_std(el, ns, r_fem, r_mks, micr, typ, comp, spr, sn, slc, plotnum):

    # Plot slices of the response
    plt.figure(num=plotnum, figsize=[13, 2.7])

    dmin = np.min([r_mks[sn, slc, :, :], r_fem[sn, slc, :, :]])
    dmax = np.max([r_mks[sn, slc, :, :], r_fem[sn, slc, :, :]])

    plt.subplot(131)
    ax = plt.imshow(micr[sn, 0, slc, :, :], origin='lower',
                    interpolation='none', cmap='jet')
    plt.colorbar(ax)
    plt.title('phase map, slice %s' % (slc))

    plt.subplot(132)
    ax = plt.imshow(r_mks[sn, slc, :, :], origin='lower',
                    interpolation='none', cmap='jet', vmin=dmin, vmax=dmax)
    plt.colorbar(ax)
    plt.title('MKS $\%s_{%s}%s$, slice %s' % (typ, comp, spr, slc))

    plt.subplot(133)
    ax = plt.imshow(r_fem[sn, slc, :, :], origin='lower',
                    interpolation='none', cmap='jet', vmin=dmin, vmax=dmax)
    plt.colorbar(ax)
    plt.title('FEM $\%s_{%s}%s$, slice %s' % (typ, comp, spr, slc))


def hist_extreme_val_2axis(el, ns, r_fem, r_mks, typ, comp, spr, plotnum):
    """
    The following generates histograms for the top strain
    value in each MVE for both the MKS and FEM strain fields. The histograms
    are normalized by the minimum and maximum strain values in the set of
    extreme values. This normalization is performed to superimpose the FEM and
    MKS extreme value distributions. This will make it clear if the
    distributions have the same shape, even if the actual values are different.
    """

    fig, ax1 = plt.subplots(num=plotnum, figsize=[10, 7])

    # define a second x-axis
    ax2 = ax1.twiny()

    # find the min and max of both datasets (in full)
    fem = np.max(np.abs(r_fem.reshape(ns, el**3)), 1)*100
    mks = np.max(np.abs(r_mks.reshape(ns, el**3)), 1)*100

    # select the desired number of bins in the histogram
    bn = 15

    # FEM histogram
    n1, bins, patches = ax1.hist(fem,
                                 bins=bn,
                                 histtype='step',
                                 color='white')
    bcnt1 = 0.5*(bins[1:]+bins[:-1])  # bin centers
    bhgt1 = n1/ns  # normalized bin heights

    # MKS histogram
    n2, bins, patches = ax1.hist(mks,
                                 bins=bn,
                                 histtype='step',
                                 color='white')
    bcnt2 = 0.5*(bins[1:]+bins[:-1])  # bin centers
    bhgt2 = n2/ns  # normalized bin heights

    femp, = ax1.plot(bcnt1,
                     bhgt1,
                     'b',
                     linestyle='-',
                     lw=1.0)

    mksp, = ax2.plot(bcnt2,
                     bhgt2,
                     'r',
                     linestyle='-',
                     lw=1.0)

    plt.grid(True)
    plt.legend([femp, mksp], ["FEM", "MKS"])

    # color the labels for the first set of axes blue
    for tl in ax1.get_xticklabels():
        tl.set_color('b')
    # color the labels for the second set of axes red
    for tl in ax2.get_xticklabels():
        tl.set_color('r')

    # set and determine x-limits for first set of axes:
    max_loc = np.mean(fem)
    half_range = np.max(np.abs([max_loc-bcnt1[0], bcnt1[-1]-max_loc]))
    ax_min = max_loc-1.1*half_range
    ax_max = max_loc+1.1*half_range
    ax1.set_xlim(ax_min, ax_max)

    # set and determine x-limits for second set of axes:
    max_loc = np.mean(mks)
    half_range = np.max(np.abs([max_loc-bcnt2[0], bcnt2[-1]-max_loc]))
    ax_min = max_loc-1.1*half_range
    ax_max = max_loc+1.1*half_range
    ax2.set_xlim(ax_min, ax_max)

    ax1.set_ylim(0, 1.2*np.max([bhgt1, bhgt2]))
    ax1.set_xlabel("%%$\%s_{%s}%s$ FEM" % (typ, comp, spr))
    ax2.set_xlabel("%%$\%s_{%s}%s$ MKS" % (typ, comp, spr))
    ax1.set_ylabel("Frequency")
    plt.title("Maximum $\%s_{%s}%s$ per MVE, FE vs. MKS"
              % (typ, comp, spr), y=1.08)


def hist_extreme_val(el, ns, r_fem, r_mks, typ, comp, spr, plotnum):
    """
    The following generates histograms for the top strain
    value in each MVE for both the MKS and FEM strain fields. The histograms
    are normalized by the minimum and maximum strain values in the set of
    extreme values. This normalization is performed to superimpose the FEM and
    MKS extreme value distributions. This will make it clear if the
    distributions have the same shape, even if the actual values are different.
    """

    fig, ax = plt.subplots(num=plotnum, figsize=[10, 7])

    # find the min and max of both datasets (in full)
    fem = np.max(np.abs(r_fem.reshape(ns, el**3)), 1)*100
    mks = np.max(np.abs(r_mks.reshape(ns, el**3)), 1)*100

    # select the desired number of bins in the histogram
    bn = 15

    # FEM histogram
    n1, bins, patches = ax.hist(fem,
                                bins=bn,
                                normed=True,
                                histtype='step',
                                color='black')

    # MKS histogram
    n2, bins, patches = ax.hist(mks,
                                bins=bn,
                                normed=True,
                                histtype='step',
                                color='blue')

    smin = np.min([fem, mks])
    smax = np.max([fem, mks])
    X_plot = np.linspace(smin, smax, 1000)[:, np.newaxis]

    kde = KernelDensity(kernel='gaussian',
                        bandwidth=0.025).fit(fem[:, np.newaxis])
    log_dens = kde.score_samples(X_plot)
    fem_dens = np.exp(log_dens)
    femp, = ax.plot(X_plot[:, 0], fem_dens, '-r')

    kde = KernelDensity(kernel='gaussian',
                        bandwidth=0.015).fit(mks[:, np.newaxis])
    log_dens = kde.score_samples(X_plot)
    mks_dens = np.exp(log_dens)
    mksp, = ax.plot(X_plot[:, 0], mks_dens, '-g')

    plt.grid(True)
    plt.legend([femp, mksp], ["FEM", "MKS"])

    ax.set_ylim(0, 1.25*np.max([fem_dens, mks_dens]))
    ax.set_xlabel("%%$\%s_{%s}%s$" % (typ, comp, spr))
    ax.set_ylabel("Relative Density")
    plt.title("Maximum $\%s_{%s}%s$ per MVE, FE vs. MKS"
              % (typ, comp, spr))


def hist_extreme_val_2axis_alt(el, ns, r_fem, r_mks, typ, comp, spr, plotnum):
    """
    The following generates histograms for the top strain
    value in each MVE for both the MKS and FEM strain fields. The histograms
    are normalized by the minimum and maximum strain values in the set of
    extreme values. This normalization is performed to superimpose the FEM and
    MKS extreme value distributions. This will make it clear if the
    distributions have the same shape, even if the actual values are different.
    """

    fig, ax1 = plt.subplots(num=plotnum, figsize=[10, 7])

    # define a second x-axis
    ax2 = ax1.twiny()

    # find the min and max of both datasets (in full)
    fem = np.max(np.abs(r_fem.reshape(ns, el**3)), 1)*100
    mks = np.max(np.abs(r_mks.reshape(ns, el**3)), 1)*100

    # select the desired number of bins in the histogram
    # bn = 15

    # # FEM histogram
    # n1, bins, patches = ax1.hist(fem,
    #                              bins=bn,
    #                              normed=True,
    #                              histtype='step',
    #                              color='black')

    # # MKS histogram
    # n2, bins, patches = ax1.hist(mks,
    #                              bins=bn,
    #                              normed=True,
    #                              histtype='step',
    #                              color='blue')

    X_plot = np.linspace(np.min(fem), np.max(fem), 1000)[:, np.newaxis]

    kde = KernelDensity(kernel='gaussian',
                        bandwidth=0.025).fit(fem[:, np.newaxis])
    log_dens = kde.score_samples(X_plot)
    fem_dens = np.exp(log_dens)
    fem_dens_rel = fem_dens/np.max(fem_dens)
    femp, = ax1.plot(X_plot[:, 0], fem_dens_rel, '-r')

    X_plot = np.linspace(np.min(mks), np.max(mks), 1000)[:, np.newaxis]

    kde = KernelDensity(kernel='gaussian',
                        bandwidth=0.015).fit(mks[:, np.newaxis])
    log_dens = kde.score_samples(X_plot)
    mks_dens = np.exp(log_dens)
    mks_dens_rel = mks_dens/np.max(mks_dens)
    mksp, = ax2.plot(X_plot[:, 0], mks_dens_rel, '-g')

    plt.grid(True)
    plt.legend([femp, mksp], ["FEM", "MKS"])

    # color the labels for the first set of axes blue
    for tl in ax1.get_xticklabels():
        tl.set_color('r')
    # color the labels for the second set of axes red
    for tl in ax2.get_xticklabels():
        tl.set_color('g')

    # set and determine x-limits for first set of axes:
    max_loc = np.mean(fem)
    half_range = np.max(np.abs([max_loc-np.min(fem), np.max(fem)-max_loc]))
    ax_min = max_loc-1.1*half_range
    ax_max = max_loc+1.1*half_range
    ax1.set_xlim(ax_min, ax_max)

    # set and determine x-limits for second set of axes:
    max_loc = np.mean(mks)
    half_range = np.max(np.abs([max_loc-np.min(mks), np.max(mks)-max_loc]))
    ax_min = max_loc-1.1*half_range
    ax_max = max_loc+1.1*half_range
    ax2.set_xlim(ax_min, ax_max)

    ax1.set_ylim(0, 1.2)
    ax1.set_xlabel("%%$\%s_{%s}%s$ FEM" % (typ, comp, spr))
    ax2.set_xlabel("%%$\%s_{%s}%s$ MKS" % (typ, comp, spr))
    ax1.set_ylabel("density relative to maximum")
    plt.title("Maximum $\%s_{%s}%s$ per MVE, FE vs. MKS"
              % (typ, comp, spr), y=1.08)


def hist_std(el, ns, r_fem, r_mks, micr, typ, comp, spr, plotnum):

    plt.figure(num=plotnum, figsize=[10, 7])

    # find the min and max of both datasets (in full)
    dmin = np.amin([r_fem, r_mks])
    dmax = np.amax([r_fem, r_mks])

    micr0 = micr[:, 0, :, :, :].reshape(ns*el*el*el).astype(int)

    r_fem_lin = r_fem.reshape(ns*el*el*el)
    r_mks_lin = r_mks.reshape(ns*el*el*el)

    tmp = np.nonzero(micr0)
    femb = r_fem_lin[tmp]
    mksb = r_mks_lin[tmp]

    tmp = np.nonzero(micr0 == 0)
    femw = r_fem_lin[tmp]
    mksw = r_mks_lin[tmp]

    # select the desired number of bins in the histogram
    bn = 40

    # FEM histogram
    n, bins, patches = plt.hist(femb, bins=bn, histtype='step', hold=True,
                                range=(dmin, dmax), color='white')
    bincenters = 0.5*(bins[1:]+bins[:-1])
    fembp, = plt.plot(bincenters, n, 'k', linestyle='--', lw=1.5)

    n, bins, patches = plt.hist(femw, bins=bn, histtype='step', hold=True,
                                range=(dmin, dmax), color='white')
    femwp, = plt.plot(bincenters, n, 'k')

    # MKS histogram
    n, bins, patches = plt.hist(mksb, bins=bn, histtype='step', hold=True,
                                range=(dmin, dmax), color='white')
    mksbp, = plt.plot(bincenters, n, 'b', linestyle='--', lw=1.5)

    n, bins, patches = plt.hist(mksw, bins=bn, histtype='step', hold=True,
                                range=(dmin, dmax), color='white')
    mkswp, = plt.plot(bincenters, n, 'b')

    plt.grid(True)

    plt.legend([fembp, femwp, mksbp, mkswp], ['FEM - stiff phase',
                                              'FEM - compliant phase',
                                              'MKS - stiff phase',
                                              'MKS - compliant phase'])

    plt.xlabel('$\%s_{%s}%s$' % (typ, comp, spr))
    plt.ylabel('Frequency')
    plt.title('Frequency comparison MKS with FE results')


def violin_extreme_val(el, ns, r_fem_lin, r_mks_lin, typ, comp, spr,
                       percentile, nfac, plotnum):

    error = ((r_fem_lin - r_mks_lin)/nfac)*100

    sort_list = np.argsort(r_fem_lin)

    e_sort = r_fem_lin[sort_list[np.round(percentile*len(error)):]]

    err_sort = error[sort_list[np.round(percentile*len(error)):]]

    # select the desired number of bins in the histogram
    bn = 10

    # number of error values per bin in the violin plot
    num_per_bin = np.floor(len(e_sort)/bn)

    error_in_bin_list = []
    bin_labels = []

    for ii in xrange(bn):

        if ii != bn-1:
            error_in_bin = err_sort[ii*num_per_bin:(ii+1)*num_per_bin-1]
            ep_in_bin = e_sort[ii*num_per_bin:(ii+1)*num_per_bin-1]
        else:
            error_in_bin = err_sort[ii*num_per_bin:]
            ep_in_bin = e_sort[ii*num_per_bin:]

        print len(ep_in_bin)

        error_in_bin_list.append(error_in_bin)

        label_cur = str(np.round(100*ep_in_bin[0], 4)) + '% - ' + \
            str(np.round(100*ep_in_bin[-1], 4)) + '%'
        bin_labels.append(label_cur)

    plt.figure(num=3, figsize=[12, 7])

    ax = plt.subplot(111)

    x = np.arange(1, bn + 1)

    ax.violinplot(dataset=error_in_bin_list, showextrema=False,
                  showmedians=False, showmeans=False)

    ax.set_xticks(x)
    ax.set_xticklabels(bin_labels, rotation='vertical')

    plt.xlabel("bin centers, $\%s_{%s}%s$" % (typ, comp, spr))
    plt.ylabel("% error")
    plt.title("Error Histogram, $\%s_{%s}%s$" % (typ, comp, spr))
    plt.grid(True)
    plt.tight_layout(pad=0.1)
    plt.ylim([1.25*np.min(err_sort), 1.25*np.max(err_sort)])


if __name__ == '__main__':
    results(21, 400, 'val008', 'epsilon', '11', '', 'test.txt')
