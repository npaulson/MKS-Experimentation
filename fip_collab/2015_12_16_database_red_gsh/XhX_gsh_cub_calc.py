import numpy as np
import matplotlib.pyplot as plt
import gsh_cub_tri_L0_16 as gsh

""" generate the euler angle array """

n_tot = 1000

emat = np.zeros((n_tot, 3))
emat[:, 0] = np.random.rand(n_tot)*np.pi/2.
emat[:, 1] = np.random.rand(n_tot)*np.pi/2.
emat[:, 2] = np.random.rand(n_tot)*np.pi/2.

print emat.shape

""" calculate XhX """

lmax = 10

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
