# -*- coding: utf-8 -*-
"""
Created on Thu May 08 22:25:15 2014

@author: nhpnp3
"""

import mks_functions_serial as rr
import numpy as np

mks_R = np.load('mks_R_ord7_1001.npy')
resp_val = np.load('resp_val.npy')
el = 21

[avgE, MASE] = rr.eval_meas(mks_R,resp_val,el)

print avgE
print MASE