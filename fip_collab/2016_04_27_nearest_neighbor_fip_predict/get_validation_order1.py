import numpy as np
import functions as rr
import matplotlib.pyplot as plt
import h5py
import time


def validate(el, ns, H, ext, set_id, wrt_file):

    st = time.time()

    """initialize important variables"""
    cmax = ext**3
    n_samp = ns*el**3  # number of data points for regression

    """gather the independent variable data"""
    f = h5py.File("spatial.hdf5", 'r')
    neig = f.get('neig_%s' % set_id)[...]
    neig = neig.reshape((n_samp, H, cmax))
    f.close()

    """gather the dependent variable data"""
    f = h5py.File("responses.hdf5", 'r')
    r_sim = f.get('fip_%s' % set_id)[...]
    r_sim = r_sim.reshape((n_samp))
    f.close()

    """retrieve the coefficient set from the regression"""
    f = h5py.File("regress_results.hdf5", 'r')
    coef = f.get('coef')[...]
    f.close()

    """calculate the indices for the regression bases"""

    xmax = 1+H*cmax  # I am only including the 0th and 1st degree polynomials

    """calculate the X matrix"""

    X = np.zeros((n_samp, xmax), dtype='float64')

    X[:, 0] = 1  # explicitly include the 0th degree polynomial vector

    c = 1
    for h in xrange(H):
        for pos in xrange(cmax):
            X[:, c] = neig[:, h, pos]
            c += 1

    """evalute the fit response"""
    r_fit = np.dot(coef, X.T)

    """evalute error metrics"""
    err = np.abs(r_sim-r_fit)
    err_mean = err.mean()
    err_max = err.max()

    r_sim_mmm = np.array([r_sim.min(), r_sim.mean(), r_sim.max()])
    r_fit_mmm = np.array([r_fit.min(), r_fit.mean(), r_fit.max()])

    print "r_sim min, mean and max: %s" % str(r_sim_mmm)
    print "r_fit min, mean and max: %s" % str(r_fit_mmm)

    print "mean error: %s" % err_mean
    print "max error: %s" % err_max

    # print "r_sim min: %s" % r_sim.min()
    # print "r_fit min: %s" % r_fit.min()
    # print "r_sim mean: %s" % r_sim.mean()
    # print "r_fit mean: %s" % r_fit.mean()
    # print "r_sim max: %s" % r_sim.max()
    # print "r_fit max: %s" % r_fit.max()

    timeE = np.round(time.time()-st, 1)
    msg = "validation completed for %s: %s s" % (set_id, timeE)
    rr.WP(msg, wrt_file)

    """plot the prediction equal to simulation line"""
    plt.figure(num=1, figsize=[10, 7])

    minval = np.min([r_sim, r_fit])
    maxval = np.max([r_sim, r_fit])

    valrange = maxval-minval
    minval += -0.5*valrange
    maxval += 0.5*valrange
    line = np.array([minval, maxval])

    plt.plot(line, line, 'k-')

    plt.plot(r_sim, r_fit,
             marker='o', markersize=7, color=[.7, .1, .2],
             linestyle='', label=set_id)

    plt.title("predicted versus simulated FIP")
    plt.xlabel("simulation")
    plt.ylabel("prediction")

    plt.xticks(rotation=20)
    plt.yticks(rotation=20)

    plt.show()

if __name__ == '__main__':
    el = 21
    ns = 2
    H = 9
    ext = 3
    set_id = "val"
    wrt_file = "test.txt"

    validate(el, ns, H, ext, set_id, wrt_file)
