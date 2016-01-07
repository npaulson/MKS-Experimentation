import numpy as np
import matplotlib.pyplot as plt
import gsh_tri_tri_L0_13 as gsh
import scipy.special as sp

inc = 2  # degree increment for angular variables
lmax = 50

n_th = 360/inc  # number of phi1 samples for FZ
n_p = (180/inc)+1  # number of Phi samples for FZ

""" generate the euler angle array """

n_tot = n_th*n_p

theta = np.random.rand(n_tot)*2*np.pi
phi = np.random.rand(n_tot)*np.pi

""" generate Imat """

Imat = np.zeros([lmax, 2])

c = 0
for n in xrange(lmax):
	for m in xrange(-n, n+1):
		Imat[c, :] = [m, n]
		c +=1
		if c == lmax:
			break
	if c == lmax:
		break

""" calculate XhX """

XhX = np.zeros((lmax, lmax), dtype='complex128')

for ii in xrange(lmax):
    print ii
    for jj in xrange(lmax):

    	m_ii, n_ii = Imat[ii]
    	m_jj, n_jj = Imat[jj]

        xii = sp.sph_harm(m_ii, n_ii, theta, phi)
        xjj = sp.sph_harm(m_jj, n_jj, theta, phi)

        # XhX[ii, jj] = np.dot(xii.conj(), xjj)
        XhX[ii, jj] = np.sum(xii.conj()*xjj*np.sin(phi))


""" plot the XhX matrix """

plt.figure(1)


plt.subplot(121)

ax = plt.imshow(np.real(XhX), origin='lower',
                interpolation='none', cmap='jet')
plt.title("real(XhX): GSH")
plt.colorbar(ax)

plt.subplot(122)

ax = plt.imshow(np.imag(XhX), origin='lower',
                interpolation='none', cmap='jet')
plt.title("imag(XhX): GSH")
plt.colorbar(ax)

plt.show()
