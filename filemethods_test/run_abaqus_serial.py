# -*- coding: utf-8 -*-
"""
Created on Thu May 29 20:36:51 2014

@author: Noah
"""

import subprocess as sp

## the number of sample microstructures for calibration.
ns = 2
## specify the set designation (string format)
set_id = 'val'


for sn in xrange(ns):
        filename = "hcp_200s_%s%s.inp" % (sn+1,set_id)
        calljob = 'abaqus job=%s interactive' % filename         
        # check_call should wait until the command completes        
        sp.check_call(calljob, shell=True)