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


def g2bunge(g):

    if np.abs(np.abs(g[2, 2]) - 1) < 1E-8:
        print "gimble lock warning"
        Phi = 0
        phi1 = np.arctan2(g[0, 1], g[0, 0])/2
        phi2 = phi1
    else:
        Phi = np.arccos(g[2, 2])
        phi1 = np.arctan2(g[2, 0]/np.sin(Phi), -g[2, 1]/np.sin(Phi))
        phi2 = np.arctan2(g[0, 2]/np.sin(Phi), g[1, 2]/np.sin(Phi))

    return np.array([phi1, Phi, phi2])


def tensnorm(mat):
    return np.sqrt(np.sum(mat**2))


def tens2mat(vec):
    mat = np.zeros((3, 3))
    mat[0, 0] = vec[0]
    mat[1, 1] = vec[1]
    mat[2, 2] = vec[2]
    mat[0, 1] = vec[3]
    mat[1, 0] = vec[3]
    mat[0, 2] = vec[4]
    mat[2, 0] = vec[4]
    mat[1, 2] = vec[5]
    mat[2, 1] = vec[5]

    return mat


def theta2eig(x):

    et_ii = np.array([np.sqrt(2./3.)*np.cos(x-(np.pi/3.)),
                      np.sqrt(2./3.)*np.cos(x+(np.pi/3.)),
                      -np.sqrt(2./3.)*np.cos(x)])
    return et_ii


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


def get_pred(el, etv, epv, euler):

    et = tens2mat(etv)
    ep = tens2mat(epv)

    # print "et (strain tensor):"
    # print et

    """find the deviatoric strain tensor"""
    hydro = (et[0, 0]+et[1, 1]+et[2, 2])/3.
    et_dev = et - hydro*np.identity(3)

    # print "et_dev (deviatoric strain tensor):"
    # print et_dev
    # print "trace(et_dev): %s" % str(np.trace(et_dev))

    """find the norm of the tensors"""
    en = tensnorm(et_dev)
    # print "en (norm(et_dev)): %s" % str(en)

    epn_CPFEM = tensnorm(ep)

    """normalize the deviatoric strain tensor"""
    et_n = et_dev/en

    # print "et_n (normalized deviatoric strain tensor):"
    # print et_n
    # print "norm(et_n): %s" % str(tensnorm(et_n))

    """find the principal values of the normalized tensor"""
    eigval, g_p2s = LA.eigh(et_n)
    esort = np.argsort(np.abs(eigval))[::-1]

    eigval = eigval[esort]
    g_p2s = g_p2s[:, esort]

    # print "principal values of et_n: %s" % str(eigval)
    # # print "eigenvectors:"
    # # print g_p2s

    # """show that the matrix of eigenvectors is g_p2s"""
    # print "use the backwards tensor transformation to " +\
    #       "get et_n_prinicipal using g_p2s\n" +\
    #       "(et_n_principal = g_p2s^t * et_n * g_p2s)"
    # print np.round(np.dot(np.dot(g_p2s.T, et_n), g_p2s), 6)

    """find the deformation mode"""
    theta = np.arctan2(-2*eigval[0]-eigval[2], np.sqrt(3)*eigval[2])
    if theta < 0:
        theta += np.pi
    # print "theta (deformation mode): %s deg" % str(theta*180/np.pi)

    # """recover the principal values from the deformation mode"""
    # print "principal values of et_n recovered from theta: %s" %\
    #       theta2eig(theta)

    """find g_p2c = g_p2s*g_s2c"""
    g_s2c = bunge2g(euler)

    # g_p2c = np.einsum('ij,jk', g_s2c, g_p2s)
    g_p2c = np.dot(g_s2c, g_p2s)

    # print g_p2c

    phi1, phi, phi2 = g2bunge(g_p2c)

    euler_p2c = np.array([phi1, phi, phi2])
    euler_p2c += 2*np.pi*np.array(euler_p2c < 0)
    # print "g_p2c euler angles: %s" % str(euler_p2c)

    # print bunge2g(euler_p2c)
    # print bunge2g(return2fz(np.array([phi1, phi, phi2])))

    # euler_p2c = return2fz(np.array([phi1, phi, phi2]))
    # print "g_p2c euler angles (euler_p2c): %s" % str(euler_p2c)

    """try to recover et_dev from theta and euler_p2c"""
    g_p2c_ = bunge2g(euler_p2c)
    if np.all(g_p2c != g_p2c_):
        print "g_p2c_ != g_p2c"
    princ_vals = theta2eig(theta)
    et_n_P = np.zeros((3, 3))
    et_n_P[0, 0] = princ_vals[0]
    et_n_P[1, 1] = princ_vals[1]
    et_n_P[2, 2] = princ_vals[2]
    et_n_C = np.dot(np.dot(g_p2c, et_n_P), g_p2c.T)
    g_c2s = g_s2c.T
    et_n_S = np.dot(np.dot(g_c2s, et_n_C), g_c2s.T)
    et_dev_ = et_n_S * en

    if not np.all(np.isclose(et_dev_, et_dev)):
        print "et_dev_ != et_dev"

    X = np.vstack([phi1, phi, phi2]).T

    epn_SPECTRAL = rr.eval_func(theta, X, en).real

    return epn_CPFEM, epn_SPECTRAL


if __name__ == '__main__':

    sn = 7
    el = 21
    ns = 100
    set_id = 'val'
    step = 1
    compl = ['11', '22', '33', '12', '13', '23']

    f = h5py.File("ref_%s%s_s%s.hdf5" % (ns, set_id, step), 'r')

    print f.get('euler').shape

    euler = f.get('euler')[sn, ...]
    euler = euler.swapaxes(0, 1)

    etv = np.zeros((el**3, 6))
    epv = np.zeros((el**3, 6))

    for ii in xrange(6):
        comp = compl[ii]
        tmp = f.get('r%s_epsilon_t' % comp)[sn, ...]
        etv[:, ii] = tmp.reshape(el**3)

        tmp = f.get('r%s_epsilon_p' % comp)[sn, ...]
        epv[:, ii] = tmp.reshape(el**3)

    f.close()

    orig_m = np.zeros(el**3)
    pred_m = np.zeros(el**3)

    for ii in xrange(el**3):
        if np.mod(ii, 100) == 0:
            print ii

        orig, pred = get_pred(el, etv[ii, :], epv[ii, :], euler[ii, :])

    orig_m = orig_m.reshape(el, el, el)
    pred_m = pred_m.reshape(el, el, el)

    maxindx = np.unravel_index(np.argmax(np.abs(orig)),
                               orig.shape)
    slc = maxindx[0]

    field_std(el, ns, orig, pred, slc, "$|\epsilon^{p}|$", 1)

    plt.show()
