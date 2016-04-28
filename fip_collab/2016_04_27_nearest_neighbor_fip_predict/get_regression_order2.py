import numpy as np
import functions as rr
import itertools as it
import h5py
import time


def regress(el, ns, H, ext, set_id, wrt_file):

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
    fip = f.get('fip_%s' % set_id)[...]
    fip = fip.reshape((n_samp))
    f.close()

    """calculate the indices for the regression bases"""

    xmax = 1+(H*cmax)+(H*(cmax**2))

    """calculate the X matrix"""

    X = np.zeros((n_samp, xmax), dtype='float64')

    c = 0  # keep track of position in X

    """for 0th order polynomial"""
    X[:, 0] = 1
    c += 1

    """for 1st order polynomial"""
    Imax = H*cmax
    Imat = np.unravel_index(np.arange(Imax), (H, cmax))
    Imat = np.array(Imat).T

    for I in xrange(Imax):
        h, pos = Imat[I, :]
        X[:, c] = neig[:, h, pos]
        c += 1

    """for 2nd order polynomial"""
    Imax = H*cmax*2
    Imat = np.unravel_index(np.arange(Imax), (H, cmax, cmax))
    Imat = np.array(Imat).T

    for I in xrange(Imax):
        h, pos1, pos2 = Imat[I, :]
        X[:, c] = neig[:, h, pos1]*neig[:, h, pos2]
        c += 1

    """calculate the XhX matrix"""

    XhX = np.zeros((xmax, xmax), dtype='float64')

    tmp = it.combinations_with_replacement(np.arange(xmax), 2)
    Imat = np.array(list(tmp))
    ImatL = Imat.shape[0]

    print "xmax: %s" % xmax
    print "ImatL: %s" % ImatL

    for I in xrange(ImatL):

        if np.mod(I, 100000) == 0:
            print I

        ii, jj = Imat[I, :]

        dotvec = np.dot(X[:, ii], X[:, jj])

        if ii == jj:
            XhX[ii, ii] = dotvec
        else:
            XhX[ii, jj] = dotvec
            XhX[jj, ii] = dotvec

    print "shape(XhX): %s" % str(XhX.shape)

    rank = np.linalg.matrix_rank(XhX)
    if rank != xmax:
        print "WARNING: XhX is rank deficient"
        print "xmax: %s" % xmax
        print "rank(XhX): %s" % rank

    """calculate XhY"""

    XhY = np.zeros(xmax, dtype='float64')

    for ii in xrange(xmax):
        XhY[ii] = np.dot(X[:, ii], fip)

    """perform the regression"""
    coef = np.linalg.lstsq(XhX, XhY)[0]

    f = h5py.File("regress_results.hdf5", 'w')
    f.create_dataset('coef', data=coef)
    f.close()

    timeE = np.round(time.time()-st, 1)
    msg = "regressions completed: %s s" % timeE
    rr.WP(msg, wrt_file)


if __name__ == '__main__':
    el = 21
    ns = 2
    H = 9
    ext = 3
    set_id = "cal"
    wrt_file = "test.txt"

    regress(el, ns, H, ext, set_id, wrt_file)
