# -*- coding: utf-8 -*-
"""
Created on Fri May 16 13:36:48 2014

@author: nhpnp3
"""

import os
import time
import numpy as np


start = time.time()

for ii in range(100):
    np.save('F%s' % ii, 'fart')
    
end = time.time()
timeE = np.round((end - start),5)
print 'wait time: %s' %timeE


start = time.time()

for ii in range(100):
    os.chdir('blerg')
    np.save('F%s' % ii, 'fart')
    os.chdir('..')
    
end = time.time()
timeE = np.round((end - start),5)
print 'switching directories time: %s' %timeE



