import numpy as np
import matplotlib.pyplot as plt
import sys

incA = np.int16(sys.argv[1])
incB = np.int16(sys.argv[2])

el = 21
slc = 7

filename = "Results_Ti64_Dream3D_ZdirLoad_210microns_9261el_AbqInp" +\
           "_PowerLaw_100inc_rotate_3_data_phi_inc%s.txt" % str(incA)
tmp = np.loadtxt(filename, skiprows=2)
indx = np.argsort(tmp[:, 4])
phi1 = tmp[indx, 1][0::8]
Phi = tmp[indx, 2][0::8]
phi2 = tmp[indx, 3][0::8]
phi1A = phi1.reshape((el, el, el))[slc, :, :]*(180/np.pi)
PhiA = Phi.reshape((el, el, el))[slc, :, :]*(180/np.pi)
phi2A = phi2.reshape((el, el, el))[slc, :, :]*(180/np.pi)

filename = "Results_Ti64_Dream3D_ZdirLoad_210microns_9261el_AbqInp" +\
           "_PowerLaw_100inc_rotate_3_data_phi_inc%s.txt" % str(incB)
tmp = np.loadtxt(filename, skiprows=2)
indx = np.argsort(tmp[:, 4])
phi1 = tmp[indx, 1][0::8]
Phi = tmp[indx, 2][0::8]
phi2 = tmp[indx, 3][0::8]
phi1B = phi1.reshape((el, el, el))[slc, :, :]*(180/np.pi)
PhiB = Phi.reshape((el, el, el))[slc, :, :]*(180/np.pi)
phi2B = phi2.reshape((el, el, el))[slc, :, :]*(180/np.pi)

"""plot for phi1"""

plt.figure(num=1, figsize=[12, 2.7])

dmin = np.min([phi1A, phi1B])
dmax = np.max([phi1A, phi1B])

plt.subplot(131)

plt.imshow(phi1A, origin='lower',
           interpolation='none', cmap='plasma',
           vmin=dmin, vmax=dmax)
plt.title("$\phi_1$, step %s" % incA)
plt.colorbar()

plt.subplot(132)

plt.imshow(phi1B, origin='lower',
           interpolation='none', cmap='plasma',
           vmin=dmin, vmax=dmax)
plt.title("$\phi_1$, step %s" % incB)
plt.colorbar()

plt.subplot(133)

diff = phi1B-phi1A

bound = np.max(np.abs(diff))

plt.imshow(diff, origin='lower',
           interpolation='none', cmap='seismic', vmin=-bound, vmax=bound)
plt.title("$\phi_1$ difference")
plt.colorbar()

"""plot for Phi"""

plt.figure(num=2, figsize=[12, 2.7])

dmin = np.min([PhiA, PhiB])
dmax = np.max([PhiA, PhiB])

plt.subplot(131)

plt.imshow(PhiA, origin='lower',
           interpolation='none', cmap='plasma',
           vmin=dmin, vmax=dmax)
plt.title("$\Phi$, step %s" % incA)
plt.colorbar()

plt.subplot(132)

plt.imshow(PhiB, origin='lower',
           interpolation='none', cmap='plasma',
           vmin=dmin, vmax=dmax)
plt.title("$\Phi$, step %s" % incB)
plt.colorbar()

plt.subplot(133)

diff = PhiB-PhiA

bound = np.max(np.abs(diff))

plt.imshow(diff, origin='lower',
           interpolation='none', cmap='seismic', vmin=-bound, vmax=bound)
plt.title("$\Phi$ difference")
plt.colorbar()

"""plot for phi2"""

plt.figure(num=3, figsize=[12, 2.7])

dmin = np.min([phi2A, phi2B])
dmax = np.max([phi2A, phi2B])

plt.subplot(131)

plt.imshow(phi2A, origin='lower',
           interpolation='none', cmap='plasma',
           vmin=dmin, vmax=dmax)
plt.title("$\phi_2$, step %s" % incA)
plt.colorbar()

plt.subplot(132)

plt.imshow(phi2B, origin='lower',
           interpolation='none', cmap='plasma',
           vmin=dmin, vmax=dmax)
plt.title("$\phi_2$, step %s" % incB)
plt.colorbar()

plt.subplot(133)

diff = phi2B-phi2A

bound = np.max(np.abs(diff))

plt.imshow(diff, origin='lower',
           interpolation='none', cmap='seismic', vmin=-bound, vmax=bound)
plt.title("$\phi_2$ difference")
plt.colorbar()

plt.show()
