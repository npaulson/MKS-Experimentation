import numpy as np
import tables as tb
import time
import itertools as it


def blur(el, ns, set_id, step, typ, comp):

    st = time.time()

    # open HDF5 file
    base = tb.open_file("ref_%s%s_s%s.h5" % (ns, set_id, step), mode="a")

    group = base.get_node('/%s' % typ, 'r%s' % comp)

    r_fem = group.r_fem[...]
    r_mks = group.r_mks[...]

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

    # save the blurred response from MKS to an array
    group = base.create_group('/%s_b' % typ,
                              'r%s' % comp,
                              'comp %s response fields' % comp)
    base.create_array(group, 'r_fem', r_fem_b)
    base.create_array(group, 'r_mks', r_mks_b)

    # close HDF5 file
    base.close()

    print 'blur completed for %s%s, elapsed time: %ss' % \
          (typ, comp, np.round(time.time()-st, 3))

if __name__ == "__main__":

    compl = ['11', '22', '33', '12', '13', '23']

    for comp in compl:
        blur(21, 100, 'val', 1, 'epsilon_p', comp)
