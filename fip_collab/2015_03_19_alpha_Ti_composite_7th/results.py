# -*- coding: utf-8 -*-
"""
Created on Wed Oct 01 13:52:33 2014

@author: nhpnp3
"""

import numpy as np
import matplotlib.pyplot as plt
import functions as rr
import tables as tb


def results(el, ns, set_id, typ, doplt, wrt_file):

    # vector of the indicial forms of the tensor components
    real_comp = '11'

    # open reference HDF5 file
    base = tb.open_file("ref_%s%s.h5" % (ns, set_id), mode="r")
    # assign data to array
    mks_R = base.root.response.mks_R[...]
    resp = base.root.resp[...]
    micr = base.root.msf.pre_micr[...]
    # close the HDF5 file
    base.close()

    maxindx = np.unravel_index(np.argmax(np.abs(resp - mks_R)), resp.shape)
    maxresp = resp[maxindx]
    maxMKS = mks_R[maxindx]
    maxerr = (np.abs(resp - mks_R)[maxindx]/np.mean(resp))*100

    print 'indices of max error'
    print maxindx
    print 'reference response at max error'
    print maxresp
    print 'MKS response at max error'
    print maxMKS
    print 'maximum error'
    print maxerr
    print micr[maxindx[0], :, maxindx[1], maxindx[2], maxindx[3]]

    # VISUALIZATION OF MKS VS. FEM

    if doplt == 1:

        # pick a slice perpendicular to the x-direction
        # slc = maxindx[1]
        # sn = maxindx[0]

        slc = 0
        sn = 0

        # Plot slices of the response
        plt.figure(num=2, figsize=[16, 8])

        dmin = np.min([mks_R[sn, slc, :, :], resp[sn, slc, :, :]])
        dmax = np.max([mks_R[sn, slc, :, :], resp[sn, slc, :, :]])

        plt.subplot(231)
        ax = plt.imshow(micr[sn, 0, slc, :, :], origin='lower',
                        interpolation='none', cmap='jet')
        plt.colorbar(ax)
        plt.title('phase map, slice %s' % (slc))

        plt.subplot(232)
        ax = plt.imshow(mks_R[sn, slc, :, :], origin='lower',
                        interpolation='none', cmap='jet', vmin=dmin, vmax=dmax)
        plt.colorbar(ax)
        plt.title('MKS $\%s_{%s}$ response, slice %s' % (typ, real_comp, slc))

        plt.subplot(233)
        ax = plt.imshow(resp[sn, slc, :, :], origin='lower',
                        interpolation='none', cmap='jet', vmin=dmin, vmax=dmax)
        plt.colorbar(ax)
        plt.title('FEM $\%s_{%s}$ response, slice %s' % (typ, real_comp, slc))

        # Plot a histogram representing the frequency of strain levels with
        # separate channels for each phase of each type of response.
        plt.subplot(212)

        # find the min and max of both datasets (in full)
        dmin = np.amin([resp, mks_R])
        dmax = np.amax([resp, mks_R])

        micr0 = micr[:, 0, :, :, :].reshape(ns*el*el*el).astype(int)

        resp_lin = resp.reshape(ns*el*el*el)
        mks_lin = mks_R.reshape(ns*el*el*el)

        tmp = np.nonzero(micr0)
        feb = resp_lin[tmp]
        mksb = mks_lin[tmp]

        tmp = np.nonzero(micr0 == 0)
        few = resp_lin[tmp]
        mksw = mks_lin[tmp]

        # select the desired number of bins in the histogram
        bn = 40

        # FEM histogram
        n, bins, patches = plt.hist(feb, bins=bn, histtype='step', hold=True,
                                    range=(dmin, dmax), color='white')
        bincenters = 0.5*(bins[1:]+bins[:-1])
        febp, = plt.plot(bincenters, n, 'k', linestyle='--', lw=1.5)

        n, bins, patches = plt.hist(few, bins=bn, histtype='step', hold=True,
                                    range=(dmin, dmax), color='white')
        fewp, = plt.plot(bincenters, n, 'k')

        # MKS histogram
        n, bins, patches = plt.hist(mksb, bins=bn, histtype='step', hold=True,
                                    range=(dmin, dmax), color='white')
        mksbp, = plt.plot(bincenters, n, 'b', linestyle='--', lw=1.5)

        n, bins, patches = plt.hist(mksw, bins=bn, histtype='step', hold=True,
                                    range=(dmin, dmax), color='white')
        mkswp, = plt.plot(bincenters, n, 'b')

        plt.grid(True)

        plt.legend([febp, fewp, mksbp, mkswp], ["FE - stiff phase",
                                                "FE - compliant phase",
                                                "MKS - stiff phase",
                                                "MKS - compliant phase"])

        plt.xlabel("Strain")
        plt.ylabel("Frequency")
        plt.title("Frequency comparison MKS with FE results")

        # VIOLIN PLOT FOR STRAIN BINS

        error = ((feb - mksb)/0.00814)*100

        sort_list = np.argsort(feb)

        e_sort = feb[sort_list[np.round(0.99*len(error)):]]

        err_sort = error[sort_list[np.round(0.99*len(error)):]]

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

        plt.xlabel("bin centers, $\%s_{%s}$" % (typ, real_comp))
        plt.ylabel("% error")
        plt.title("Error Histogram, $\%s_{%s}$" % (typ, real_comp))
        plt.grid(True)
        plt.tight_layout(pad=0.1)
        plt.ylim([1.25*np.min(err_sort), 1.25*np.max(err_sort)])

        # MAX ERROR DISTRIBUTIONS

        plt.figure(num=4, figsize=[10, 7])

        # find the min and max of both datasets (in full)

        fe = np.max(resp.reshape(ns, el**3), 1)*100
        mks = np.max(mks_R.reshape(ns, el**3), 1)*100

        print fe.shape

        dmin = np.amin([fe, mks])
        dmax = np.amax([fe, mks])

        # select the desired number of bins in the histogram
        bn = 15

        # FEM histogram
        n, bins, patches = plt.hist(fe, bins=bn, histtype='step', hold=True,
                                    range=(dmin, dmax), color='white')
        bincenters = 0.5*(bins[1:]+bins[:-1])
        fep, = plt.plot(bincenters, n, 'b', linestyle='-', lw=1.0)

        # MKS histogram
        n, bins, patches = plt.hist(mks, bins=bn, histtype='step', hold=True,
                                    range=(dmin, dmax), color='white')
        mksp, = plt.plot(bincenters, n, 'r', linestyle='-', lw=1.0)

        plt.grid(True)

        plt.legend([fep, mksp], ["FE", "MKS"])

        plt.xlabel("$\%s_{%s}$ %%" % ('epsilon', '11'))
        plt.ylabel("Frequency")
        plt.title("Maximum $\%s_{%s}$ per MVE, FE vs. MKS,"
                  % ('epsilon', '11'))

    # MEAN ABSOLUTE STRAIN ERROR (MASE)
    avgr_fe_tot = 0
    avgr_mks_tot = 0
    max_diff_all = np.zeros(ns)

    for sn in xrange(ns):
        avgr_fe_indv = np.average(resp[sn, ...])
        avgr_mks_indv = np.average(mks_R[sn, ...])

        avgr_fe_tot += avgr_fe_indv
        avgr_mks_tot += avgr_mks_indv
        max_diff_all[sn] = np.amax(abs(resp[sn, ...]-mks_R[sn, ...]))

    avgr_fe = avgr_fe_tot/ns
    avgr_mks = avgr_mks_tot/ns

    # DIFFERENCE MEASURES
    mean_diff_meas = np.mean(abs(resp-mks_R))/avgr_fe
    mean_max_diff_meas = np.mean(max_diff_all)/avgr_fe
    max_diff_meas_all = np.amax(abs(resp-mks_R))/avgr_fe

    msg = 'Mean voxel difference over all microstructures'\
        ' (divided by mean von-Mises meas), %s%s: %s%%' \
        % (typ, real_comp, mean_diff_meas*100)
    rr.WP(msg, wrt_file)
    msg = 'Average Maximum voxel difference per microstructure'\
        ' (divided by mean von-Mises meas), %s%s: %s%%' \
        % (typ, real_comp, mean_max_diff_meas*100)
    rr.WP(msg, wrt_file)
    msg = 'Maximum voxel difference in all microstructures '\
        '(divided by mean von-Mises meas), %s%s: %s%%' \
        % (typ, real_comp, max_diff_meas_all*100)
    rr.WP(msg, wrt_file)

    # STANDARD STATISTICS
    msg = 'Average, %s%s, FEM: %s' % (typ, real_comp, avgr_fe)
    rr.WP(msg, wrt_file)
    msg = 'Average, %s%s, MKS: %s' % (typ, real_comp, avgr_mks)
    rr.WP(msg, wrt_file)
    msg = 'Standard deviation, %s%s, FEM: %s' \
        % (typ, real_comp, np.std(resp))
    rr.WP(msg, wrt_file)
    msg = 'Standard deviation, %s%s, MKS: %s' \
        % (typ, real_comp, np.std(mks_R))
    rr.WP(msg, wrt_file)

    resp_min = np.mean(np.amin(resp.reshape([el**3, ns]), axis=0))
    mks_R_min = np.mean(np.amin(mks_R.reshape([el**3, ns]), axis=0))

    resp_max = np.mean(np.amax(resp.reshape([el**3, ns]), axis=0))
    mks_R_max = np.mean(np.amax(mks_R.reshape([el**3, ns]), axis=0))

    msg = 'Mean minimum, %s%s, FEM: %s' % (typ, real_comp, resp_min)
    rr.WP(msg, wrt_file)
    msg = 'Mean minimum, %s%s, MKS: %s' % (typ, real_comp, mks_R_min)
    rr.WP(msg, wrt_file)
    msg = 'Mean maximum, %s%s, FEM: %s' % (typ, real_comp, resp_max)
    rr.WP(msg, wrt_file)
    msg = 'Mean maximum, %s%s, MKS: %s' % (typ, real_comp, mks_R_max)
    rr.WP(msg, wrt_file)

    plt.show()


if __name__ == '__main__':
    results(21, 400, 'val', 'epsilon', 1, 'test.txt')
