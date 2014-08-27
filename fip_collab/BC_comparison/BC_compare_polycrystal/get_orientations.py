# -*- coding: utf-8 -*-
"""
Created on Mon Aug 25 11:38:34 2014

This file simply reads a vtk file and pulls out the euler angle information
and saves it to a .mat file

@author: nhpnp3
"""

import functions_ti_alpha_fip_v1 as rr
import scipy.io as sio

euler = rr.read_vtk('Results_Ti64_RandomMicroFZreducedNewBCs_21x21x21_AbqInp_PowerLaw_00001_data_v2_00.vtk')

sio.savemat('euler_priddy_test', {'euler':euler})
