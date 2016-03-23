import numpy as np
from numpy import linalg as LA
import h5py
import functions as rr
import euler_func as ef
import matplotlib.pyplot as plt


def field_std(el, ns, traSET, newSET, slc, typecomp, plotnum):

    """Plot slices of the response"""
    plt.figure(num=plotnum, figsize=[9, 2.7])

    # dmin = np.min([newSET[slc, :, :], traSET[slc, :, :]])
    # dmax = np.max([newSET[slc, :, :], traSET[slc, :, :]])

    plt.subplot(121)
    ax = plt.imshow(newSET[slc, :, :], origin='lower',
                    interpolation='none', cmap='jet')  # , vmin=dmin, vmax=dmax)
    plt.colorbar(ax)
    plt.title('New Approach, %s, slice %s' % (typecomp, slc))

    plt.subplot(122)
    ax = plt.imshow(traSET[slc, :, :], origin='lower',
                    interpolation='none', cmap='jet')  # , vmin=dmin, vmax=dmax)
    plt.colorbar(ax)
    plt.title('Standard Approach, %s, slice %s' % (typecomp, slc))


def tensnorm(tensvec):
    return np.sqrt(np.sum(tensvec[:, 0:3]**2+2*tensvec[:, 3:]**2, 1))


def tens2mat(vec):
    mat = np.zeros((vec.shape[0], 3, 3))
    mat[:, 0, 0] = vec[:, 0]
    mat[:, 1, 1] = vec[:, 1]
    mat[:, 2, 2] = vec[:, 2]
    mat[:, 0, 1] = vec[:, 3]
    mat[:, 1, 0] = vec[:, 3]
    mat[:, 0, 2] = vec[:, 4]
    mat[:, 2, 0] = vec[:, 4]
    mat[:, 1, 2] = vec[:, 5]
    mat[:, 2, 1] = vec[:, 5]

    return mat


def get_pred(sn, el, ns, set_id, step, compl):

    """read the file for euler angle, total strain and plastic strain fields"""

    f = h5py.File("ref_%s%s_s%s.hdf5" % (ns, set_id, step), 'r')

    print f.get('euler').shape

    euler = f.get('euler')[sn, ...]
    euler = euler.swapaxes(0, 1)

    print euler.shape

    et = np.zeros((el**3, 6))
    ep = np.zeros((el**3, 6))

    for ii in xrange(6):
        comp = compl[ii]
        tmp = f.get('r%s_epsilon_t' % comp)[sn, ...]
        et[:, ii] = tmp.reshape(el**3)

        tmp = f.get('r%s_epsilon_p' % comp)[sn, ...]
        ep[:, ii] = tmp.reshape(el**3)

    f.close()

    """find the deviatoric strain tensor"""
    isdev = np.all(np.isclose(np.sum(et[:, 0:3]), np.zeros(el**3)))
    print "is trace(et) == 0?: %s" % isdev

    et_ = np.zeros(et.shape)
    et_[:, 0:3] = et[:, 0:3] - (1./3.)*np.expand_dims(np.sum(et[:, 0:3], 1), 1)
    et_[:, 3:] = et[:, 3:]

    isdev = np.all(np.isclose(np.sum(et_[:, 0:3]), np.zeros(el**3)))
    print "is trace(et_) == 0?: %s" % isdev

    """find the norm of the tensors"""
    en = tensnorm(et_)

    print "sn: %s" % sn
    print "min(en): %s" % en.min()
    print "max(en): %s" % en.max()

    """normalize the deviatoric strain tensor"""
    et_n = et_/np.expand_dims(en, 1)

    isnorm = np.all(np.isclose(tensnorm(et_n), np.ones(el**3)))
    print "is norm(et_n) == 0?: %s" % isnorm

    """write the normalized deviatioric total strain and plastic strains
    in matrix form"""
    et_m = tens2mat(et_n)

    epn = tensnorm(ep)
    # epn_max = np.argmax(epn)
    orig = epn
    # print "max(norm(ep)): %s" % epn[epn_max]
    # print "euler @ max(norm(ep)): %s" % str(euler[epn_max, ...])
    # print et[epn_max, ...]
    # print et_[epn_max, ...]
    # print et_n[epn_max, ...]

    """find the eigenvalues of the normalized tensor"""
    eigval_, g_p2s_ = LA.eigh(et_m)
    del et_m

    print "eigval_ example (before sort): %s" % str(eigval_[0, :])
    print "g_p2s_ example (before sort):"
    print g_p2s_[0, ...]

    """sort the eigenvalues/vectors by highest to lowest magnitude
    eigenvalue"""
    esort = np.argsort(np.abs(eigval_))[:, ::-1]

    eigval = np.zeros(eigval_.shape)
    g_p2s = np.zeros(g_p2s_.shape)

    for ii in xrange(el**3):
        eigval[ii, :] = eigval_[ii, esort[ii, :]]
        for jj in xrange(3):
            g_p2s[ii, jj, :] = g_p2s_[ii, jj, esort[ii, :]]

    print "eigval example (after sort): %s" % str(eigval[0, :])
    print "g_p2s example (after sort):"
    print g_p2s[0, ...]

    """find the deformation mode"""
    theta = np.arctan2(-2*eigval[:, 0]-eigval[:, 2], np.sqrt(3)*eigval[:, 2])
    theta += np.pi*(theta < 0)

    print "min(theta): %s" % np.str(theta.min()*180./np.pi)
    print "mean(theta): %s" % np.str(theta.mean()*180./np.pi)
    print "max(theta): %s" % np.str(theta.max()*180./np.pi)

    """find g_p2c = g_p2s*g_s2c"""
    g_s2c = ef.bunge2g(euler[:, 0], euler[:, 1], euler[:, 2])

    """this application of einsum is validated vs loop with np.dot()"""
    g_p2c = np.einsum('...ij,...jk', g_s2c, g_p2s)

    phi1, phi, phi2 = ef.g2bunge(g_p2c)

    X = np.vstack([phi1, phi, phi2]).T
    # X = np.array(ef.g2bunge(g_p2c)).T
    # X = np.array(ef.g2bunge(g_p2c.swapaxes(1, 2))).T
    # X = np.array(ef.g2bunge(g_p2s)).T
    # X = np.array(ef.g2bunge(g_p2s.swapaxes(1, 2))).T
    # X = np.array(ef.g2bunge(g_s2c)).T
    # X = np.array(ef.g2bunge(g_s2c.swapaxes(1, 2))).T

    del phi1, phi, phi2

    pred = rr.eval_func(theta, X, en).real

    print "min(orig): %s" % orig.min()
    print "min(pred): %s" % pred.min()
    print "max(orig): %s" % orig.max()
    print "max(pred): %s" % pred.max()

    return orig, pred


if __name__ == '__main__':
    sn = 6
    el = 21
    ns = 100
    set_id = 'val'
    step = 1
    compl = ['11', '22', '33', '12', '13', '23']

    orig, pred = get_pred(sn, el, ns, set_id, step, compl)
    orig = orig.reshape(el, el, el)
    pred = pred.reshape(el, el, el)

    maxindx = np.unravel_index(np.argmax(np.abs(orig)),
                               orig.shape)
    slc = maxindx[0]

    field_std(el, ns, orig, pred, slc, "$|\epsilon^{p}|$", 1)

    plt.show()
