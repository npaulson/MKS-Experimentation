# -*- coding: utf-8 -*-
"""
Created on Wed Dec 17 13:21:17 2014

@author: nhpnp3
"""

import os

c = 0

for filename in os.listdir(os.getcwd()):
    if filename.endswith('.dat'):              
        newname = 'cal_rand_delta_%s.dat' % c
        os.rename(filename, newname)
        c += 1
    