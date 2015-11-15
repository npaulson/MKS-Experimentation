import numpy as np
import numpy.polynomial.legendre as leg
import gsh_hex_tri_L0_8 as gsh
import h5py
import time


inc = 3  # degree increment for angular variables

n_th_max = 120/inc  # number of theta samples in FOS
n_max = 360/inc  # number of phi1, Phi and phi2 samples in FOS
n_hlf = 180/inc  # half n_max

n_th = (60/inc)+1  # number of theta samples for FZ
n_p1 = 360/inc  # number of phi1 samples for FZ
n_P = (90/inc)+1  # number of Phi samples for FZ
n_p2 = 60/inc  # number of phi2 samples for FZ

f = h5py.File('pre_fourier.hdf5', 'r+')
ep_set = f.get('ep_set')

theta = ep_set[:, 0]
e_angles = ep_set[:, 1:4]
et_norm = ep_set[:, 4]
Y = ep_set[:, 5]

L = (2.*np.pi)/3.
N_L = 15
N_p = 8
N_q = 8

cmax = N_L*N_p*N_q
cvec = np.zeros([dmax, 3])
c = 0

st = time.time()

for L in xrange(N_L):
    for p in xrange(N_p):

        p_vec = np.zeros(N_p)
        p_vec[p] = 1

        for q in xrange(N_q):

            vec = gsh.gsh(e_angles, L) * \
                  leg.legval(et_norm, p_vec) * \
                  np.exp((1j*2*np.pi*q*theta)/L)

            set_id = 'set_%s_%s_%s' % (L, p, q)
            ep_set = f.create_dataset(set_id, data=vec)

            tmp = np.array([L, p, q])
            print tmp
            cvec[c, :] = tmp
            c += 1

print "basis evaluation complete: %ss" % np.round(time.time()-st, 3)

XtX = np.zeros((dmax,dmax)) 

st = time.time()

for ii in xrange(cmax):
	for jj in xrange(ii, cmax):

			L, p, q = cvec[ii, :]
			set_id_ii = 'set_%s_%s_%s' % (L, p, q)
			ep_set_ii = f.get(set_id_ii)

			L, p, q = cvec[jj, :]
			set_id_jj = 'set_%s_%s_%s' % (L, p, q)
			ep_set_jj = f.get(set_id_jj)


			tmp = np.dot(ep_set_ii, ep_set_jj)

			if ii == jj:
				XtX[ii, ii] =  tmp
			else:
				XtX[ii, jj] =  tmp
				XtX[jj, ii] =  tmp            

XtY	= np.zeros(dmax)

for ii in xrange(cmax):
	L, p, q = cvec[ii, :]
	set_id_ii = 'set_%s_%s_%s' % (L, p, q)
	ep_set_ii = f.get(set_id_ii)

	XtY[ii] = np.dot(ep_st_ii, Y)

print "XtX and XtY prepared: %ss" % np.round(time.time()-st, 3)

f.close()

coeff = np.linalg.solve(XtX, XtY)

print coeff

coeff_vec = np.zeros([dmax, 4])
coeff_vec[:, :3] = cvec
coeff_vec[:, 3] = coeff 

f = h5py.File('fourier_coeff.hdf5', 'r+')
f.create_dataset('coeff_vec', data=coeff_vec)
