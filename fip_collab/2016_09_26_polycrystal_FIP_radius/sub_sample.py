import numpy as np
import functions as rr
from constants import const
import scipy.stats as ss
import sklearn.metrics as sm
from sklearn.decomposition import PCA
import h5py
import time


def fit_gamma_robust(tail):
    s_f = 0.8

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

    start = time.time()

    f1 = h5py.File("raw_responses.hdf5", 'r')
    allfip = f1.get('fip_%s' % sid)[...]
    f1.close()

    f_red = h5py.File("spatial_reduced_L%s.hdf5" % C['H'], 'r')
    reduced = f_red.get('reduced_%s' % sid)[...]
    f_red.close()

    """perform PCA on the SVE cluster to identify its extreme boundaries"""

    pca = PCA()
    pca.fit(reduced)
    reduced_ = pca.transform(reduced)

    """pick points at the maximum and minimum extremes of the SVE cluster
    for each PC up to the specified level"""

    f2 = h5py.File("sample_L%s.hdf5" % C['H'], 'a')

    mu = np.zeros((2*C['n_pc_samp'],))
    sigma = np.zeros((2*C['n_pc_samp'],))
    r2 = np.zeros((2*C['n_pc_samp'],))
    samp = np.zeros((2*C['n_pc_samp'], C['n_samp'], C['n_pc_tot']))

    for pc in xrange(C['n_pc_samp']):

        """find the index of the minimum cluster bound
        in the new PC space"""
        I_seed1 = np.argmin(reduced_[:, pc])
        """find the index of the maximum cluster bound
        in the new PC space"""
        I_seed2 = np.argmax(reduced_[:, pc])

        """get seed1 in the original PC space"""
        seed1 = reduced[I_seed1, :]
        """get seed2 in the original PC space"""
        seed2 = reduced[I_seed2, :]

        """find the closest n_samp points to seed1"""
        dist = np.zeros((ns,))
        for ii in xrange(ns):
            point = reduced[ii, :]
            dist[ii] = np.sqrt(np.sum((seed1-point)**2))
            # dist[ii] = np.sqrt(np.sum((seed1[:2]-point[:2])**2))

        I_sort = np.argsort(dist)
        samp1 = reduced[I_sort[:C['n_samp']], :]
        fip1 = allfip[I_sort[:C['n_samp']], :]

        """find the closest n_samp points to seed2"""
        dist = np.zeros((ns,))
        for ii in xrange(ns):
            point = reduced[ii, :]
            dist[ii] = np.sqrt(np.sum((seed2-point)**2))
            # dist[ii] = np.sqrt(np.sum((seed2[:2]-point[:2])**2))

        I_sort = np.argsort(dist)
        samp2 = reduced[I_sort[:C['n_samp']], :]
        fip2 = allfip[I_sort[:C['n_samp']], :]

        """find the fip evd and parameters for samp1"""
        evd_1, mu_1, sigma_1, r2_1 = resp(fip1, C['n_samp'])

        """find the fip evd and parameters for samp2"""
        evd_2, mu_2, sigma_2, r2_2 = resp(fip2, C['n_samp'])

        """write to the data summary file"""
        mu[2*pc] = mu_1
        mu[2*pc+1] = mu_2
        sigma[2*pc] = sigma_1
        sigma[2*pc+1] = sigma_2
        r2[2*pc] = r2_1
        r2[2*pc+1] = r2_2
        samp[2*pc, ...] = samp1
        samp[2*pc+1, ...] = samp2
        f2.create_dataset('evd_pc%s_%s' % (str(2*pc), sid),
                          data=evd_1)
        f2.create_dataset('evd_pc%s_%s' % (str(2*pc+1), sid),
                          data=evd_2)

    f2.create_dataset('mu_%s' % sid, data=np.log(mu))
    f2.create_dataset('sigma_%s' % sid, data=np.log(sigma))
    f2.create_dataset('r2_%s' % sid, data=r2)
    f2.create_dataset('samp_%s' % sid, data=samp)

    f2.close()

    end = time.time()
    timeE = np.round((end - start), 3)

    msg = 'samples extracted for %s: %s seconds' \
          % (sid, timeE)
    rr.WP(msg, C['wrt_file'])


if __name__ == '__main__':
    C = const()
    ns = C['ns'][0]
    sid = C['sid'][0]

    f2 = h5py.File("sample.hdf5", 'w')
    f2.close()

    sample(ns, sid)

    # f_red = h5py.File("spatial_reduced_L%s.hdf5" % C['H'], 'r')
    # reduced = f_red.get('reduced_%s' % sid)[...]
    # f_red.close()

    # f2 = h5py.File("sample.hdf5", 'a')
    # samp = f2.get('samp_%s' % sid)[...]

    # pcA = 0
    # pcB = 1
    # pcC = 2
    # pc_sampA = 0
    # pc_sampB = 1

    # import matplotlib.pyplot as plt
    # from mpl_toolkits.mplot3d import Axes3D

    # """plot the selection of samples in the cluster in 2 and 3d"""

    # plt.figure(1)
    # plt.plot(reduced[:, pcA], reduced[:, pcB],
    #          marker='o', markersize=5, color='b',
    #          linestyle='', alpha=.2)

    # plt.plot(samp[pc_sampA, :, pcA], samp[pc_sampA, :, pcB],
    #          marker='o', markersize=5, color='r',
    #          linestyle='', alpha=.3)

    # tmp = np.mean(samp, 1)
    # plt.plot(tmp[pc_sampA, pcA], tmp[pc_sampA, pcB],
    #          marker='o', markersize=8, color='r',
    #          linestyle='', alpha=.99)

    # plt.margins(.2)

    # fig = plt.figure(2)
    # ax = fig.add_subplot(111, projection='3d')

    # ax.scatter(reduced[:, pcA], reduced[:, pcB], reduced[:, pcC],
    #            c='b', marker='o', s=40, alpha=.3)
    # ax.scatter(samp[pc_sampA, :, pcA], samp[pc_sampA, :, pcB], samp[pc_sampA, :, pcC],
    #            c='r', marker='o', s=40, alpha=.3)

    # plt.margins(.2)

    # plt.figure(3)

    # mu = f2.get('mu_%s' % sid)[...]
    # sigma = f2.get('sigma_%s' % sid)[...]
    # evdA = f2.get('evd_pc%s_%s' % (pc_sampA, sid))[...]
    # evdB = f2.get('evd_pc%s_%s' % (pc_sampB, sid))[...]
    # f2.close()

    # y = (np.arange(evdA.size)+1)/np.float32(evdA.size)
    # plt.plot(np.log(evdA), y, '-', color='r',
    #          label=sid)

    # y = ss.gamma.cdf(evdA, 0.8, loc=mu[pc_sampA], scale=sigma[pc_sampA])
    # plt.plot(np.log(evdA), y, '-', color='r',
    #          label=sid)

    # y = (np.arange(evdB.size)+1)/np.float32(evdB.size)
    # plt.plot(np.log(evdB), y, '-', color='b',
    #          label=sid)

    # y = ss.gamma.cdf(evdB, 0.8, loc=mu[pc_sampB], scale=sigma[pc_sampB])
    # plt.plot(np.log(evdB), y, '-', color='b',
    #          label=sid)

    # plt.margins(.2)

    # plt.show()
