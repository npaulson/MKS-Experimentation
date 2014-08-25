# -*- coding: utf-8 -*-
"""
Created on Fri Aug 22 16:47:25 2014

@author: nhpnp3
"""
import numpy as np
import functions_small as fs

dat1 = fs.res_red2(filename = 'Ti64_RandomMicroFZreducedNewBCs_21x21x21_AbqInp_PowerLaw_00001.inp', line0 = 10725)

dat2 = fs.res_red2(filename = 'Yuksel_BCs.dat', line0 = 0)

if np.all(dat1 == dat2) == True:
    print "fields are equal"
else:
    print "fields are not equal"