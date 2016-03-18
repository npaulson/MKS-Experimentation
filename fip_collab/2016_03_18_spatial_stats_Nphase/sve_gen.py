import time
import h5py
import numpy as np
import functions as rr


def bicrystal(el, ns, H, set_id, step, wrt_file):

    start = time.time()

    sshape = (ns, el, el, el)

    f = h5py.File("ref_%s%s_s%s.hdf5" % (ns, set_id, step), 'w')
    sves = f.create_dataset("sves", sshape, dtype='int64')

    for sn in xrange(ns):

        sves[sn, ...] = np.int64(H*np.random.rand())

        direc = np.int8(3*np.random.rand())  # define a random direction
        vf = np.int8(20*np.random.rand())+1  # define a random volume fraction

        if direc == 0:
            sves[sn, :vf, :, :] = np.int64(H*np.random.rand())
        elif direc == 1:
            sves[sn, :, :vf, :] = np.int64(H*np.random.rand())
        elif direc == 2:
            sves[sn, :, :, :vf] = np.int64(H*np.random.rand())

    f.close()

    end = time.time()
    timeE = np.round((end - start), 3)

    msg = "%s bicrystal SVEs generated: %ss" % (ns, timeE)
    rr.WP(msg, wrt_file)


def delta(el, ns, H, set_id, step, wrt_file):

    start = time.time()

    sshape = (ns, el, el, el)

    f = h5py.File("ref_%s%s_s%s.hdf5" % (ns, set_id, step), 'w')
    sves = f.create_dataset("sves", sshape, dtype='int64')

    for sn in xrange(ns):
        sves[sn, ...] = np.int64(H*np.random.rand())
        sves[sn, 10, 10, 10] = np.int64(H*np.random.rand())

    f.close()

    end = time.time()
    timeE = np.round((end - start), 3)

    msg = "%s delta SVEs generated: %ss" % (ns, timeE)
    rr.WP(msg, wrt_file)


def inclusion(el, ns, H, set_id, step, wrt_file, vfrac):

    start = time.time()

    sshape = (ns, el, el, el)
    n_phase = len(vfrac)

    f = h5py.File("ref_%s%s_s%s.hdf5" % (ns, set_id, step), 'w')
    sves = f.create_dataset("sves", sshape, dtype='int64')

    for sn in xrange(ns):
        svetmp = np.int64(H*np.random.rand()*np.ones(el**3))

        tmp = np.random.rand(el**3)

        for ii in xrange(n_phase):

            indx = (tmp > np.sum(vfrac[:ii]))*(tmp < np.sum(vfrac[:(ii+1)]))
            svetmp[indx] = np.int64(H*np.random.rand())

        sves[sn, ...] = svetmp.reshape(el, el, el)

    f.close()

    end = time.time()
    timeE = np.round((end - start), 3)

    msg = "%s SVEs with inclusions generated: %ss" % (ns, timeE)
    rr.WP(msg, wrt_file)


def inclusion_red(el, ns, H, set_id, step, wrt_file, vfrac):
    """this code generates inclusions in a matrix of the H=0 material
    based on a user supplied vector of inclusion volume fractions.
    These volume fractions are perturbed such as to blur the distinction
    between the SVE distributions"""

    start = time.time()

    sshape = (ns, el, el, el)

    vfrac = np.array(vfrac)
    n_phase = len(vfrac)

    f = h5py.File("ref_%s%s_s%s.hdf5" % (ns, set_id, step), 'w')
    sves = f.create_dataset("sves", sshape, dtype='int64')

    for sn in xrange(ns):

        # perturb vfrac to make things less defined
        delta = 0.015*(2*(np.random.random(n_phase))-1)
        vfrac_ = vfrac + delta

        if np.any(vfrac_ < 0):
            print "negative volume fraction detected!!!"

        svetmp = np.zeros(el**3)

        tmp = np.random.rand(el**3)

        for ii in xrange(n_phase):

            indx = (tmp > np.sum(vfrac_[:ii]))*(tmp < np.sum(vfrac_[:(ii+1)]))
            svetmp[indx] = ii+1

        sves[sn, ...] = svetmp.reshape(el, el, el)

    f.close()

    end = time.time()
    timeE = np.round((end - start), 3)

    msg = "%s SVEs with inclusions generated: %ss" % (ns, timeE)
    rr.WP(msg, wrt_file)


def rod(el, ns, H, set_id, step, wrt_file, raxis):

    start = time.time()

    sshape = (ns, el, el, el)

    f = h5py.File("ref_%s%s_s%s.hdf5" % (ns, set_id, step), 'w')
    sves = f.create_dataset("sves", sshape, dtype='int64')

    cmat = np.unravel_index(np.arange(el**2), [el, el])
    cmat = np.array(cmat).T

    for c in xrange(el**2):
        ii, jj = cmat[c, :]

        if raxis == 0:
            sves[:, :, ii, jj] = np.int64(H*np.random.rand())
        elif raxis == 1:
            sves[:, ii, :, jj] = np.int64(H*np.random.rand())
        elif raxis == 2:
            sves[:, ii, jj, :] = np.int64(H*np.random.rand())

    f.close()

    end = time.time()
    timeE = np.round((end - start), 3)

    msg = "%s SVEs with inclusions generated: %ss" % (ns, timeE)
    rr.WP(msg, wrt_file)


if __name__ == '__main__':
    el = 21
    ns = 2
    H = 5
    set_id = 'test'
    step = 0
    wrt_file = 'test.txt'

    delta(el, ns, H, set_id, step, wrt_file)
