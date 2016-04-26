import numpy as np
import h5py
import sys
import functions as rr


def vtk_write_euler(el, euler, fname):

    nx_el, ny_el, nz_el = el, el, el
    nx_pt, ny_pt, nz_pt = el + 1, el + 1, el + 1

    no_el = nx_el * ny_el * nz_el
    dx, dy, dz = 0.02, 0.02, 0.02
    lx, ly, lz = dx*nx_el, dy*ny_el, dz*nz_el

    # Coordinates
    X = np.arange(0, lx+dx, dx)
    Y = np.arange(0, ly+dx, dy)
    Z = np.arange(0, lz+dx, dz)

    file_vtk = open(fname, 'w')

    rr.VTK_Header(file_vtk, 'MKS_results', nx_pt, ny_pt, nz_pt, X, Y,
                  Z, no_el)

    rr.VTK_Vector(file_vtk, 'Euler_phi1Phi0phi2', euler, nx_el)

    file_vtk.close()


def dist_complex(set1, set2):
    """
    compute the distance between all points in set 1 and
    all points in set 2 using euclidean distance.
    Do so for complex numbers
    """

    s1len = set1.shape[0]
    s2len = set2.shape[0]

    dist = np.zeros((s1len, s2len))

    for ii in xrange(s1len):
        for jj in xrange(s2len):

            tmp = set1[ii, :] - set2[jj, :]
            tmp = np.sqrt(np.sum(tmp.conj()*tmp))

            dist[ii, jj] = tmp.real

    return dist


def get_file(el, ns, set_id, PC_A, PC_B, PCvalA, PCvalB):

    f_red = h5py.File("sve_reduced.hdf5", 'r')
    f_eul = h5py.File("spatial_stats.hdf5", 'r')

    reducedA = f_red.get('reduced_%s' % set_id)[:, PC_A]
    reducedB = f_red.get('reduced_%s' % set_id)[:, PC_B]
    euler = f_eul.get('euler_%s' % set_id)[...]

    f_red.close()
    f_eul.close()

    """find the closest point to [PCvalA, PCvalB]"""

    print "guess: PCvalA=%s, PCvalB=%s" % (PCvalA, PCvalB)

    dist = dist_complex(np.array([PCvalA, PCvalB])[None, :],
                        np.vstack([reducedA, reducedB]).T)
    mindx = np.argmin(dist)

    print "mindx: %s" % mindx
    print dist

    print "closest: PCvalA=%s, PCvalB=%s" % (reducedA[mindx],
                                             reducedB[mindx])

    """get the euler angles associated with that point"""
    euler = euler[mindx, ...].swapaxes(0, 1)

    """create 3D coordinates associated with that point"""
    vec = np.arange(el)
    Y, X, Z = np.meshgrid(vec, vec, vec)
    X = X.reshape(X.size)
    Y = Y.reshape(Y.size)
    Z = Z.reshape(Z.size)

    """print this data to a file for use in MTEX to plot
    pole figures"""
    data = np.zeros((el**3, 6))
    data[:, :3] = euler
    data[:, 3] = X
    data[:, 4] = Y
    data[:, 5] = Z

    fname = "ebsd_%s_%s.txt" % (set_id, mindx)
    np.savetxt(fname, data)
    fname = "micr_%s_%s.vtk" % (set_id, mindx)
    vtk_write_euler(el, euler, fname)

if __name__ == '__main__':
    el = 21
    ns_cal = 20
    set_id_cal = sys.argv[1]
    PC_A = 0
    PC_B = 1
    PCvalA = np.float64(sys.argv[2])
    PCvalB = np.float64(sys.argv[3])

    get_file(el, ns_cal, set_id_cal, PC_A, PC_B, PCvalA, PCvalB)
