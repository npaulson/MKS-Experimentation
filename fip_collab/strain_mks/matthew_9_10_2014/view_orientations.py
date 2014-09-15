# -*- coding: utf-8 -*-
"""
Created on Fri May 23 14:25:50 2014

This script evaluates the success of a given MKS calibration and validation
through metrics like MASE and maximum error as well as plotting strain
fields and histograms.

@author: nhpnp3
"""

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


euler = np.load('euler_50val.npy')

sn=0
max = 1000

fig = plt.figure()
ax3D = fig.add_subplot(111, projection='3d')
p3d = ax3D.scatter(euler[:max,sn,0],euler[:max,sn,1],euler[:max,sn,2])

plt.figure(2)
plt.scatter(euler[:max,sn,0],euler[:max,sn,1])