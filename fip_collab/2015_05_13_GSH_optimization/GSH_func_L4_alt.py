# -*- coding: utf-8 -*-
"""
Created on Mon Dec 15 09:32:40 2014

@author: nhpnp3
"""

import numpy as np


def gsh(e_angles):

    phi1 = e_angles[0, :]
    phi = e_angles[1, :]

    zvec = np.abs(phi) < 10e-17
    zvec = zvec.astype(int)
    randvec = np.round(np.random.rand(zvec.shape[0]))
    randvecopp = np.ones(zvec.shape[0]) - randvec
    phi += (1e-7)*zvec*(randvec - randvecopp)

    t2 = np.exp((-2j) * phi1)
    t3 = np.sqrt(0.6e1)
    t5 = np.cos(phi)
    t6 = 0.1e1 - t5
    t7 = 0.1e1 + t5
    t8 = t6 * t7
    t12 = np.exp((-1j) * phi1)
    t15 = np.sqrt(t6)
    t16 = 0.1e1 / t15
    t17 = np.sqrt(t7)
    t18 = t16 * t17
    t19 = t6 ** 2
    t23 = t7 ** 2
    t27 = np.exp((1j) * phi1)
    t30 = 0.1e1 / t17
    t31 = t15 * t30
    t36 = np.exp((2j) * phi1)
    t41 = np.exp((-4j) * phi1)
    t42 = np.sqrt(0.70e2)
    t44 = t19 * t23
    t48 = np.exp((-3j) * phi1)
    t50 = np.sqrt(0.35e2)
    t52 = t15 * t6
    t53 = 0.1e1 / t52
    t54 = t17 * t7
    t55 = t53 * t54
    t56 = t19 * t6
    t57 = t56 * t7
    t58 = t19 ** 2
    t62 = np.sqrt(0.10e2)
    t64 = 0.1e1 / t6
    t65 = t64 * t7
    t66 = 0.360e3 * t44
    t74 = np.sqrt(0.5e1)
    t76 = t23 * t7
    t77 = t6 * t76
    t79 = 0.720e3 * t44
    t85 = t23 ** 2
    t99 = 0.1e1 / t7
    t100 = t6 * t99
    t108 = np.exp((3j) * phi1)
    t111 = 0.1e1 / t54
    t112 = t52 * t111
    t117 = np.exp((4j) * phi1)

    out_tvalues = np.zeros([14,e_angles.shape[1]], dtype = 'complex128')

    out_tvalues[0,:] = -(t2 * t3 * t8 / 4)
    out_tvalues[1,:] = (((-0.1e1 / 0.4e1)*1j) * t12 * t3 * t18 * (t8 - t19))
    out_tvalues[2,:] = (t23 / 0.4e1 - t8 + t19 / 0.4e1)
    out_tvalues[3,:] = (((0.1e1 / 0.4e1)*1j) * t27 * t3 * t31 * (-t23 + t8))
    out_tvalues[4,:] = -(t36 * t3 * t8 / 4)
    out_tvalues[5,:] = (t41 * t42 * t44 / 16)
    out_tvalues[6,:] = (((0.1e1 / 0.8e1)*1j) * t48 * t50 * t55 * (t57 - t58))
    out_tvalues[7,:] = -(t2 * t62 * t65 * (t66 - 0.960e3 * t57 + 0.360e3 * t58) / 1920)
    out_tvalues[8,:] = (((-0.1e1 / 0.960e3)*1j) * t12 * t74 * t18 * (0.120e3 * t77 - t79 + 0.720e3 * t57 - 0.120e3 * t58))
    out_tvalues[9,:] = (t85 / 0.16e2 - t77 + 0.9e1 / 0.4e1 * t44 - t57 + t58 / 0.16e2)
    out_tvalues[10,:] = (((0.1e1 / 0.960e3)*1j) * t27 * t74 * t31 * (-0.120e3 * t85 + 0.720e3 * t77 - t79 + 0.120e3 * t57))
    out_tvalues[11,:] = -(t36 * t62 * t100 * (0.360e3 * t85 - 0.960e3 * t77 + t66) / 1920)
    out_tvalues[12,:] = (((-0.1e1 / 0.8e1)*1j) * t108 * t50 * t112 * (-t85 + t77))
    out_tvalues[13,:] = (t117 * t42 * t44 / 16)

    return out_tvalues


