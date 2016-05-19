# -*- coding: utf-8 -*-
import functions as rr
import numpy as np
import os
import matplotlib.pyplot as plt
from sklearn.neighbors import KernelDensity


def hist_pdf(x, nbins, plotnum):

    fig, ax = plt.subplots(num=plotnum, figsize=[10, 7])

    # FEM histogram
    n1, bins, patches = ax.hist(x,
                                bins=nbins,
                                normed=True,
                                histtype='stepfilled',
                                fc=[0, 0, .5],
                                alpha=0.2)

    X_plot = np.linspace(x.min(), x.max(), 1000)[:, None]

    bw_silverman = ((4*np.std(x)**5)/(3*x.size))**(1./5.)
    kde = KernelDensity(kernel='gaussian', bandwidth=bw_silverman).fit(x[:, None])

    x_dens = np.exp(kde.score_samples(X_plot))

    xp, = ax.plot(X_plot[:, 0],
                  x_dens,
                  linewidth=2,
                  alpha=0.5,
                  color=[0., 0., 1.])

    plt.grid(True)

    ax.set_ylim(0, 1.5*x_dens.max())
    ax.set_xlabel("x")
    ax.set_ylabel("Relative Density")
    plt.title("Histogram and PDF for x")


if __name__ == '__main__':

    newdir = 'cal'
    n_pts = 43

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
    x = x[-1*n_pts:]
    # x = np.log(x)

    print "# points: %s" % x.size
    print "mean value: %s" % x.mean()
    print "mean + std: %s" % str(x.mean()+x.std())

    """get the histogram and PDF"""
    hist_pdf(x, 15, 0)

    plt.show()
