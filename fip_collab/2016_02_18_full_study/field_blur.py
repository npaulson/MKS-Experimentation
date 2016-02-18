import numpy as np
import time
import itertools as it
import h5py


def blur(el, ns, set_id, step, typ, comp):

    st = time.time()

    f = h5py.File("ref_%s%s_s%s.hdf5" % (ns, set_id, step), 'a')
    r_fem = f.get('r%s_%s' % (comp, typ))[...]
    r_mks = f.get('rmks%s_%s' % (comp, typ))[...]

    r_fem_b = np.zeros(r_fem.shape)
    r_mks_b = np.zeros(r_mks.shape)

    trans = np.array(list(it.product([-1, 1, 0], repeat=3)))

    for t in xrange(trans.shape[0]):
        tmp = np.roll(r_fem, trans[t, 0], 1)
        tmp = np.roll(tmp, trans[t, 1], 2)
        tmp = np.roll(tmp, trans[t, 2], 3)

        r_fem_b += tmp

        tmp = np.roll(r_mks, trans[t, 0], 1)
        tmp = np.roll(tmp, trans[t, 1], 2)
        tmp = np.roll(tmp, trans[t, 2], 3)
        r_mks_b += tmp

    r_fem_b = r_fem_b / trans.shape[0]
    r_mks_b = r_mks_b / trans.shape[0]

    # save the blurred responses to an array
    f.create_dataset('rb%s_%s' % (comp, typ), data=r_fem_b)
    f.create_dataset('rmksb%s_%s' % (comp, typ), data=r_mks_b)

    # close HDF5 file
    f.close()

    print 'blur completed for %s%s, elapsed time: %ss' % \
          (typ, comp, np.round(time.time()-st, 3))

if __name__ == "__main__":

    compl = ['11', '22', '33', '12', '13', '23']

    for comp in compl:
        blur(21, 100, 'val', 1, 'epsilon_t', comp)
