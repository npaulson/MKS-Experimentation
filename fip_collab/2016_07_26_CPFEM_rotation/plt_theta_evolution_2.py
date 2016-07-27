import numpy as np
import matplotlib.pyplot as plt
import sys

incA = np.int16(sys.argv[1])
incB = np.int16(sys.argv[2])

el = 21
slc = 7

filename = "Results_Ti64_Dream3D_ZdirLoad_210microns_9261el_AbqInp" +\
           "_PowerLaw_100inc_3_data_theta_inc%s.txt" % str(incA)
tmp = np.loadtxt(filename, skiprows=2)
thetaA = tmp.reshape((el, el, el))[slc, :, :]*(180/np.pi)

filename = "Results_Ti64_Dream3D_ZdirLoad_210microns_9261el_AbqInp" +\
           "_PowerLaw_100inc_3_data_theta_inc%s.txt" % str(incB)
tmp = np.loadtxt(filename, skiprows=2)
thetaB = tmp.reshape((el, el, el))[slc, :, :]*(180/np.pi)

plt.figure(num=1, figsize=[12, 2.7])

dmin = np.min([thetaA, thetaB])
dmax = np.max([thetaA, thetaB])

plt.subplot(131)

plt.imshow(thetaA, origin='lower',
           interpolation='none', cmap='plasma',
           vmin=dmin, vmax=dmax)
plt.title("$\\theta$, step %s" % incA)
plt.colorbar()

plt.subplot(132)

plt.imshow(thetaB, origin='lower',
           interpolation='none', cmap='plasma',
           vmin=dmin, vmax=dmax)
plt.title("$\\theta$, step %s" % incB)
plt.colorbar()

plt.subplot(133)

diff = thetaB-thetaA

bound = np.max(np.abs(diff))

plt.imshow(diff, origin='lower',
           interpolation='none', cmap='seismic', vmin=-bound, vmax=bound)
plt.title("$\\theta$ difference")
plt.colorbar()

plt.show()
