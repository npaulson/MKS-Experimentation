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
    dmin = np.min(newSET[slc, :, :])
    dmax = np.max(newSET[slc, :, :])

    plt.subplot(121)
    ax = plt.imshow(newSET[slc, :, :], origin='lower',
                    interpolation='none', cmap='jet', vmin=dmin, vmax=dmax)
    plt.colorbar(ax)
    plt.title('New Approach, %s, slice %s' % (typecomp, slc))

    plt.subplot(122)
    ax = plt.imshow(traSET[slc, :, :], origin='lower',
                    interpolation='none', cmap='jet', vmin=dmin, vmax=dmax)
    plt.colorbar(ax)
    plt.title('Standard Approach, %s, slice %s' % (typecomp, slc))


# def field_std(el, ns, traSET, newSET, slc, typecomp, plotnum):

#     """Plot slices of the response"""
#     plt.figure(num=plotnum, figsize=[9, 2.7])

#     plt.subplot(121)
#     ax = plt.imshow(newSET[slc, :, :], origin='lower',
#                     interpolation='none', cmap='jet')
#     plt.colorbar(ax)
#     plt.title('New Approach, %s, slice %s' % (typecomp, slc))

#     plt.subplot(122)
#     ax = plt.imshow(traSET[slc, :, :], origin='lower',
#                     interpolation='none', cmap='jet')
#     plt.colorbar(ax)
#     plt.title('Standard Approach, %s, slice %s' % (typecomp, slc))


def theta2et_P(theta):

    et_P = np.zeros((theta.size, 3, 3))

    et_P[:, 0, 0] = np.sqrt(2./3.)*np.cos(theta-(np.pi/3.))
    et_P[:, 1, 1] = np.sqrt(2./3.)*np.cos(theta+(np.pi/3.))
    et_P[:, 2, 2] = -np.sqrt(2./3.)*np.cos(theta)

    return et_P


def tensnorm(tensor):
    return np.sqrt(np.sum(tensor**2, axis=(1, 2)))


def thydro(tensor):
    return (tensor[:, 0, 0] + tensor[:, 1, 1] + tensor[:, 2, 2])/3.


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


def is_equiv_g(g1, g2):
    symhex = ef.symhex()
    is_equiv = False

    for ii in xrange(symhex.shape[0]):
        g_symm = np.dot(symhex[ii, ...], g1)
        if np.all(np.isclose(g2, g_symm)):
            is_equiv = True

    return is_equiv


def bunge2g(euler):
    # this has been cross-checked
    # only works for radians

    phi1 = euler[0]
    Phi = euler[1]
    phi2 = euler[2]

    g = np.zeros([3, 3])

    g[0, 0] = np.cos(phi1)*np.cos(phi2) - \
        np.sin(phi1)*np.sin(phi2)*np.cos(Phi)

    g[0, 1] = np.sin(phi1)*np.cos(phi2) + \
        np.cos(phi1)*np.sin(phi2)*np.cos(Phi)

    g[0, 2] = np.sin(phi2)*np.sin(Phi)

    g[1, 0] = -np.cos(phi1)*np.sin(phi2) - \
        np.sin(phi1)*np.cos(phi2)*np.cos(Phi)

    g[1, 1] = -np.sin(phi1)*np.sin(phi2) + \
        np.cos(phi1)*np.cos(phi2)*np.cos(Phi)

    g[1, 2] = np.cos(phi2)*np.sin(Phi)

    g[2, 0] = np.sin(phi1)*np.sin(Phi)

    g[2, 1] = -np.cos(phi1)*np.sin(Phi)

    g[2, 2] = np.cos(Phi)

    return g


def return2fz(euler):
    g = bunge2g(euler)
    symhex = ef.symhex()
    for ii in xrange(symhex.shape[0]):
        g_symm = np.dot(symhex[ii, ...], g)
        euler_ = g2bunge(g_symm)
        euler_ += 2*np.pi*np.array(euler_ < 0)
        if np.all(euler_ < np.array([2*np.pi, np.pi/2, np.pi/3])):
            break
    return euler_


def g2bunge(g):

    # if np.abs(np.abs(g[2, 2]) - 1) < 1E-8:
    if np.abs(np.abs(g[2, 2]) - 1) < 1E-5:
        print "gimble lock warning"
        Phi = 0
        phi1 = np.arctan2(g[0, 1], g[0, 0])/2
        phi2 = phi1
    else:
        Phi = np.arccos(g[2, 2])
        phi1 = np.arctan2(g[2, 0]/np.sin(Phi), -g[2, 1]/np.sin(Phi))
        phi2 = np.arctan2(g[0, 2]/np.sin(Phi), g[1, 2]/np.sin(Phi))

    return np.array([phi1, Phi, phi2])


