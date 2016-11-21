import numpy as np
import matplotlib.pyplot as plt
import h5py


L_ = 15
el = 21


f = h5py.File('coef_zdir.hdf5', 'r')

print f.keys()
coef_dft = f.get('coef12_400cal_s1')[...].reshape(L_, el, el, el)

f.close()

print "coef_dft.shape: %s" % str(coef_dft.shape)

coef = np.fft.ifftn(coef_dft, [el, el, el], [1, 2, 3])

coef_cent = np.fft.fftshift(coef, axes=[1, 2, 3])

print "coef_cent.shape: %s" % str(coef_cent.shape)

plt.figure(figsize=[8, 2.7])

L = 14
tmp = coef_cent[L, 10, :, :]

plt.subplot(121)
ax = plt.imshow(tmp.real, origin='lower',
                interpolation='none', cmap='magma')
plt.colorbar(ax)
plt.title('L=%s real' % L)

plt.subplot(122)
ax = plt.imshow(tmp.imag, origin='lower',
                interpolation='none', cmap='magma')
plt.colorbar(ax)
plt.title('L=%s imaginary' % L)

plt.show()
