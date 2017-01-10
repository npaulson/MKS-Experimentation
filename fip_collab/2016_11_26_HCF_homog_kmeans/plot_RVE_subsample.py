import numpy as np
from constants import const
import scipy.stats as ss
import sklearn.metrics as sm
import h5py
import matplotlib.pyplot as plt
import random


def fit_gamma_robust(tail):
    s_f = 0.8

    # fit 4 (alternate)
    # stats = ss.gamma.fit(tail, fa=s_f, floc=np.min(tail)*.99999)

    stats = ss.gamma.fit(tail, fa=s_f)

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


def findRVE(one_v_two, n_samp):

    f = h5py.File("sample_rve.hdf5", 'r')

    if one_v_two == 1:
        fip = f.get('fip1')[...]
    else:
        fip = f.get('fip2')[...]

    f.close()

    mu = np.zeros((n_samp-10,))
    sigma = np.zeros((n_samp-10,))
    r2 = np.zeros((n_samp-10,))

    tmp = np.arange(n_samp)
    random.shuffle(tmp)

    for ii in xrange(10, n_samp):

        """find the fip evd and parameters for samp1"""
        evd, mu_, sigma_, r2_ = resp(fip[tmp[:ii], :], ii)

        print ii

        mu[ii-10] = mu_
        sigma[ii-10] = sigma_
        r2[ii-10] = r2_

    plt.figure(num=1, figsize=[9, 4])

    plt.subplot(131)

    plt.plot(np.arange(11, n_samp+1), np.log(mu), 'b.')
    plt.xlabel("number of SVEs")
    plt.ylabel("$log(\mu_g)$")
    plt.axis([10., n_samp, -18, -13])
    plt.grid(True)

    plt.subplot(132)

    plt.plot(np.arange(11, n_samp+1), np.log(sigma), 'b.')
    plt.xlabel("number of SVEs")
    plt.ylabel("$log(\sigma_g)$")
    plt.axis([10., n_samp, -18, -14])
    plt.grid(True)

    plt.subplot(133)

    plt.plot(np.arange(11, n_samp+1), r2, 'b.')
    plt.xlabel("number of SVEs")
    plt.ylabel("$r^2$")
    plt.axis([10., n_samp, 0.95, 1.0])
    plt.grid(True)

    plt.tight_layout()


if __name__ == '__main__':
    C = const()

    one_v_two = 1
    n_samp = 100

    findRVE(one_v_two, n_samp)

    plt.show()
