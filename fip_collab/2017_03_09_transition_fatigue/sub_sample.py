import numpy as np
import functions as rr
from constants import const
import scipy.stats as ss
import sklearn.metrics as sm
from sklearn.decomposition import PCA
import h5py
import time
from scipy.stats import multivariate_normal as mnP
from numpy.random import multivariate_normal as mnR
from sklearn.neighbors.kde import KernelDensity


def fit_gamma_robust(tail):
    C = const()
    s_f = C['alpha']

    # fit 4 (alternate)
    stats = ss.gamma.fit(tail, fa=s_f, floc=np.min(tail)*.99999)

    # calculate the r**2 for the CDF fit
    cdf = (np.arange(len(tail)) + 1) / float(len(tail))
    pred_ys = ss.gamma.cdf(tail, *stats)
    r2 = sm.r2_score(pred_ys, cdf)

    # otherwise return the second set of parameters
    return stats, r2


def resp(fip_sample, ns):

    C = const()

    rawfip = fip_sample.reshape((ns*C['el']**3,))
    x = np.sort(rawfip)
    x = x[np.int64(C['pcnt']*x.size):, None]

    gamma_stats, r2 = fit_gamma_robust(x)

    mu = gamma_stats[1]
    sigma = gamma_stats[2]

    return x, mu, sigma, r2


def sample(ns, sid):

    C = const()

    np.random.seed(1)

    start = time.time()

    f1 = h5py.File("raw_responses.hdf5", 'r')
    allfip = f1.get('fip_%s' % sid)[...]
    f1.close()

    f_red = h5py.File("spatial_reduced_L%s.hdf5" % C['H'], 'r')
    reduced = f_red.get('reduced_%s' % sid)[...]
    f_red.close()

    f2 = h5py.File("sample_L%s.hdf5" % C['H'], 'a')

    mu = f2.create_dataset("mu_%s" % sid, (C['n_sc'],), dtype='float32')
    sigma = f2.create_dataset("sigma_%s" % sid, (C['n_sc'],), dtype='float32')
    r2 = f2.create_dataset("r2_%s" % sid, (C['n_sc'],), dtype='float32')
    samp = f2.create_dataset("samp_%s" % sid,
                             (C['n_sc'], C['n_samp'], C['n_pc_tot']),
                             dtype='float32')

    for sc in xrange(C['n_sc']):

        """extract indices of selected subsample"""
        indxv = select_sample(reduced)

        """extract the locations of the points and assocated responses
        for the subsample"""
        samp_ = reduced[indxv, :]
        fip_ = allfip[indxv, :]

        """find the fip evd and parameters for samp1"""
        evd_, mu_, sigma_, r2_ = resp(fip_, C['n_samp'])

        """write to the data summary file"""
        mu[sc] = np.log(mu_)
        sigma[sc] = np.log(sigma_)
        r2[sc] = r2_
        samp[sc, ...] = samp_
        f2.create_dataset('evd%s_%s' % (sc, sid),
                          data=evd_)

    f2.close()

    end = time.time()
    timeE = np.round((end - start), 3)

    msg = 'samples extracted for %s: %s seconds' \
          % (sid, timeE)
    rr.WP(msg, C['wrt_file'])


def select_sample(reduced):

    C = const()

    """perform PCA on the original point cloud to find the directions of
    maximum variance"""
    dof = 3
    pca = PCA(n_components=dof)
    Xorig = pca.fit_transform(reduced)

    """find the std. dev. of the original point cloud in each dimension
    the means are all zero due to the PCA algorithm"""
    sig = np.std(Xorig, 0)

    err = 100*np.ones((dof*2,))
    while np.any(err > 10):

        sel = Xorig
        indxv = np.arange(C['ncld'])

        """randomly select the mean and std. dev. of the new point cloud."""
        # mu_ = (2*np.random.rand(dof)-1)*sig
        # sig_ = 0.5*sig+0.5*np.random.rand(dof)*(sig-np.abs(mu_))

        # mu_ = (2*np.random.rand(dof)-1)*sig
        # sig_ = 0.5*sig + 0.8*np.random.rand(dof)*(sig-np.abs(mu_))

        mu_ = sig*np.random.uniform(-1, 1, size=(dof,))
        sig_ = sig*np.log(np.random.uniform(1000**.5, 1000, size=(dof,)))/np.log(1000)

        for ii in xrange(C['ncld']-C['n_samp']):

            """calculate the kernel bandwidth for KDE based on Silverman's
            rule of thumb"""
            bw = sel.std()*(0.25*indxv.size*(dof+2.))**(-1./(dof+4.))
            """randomize the bandwidth to avoid formation of patterns in
            selected points"""
            # bw = 0.1*bw
            bw = bw*np.random.uniform(0.1, 0.3)
            """train the KDE model with the selected points"""
            kde = KernelDensity(kernel='gaussian', bandwidth=bw).fit(sel)
            """obtain the estimated probability density at selected
            points"""
            Adens = np.exp(kde.score_samples(sel))
            """find the desired probability density at selected points"""
            target_d = mnP.pdf(sel, mean=mu_, cov=np.diag(sig_**2))
            """evaluate the error between the desired and actual probability
            densities at selected points"""
            err = Adens - target_d
            """remove point in sel closest to location of max positive error"""
            sel = np.delete(sel, np.argmax(err), axis=0)
            indxv = np.delete(indxv, np.argmax(err))

        des = np.concatenate((np.mean(sel, 0), np.std(sel, 0)))
        tru = np.concatenate((mu_, sig_))
        nor = np.concatenate((sig_, sig_))
        err = np.abs(tru-des)/nor

        # print sig
        # print tru
        # print des
        # print err

    # """plot the distribution of points in pc one versus the
    # associated normal distribution"""
    # import matplotlib.pyplot as plt
    # tmp = np.sort(Xorig[:, 0])
    # bw = sel.std()*(0.25*tmp.size*(dof+2.))**(-1./(dof+4.))
    # kde = KernelDensity(kernel='gaussian', bandwidth=0.5*bw).fit(tmp[:, None])
    # Adens = np.exp(kde.score_samples(tmp[:, None]))
    # plt.plot(tmp, Adens, 'b-')
    # plt.plot(tmp, ss.norm.pdf(tmp, loc=tmp.mean(), scale=tmp.std()), 'k-')
    # plt.show()

    # """plot the subclustering if desired"""
    # import matplotlib.pyplot as plt

    # plt.scatter(Xorig[:, 0], Xorig[:, 1],
    #             marker='o', s=20,
    #             color='k', linewidths=0.0, edgecolors=None, alpha=.3)

    # target = mnR(mean=mu_, cov=np.diag(sig_**2), size=C['n_samp'])
    # plt.scatter(target[:, 0], target[:, 1],
    #             marker='s', s=15,
    #             color='b', linewidths=0.0, edgecolors=None, alpha=.5)

    # plt.scatter(Xorig[indxv, 0], Xorig[indxv, 1],
    #             marker='x', s=40, c='r', edgecolors=None,
    #             linewidths=1.0, alpha=0.5,
    #             label='selected')

    # plt.axes().set_aspect('equal')
    # plt.tight_layout()
    # plt.show()

    return indxv


if __name__ == '__main__':
    C = const()
    setnum = 0
    ns = C['ns'][setnum]
    sid = C['sid'][setnum]

    f2 = h5py.File("sample_L%s.hdf5" % C['H'], 'w')
    f2.close()

    sample(ns, sid)
