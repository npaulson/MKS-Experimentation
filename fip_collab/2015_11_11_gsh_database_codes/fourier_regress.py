import numpy as np
import h5py
import time


N_L = 15
N_p = 8
N_q = 8
cmax = N_L*N_p*N_q
cvec = np.unravel_index(np.arange(cmax), [N_L, N_p, N_q])
cvec = np.array(cvec).transpose()

XtX = np.zeros((cmax, cmax), dtype='complex128')

st = time.time()

for ii in xrange(cmax):

    L, p, q = cvec[ii, :]

    set_id_ii = 'set_%s_%s_%s' % (L, p, q)

    f = h5py.File('pre_fourier_p%s_q%s.hdf5' % (p, q), 'r')
    ep_set_ii = f.get(set_id_ii)[:]
    f.close()

    for jj in xrange(ii, cmax):

        print np.array([ii, jj])

        st = time.time()

        L, p, q = cvec[jj, :]

        set_id_jj = 'set_%s_%s_%s' % (L, p, q)

        f = h5py.File('pre_fourier_p%s_q%s.hdf5' % (p, q), 'r')
        ep_set_jj = f.get(set_id_jj)[:]
        f.close()

        print "load time: %ss" % np.round(time.time()-st, 3)

        st = time.time()

        # tmp = np.sum(ep_set_ii[:]*ep_set_jj[:])
        tmp = np.dot(ep_set_ii.conjugate(), ep_set_jj)

        del ep_set_jj

        print "dot product time: %ss" % np.round(time.time()-st, 3)

        st = time.time()          

        if ii == jj:
            XtX[ii, ii] = tmp
        else:
            XtX[ii, jj] = tmp
            XtX[jj, ii] = tmp

        del tmp
        print "save time: %ss" % np.round(time.time()-st, 3)

    del ep_set_ii

f1 = h5py.File('pre_fourier.hdf5', 'r')
ep_set = f1.get('ep_set')
Y = ep_set[:, 5]
f1.close

XtY = np.zeros(cmax, dtype='complex128')

for ii in xrange(cmax):

    print ii

    L, p, q = cvec[ii, :]
    set_id_ii = 'set_%s_%s_%s' % (L, p, q)

    f = h5py.File('pre_fourier_p%s_q%s.hdf5' % (p, q), 'r')
    ep_set_ii = f.get(set_id_ii)[:]
    f.close()

    XtY[ii] = np.dot(ep_set_ii, Y)

print "XtX and XtY prepared: %ss" % np.round(time.time()-st, 3)

coeff = np.linalg.solve(XtX, XtY)

print coeff

coeff_vec = np.zeros([cmax, 4])
coeff_vec[:, :3] = cvec
coeff_vec[:, 3] = coeff

f = h5py.File('fourier_coeff.hdf5', 'w')
f.create_dataset('coeff_vec', data=coeff_vec)
f.close()
