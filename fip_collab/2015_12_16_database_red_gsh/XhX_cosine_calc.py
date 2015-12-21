import numpy as np
import matplotlib.pyplot as plt


""" generate the theta array """

inc = 6  # degree increment for angular variables

n_th = (60/inc)+1  # number of theta samples for FZ

emat = np.arange(n_th)*(inc*np.pi/180.)

print emat.shape

""" calculate XhX """

lmax = 10

L_th = (2.*np.pi)/3.

XhX = np.zeros((lmax, lmax), dtype='complex128')

for ii in xrange(lmax):
    for jj in xrange(lmax):

        xii = np.cos(2*np.pi*ii*emat/L_th)

        xjj = np.cos(2*np.pi*jj*emat/L_th)

        XhX[ii, jj] = np.dot(xii.conj(), xjj)


""" plot the XhX matrix """

plt.figure(1)

ax = plt.imshow(np.real(XhX), origin='lower',
                interpolation='none', cmap='jet')
plt.title("XhX: cosine")
plt.colorbar(ax)

plt.figure(2)

emat_ext = np.arange(120)*(np.pi/180.)
plt.plot(emat_ext, np.cos(2*np.pi*1*emat_ext/L_th))

plt.show()
