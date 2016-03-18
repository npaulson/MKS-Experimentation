import time
import h5py
import numpy as np
import functions as rr


def rpha(shape):
    """return vector of same random euler angles"""
    return np.int8(2*np.random.random()*np.ones(shape))


def rand(el, ns, set_id, step, wrt_file):

    start = time.time()

    sshape = (ns, el, el, el)

    f = h5py.File("ref_%s%s_s%s.hdf5" % (ns, set_id, step), 'a')
    sves = f.create_dataset("sves", sshape, dtype='int8')
    M = f.create_dataset("M", sshape, dtype='complex64')

    tmp = np.int8(2*np.random.random(sshape))
    sves[...] = tmp
    M[...] = np.fft.fftn(tmp, axes=[1, 2, 3])

    f.close()

    end = time.time()
    timeE = np.round((end - start), 3)

    msg = "%s random SVEs generated: %ss" % (ns, timeE)
    rr.WP(msg, wrt_file)


def delta(el, ns, set_id, step, wrt_file):

    start = time.time()

    sshape = (2, el, el, el)

    f = h5py.File("ref_%s%s_s%s.hdf5" % (ns, set_id, step), 'a')
    sves = f.create_dataset("sves", sshape, dtype='int8')
    M = f.create_dataset("M", sshape, dtype='complex64')

    sves[0, ...] = np.zeros((el, el, el))
    sves[0, 10, 10, 10] = 1
    sves[1, ...] = np.ones((el, el, el))
    sves[1, 10, 10, 10] = 0

    M[...] = np.fft.fftn(sves[...], axes=[1, 2, 3])

    f.close()

    end = time.time()
    timeE = np.round((end - start), 3)

    msg = "%s delta SVEs generated: %ss" % (ns, timeE)
    rr.WP(msg, wrt_file)


def inclusion(el, ns, set_id, step, wrt_file):

    start = time.time()

    sshape = (ns, el, el, el)

    f = h5py.File("ref_%s%s_s%s.hdf5" % (ns, set_id, step), 'a')
    sves = f.create_dataset("sves", sshape, dtype='int8')
    M = f.create_dataset("M", sshape, dtype='complex64')

    for sn in xrange(ns):

        indx = np.random.random((el, el, el)) > np.random.rand()
        sves[sn, ...] = indx

    M[...] = np.fft.fftn(sves[...], axes=[1, 2, 3])

    f.close()

    end = time.time()
    timeE = np.round((end - start), 3)

    msg = "%s SVEs with inclusions generated: %ss" % (ns, timeE)
    rr.WP(msg, wrt_file)


def bicrystal(el, ns, set_id, step, wrt_file):

    start = time.time()

    sshape = (ns, el, el, el)

    f = h5py.File("ref_%s%s_s%s.hdf5" % (ns, set_id, step), 'a')
    sves = f.create_dataset("sves", sshape, dtype='int8')
    M = f.create_dataset("M", sshape, dtype='complex64')

    sves[...] = np.zeros(sshape)

    for sn in xrange(ns):

        direc = np.int8(3*np.random.rand())  # define a random direction
        vf = np.int8(20*np.random.rand())+1  # define a random volume fraction

        if direc == 0:
            sves[sn, :vf, :, :] = np.ones((vf, el, el))
        elif direc == 1:
            sves[sn, :, :vf, :] = np.ones((el, vf, el))
        elif direc == 2:
            sves[sn, :, :, :vf] = np.ones((el, el, vf))

    M[...] = np.fft.fftn(sves[...], axes=[1, 2, 3])

    f.close()

    end = time.time()
    timeE = np.round((end - start), 3)

    msg = "%s bicrystal SVEs generated: %ss" % (ns, timeE)
    rr.WP(msg, wrt_file)


if __name__ == '__main__':
    el = 21
    ns = 2
    set_id = 'test'
    step = 0
    wrt_file = 'test.txt'

    rand(el, ns, set_id, step, wrt_file)
