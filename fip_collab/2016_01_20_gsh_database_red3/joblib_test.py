import numpy as np
from joblib import Parallel, delayed
from joblib.pool import has_shareable_memory
import time


if __name__ == "__main__":

    n_s = np.int64(1E7)
    n_l = np.int64(10)

    a = np.random.rand(n_s)
    print "size of a: %sgb" % str(a.nbytes/(1E9))

    b = np.random.rand(n_s)

    st = time.time()

    c1 = np.zeros(n_l)
    for ii in xrange(n_l):
        c1[ii] = np.sum(a*b)

    print "standard dot product time: %ss" % str(time.time()-st)

    st = time.time()

    c2 = np.zeros(n_l)
    for ii in xrange(n_l):
        c2[ii] = np.dot(a, b)

    print "numpy dot product time: %ss" % str(time.time()-st)

    st = time.time()

    c3 = np.zeros(n_l)
    for ii in xrange(n_l):
        c3[ii] = np.inner(a, b)

    print "numpy inner product time: %ss" % str(time.time()-st)

    st = time.time()

    c4 = Parallel(n_jobs=2, max_nbytes=1e6)(
        delayed(has_shareable_memory)(np.inner(a, b))
        for ii in xrange(n_l))

    print "parallel numpy inner product time: %ss" % str(time.time()-st)

    print "equal results?: %s" % str(np.all(np.isclose(c4, c3)))
