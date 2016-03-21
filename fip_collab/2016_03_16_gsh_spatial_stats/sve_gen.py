import time
import h5py
import numpy as np
import functions as rr
from scipy.spatial.distance import cdist


def reul(shape):
    """return vector of same random euler angles"""
    return 360*np.random.rand()*np.ones(shape)


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
        euler[sn, 0, :] = reul(el**3)
        euler[sn, 1, :] = reul(el**3)
        euler[sn, 2, :] = reul(el**3)
        euler[sn, :, 4630] = reul(3)

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
        euler[sn, 0, :] = reul(el**3)
        euler[sn, 1, :] = reul(el**3)
        euler[sn, 2, :] = reul(el**3)

        tmp = np.random.rand(el**3)

        for ii in xrange(n_phase):

            indx = (tmp > np.sum(vfrac[:ii]))*(tmp < np.sum(vfrac[:(ii+1)]))

            euler[sn, 0, indx] = reul(np.sum(indx))
            euler[sn, 1, indx] = reul(np.sum(indx))
            euler[sn, 2, indx] = reul(np.sum(indx))

            del indx

    f.close()

    end = time.time()
    timeE = np.round((end - start), 3)

    msg = "%s SVEs with inclusions generated with %s orientations: %ss" \
          % (ns, n_phase, timeE)
    rr.WP(msg, wrt_file)


def bicrystal(el, ns, set_id, step, wrt_file):

    start = time.time()

    sshape = (ns, 3, el**3)

    f = h5py.File("ref_%s%s_s%s.hdf5" % (ns, set_id, step), 'w')
    euler = f.create_dataset("euler", sshape, dtype='float64')

    gridvec = np.arange(el)
    gridx, gridy, gridz = np.meshgrid(gridvec, gridvec, gridvec)
    gridx = gridx.reshape(gridx.size)
    gridy = gridy.reshape(gridy.size)
    gridz = gridz.reshape(gridz.size)
    grid = np.vstack([gridx, gridy, gridz]).T

    for sn in xrange(ns):

        loc1 = np.zeros((1, 3))

        randi2 = np.int8(2*np.random.rand())
        randi6 = np.int8(6*np.random.rand())

        if randi6 == 0:
            loc1[0, 0] = 0
            loc1[0, 1] = np.int8(el*np.random.rand())
            loc1[0, 2] = np.int8(el*np.random.rand())
        elif randi6 == 1:
            loc1[0, 0] = el-1
            loc1[0, 1] = np.int8(el*np.random.rand())
            loc1[0, 2] = np.int8(el*np.random.rand())
        elif randi6 == 2:
            loc1[0, 0] = np.int8(el*np.random.rand())
            loc1[0, 1] = 0
            loc1[0, 2] = np.int8(el*np.random.rand())
        elif randi6 == 3:
            loc1[0, 0] = np.int8(el*np.random.rand())
            loc1[0, 1] = el-1
            loc1[0, 2] = np.int8(el*np.random.rand())
        elif randi6 == 4:
            loc1[0, 0] = np.int8(el*np.random.rand())
            loc1[0, 1] = np.int8(el*np.random.rand())
            loc1[0, 2] = 0
        elif randi6 == 5:
            loc1[0, 0] = np.int8(el*np.random.rand())
            loc1[0, 1] = np.int8(el*np.random.rand())
            loc1[0, 2] = el-1

        loc2 = np.int8(el*np.random.random((1, 3)))

        dist_loc1 = np.squeeze(cdist(grid, loc1))
        dist_loc2 = np.squeeze(cdist(grid, loc2))

        if randi2 == 0:
            dist_xgy = dist_loc1 >= dist_loc2
        if randi2 == 1:
            dist_xgy = dist_loc1 < dist_loc2

        dist_xgy = np.int8(dist_xgy)

        sve = np.zeros([3, el**3], dtype='int8')

        sve[0, dist_xgy == 0] = 360*np.random.rand()
        sve[1, dist_xgy == 0] = 360*np.random.rand()
        sve[2, dist_xgy == 0] = 360*np.random.rand()
        sve[0, dist_xgy == 1] = 360*np.random.rand()
        sve[1, dist_xgy == 1] = 360*np.random.rand()
        sve[2, dist_xgy == 1] = 360*np.random.rand()

        # print np.unique(sve)

        euler[sn, ...] = sve

    f.close()

    end = time.time()
    timeE = np.round((end - start), 3)

    msg = "%s bicrystal SVEs generated: %ss" % (ns, timeE)
    rr.WP(msg, wrt_file)


def bicrystal_orthog(el, ns, set_id, step, wrt_file):

    start = time.time()

    f = h5py.File("ref_%s%s_s%s.hdf5" % (ns, set_id, step), 'a')

    euler = np.zeros((ns, 3, el, el, el))

    for sn in xrange(ns):
        euler[sn, 0, ...] = reul((el, el, el))
        euler[sn, 1, ...] = reul((el, el, el))
        euler[sn, 2, ...] = reul((el, el, el))

        # define a random direction
        direc = np.int8(3*np.random.rand())
        # define a random volume fraction
        vf = np.int8(22*np.random.rand())

        if direc == 0:
            euler[sn, 0, :vf, :, :] = reul((vf, el, el))
            euler[sn, 1, :vf, :, :] = reul((vf, el, el))
            euler[sn, 2, :vf, :, :] = reul((vf, el, el))
        elif direc == 1:
            euler[sn, 0, :, :vf, :] = reul((el, vf, el))
            euler[sn, 1, :, :vf, :] = reul((el, vf, el))
            euler[sn, 2, :, :vf, :] = reul((el, vf, el))
        elif direc == 2:
            euler[sn, 0, :, :, :vf] = reul((el, el, vf))
            euler[sn, 1, :, :, :vf] = reul((el, el, vf))
            euler[sn, 2, :, :, :vf] = reul((el, el, vf))

    f.create_dataset('euler', data=euler.reshape(ns, 3, el**3))

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
