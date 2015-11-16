# -*- coding: utf-8 -*-
"""
Created on 11/9/2015 by Noah Paulson
"""

import numpy as np
import vtk_read as vtk_r

ns_cal = 1
set_id_cal = 'cal'
dir_cal = 'cal'

comp_app = 0
loading = 'Xdir'

H = 15
el = 21

compl = ['11', '22', '33', '12', '23', '13']

# PERFORM CALIBRATION

wrt_file = 'test.txt'
step = 1

# The tensorID determines the type of tensor data read from the .vtk
# file
# if tensorID == 0, we read the stress tensor
# if tensorID == 1, we read the strain tensor
# if tensorID == 2, we read the plastic strain tensor

# Read strain from calibration .vtk files
tensor_ID = 1
for comp in compl:
    vtk_r.read_meas(el, ns_cal, set_id_cal, step, comp, tensor_ID, dir_cal,
                    wrt_file)

et11 = np.load('epsilon11_fem_%scal_s1.npy' % ns_cal)
et22 = np.load('epsilon22_fem_%scal_s1.npy' % ns_cal)
et33 = np.load('epsilon33_fem_%scal_s1.npy' % ns_cal)
et12 = np.load('epsilon12_fem_%scal_s1.npy' % ns_cal)
et23 = np.load('epsilon23_fem_%scal_s1.npy' % ns_cal)
et13 = np.load('epsilon13_fem_%scal_s1.npy' % ns_cal)

et11 = et11.reshape(et11.size)
et22 = et22.reshape(et22.size)
et33 = et33.reshape(et33.size)
et12 = et12.reshape(et12.size)
et23 = et23.reshape(et23.size)
et13 = et13.reshape(et13.size)

et = np.zeros([3, 3, et11.size])

et[0, 0, :] = et11
et[0, 1, :] = et12
et[0, 2, :] = et13
et[1, 0, :] = et12
et[1, 1, :] = et22
et[1, 2, :] = et23
et[2, 0, :] = et13
et[2, 1, :] = et23
et[2, 2, :] = et33


etnorm = np.sqrt(np.sum(et**2, axis=(0, 1)))
print "for the norm of the total strain"
print "mean strain: %s" % np.mean(etnorm)
print "min strain: %s" % np.min(etnorm)
print "max strain: %s" % np.max(etnorm)


trace = (1./3.)*(et11+et22+et33)

et_ = np.zeros(et.shape)
et_[0, 0, :] = et[0, 0, :] - trace
et_[1, 1, :] = et[1, 1, :] - trace
et_[2, 2, :] = et[2, 2, :] - trace

et_norm = np.sqrt(np.sum(et_**2, axis=(0, 1)))

print "for the norm of the deviatoric total strain"
print "mean strain: %s" % np.mean(et_norm)
print "min strain: %s" % np.min(et_norm)
print "max strain: %s" % np.max(et_norm)
