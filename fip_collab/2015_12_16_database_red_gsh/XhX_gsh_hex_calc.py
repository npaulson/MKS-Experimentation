import numpy as np
import matplotlib.pyplot as plt
import gsh_hex_tri_L0_16 as gsh

inc = 5  # degree increment for angular variables

n_p1 = 360/inc  # number of phi1 samples for FZ
n_P = (90/inc)+1  # number of Phi samples for FZ
n_p2 = 60/inc  # number of phi2 samples for FZ

""" generate the euler angle array """

n_tot = n_p1*n_P*n_p2

emat = np.zeros((n_tot, 3))
emat[:, 0] = np.random.rand(n_tot)*2*np.pi
emat[:, 1] = np.random.rand(n_tot)*np.pi/2.
emat[:, 2] = np.random.rand(n_tot)*np.pi/3.

print emat.shape

""" calculate XhX """

lmax = 50

XhX = np.zeros((lmax, lmax), dtype='complex128')

for ii in xrange(lmax):
    print ii
    for jj in xrange(lmax):

        xii = gsh.gsh_eval(emat, [ii])[:, 0]
        xjj = gsh.gsh_eval(emat, [jj])[:, 0]

        XhX[ii, jj] = np.sum(xii.conj()*xjj*np.sin(emat[:, 1]))
        # XhX[ii, jj] = np.dot(xii.conj(), xjj)


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
