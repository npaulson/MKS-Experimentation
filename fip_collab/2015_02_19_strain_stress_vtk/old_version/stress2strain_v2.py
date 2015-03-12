# -*- coding: utf-8 -*-
"""
Created on Thu Feb 05 15:06:31 2015

@author: nhpnp3
"""

import numpy as np
import stiffness_calc as sc
import time


def bungemtrx(euler, israd):
    # this has been cross-checked

    if israd != 1:
        euler = euler * (np.pi/180)

    phi1 = euler[:, 0, :]
    Phi = euler[:, 1, :]
    phi2 = euler[:, 2, :]

    g = np.zeros([euler.shape[0], euler.shape[2], 3, 3])

    g[..., 0, 0] = np.cos(phi1)*np.cos(phi2) - \
        np.sin(phi1)*np.sin(phi2)*np.cos(Phi)

    g[..., 0, 1] = np.sin(phi1)*np.cos(phi2) + \
        np.cos(phi1)*np.sin(phi2)*np.cos(Phi)

    g[..., 0, 2] = np.sin(phi2)*np.sin(Phi)

    g[..., 1, 0] = -np.cos(phi1)*np.sin(phi2) - \
        np.sin(phi1)*np.cos(phi2)*np.cos(Phi)

    g[..., 1, 1] = -np.sin(phi1)*np.sin(phi2) + \
        np.cos(phi1)*np.cos(phi2)*np.cos(Phi)

    g[..., 1, 2] = np.cos(phi2)*np.sin(Phi)

    g[..., 2, 0] = np.sin(phi1)*np.sin(Phi)

    g[..., 2, 1] = -np.cos(phi1)*np.sin(Phi)

    g[..., 2, 2] = np.cos(Phi)

    return g


# (1c) Extract the material constants from the .inp files
# This should be automated, but for now we can hard code the input parameters

C11 = 172832.50
C12 = 97910.060
C13 = 73432.550
C33 = 192308.10
C44 = 49700.000
C66 = 0.5 * (C11 - C12)
shear_mod = (C44 * C66) ** 0.5

# For HCP crystal structures (e.g. Titanium)

Cij = np.zeros([6, 6])

Cij[0, 0] = C11
Cij[1, 1] = C11
Cij[0, 1] = C12
Cij[1, 0] = C12
Cij[0, 2] = C13
Cij[1, 2] = C13
Cij[2, 0] = C13
Cij[2, 1] = C13
Cij[2, 2] = C33
Cij[3, 3] = C44
Cij[4, 4] = C44
Cij[5, 5] = C66

ns = 50
set_id = "val_equi"
step = 1
el = 21

euler = np.load('euler_%s%s_s%s.npy' % (ns, set_id, step))
print 'euler shape'
print euler.shape
print 'example euler angles'
print euler[0, :, 0]*(180/np.pi)

strain_s = np.zeros([ns, el**3, 3, 3])

tmp = np.load('r%s_%s%s_s%s.npy' % ('11', ns, set_id, step))
strain_s[:, :, 0, 0] = tmp.reshape([ns, el**3])
tmp = np.load('r%s_%s%s_s%s.npy' % ('22', ns, set_id, step))
strain_s[:, :, 1, 1] = tmp.reshape([ns, el**3])
tmp = np.load('r%s_%s%s_s%s.npy' % ('33', ns, set_id, step))
strain_s[:, :, 2, 2] = tmp.reshape([ns, el**3])
tmp = np.load('r%s_%s%s_s%s.npy' % ('12', ns, set_id, step))
strain_s[:, :, 0, 1] = tmp.reshape([ns, el**3])
strain_s[:, :, 1, 0] = strain_s[:, :, 0, 1]
tmp = np.load('r%s_%s%s_s%s.npy' % ('31', ns, set_id, step))
strain_s[:, :, 0, 2] = tmp.reshape([ns, el**3])
strain_s[:, :, 2, 0] = strain_s[:, :, 0, 2]
tmp = np.load('r%s_%s%s_s%s.npy' % ('23', ns, set_id, step))
strain_s[:, :, 1, 2] = tmp.reshape([ns, el**3])
strain_s[:, :, 2, 1] = strain_s[:, :, 1, 2]

del tmp

print "number of bytes in strain_s and shape:"
print strain_s.nbytes
print strain_s.shape

print 'example strain tensor in sample frame:'
print strain_s[0, 0, :, :]

g = bungemtrx(euler, 0)

print 'g shape'
print g.shape
print g[0, 0, :, :]

strain_c = np.einsum('...ik,...jl,...kl', g, g, strain_s)
del strain_s

print 'strain_c shape'
print strain_c.shape

strain_c_L = np.zeros([ns, el**3, 6])
strain_c_L[..., 0] = strain_c[..., 0, 0]
strain_c_L[..., 1] = strain_c[..., 1, 1]
strain_c_L[..., 2] = strain_c[..., 2, 2]
strain_c_L[..., 3] = 2*strain_c[..., 1, 2]
strain_c_L[..., 4] = 2*strain_c[..., 0, 2]
strain_c_L[..., 5] = 2*strain_c[..., 0, 1]

del strain_c

stress_c_L = np.einsum('...ij,...j', Cij, strain_c_L)

print 'stress_c_L shape'
print stress_c_L.shape

stress_c = np.zeros([ns, el**3, 3, 3])
stress_c[..., 0, 0] = stress_c_L[..., 0]
stress_c[..., 1, 1] = stress_c_L[..., 1]
stress_c[..., 2, 2] = stress_c_L[..., 2]
stress_c[..., 1, 2] = stress_c_L[..., 3]
stress_c[..., 2, 1] = stress_c_L[..., 3]
stress_c[..., 0, 2] = stress_c_L[..., 4]
stress_c[..., 2, 0] = stress_c_L[..., 4]
stress_c[..., 0, 1] = stress_c_L[..., 5]
stress_c[..., 1, 0] = stress_c_L[..., 5]

del stress_c_L

stress_s = np.einsum('...ki,...lj,...kl', g, g, stress_c)

del stress_c, g

print 'example stress tensor in sample frame:'
print stress_s[0, 0, :, :]
