import numpy as np
import matplotlib.pyplot as plt
import euler_func as ef
import sys

inc = np.int16(sys.argv[1])

el = 21
slc = 7

filename = "Results_Ti64_Dream3D_ZdirLoad_210microns_9261el_AbqInp" +\
           "_PowerLaw_100inc_3_data_phi_inc%s.txt" % str(inc)
tmp = np.loadtxt(filename, skiprows=2)
indx = np.argsort(tmp[:, 4])
phi1_ = tmp[indx, 1][0::8]
Phi_ = tmp[indx, 2][0::8]
phi2_ = tmp[indx, 3][0::8]


"""put back into hexagonal FZ"""

n_sym = 12

g = ef.bunge2g(phi1_, Phi_, phi2_)
print "g.shape: %s" % str(g.shape)
g_sym = np.zeros((n_sym, 21**3, 3, 3))
O_h = ef.symhex()

for ii in xrange(n_sym):
    g_sym[ii, ...] = np.einsum('ij,...jk', O_h[ii, ...], g)

phi1_, Phi_, phi2_ = ef.g2bunge(g_sym)

print "phi1.shape: %s" % str(phi1_.shape)

lt0 = phi1_ < 0
phi1_ += 2*np.pi*lt0

lt0 = Phi_ < 0
Phi_ += 2*np.pi*lt0

lt0 = phi2_ < 0
phi2_ += 2*np.pi*lt0

indx = (phi1_ < 2.*np.pi)*(Phi_ <= np.pi/2.)*(phi2_ < np.pi/3.)
indx = np.int8(indx)

indx = indx*(np.arange(n_sym)[:, None])
indx = indx.sum(0)

# plt.imshow(indx.reshape(el, el, el)[slc, ...], origin='lower',
#            interpolation='none', cmap='plasma')

phi1 = np.zeros(el**3)
Phi = np.zeros(el**3)
phi2 = np.zeros(el**3)

for ii in xrange(el**3):
    phi1[ii] = phi1_[indx[ii], ii]
    Phi[ii] = Phi_[indx[ii], ii]
    phi2[ii] = phi2_[indx[ii], ii]

phi1 = phi1.reshape((el, el, el))[slc, :, :]
Phi = Phi.reshape((el, el, el))[slc, :, :]
phi2 = phi2.reshape((el, el, el))[slc, :, :]

"""plot euler angles"""

plt.figure(num=1, figsize=[12, 2.7])

plt.subplot(131)

plt.imshow(phi1*(180/np.pi), origin='lower',
           interpolation='none', cmap='plasma',
           vmin=0, vmax=360)
plt.title("$\phi_1$, step %s" % inc)
plt.colorbar()

plt.subplot(132)

plt.imshow(Phi*(180/np.pi), origin='lower',
           interpolation='none', cmap='plasma',
           vmin=0, vmax=90)
plt.title("$\Phi$, step %s" % inc)
plt.colorbar()

plt.subplot(133)

plt.imshow(phi2*(180/np.pi), origin='lower',
           interpolation='none', cmap='plasma',
           vmin=0, vmax=60)
plt.title("$\phi_2$, step %s" % inc)
plt.colorbar()

plt.show()