def get_pred(sn, el, ns, set_id, step, compl):

    """read the file for euler angle, total strain and plastic strain fields"""

    rcell = np.random.randint(0, el**3)

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

    """write et and ep in matrix form"""
    et = tens2mat(et)
    ep = tens2mat(ep)

    """find the deviatoric strain tensor"""
    isdev = np.all(np.abs(thydro(et)) < 1e-5)
    print "\nis hydro(et) == 0?: %s" % isdev

    et_ = np.zeros(et.shape)
    Id = np.zeros(et.shape)
    Id[:, 0, 0] = 1
    Id[:, 1, 1] = 1
    Id[:, 2, 2] = 1
    et_ = et - thydro(et)[:, None, None]*Id

    isdev = np.all(np.abs(thydro(et_)) < 1e-5)
    print "is hydro(et_) == 0?: %s\n" % isdev

    """find the norm of the tensors"""
    en = tensnorm(et_)

    print "min(en): %s" % en.min()
    print "max(en): %s" % en.max()

    """normalize the deviatoric strain tensor"""
    et_n = et_/en[:, None, None]

    isnorm = np.all(np.isclose(tensnorm(et_n), np.ones(el**3)))
    print "is norm(et_n) == 0?: %s\n" % isnorm

    """write the normalized deviatioric total strain and plastic strains
    in matrix form"""

    """find the eigenvalues of the normalized tensor"""
    eigval_, g_p2s_ = LA.eigh(et_n)
    del et_n

    print "eigval_ (before sort) for cell #%s: %s" % (rcell, str(eigval_[rcell, :]))
    print "g_p2s_ (before sort) for cell #%s:" % rcell
    print g_p2s_[rcell, ...]

    """sort the eigenvalues/vectors by highest to lowest magnitude
    eigenvalue"""
    esort = np.argsort(np.abs(eigval_))[:, ::-1]

    eigval = np.zeros(eigval_.shape)
    g_p2s = np.zeros(g_p2s_.shape)

    for ii in xrange(el**3):
        eigval[ii, :] = eigval_[ii, esort[ii, :]]
        for jj in xrange(3):
            g_p2s[ii, jj, :] = g_p2s_[ii, jj, esort[ii, :]]

    print "\neigval (after sort) for cell #%s: %s" % (rcell, str(eigval[rcell, :]))
    print "g_p2s (after sort) for cell #%s:" % rcell
    print g_p2s[rcell, ...]

    """find the deformation mode"""
    theta = np.arctan2(-2*eigval[:, 0]-eigval[:, 2], np.sqrt(3)*eigval[:, 2])
    theta += np.pi*(theta < 0)

    print "\nmin(theta): %s" % np.str(theta.min()*180./np.pi)
    print "mean(theta): %s" % np.str(theta.mean()*180./np.pi)
    print "max(theta): %s\n" % np.str(theta.max()*180./np.pi)

    """find g_p2c = g_p2s*g_s2c"""

    g_s2c = np.zeros((el**3, 3, 3))
    for ii in xrange(el**3):
        g_s2c[ii, ...] = bunge2g(euler[ii, :])

    # g_s2c = ef.bunge2g(euler[:, 0], euler[:, 1], euler[:, 2])

    """this application of einsum is validated vs loop with np.dot()"""
    g_p2c = np.einsum('...ij,...jk', g_s2c, g_p2s)

    phi1 = np.zeros(el**3)
    phi = np.zeros(el**3)
    phi2 = np.zeros(el**3)
    for ii in xrange(el**3):
        tmp = g2bunge(g_p2c[ii, ...])
        phi1[ii] = tmp[0]
        phi[ii] = tmp[1]
        phi2[ii] = tmp[2]

    # phi1, phi, phi2 = ef.g2bunge(g_p2c)

    # euler_fz = np.zeros((el**3, 3))

    # for ii in xrange(el**3):
    #     tmp = np.array([phi1[ii], phi[ii], phi2[ii]])
    #     euler_fz[ii, :] = return2fz(tmp)

    """try to reconstruct et_"""

    g_p2c_ = np.zeros((el**3, 3, 3))
    for ii in xrange(el**3):
        g_p2c_[ii, ...] = bunge2g(np.array([phi1[ii], phi[ii], phi2[ii]]))

    # g_p2c_ = ef.bunge2g(phi1, phi, phi2)

    eultmp = np.array([phi1[rcell], phi[rcell], phi2[rcell]])
    print "euler angles for cell#%s: %s" % (rcell, eultmp)

    geq = np.all(np.isclose(g_p2c[rcell, ...], g_p2c_[rcell, ...]))
    print "are g_p2c and g_p2c_ equal for cell #%s?: %s" % (rcell, geq)

    is_equiv = is_equiv_g(g_p2c[rcell, ...], g_p2c_[rcell, ...])
    print "are g_p2c and g_p2c_ equivalent for cell #%s?: %s\n" % (rcell, is_equiv)

    et_n_P = theta2et_P(theta)

    et_n_C = np.einsum('...ij,...jk,...lk', g_p2c_, et_n_P, g_p2c_)

    g_c2s = g_s2c.swapaxes(1, 2)

    et_n_S = np.einsum('...ij,...jk,...lk', g_c2s, et_n_C, g_c2s)

    et_recon = et_n_S * en[:, None, None]

    print "et_ for cell #%s:" % rcell
    print et_[rcell, ...]
    print "et_ reconstructed from theta, euler_p2c and en same cell:"
    print et_recon[rcell, ...]

    X = np.vstack([phi1, phi, phi2]).T
    # X = np.array(ef.g2bunge(g_p2c)).T
    # X = np.array(ef.g2bunge(g_p2c.swapaxes(1, 2))).T
    # X = np.array(ef.g2bunge(g_p2s)).T
    # X = np.array(ef.g2bunge(g_p2s.swapaxes(1, 2))).T
    # X = np.array(ef.g2bunge(g_s2c)).T
    # X = np.array(ef.g2bunge(g_s2c.swapaxes(1, 2))).T

    orig = tensnorm(ep)
    pred = rr.eval_func(theta, X, en).real

    print "\nmin(orig): %s" % orig.min()
    print "min(pred): %s" % pred.min()
    print "max(orig): %s" % orig.max()
    print "max(pred): %s" % pred.max()

    return orig, pred


if __name__ == '__main__':
    sn = 7
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
