# -*- coding: utf-8 -*-
"""
Created on Mon Dec 15 09:32:40 2014

@author: nhpnp3
"""

import numpy as np

def gsh_hcp_tri_L_7(e_angles):

    phi1 = e_angles[0]
    phi = e_angles[1]
    phi2 = e_angles[2]
    
    if abs(phi) < 10e-17:
        lil_const = 1e-7
        binary = np.round(np.rand())
        if binary == 0:
            random_num = -lil_const
        elif binary == 1:
            random_num = lil_const
    
        phi = phi + random_num
     
    t2 = np.exp((-2j) * phi1)
    print t2
    t3 = np.sqrt(0.6e1)
    print t3
    t5 = np.cos(phi)
    print t5    
    t6 = 0.1e1 - t5
    print t6
    t7 = 0.1e1 + t5
    print t7
    t8 = t6 * t7
    print t8
    t12 = np.exp((-1j) * phi1)
    print t12
    t15 = np.sqrt(t6)
    print t15
    t16 = 0.1e1 / t15
    print t16
    t17 = np.sqrt(t7)
    print t17
    t18 = t16 * t17
    print t18
    t19 = t6 ** 2
    print t19
    t23 = t7 ** 2
    print t23
    t27 = np.exp((1j) * phi1)
    print t27
    t30 = 0.1e1 / t17
    print t30
    t31 = t15 * t30
    print t31
    t36 = np.exp((2j) * phi1)
    print t36
    t41 = np.exp((-4j) * phi1)
    print t41
    t42 = np.sqrt(0.70e2)
    print t42
    t44 = t19 * t23
    print t44
    t48 = np.exp((-3j) * phi1)
    print t48
    t50 = np.sqrt(0.35e2)
    print t50
    t52 = t15 * t6
    print t52
    t53 = 0.1e1 / t52
    print t53
    t54 = t17 * t7
    print t54
    t55 = t53 * t54
    print t55
    t56 = t19 * t6
    print t56
    t57 = t56 * t7
    print t57
    t58 = t19 ** 2
    print t58
    t62 = np.sqrt(0.10e2)
    print t62
    t64 = 0.1e1 / t6
    print t64
    t65 = t64 * t7
    print t65
    t66 = 0.360e3 * t44
    print t66
    t74 = np.sqrt(0.5e1)
    print t74
    t76 = t23 * t7
    print t76
    t77 = t6 * t76
    print t77
    t79 = 0.720e3 * t44
    print t79
    t85 = t23 ** 2
    print t85
    t99 = 0.1e1 / t7
    print t99
    t100 = t6 * t99
    print t100
    t108 = np.exp((3j) * phi1)
    print t108
    t111 = 0.1e1 / t54
    print t111
    t112 = t52 * t111
    print t112
    t117 = np.exp((4j) * phi1)
    print t117
    
    out_tvalues = np.zeros([15], dtype = 'complex128')    
    
    out_tvalues[0] = 1
    out_tvalues[1] = -(t2 * t3 * t8 / 4)
    out_tvalues[2] = (((-0.1e1 / 0.4e1)*1j) * t12 * t3 * t18 * (t8 - t19))
    out_tvalues[3] = (t23 / 0.4e1 - t8 + t19 / 0.4e1)
    out_tvalues[4] = (((0.1e1 / 0.4e1)*1j) * t27 * t3 * t31 * (-t23 + t8))
    out_tvalues[5] = -(t36 * t3 * t8 / 4)
    out_tvalues[6] = (t41 * t42 * t44 / 16)
    out_tvalues[7] = (((0.1e1 / 0.8e1)*1j) * t48 * t50 * t55 * (t57 - t58))
    out_tvalues[8] = -(t2 * t62 * t65 * (t66 - 0.960e3 * t57 + 0.360e3 * t58) / 1920)
    out_tvalues[9] = (((-0.1e1 / 0.960e3)*1j) * t12 * t74 * t18 * (0.120e3 * t77 - t79 + 0.720e3 * t57 - 0.120e3 * t58))
    out_tvalues[10] = (t85 / 0.16e2 - t77 + 0.9e1 / 0.4e1 * t44 - t57 + t58 / 0.16e2)
    out_tvalues[11] = (((0.1e1 / 0.960e3)*1j) * t27 * t74 * t31 * (-0.120e3 * t85 + 0.720e3 * t77 - t79 + 0.120e3 * t57))
    out_tvalues[12] = -(t36 * t62 * t100 * (0.360e3 * t85 - 0.960e3 * t77 + t66) / 1920)
    out_tvalues[13] = (((-0.1e1 / 0.8e1)*1j) * t108 * t50 * t112 * (-t85 + t77))
    out_tvalues[14] = (t117 * t42 * t44 / 16)
    
    return out_tvalues


if __name__ == '__main__':
    tvals = gsh_hcp_tri_L_7([0.1,0.2+np.pi,0.3])
    print tvals.T