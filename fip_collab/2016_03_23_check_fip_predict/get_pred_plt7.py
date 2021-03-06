import numpy as np
from numpy import linalg as LA
import h5py
import functions as rr
import euler_func as ef
import matplotlib.pyplot as plt


def field_std(el, ns, SET1, SET2, SET3, slc, typecomp, plotnum):

    """Plot slices of the response"""
    plt.figure(num=plotnum, figsize=[12, 2.7])

    dmin = np.min([SET1[slc, :, :], SET2[slc, :, :]])
    dmax = np.max([SET1[slc, :, :], SET2[slc, :, :]])

    plt.subplot(131)
    ax = plt.imshow(SET1[slc, :, :], origin='lower',
                    interpolation='none', cmap='magma', vmin=dmin, vmax=dmax)
    plt.colorbar(ax)
    plt.title('spectral method, %s, slice %s' % (typecomp, slc))

    plt.subplot(132)
    ax = plt.imshow(SET2[slc, :, :], origin='lower',
                    interpolation='none', cmap='magma', vmin=dmin, vmax=dmax)
    plt.colorbar(ax)
    plt.title('single point CP, %s, slice %s' % (typecomp, slc))

    plt.subplot(133)
    ax = plt.imshow(SET3[slc, :, :], origin='lower',
                    interpolation='none', cmap='viridis')
    plt.colorbar(ax)
    plt.title('CPFEM, %s, slice %s' % (typecomp, slc))


def field_euler(slc, euler, plotnum):

    """Plot slices of the response"""
    plt.figure(num=plotnum, figsize=[4, 2.7])

    plt.imshow(euler[slc, :, :, 0], origin='lower',
               interpolation='none', cmap='magma')
    plt.title("Grain Structure")


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


def get_sp_answer(el):

    # open file containing Matthew's data
    filename = 'Results_tensor_%s.hdf5' % str(0).zfill(2)
    f = h5py.File(filename, 'r')

    resp = np.zeros((el**3))

    for ii in xrange(el**3):
        test_id = 'sim%s' % str(ii+1).zfill(7)
        dset = f.get(test_id)

        """
        Column order in each dataset:
        time,...
        sig11,sig22,sig33,sig12,sig13,sig23...
        e11,e22,e33,e12,e13,e23
        ep11,ep22,ep33,ep12,ep13,ep23,
        fip,gamdot,signorm
        """

        tmp = dset[-1, 13:19]
        tmp = tens2mat(tmp)
        var = tensnorm(tmp)

        resp[ii] = var

    return resp


def get_pred(el, etv, epv, euler):

    et = tens2mat(etv)
    ep = tens2mat(epv)

    """find the deviatoric strain tensor"""
    hydro = (et[0, 0]+et[1, 1]+et[2, 2])/3.
    et_dev = et - hydro*np.identity(3)

    """find the norm of the tensors"""
    en = tensnorm(et_dev)

    CPFEM = tensnorm(ep)

    """normalize the deviatoric strain tensor"""
    et_n = et_dev/en

    """find the principal values of the normalized tensor"""
    eigval_, g_p2s_ = LA.eigh(et_n)

    # esort = np.argsort(eigval)[::-1]
    esort = np.argsort(np.abs(eigval_))[::-1]

    eigval = eigval_[esort]
    g_p2s = g_p2s_[:, esort]

    """check for improper rotations"""
    if np.isclose(np.linalg.det(g_p2s), -1.0):
        # print "warning: improper rotation"
        g_p2s[:, 2] = -1*g_p2s[:, 2]

    """find the deformation mode"""
    theta = np.arccos(-np.sqrt(3./2.)*np.min(eigval_))
    # theta = np.arctan2(-2*eigval[0]-eigval[2], np.sqrt(3)*eigval[2])
    if theta < 0:
        theta += np.pi

    """find g_p2c = g_p2s*g_s2c"""
    g_s2c = bunge2g(euler)

    g_p2c = np.dot(g_s2c, g_p2s)

    if np.isclose(np.linalg.det(g_p2c), -1.0):
        print "warning: g_p2c is improper"

    phi1, phi, phi2 = g2bunge(g_p2c)

    euler_p2c = np.array([phi1, phi, phi2])
    euler_p2c += 2*np.pi*np.array(euler_p2c < 0)

    """try to recover et_dev from theta and euler_p2c"""
    g_p2c_ = bunge2g(euler_p2c)
    # if np.all(g_p2c != g_p2c_):
    #     print "g_p2c_ != g_p2c"
    princ_vals = theta2eig(theta)
    et_n_P = np.zeros((3, 3))
    et_n_P[0, 0] = princ_vals[0]
    et_n_P[1, 1] = princ_vals[1]
    et_n_P[2, 2] = princ_vals[2]
    et_n_C = np.dot(np.dot(g_p2c_, et_n_P), g_p2c_.T)
    g_c2s = g_s2c.T
    et_n_S = np.dot(np.dot(g_c2s, et_n_C), g_c2s.T)
    et_dev_ = et_n_S * en

    if not np.all(np.isclose(et_dev_, et_dev)):
        print "et_dev_ != et_dev"

    X = np.vstack([phi1, phi, phi2]).T

    return CPFEM, theta, X, en, eigval


if __name__ == '__main__':

    sn = 2
    el = 21
    ns = 100
    set_id = 'val'
    step = 1
    compl = ['11', '22', '33', '12', '13', '23']

    f = h5py.File("ref_%s%s_s%s.hdf5" % (ns, set_id, step), 'r')

    print f.get('euler').shape

    euler = f.get('euler')[sn, ...]

    np.save('euler.npy', euler)

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

    CPFEM_m = np.zeros(el**3)
    theta_m = np.zeros(el**3)
    X_m = np.zeros((el**3, 3))
    en_m = np.zeros(el**3)
    eigval_m = np.zeros((el**3, 3))

    for ii in xrange(el**3):
        if np.mod(ii, 100) == 0:
            print ii

        CPFEM, theta, X, en, eigval = get_pred(el, etv[ii, :], epv[ii, :], euler[ii, :])
        CPFEM_m[ii] = CPFEM
        theta_m[ii] = theta
        X_m[ii, :] = X
        en_m[ii] = en
        eigval_m[ii, :] = eigval

    """write file for matthew"""

    # tempm = np.hstack([eigval_m*en_m[:, None], X_m])
    # np.savetxt('et_file.txt', tempm)

    SPECTRAL_m = rr.eval_func(theta_m, X_m, en_m).real
    SPCP_m = get_sp_answer(el)

    SPECTRAL_m = SPECTRAL_m.reshape(el, el, el)
    SPCP_m = SPCP_m.reshape(el, el, el)
    CPFEM_m = CPFEM_m.reshape(el, el, el)

    maxindx = np.unravel_index(np.argmax(np.abs(CPFEM_m)),
                               CPFEM_m.shape)
    slc = maxindx[0]

    field_std(el, ns, SPECTRAL_m, SPCP_m, CPFEM_m, slc, "$|\epsilon^{p}|$", 1)

    print 'shape of euler: %s' % str(euler.shape)

    field_euler(slc, euler.reshape((el, el, el, 3)), 2)

    plt.show()
