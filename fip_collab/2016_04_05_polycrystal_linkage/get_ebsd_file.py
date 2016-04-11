import numpy as np
import h5py


def dist_complex(pt, set1):
    """
    compute the distance between point 1 and
    all points in set 2 using euclidean distance.
    Do so for complex numbers
    """

    slen = set1.shape[0]

    dist = np.zeros((slen))

    for ii in xrange(slen):
        tmp = pt - set1[ii]
        tmp = np.sqrt(np.sum(tmp.conj()*tmp))
        dist[ii] = tmp.real

    return dist


def get_file(el, ns, set_id, PCnum, Rval, Ival):

    f_red = h5py.File("sve_reduced.hdf5", 'r')
    f_eul = h5py.File("spatial_stats.hdf5", 'r')

    reduced = f_red.get('reduced_%s' % set_id)[:, PCnum]
    euler = f_eul.get('euler_%s' % set_id)[...]

    f_red.close()
    f_eul.close()

    """find the closest point to [Rval, Ival]"""

    print "guess: Rval=%s, Ival=%s" % (Rval, Ival)

    dist = dist_complex(Rval+1j*Ival, reduced)
    mindx = np.argmin(dist)

    print reduced
    print dist

    print "closest: Rval=%s, Ival=%s" % (reduced[mindx].real,
                                         reduced[mindx].imag)

    """get the euler angles associated with that point"""
    euler = euler[mindx, ...].swapaxes(0, 1)

    """create 3D coordinates associated with that point"""
    vec = np.arange(el)
    X, Y, Z = np.meshgrid(vec, vec, vec)
    X = X.reshape(X.size)
    Y = Y.reshape(Y.size)
    Z = Z.reshape(Z.size)

    """print this data to a file for use in MTEX to plot
    pole figures"""
    data = np.zeros((el**3, 6))
    data[:, :3] = euler
    data[:, 3] = X
    data[:, 3] = Y
    data[:, 3] = Z

    np.savetxt("ebsd_%s_%s.txt" % (set_id, mindx), data)


if __name__ == '__main__':
    el = 21
    ns_cal = 10
    set_id_cal = 'transverseD3D'
    PCnum = 0
    Rval = -50000
    Ival = 10000

    get_file(el, ns_cal, set_id_cal, PCnum, Rval, Ival)
