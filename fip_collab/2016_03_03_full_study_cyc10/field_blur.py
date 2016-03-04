import numpy as np
import time
import itertools as it
import h5py


def blur(el, ns, set_id, step, parID):

    st = time.time()

    f = h5py.File("fip_%s%s_s%s.hdf5" % (ns, set_id, step), 'a')

    parSET = f.get('%s' % parID)[...]
    print parSET.shape
    parSET = parSET.reshape(ns, el, el, el)

    parSET_b = np.zeros(parSET.shape)

    trans = np.array(list(it.product([-1, 1, 0], repeat=3)))

    for t in xrange(trans.shape[0]):
        tmp = np.roll(parSET, trans[t, 0], 1)
        tmp = np.roll(tmp, trans[t, 1], 2)
        tmp = np.roll(tmp, trans[t, 2], 3)

        parSET_b += tmp

    parSET_b = parSET_b / trans.shape[0]

    f.create_dataset('%sb' % parID, data=parSET_b)
    f.close()

    print 'blur completed, elapsed time: %ss' % \
          np.round(time.time()-st, 3)


if __name__ == "__main__":

    el = 21
    ns = 100
    set_id = 'val'
    step = 5
    parID = 'fip'

    blur(el, ns, set_id, step, parID)
