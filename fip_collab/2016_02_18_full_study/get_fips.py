import numpy as np
from numpy import linalg as LA
import h5py


def fip(sn, el, ns, set_id, step, typ, compl):

    f = h5py.File("ref_%s%s_s%s.hdf5" % (ns, set_id, step), 'r')

    print f.keys()

    euler = f.get('euler')[sn, ...].reshape(3, el**3)
    euler = euler.swapaxes(0, 1)

    et = np.zeros((el**3, 6))

    for ii in xrange(6):
        comp = compl[ii]
        tmp = f.get('r%s_%s' % (comp, typ))[sn, ...]
        print tmp.shape
        et[:, ii] = tmp.reshape(el**3)

    f.close()

    """ find the deviatoric strain tensor """
    et_ = np.zeros(et.shape)
    et_[:, 0:3] = et[:, 0:3] - (1./3.)*np.sum(et[:, 0:3], 1)

    print np.all(np.isclose(np.sum(et[:, 0:3]), np.zeros(el**3)))

    """ find the norm of the deviatoric strain tensor """
    en = np.sqrt(np.sum(et_[:, 0:3]**2+2*et_[:, 3:]**2, 1))

    """ normalize the deviatoric strain tensor """
    et_n = et_/en

    print np.all(np.isclose(np.sqrt(np.sum(et_n[:, 0:3]**2+2*et_n[:, 3:]**2, 1)), np.ones(el**3)))

    et_m = np.zeros((el**3, 3, 3))
    et_m[:, 0, 0] = et_n[:, 0]
    et_m[:, 1, 1] = et_n[:, 1]
    et_m[:, 2, 2] = et_n[:, 2]
    et_m[:, 0, 1] = et_n[:, 3]
    et_m[:, 1, 0] = et_n[:, 3]
    et_m[:, 0, 2] = et_n[:, 4]
    et_m[:, 2, 0] = et_n[:, 4]
    et_m[:, 1, 2] = et_n[:, 5]
    et_m[:, 2, 1] = et_n[:, 5]

    """ find the eigenvalues of the normalized tensor"""
    eigval, g_s2p = LA.eigh(et_m)

    print eigval.shape
    print g_s2p.shape

    print eigval[:5, :]

    # """ sort the principal strains in descending order """
    # indx = np.argsort(eigval)
    # indx = indx[::-1]
    # eigval = eigval[indx]

    """ find the deformation mode """
    theta = np.arccos(-np.sqrt(3./2.)*eigval[:, 2])

    print np.unique(theta)*(180./np.pi())


if __name__ == '__main__':
    sn = 10
    el = 21
    ns = 100
    set_id = 'val'
    step = 5
    typ = 'epsilon_t'
    compl = ['11', '22', '33', '12', '13', '23']

    fip(sn, el, ns, set_id, step, typ, compl)
