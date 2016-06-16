# -*- coding: utf-8 -*-
import functions_alt as rr
import numpy as np
import os
import matplotlib.pyplot as plt
import scipy.stats as ss
import sklearn.metrics as sm


def fit_gamma_robust(tail):
    r2s = []
    diff_stats = []
    s_f = 0.8

    for j in range(2):
        if j == 0:
            # fix the start location (mu_g) slightly  left of the
            # lowest tail value. Provide a guess for the shape (alpha)
            # at s_f

            # original fit 0
            stats = ss.gamma.fit(tail, a=s_f, floc=np.min(tail)*.999)
        else:
            # fix the shape as s_f

            # # original fit 1
            # stats = ss.gamma.fit(tail, fa=s_f)  # original fit 1

            # alternate fit 1
            stats = ss.gamma.fit(tail)

        # add fitting parameters to list for particular j
        diff_stats.append(stats)

        # calculate the r**2 for the CDF fit
        cdf = (np.arange(len(tail)) + 1) / float(len(tail))
        pred_ys = ss.gamma.cdf(tail, *stats)
        r2 = sm.r2_score(pred_ys, cdf)

        # add r2 to list for particular j
        r2s.append(r2)

        print "fit #%s" % j
        print "fitting parameters: %s" % str(stats)
        print "r**2 for fit: %s" % r2

    # if the first set of parameters has a greater r**2 return them
    if r2s[0] > r2s[1]:
        return diff_stats[0][:3]

    # otherwise return the second set of parameters
    return diff_stats[1][:3]


if __name__ == '__main__':

    newdir = 'cal'
    pcnt = .995

    # nwd = os.getcwd() + '\\' + newdir
    nwd = os.getcwd() + '/' + newdir  # for unix
    os.chdir(nwd)

    for filename in os.listdir(nwd):
        fip = rr.read_vtk_scalar(filename=filename)

    fip = np.sort(fip)

    """return to the original directory"""
    os.chdir('..')

    """get the data for the fit"""

    x = fip
    x = x[np.int64(pcnt*x.size):, None]

    # y = (np.arange(fip.size)+1)/np.float32(fip.size)
    # y = y[np.int64(pcnt*y.size):, None]

    y = (np.arange(x.size)+1)/np.float32(x.size)

    """get the desired fits"""
    gamma_stats = fit_gamma_robust(x)

    """plot the original data and the fits"""

    plt.figure()

    plt.plot(np.log(x), y, 'b.', markersize=3)

    shape = gamma_stats[0]
    # shape = .9
    # loc = gamma_stats[1]
    loc = np.exp(-14)
    # scale = gamma_stats[2]
    scale = np.exp(-14.1)

    x_ = np.linspace(x.min(), x.max(), 1000)

    plt.plot(np.log(x_), ss.gamma.cdf(x_, shape, loc=loc,
             scale=scale), 'r-', lw=2, label='gamma cdf')

    ymin = y.min()
    ymax = y.max()
    rng = ymax - ymin
    ymin += -0.1*rng
    ymax += 0.1*rng

    plt.ylim((ymin, ymax))

    plt.xlabel("ln(FIP)")
    plt.ylabel("CDF")

    plt.show()
