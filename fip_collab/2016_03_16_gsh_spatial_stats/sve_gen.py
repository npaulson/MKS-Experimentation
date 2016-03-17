import time
import h5py
import numpy as np
import functions as rr


def rand(el, ns, set_id, step, wrt_file):

    start = time.time()

    f = h5py.File("ref_%s%s_s%s.hdf5" % (ns, set_id, step), 'a')
    euler = f.create_dataset("euler", (ns, 3, el**3), dtype='float64')
    euler[...] = np.random.rand(ns, 3, el**3)*360
    f.close()

    end = time.time()
    timeE = np.round((end - start), 3)

    msg = "%s random SVEs generated random orientations: %ss" % (ns, timeE)
    rr.WP(msg, wrt_file)


def delta(el, ns, set_id, step, wrt_file):

    start = time.time()

    f = h5py.File("ref_%s%s_s%s.hdf5" % (ns, set_id, step), 'a')
    euler = f.create_dataset("euler", (ns, 3, el**3), dtype='float64')

    for sn in xrange(ns):
        euler[sn, 0, :] = 360*np.random.rand()*np.ones((el**3,))
        euler[sn, 1, :] = 360*np.random.rand()*np.ones((el**3,))
        euler[sn, 2, :] = 360*np.random.rand()*np.ones((el**3,))
        euler[sn, :, 4630] = 360*np.random.rand(3)

    f.close()

    end = time.time()
    timeE = np.round((end - start), 3)

    msg = "%s delta SVEs generated random orientations: %ss" % (ns, timeE)
    rr.WP(msg, wrt_file)


def inclusion(el, ns, set_id, step, wrt_file, vfrac):

    start = time.time()

    n_phase = len(vfrac)

    f = h5py.File("ref_%s%s_s%s.hdf5" % (ns, set_id, step), 'a')
    euler = f.create_dataset("euler", (ns, 3, el**3), dtype='float64')

    for sn in xrange(ns):
        euler[sn, 0, :] = 360*np.random.rand()*np.ones((el**3,))
        euler[sn, 1, :] = 360*np.random.rand()*np.ones((el**3,))
        euler[sn, 2, :] = 360*np.random.rand()*np.ones((el**3,))

        tmp = np.random.rand(el**3)

        for ii in xrange(n_phase):

            indx = (tmp > np.sum(vfrac[:ii]))*(tmp < np.sum(vfrac[:(ii+1)]))

            euler[sn, 0, indx] = 360*np.random.rand()*np.ones((np.sum(indx)))
            euler[sn, 1, indx] = 360*np.random.rand()*np.ones((np.sum(indx)))
            euler[sn, 2, indx] = 360*np.random.rand()*np.ones((np.sum(indx)))

            del indx

    f.close()

    end = time.time()
    timeE = np.round((end - start), 3)

    msg = "%s SVEs with inclusions generated with %s orientations: %ss" \
          % (ns, n_phase, timeE)
    rr.WP(msg, wrt_file)


if __name__ == '__main__':
    el = 21
    ns = 2
    set_id = 'test'
    step = 0
    wrt_file = 'test.txt'

    rand(el, ns, set_id, step, wrt_file)
