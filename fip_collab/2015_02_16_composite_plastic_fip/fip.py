import numpy as np
import matplotlib.pyplot as plt
import functions_composite as rr


def fip_calc(el, ns, set_id, wrt_file):

    mks_R = np.load('mksR_%s%s.npy' % (ns, set_id))
    resp = np.load('r_%s%s.npy' % (ns, set_id)).reshape([ns, el, el, el])
    micr = np.load('pre_msf_%s%s.npy' % (ns, set_id))

    # DEFINE RELEVANT PARAMETERS

    typ = 'epsilon'
    real_comp = '11'

    y_0 = 0.1  # phase 0 yield point
    y_1 = 0.125  # phase 1 yield point
    E_0 = 100  # phase 0 Young's Modulus
    E_1 = 100  # phase 1 Young's Modulus

    K = 1000.0  # constant in F-S parameter

    ey_0 = y_0/E_0  # strain at yield for phase 0
    ey_1 = y_1/E_1  # strain at yield for phase 1

    # CALCULATE THE PLASTIC AND ELASTIC STRAIN DISTRIBUTIONS

    # FEM results

    # plastic strain phase 0
    ep_0 = micr[:, 0, ...] * resp - ey_0 * micr[:, 0, ...] > 0
    ep_0 = ep_0 * (resp - ey_0 * micr[:, 0, ...])
    ee_0 = micr[:, 0, ...] * resp - ep_0  # elastic strain phase 0

    # plastic strain phase 1
    ep_1 = micr[:, 1, ...] * resp - ey_1 * micr[:, 1, ...] > 0
    ep_1 = ep_1 * (resp - ey_1 * micr[:, 1, ...])
    ee_1 = micr[:, 1, ...] * resp - ep_1  # elastic strain phase 1

    ep_t = ep_0 + ep_1  # plastic strain for both phases
    ee_t = ee_0 + ee_1  # elastic strain for both phases

    # calculate the FIP
    FIP_0 = ep_0 * (micr[:, 0, ...] + K * ((E_0 * ee_0) / y_0))
    FIP_1 = ep_1 * (micr[:, 1, ...] + K * ((E_1 * ee_1) / y_1))
    FIP_t = FIP_0 + FIP_1

    # MKS results

    ep_0_mks = micr[:, 0, ...] * mks_R - ey_0 * micr[:, 0, ...] > 0
    ep_0_mks = ep_0_mks * (mks_R - ey_0 * micr[:, 0, ...])
    ee_0_mks = micr[:, 0, ...] * mks_R - ep_0  # elastic strain phase 0

    # plastic strain phase 1
    ep_1_mks = micr[:, 1, ...] * mks_R - ey_1 * micr[:, 1, ...] > 0
    ep_1_mks = ep_1_mks * (mks_R - ey_1 * micr[:, 1, ...])
    ee_1_mks = micr[:, 1, ...] * mks_R - ep_1  # elastic strain phase 1

    ep_t_mks = ep_0_mks + ep_1_mks  # plastic strain for both phases
    ee_t_mks = ee_0_mks + ee_1_mks  # elastic strain for both phases

