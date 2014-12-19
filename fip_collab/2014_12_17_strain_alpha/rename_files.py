# -*- coding: utf-8 -*-
"""
Created on Wed Dec 17 13:21:17 2014

@author: nhpnp3
"""

import os

c = 0

for filename in os.listdir(os.getcwd()):
    if filename.endswith('.vtk'):        
        l_sn = str(c).zfill(3)        
        newname = 'random%s.vtk' % l_sn
        os.rename(filename, newname)
        c += 1
    