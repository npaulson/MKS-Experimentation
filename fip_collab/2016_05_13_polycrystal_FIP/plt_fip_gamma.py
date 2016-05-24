# -*- coding: utf-8 -*-
import functions as rr
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
            stats = ss.gamma.fit(tail, a=s_f, floc=np.min(tail)*.999)
        else:
            stats = ss.gamma.fit(tail, fa=s_f)
        # x_old = np.linspace(np.min(tail), np.max(tail), 100)
        # x = np.log(x_old)
        cdf = (np.arange(len(tail)) + 1) / float(len(tail))
        pred_ys = ss.gamma.cdf(tail, *stats)
        # tail_log = np.log(tail)
        r2 = sm.r2_score(pred_ys, cdf)
        temp_stats = (len(tail),) + stats + (r2,)
        r2s.append(r2)
        diff_stats.append(temp_stats)

    if r2s[0] > r2s[1]:
        return diff_stats[0][1:4]

    return diff_stats[1][1:4]


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

    print gamma_stats

    """plot the original data and the fits"""

    plt.figure()

    plt.plot(np.log(x), y, 'b.', markersize=3)

    plt.plot(np.log(x), ss.gamma.cdf(x, gamma_stats[0], loc=gamma_stats[1],
             scale=gamma_stats[2]), 'r-', lw=2, label='gamma cdf')

    ymin = y.min()
    ymax = y.max()
    rng = ymax - ymin
    ymin += -0.1*rng
    ymax += 0.1*rng

    plt.ylim((ymin, ymax))

    plt.xlabel("ln(FIP)")
    plt.ylabel("CDF")

    plt.show()
