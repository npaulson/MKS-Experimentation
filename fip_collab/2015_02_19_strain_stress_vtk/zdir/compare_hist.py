# -*- coding: utf-8 -*-
"""
Created on Wed Oct 01 13:52:33 2014

@author: nhpnp3
"""

import numpy as np
import matplotlib.pyplot as plt

comp = '33'
typ = 'epsilon'
ns = 400
step = 1
el = 21

mks1 = np.load('mksR%s_%s%s_s%s.npy' % (comp, ns, 'val_random', step))
mks2 = np.load('mksR%s_%s%s_s%s.npy' % (comp, ns, 'val_trans', step))
mks3 = np.load('mksR%s_%s%s_s%s.npy' % (comp, ns, 'val_basaltrans', step))
mks4 = np.load('mksR%s_%s%s_s%s.npy' % (comp, ns, 'val_actual', step))
# mks1 = np.load('stress%s_%s%s_s%s.npy' % (comp, ns, 'val_random', step))
# mks2 = np.load('stress%s_%s%s_s%s.npy' % (comp, ns, 'val_trans', step))
# mks3 = np.load('stress%s_%s%s_s%s.npy' % (comp, ns, 'val_basaltrans', step))
# mks4 = np.load('stress%s_%s%s_s%s.npy' % (comp, ns, 'val_actual', step))


# Plot a histogram representing the frequency of strain levels with
# separate channels for each phase of each type of response.
plt.figure(num=1, figsize=[12, 5])

# find the min and max of both datasets (in full)
dmin = np.amin([mks1, mks2, mks3, mks4])
dmax = np.amax([mks1, mks2, mks3, mks4])

mks1L = np.reshape(mks1, ns*(el**3))
mks2L = np.reshape(mks2, ns*(el**3))
mks3L = np.reshape(mks3, ns*(el**3))
mks4L = np.reshape(mks4, ns*(el**3))

# select the desired number of bins in the histogram
bn = 200
weight = np.ones_like(mks1L)/(el**3)

n, bins, patches = plt.hist(mks1L,
                            bins=bn,
                            histtype='step',
                            hold=True,
                            range=(dmin, dmax),
                            weights=weight,
                            color='white')
bincenters = 0.5*(bins[1:]+bins[:-1])
mks1L, = plt.plot(bincenters, n, 'k', linestyle='-', lw=0.75)

n, bins, patches = plt.hist(mks2L,
                            bins=bn,
                            histtype='step',
                            hold=True,
                            range=(dmin, dmax),
                            weights=weight,
                            color='white')
mks2L, = plt.plot(bincenters, n, 'b', linestyle='-', lw=0.75)

n, bins, patches = plt.hist(mks3L,
                            bins=bn,
                            histtype='step',
                            hold=True,
                            range=(dmin, dmax),
                            weights=weight,
                            color='white')
mks3L, = plt.plot(bincenters, n, 'r', linestyle='-', lw=0.75)
plt.grid(True)

n, bins, patches = plt.hist(mks4L,
                            bins=bn,
                            histtype='step',
                            hold=True,
                            range=(dmin, dmax),
                            weights=weight,
                            color='white')
mks4L, = plt.plot(bincenters, n, 'g', linestyle='-', lw=0.75)

plt.legend([mks1L, mks2L, mks3L, mks4L],
           ["random", "transverse", "basal-transverse", "actual"])

plt.xlabel("$\%s_{%s}$" % (typ, comp))
plt.ylabel("Count")
plt.ylim([0, 30])
plt.title("$\%s_{%s}$ histograms for $\%s$-Ti textures" % (typ, comp, 'alpha'))

plt.show()
