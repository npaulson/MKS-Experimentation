# -*- coding: utf-8 -*-
"""
Created on Thu Feb 05 15:06:31 2015

@author: nhpnp3
"""

import time
import numpy as np
import functions as rr


def strain2stress(el, ns, set_id, step, wrt_file):

    st = time.time()

    C11 = 172832.50
    C12 = 97910.060
    C13 = 73432.550
    C33 = 192308.10
    C44 = 49700.000
    C66 = 0.5 * (C11 - C12)

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

    euler = np.load('euler_%s%s_s%s.npy' % (ns, set_id, step))

    strain_s = np.zeros([ns, el**3, 3, 3])

    tmp = np.load('mksR%s_%s%s_s%s.npy' % ('11', ns, set_id, step))
    strain_s[:, :, 0, 0] = tmp.reshape([ns, el**3])
    tmp = np.load('mksR%s_%s%s_s%s.npy' % ('22', ns, set_id, step))
    strain_s[:, :, 1, 1] = tmp.reshape([ns, el**3])
    tmp = np.load('mksR%s_%s%s_s%s.npy' % ('33', ns, set_id, step))
    strain_s[:, :, 2, 2] = tmp.reshape([ns, el**3])
    tmp = np.load('mksR%s_%s%s_s%s.npy' % ('12', ns, set_id, step))
    strain_s[:, :, 0, 1] = tmp.reshape([ns, el**3])
    strain_s[:, :, 1, 0] = strain_s[:, :, 0, 1]
    tmp = np.load('mksR%s_%s%s_s%s.npy' % ('31', ns, set_id, step))
    strain_s[:, :, 0, 2] = tmp.reshape([ns, el**3])
    strain_s[:, :, 2, 0] = strain_s[:, :, 0, 2]
    tmp = np.load('mksR%s_%s%s_s%s.npy' % ('23', ns, set_id, step))
    strain_s[:, :, 1, 2] = tmp.reshape([ns, el**3])
    strain_s[:, :, 2, 1] = strain_s[:, :, 1, 2]

    del tmp

    g = rr.bungemtrx(euler, 0)

    strain_c = np.einsum('...ik,...jl,...kl', g, g, strain_s)
    del strain_s

    strain_c_L = np.zeros([ns, el**3, 6])
    strain_c_L[..., 0] = strain_c[..., 0, 0]
    strain_c_L[..., 1] = strain_c[..., 1, 1]
    strain_c_L[..., 2] = strain_c[..., 2, 2]
    strain_c_L[..., 3] = 2*strain_c[..., 1, 2]
    strain_c_L[..., 4] = 2*strain_c[..., 0, 2]
    strain_c_L[..., 5] = 2*strain_c[..., 0, 1]

    del strain_c

    stress_c_L = np.einsum('...ij,...j', Cij, strain_c_L)

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

    np.save('stress%s_%s%s_s%s.npy' % ('11', ns, set_id, step),
            stress_s[..., 0, 0])
    np.save('stress%s_%s%s_s%s.npy' % ('22', ns, set_id, step),
            stress_s[..., 1, 1])
    np.save('stress%s_%s%s_s%s.npy' % ('33', ns, set_id, step),
            stress_s[..., 2, 2])
    np.save('stress%s_%s%s_s%s.npy' % ('12', ns, set_id, step),
            stress_s[..., 0, 1])
    np.save('stress%s_%s%s_s%s.npy' % ('31', ns, set_id, step),
            stress_s[..., 0, 2])
    np.save('stress%s_%s%s_s%s.npy' % ('23', ns, set_id, step),
            stress_s[..., 1, 2])

    msg = 'conversion from strain to stress: %ss' % (time.time()-st)
    rr.WP(msg, wrt_file)
