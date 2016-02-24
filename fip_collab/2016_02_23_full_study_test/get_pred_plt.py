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


def get_pred(sn, el, ns, set_id, step, typ, compl):

    f = h5py.File("ref_%s%s_s%s.hdf5" % (ns, set_id, step), 'r')

    euler = f.get('euler')[sn, ...].reshape(3, el**3)
    euler = euler.swapaxes(0, 1)

    et = np.zeros((el**3, 6))

    for ii in xrange(6):
        comp = compl[ii]
        tmp = f.get('r%s_%s' % (comp, typ))[sn, ...]
        et[:, ii] = tmp.reshape(el**3)

    f.close()

    """ find the deviatoric strain tensor """
    et_ = et
    et_[:, 0:3] = et_[:, 0:3] - (1./3.)*np.expand_dims(np.sum(et[:, 0:3], 1), 1)

    print np.all(np.isclose(np.sum(et[:, 0:3]), np.zeros(el**3)))

    """ find the norm of the deviatoric strain tensor """
    en = np.sqrt(np.sum(et_[:, 0:3]**2+2*et_[:, 3:]**2, 1))

    print "sn: %s" % sn
    print "min(en): %s" % en.min()
    print "max(en): %s" % en.max()

    """ normalize the deviatoric strain tensor """
    et_n = et_/np.expand_dims(en, 1)

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

    print et_m[0, ...]

    """ find the eigenvalues of the normalized tensor"""
    eigval, g_p2s = LA.eigh(et_m)

    print eigval[:5, :]

    # """ sort the principal strains in descending order """
    # indx = np.argsort(eigval)
    # indx = indx[::-1]
    # eigval = eigval[indx]

    """ find the deformation mode """
    # theta = np.arccos(np.sqrt(3./2.)*eigval[:, 2])+(np.pi/3.)
    # print theta[:10]*(180./np.pi)
    # theta = np.arccos(np.sqrt(3./2.)*eigval[:, 1])-(np.pi/3.)
    # print theta[:10]*(180./np.pi)
    theta = np.arccos(-np.sqrt(3./2.)*eigval[:, 0])
    # print theta[:10]*(180./np.pi)

    print "min(theta): %s" % np.str(theta.min()*180./np.pi)
    print "mean(theta): %s" % np.str(theta.mean()*180./np.pi)
    print "max(theta): %s" % np.str(theta.max()*180./np.pi)

    """ find g_p2c = g_p2s*g_s2c """

    g_s2c = ef.bunge2g(euler[:, 0], euler[:, 1], euler[:, 2])    

    # g_p2c = np.einsum('...ik,...kj', g_s2c, g_p2s)
    g_p2c = np.dot(g_s2c, g_p2s)

    # g_p2c = g_p2c.swapaxes(1, 2) # don't trust

    del g_s2c, g_p2s

    phi1, phi, phi2 = ef.g2bunge(g_p2c)

    X = np.vstack([phi1, phi, phi2]).T
    del phi1, phi, phi2

    pred = rr.eval_func(theta, X, en).real

    print "min(pred): %s" % pred.min()
    print "max(pred): %s" % pred.max()

    return pred


if __name__ == '__main__':
    sn = 5
    el = 21
    ns = 100
    set_id = 'val'
    step = 1
    comp = '11'
    typ = 'epsilon_t'
    compl = ['11', '22', '33', '12', '13', '23']

    f = h5py.File("ref_%s%s_s%s.hdf5" % (ns, set_id, step), 'r')
    print f.keys()
    pred = f.get('r%s_epsilon_p' % comp)[sn, ...].reshape(el, el, el)
    f.close()

    pred_ = get_pred(sn, el, ns, set_id, step, typ, compl)
    pred_ = pred_.reshape(el, el, el)

    maxindx = np.unravel_index(np.argmax(np.abs(pred)),
                               pred.shape)
    slc = maxindx[0]

    field_std(el, ns, pred, pred_, slc, typ+comp, 1)

    plt.show()