def GSH_Hexagonal_Triclinic(e_angles):

    phi1 = e_angles[0,:]
    phi = e_angles[1,:]

    zvec = np.abs(phi) < 10e-17
    randvec = np.round(np.random.rand(zvec.shape[0]))
    randvecopp = randvec == 0
    phi += (1e-7)*zvec*(randvec - randvecopp).astype(float)

    t1 = np.sqrt(0.6e1)
    t3 = np.exp((-2j) * phi1)
    t5 = np.sin(phi)
    t6 = t5 ** 2
    t9 = ((-0.5e1 / 0.2e1)*1j) * t1
    t10 = np.cos(phi)
    t11 = 0.1e1 - t10
    t12 = np.sqrt(t11)
    t14 = 0.1e1 + t10
    t15 = np.sqrt(t14)
    t16 = t15 * t10
    t18 = np.exp((-1j) * phi1)
    t21 = t10 ** 2
    t24 = np.exp((1j) * phi1)
    t29 = np.exp((2j) * phi1)
    t33 = np.sqrt(0.70e2)
    t35 = np.exp((-4j) * phi1)
    t37 = t6 ** 2
    t40 = np.sqrt(0.35e2)
    t44 = t15 * t14
    t47 = np.exp((-3j) * phi1)
    t50 = np.sqrt(0.10e2)
    t52 = 0.7e1 * t21
    t54 = t6 * (-0.1e1 + t52)
    t57 = np.sqrt(0.5e1)
    t66 = t21 ** 2
    t75 = 0.1e1 / t12
    t87 = np.exp((3j) * phi1)
    t93 = np.exp((4j) * phi1)

    Tsym = np.zeros([15,e_angles.shape[1]], dtype = 'complex128')

    Tsym[0,:] = 1
    Tsym[1,:] = -((0.5e1 / 0.4e1) * t1 * t3 * t6)
    Tsym[2,:] = (t9 * t12 * t16 * t18)
    Tsym[3,:] = (-0.5e1 / 0.2e1 + 0.15e2 / 0.2e1 * t21)
    Tsym[4,:] = (t9 * t24 * t16 * t12)
    Tsym[5,:] = -((0.5e1 / 0.4e1) * t1 * t29 * t6)
    Tsym[6,:] = ((0.9e1 / 0.16e2) * t33 * t35 * t37)
    Tsym[7,:] = ((0.9e1 / 0.4e1)*1j) * t40 * t12 * t11 * t44 * t10 * t47
    Tsym[8,:] = -((0.9e1 / 0.8e1) * t50 * t3 * t54)
    Tsym[9,:] = ((-0.9e1 / 0.4e1)*1j) * t57 * t18 * t12 * t15 * t10 * (-0.3e1 + t52)
    Tsym[10,:] = (0.27e2 / 0.8e1 - 0.135e3 / 0.4e1 * t21 + 0.315e3 / 0.8e1 * t66)
    Tsym[11,:] = ((0.9e1 / 0.4e1)*1j) * t57 * t24 * t16 * (0.3e1 - t52 - 0.3e1 * t10 + 0.7e1 * t21 * t10) * t75
    Tsym[12,:] = -((0.9e1 / 0.8e1) * t50 * t29 * t54)
    Tsym[13,:] = ((0.9e1 / 0.4e1)*1j) * t10 * t44 * (0.1e1 + t21 - 0.2e1 * t10) * t87 * t40 * t75
    Tsym[14,:] = ((0.9e1 / 0.16e2) * t33 * t93 * t37)

    Tsym = np.conjugate(Tsym)

    return Tsym


if __name__ == '__main__':
    # tvals = GSH_Hexagonal_Triclinic(np.array([[0.,100.],[0.,200.],[0.,300.]]))
    # print tvals
    tvals = gsh_hcp_tri_L_4(np.array([[0.,100.],[0.,200.],[0.,300.]]))
    print tvals
