# -*- coding: utf-8 -*-
"""
Created on Fri Jun 20 15:59:12 2014

@author: nhpnp3
"""

import numpy as np
import matplotlib.pyplot as plt

preMM = np.load('preMM2.npy')
print preMM.shape

plt.subplot(111)
ax = plt.imshow(preMM[4000:7000,13000:15000], origin='lower', interpolation='none',
    cmap='binary')
plt.colorbar(ax)