# CALCULATE ERROR IN PLASTIC STRAIN PREDICTION

    avgr_fe_tot = 0
    max_diff_all = np.zeros(ns)

    for sn in xrange(ns):
        avgr_fe_indv = np.average(ep_t[sn, ...])

        avgr_fe_tot += avgr_fe_indv
        max_diff_all[sn] = np.amax(abs(ep_t[sn, ...]-ep_t_mks[sn, ...]))

    avgr_fe = avgr_fe_tot/ns

    # difference measure
    # mean_diff_meas = np.mean(abs(ep_t-ep_t_mks))/avgr_fe
    # mean_max_diff_meas = np.mean(max_diff_all)/avgr_fe
    # max_diff_meas_all = np.amax(abs(ep_t-ep_t_mks))/avgr_fe

    mean_diff_meas = np.mean(abs(ep_t-ep_t_mks))/0.000125
    mean_max_diff_meas = np.mean(max_diff_all)/0.000125
    max_diff_meas_all = np.amax(abs(ep_t-ep_t_mks))/0.000125

    msg = 'Mean plastic strain:, %s%%' % avgr_fe
    rr.WP(msg, wrt_file)

    msg = 'Mean voxel difference over all microstructures'\
        ' (normalized by mean strain), %s%sp: %s%%' \
        % (typ, real_comp, mean_diff_meas*100)
    rr.WP(msg, wrt_file)

    msg = 'Average Maximum voxel difference per microstructure'\
        ' (normalized by mean strain), %s%sp: %s%%' \
        % (typ, real_comp, mean_max_diff_meas*100)
    rr.WP(msg, wrt_file)

    msg = 'Maximum voxel difference in all microstructures '\
        '(normalized by mean strain), %s%sp: %s%%' \
        % (typ, real_comp, max_diff_meas_all*100)
    rr.WP(msg, wrt_file)

    # PLOT THE STRAIN FIELDS

    # find indices of max error and use them for plotting
    maxindx = np.unravel_index(np.argmax(np.abs(ep_t - ep_t_mks)), ep_t.shape)
    slc = maxindx[1]
    sn = maxindx[0]

    # choose indices for plotting
    # slc = 10
    # sn = 100

    # Plot slices of the response
    plt.figure(num=3, figsize=[11, 8])

    dmin = np.min([mks_R[sn, slc, :, :], resp[sn, slc, :, :]])
    dmax = np.max([mks_R[sn, slc, :, :], resp[sn, slc, :, :]])

    plt.subplot(221)
    ax = plt.imshow(micr[sn, 0, slc, :, :], origin='lower',
                    interpolation='none', cmap='jet')
    plt.colorbar(ax)
    plt.title('phase map, slice %s' % (slc))

    plt.subplot(222)
    ax = plt.imshow(resp[sn, slc, :, :], origin='lower',
                    interpolation='none', cmap='jet', vmin=dmin, vmax=dmax)
    plt.colorbar(ax)
    plt.title('FEM $\%s_{%s}$ response, slice %s' % ('epsilon', '11', slc))

    dmin = np.min([ep_t[sn, slc, :, :], ep_t_mks[sn, slc, :, :]])
    dmax = np.max([ep_t[sn, slc, :, :], ep_t_mks[sn, slc, :, :]])

    plt.subplot(223)
    ax = plt.imshow(ep_t[sn, slc, :, :], origin='lower',
                    interpolation='none', cmap='jet', vmin=dmin, vmax=dmax)
    plt.colorbar(ax)
    plt.title('FEM $\%s_{%s}^p$ response, slice %s' % ('epsilon', '11', slc))

    plt.subplot(224)
    ax = plt.imshow(ep_t_mks[sn, slc, :, :], origin='lower',
                    interpolation='none', cmap='jet', vmin=dmin, vmax=dmax)
    plt.colorbar(ax)
    plt.title('MKS $\%s_{%s}^p$ response, slice %s' % ('epsilon', '11', slc))

    # plt.show()

    # PLOT PLASTIC STRAIN DISTRIBUTIONS
    # (only plot distributions for soft phase)

    plt.figure(num=4, figsize=[10, 7])

    # find the min and max of both datasets (in full)
    dmin = np.amin([ep_t, ep_t_mks])
    dmax = np.amax([ep_t, ep_t_mks])

    micr0 = micr[:, 0, ...].reshape(ns*el*el*el).astype(int)

    ep_t_lin = ep_t.reshape(ns*el*el*el)
    ep_t_mks_lin = ep_t_mks.reshape(ns*el*el*el)

    tmp = np.nonzero(micr0)
    fe = ep_t_lin[tmp]
    mks = ep_t_mks_lin[tmp]

    # select the desired number of bins in the histogram
    bn = 100

    # FEM histogram
    n, bins, patches = plt.hist(fe, bins=bn, histtype='step', hold=True,
                                range=(dmin, dmax), color='white')
    bincenters = 0.5*(bins[1:]+bins[:-1])
    fep, = plt.plot(bincenters, n, 'k', linestyle='-', lw=1.0)

    # MKS histogram
    n, bins, patches = plt.hist(mks, bins=bn, histtype='step', hold=True,
                                range=(dmin, dmax), color='white')
    mksp, = plt.plot(bincenters, n, 'b', linestyle='-', lw=1.0)

    plt.grid(True)

    plt.legend([fep, mksp], ["FE - compliant phase", "MKS - compliant phase"])

    plt.xlabel("$\%s_{%s}^p$" % ('epsilon', '11'))
    plt.ylabel("Frequency")
    plt.title("$\%s_{%s}^p$ Frequency Histogram, FE vs. MKS,"
              % ('epsilon', '11'))

    # PLOT VIOLIN PLOT FOR PLASTIC STRAIN BINS

    error = ((ep_t_lin - ep_t_mks_lin)/0.000125)*100

    sort_list = np.argsort(ep_t_lin)

    ep_sort = ep_t_lin[sort_list[np.round(0.999*len(error)):]]

    err_sort = error[sort_list[np.round(0.999*len(error)):]]

    # select the desired number of bins in the histogram
    bn = 10

    # number of error values per bin in the violin plot
    num_per_bin = np.floor(len(ep_sort)/bn)

    error_in_bin_list = []
    bin_labels = []

    for ii in xrange(bn):

        if ii != bn-1:
            error_in_bin = err_sort[ii*num_per_bin:(ii+1)*num_per_bin-1]
            ep_in_bin = ep_sort[ii*num_per_bin:(ii+1)*num_per_bin-1]
        else:
            error_in_bin = err_sort[ii*num_per_bin:]
            ep_in_bin = ep_sort[ii*num_per_bin:]

        print len(ep_in_bin)

        error_in_bin_list.append(error_in_bin)

        label_cur = str(np.round(100*ep_in_bin[0], 4)) + '% - ' + \
            str(np.round(100*ep_in_bin[-1], 4)) + '%'
        bin_labels.append(label_cur)

    plt.figure(num=5, figsize=[12, 7])

    ax = plt.subplot(111)

    x = np.arange(1, bn + 1)

    ax.violinplot(dataset=error_in_bin_list, showextrema=False,
                  showmedians=False, showmeans=False)

    ax.set_xticks(x)
    ax.set_xticklabels(bin_labels, rotation='vertical')

    plt.xlabel("bin centers, $\%s_{%s}$" % (typ, real_comp))
    plt.ylabel("%% error")
    plt.title("Error Histogram, $\%s_{%s}$" % (typ, real_comp))
    plt.grid(True)
    plt.tight_layout(pad=0.1)
    plt.ylim([1.25*np.min(err_sort), 1.25*np.max(err_sort)])

    plt.figure(num=6, figsize=[10, 7])

    # find the min and max of both datasets (in full)

    ep_t_l = ep_t.reshape(ns, el**3)*100
    ep_t_mks_l = ep_t_mks.reshape(ns, el**3)*100

    fe = np.max(ep_t_l, 1)
    mks = np.max(ep_t_mks_l, 1)

    dmin = np.amin([fe, mks])
    dmax = np.amax([fe, mks])

    # select the desired number of bins in the histogram
    bn = 25

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

    plt.xlabel("$\%s_{%s}^p$ %%" % ('epsilon', '11'))
    plt.ylabel("Frequency")
    plt.title("Maximum $\%s_{%s}^p$ per MVE, FE vs. MKS,"
              % ('epsilon', '11'))

    plt.show()
