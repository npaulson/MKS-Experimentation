# -*- coding: utf-8 -*-
"""
Created on Thu Sep 25 11:59:48 2014

@author: nhpnp3
"""

import numpy as np

resp = np.array([200,100,100,20,20,20]).astype('float64')

von_mis_resp = np.sqrt( 0.5*( (resp[0]-resp[1])**2 +(resp[1]-resp[2])**2 + (resp[2]-resp[0])**2 + 6*(resp[3]**2 + resp[4]**2 + resp[5]**2) ) )

print 'von mises, resp: ' + str(von_mis_resp) 
print von_mis_resp


resp1 = resp - np.ones_like(resp)
resp1 = resp1.astype('float64')

von_mis_resp1 = np.sqrt( 0.5*( (resp1[0]-resp1[1])**2 +(resp1[1]-resp1[2])**2 + (resp1[2]-resp1[0])**2 + 6*(resp1[3]**2 + resp1[4]**2 + resp1[5]**2) ) )

print 'von mises, resp1: ' + str(von_mis_resp1)

error_all = abs(resp1 - resp)/100

print 'component-wise error:'
print error_all

error_vm = abs(von_mis_resp1 - von_mis_resp)/100

print 'error vm = ' + str(error_vm)