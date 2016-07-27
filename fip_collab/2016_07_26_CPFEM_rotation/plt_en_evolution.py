import numpy as np
import matplotlib.pyplot as plt
import sys

incA = np.int16(sys.argv[1])
incB = np.int16(sys.argv[2])

el = 21
slc = 7

filename = "Results_Ti64_Dream3D_ZdirLoad_210microns_9261el_AbqInp" +\
           "_PowerLaw_100inc_3_data_en_inc%s.txt" % str(incA)
tmp = np.loadtxt(filename, skiprows=2)
enA = tmp.reshape((el, el, el))[slc, :, :]

filename = "Results_Ti64_Dream3D_ZdirLoad_210microns_9261el_AbqInp" +\
           "_PowerLaw_100inc_3_data_en_inc%s.txt" % str(incB)
tmp = np.loadtxt(filename, skiprows=2)
enB = tmp.reshape((el, el, el))[slc, :, :]
plt.figure(num=1, figsize=[8, 2.7])

dmin = np.min([enA, enB])
dmax = np.max([enA, enB])

plt.subplot(121)

plt.imshow(enA, origin='lower',
           interpolation='none', cmap='plasma')
plt.title("$\\vert\epsilon_t\\vert$, step %s" % incA)
plt.colorbar()

plt.subplot(122)

plt.imshow(enB, origin='lower',
           interpolation='none', cmap='plasma')
plt.title("$\\vert\epsilon_t\\vert$, step %s" % incB)
plt.colorbar()

plt.show()
