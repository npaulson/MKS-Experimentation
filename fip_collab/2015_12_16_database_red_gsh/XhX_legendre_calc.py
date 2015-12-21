import numpy as np
import matplotlib.pyplot as plt
import numpy.polynomial.legendre as leg


""" generate the en array """

emat = np.linspace(-1, 1, 35)

print emat.shape

""" calculate XhX """

lmax = 10

XhX = np.zeros((lmax, lmax), dtype='complex128')

for ii in xrange(lmax):
    for jj in xrange(lmax):

        p_vec = np.zeros(ii+1)
        p_vec[ii] = 1
        xii = leg.legval(emat, p_vec)

        p_vec = np.zeros(jj+1)
        p_vec[jj] = 1
        xjj = leg.legval(emat, p_vec)

        XhX[ii, jj] = np.dot(xii.conj(), xjj)


""" plot the XhX matrix """

plt.figure(1)

ax = plt.imshow(np.real(XhX), origin='lower',
                interpolation='none', cmap='jet')
plt.title("XhX: Legendre")
plt.colorbar(ax)

plt.show()
