import numpy as np
import functions as rr
from constants import const
from sklearn.preprocessing import PolynomialFeatures
import h5py
import time


def features(ns, set_id):

    st = time.time()

    C = const()

    """gather the independent variable data"""
    f = h5py.File("spatial.hdf5", 'r')
    neig = f.get('neig_%s' % set_id)[...]
    neig = neig.reshape((ns*C['el']**3, C['H'], C['cmax']))
    f.close()

    """calculate the X matrix"""

    poly = PolynomialFeatures(degree=2)

    X1 = neig[:, 0, :]
    X2 = neig[:, 1, :]

    print "X1.shape: %s" % str(X1.shape)

    X1 = poly.fit_transform(X1)
    X2 = poly.fit_transform(X2)

    print "X1.shape: %s" % str(X1.shape)

    X = np.hstack([X1, X2])

    print "X.shape: %s:" % str(X.shape)

    # X = np.zeros((C['n_samp'], C['xmax']), dtype='float64')

    # c = 0  # keep track of position in X

    # """for 0th order polynomial"""
    # X[:, 0] = 1
    # c += 1

    # """for 1st order polynomial"""
    # Imax = C['H']*C['cmax']
    # Imat = np.unravel_index(np.arange(Imax), (C['H'], C['cmax']))
    # Imat = np.array(Imat).T

    # for I in xrange(Imax):
    #     h, pos = Imat[I, :]
    #     X[:, c] = neig[:, h, pos]
    #     c += 1

    # """for 2nd order polynomial"""
    # Imax = C['H']*C['cmax']**2
    # Imat = np.unravel_index(np.arange(Imax), (C['H'], C['cmax'], C['cmax']))
    # Imat = np.array(Imat).T

    # for I in xrange(Imax):
    #     h, pos1, pos2 = Imat[I, :]
    #     X[:, c] = neig[:, h, pos1]*neig[:, h, pos2]
    #     c += 1

    f = h5py.File("pre_regress_%s.hdf5" % set_id, 'w')
    f.create_dataset('X', data=X)
    f.close()

    timeE = np.round(time.time()-st, 1)
    msg = "features extracted for %s: %s s" % (set_id, timeE)
    rr.WP(msg, C['wrt_file'])


if __name__ == '__main__':
    ns = 2
    set_id = "cal"

    features(ns, set_id)
