import numpy as np
import h5py
import sys
from constants import const
from shutil import copyfile
import functions as rr
import os


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


def get_file(name, PC_A, PC_B, H, PCvalA, PCvalB):

    C = const()

    f_red = h5py.File("spatial_reduced_L%s.hdf5" % H, 'r')
    f_eul = h5py.File("spatial_L%s.hdf5" % H, 'r')

    set_id = name + '_val'
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

    print dist

    print "closest: PCvalA=%s, PCvalB=%s" % (reducedA[mindx],
                                             reducedB[mindx])

    """get the euler angles associated with that point"""
    euler = euler[mindx, ...].swapaxes(0, 1)

    """create 3D coordinates associated with that point"""
    vec = np.arange(C['el'])
    Y, X, Z = np.meshgrid(vec, vec, vec)
    X = X.reshape(X.size)
    Y = Y.reshape(Y.size)
    Z = Z.reshape(Z.size)

    """print this data to a file for use in MTEX to plot
    pole figures"""
    data = np.zeros((C['el']**3, 6))
    data[:, :3] = euler
    data[:, 3] = X
    data[:, 4] = Y
    data[:, 5] = Z

    fname = "ebsd_%s_%s.txt" % (name, mindx)
    np.savetxt(fname, data)

    """copy a version of the vtk file to extract field images"""
    owd = os.getcwd()
    nwd = os.getcwd() + '/' + name
    os.chdir(nwd)

    sn = mindx+1
    tmp = "Ti64_Dream3D_v01_Output_%s.vtk" % sn
    f1 = nwd + '/' + tmp
    tmp = "micr_%s_%s.vtk" % (name, mindx)
    f2 = owd + '/' + tmp
    copyfile(f1, f2)

    os.chdir('..')


if __name__ == '__main__':
    PC_A = 0
    PC_B = 1
    H = 15

    name = sys.argv[1]
    PCvalA = np.int64(sys.argv[2])
    PCvalB = np.int64(sys.argv[3])

    get_file(name, PC_A, PC_B, H, PCvalA, PCvalB)
