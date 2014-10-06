# -*- coding: utf-8 -*-
"""
Created on Tue Jul 15 10:25:21 2014

@author: nhpnp3
"""
import numpy as np

def GSH_Hexagonal_Triclinic(e_angles):

    phi1 = e_angles[0]
    Phi = e_angles[1]  
    phi2 = e_angles[2]        
    
    
    if abs(Phi) < 10e-17:
        lil_num = 1e-7
        binary = round(np.random.rand())
     
        if binary== 1:
            add_on = lil_num
        elif binary == 0:
            add_on = -lil_num
                    
        Phi = Phi + add_on
    
    Tsym = np.zeros([15], dtype = 'complex128')    
    
    t1 = np.sqrt(0.6e1)
    t3 = np.exp(-2j * phi1)
    t5 = np.sin(Phi)
    t6 = t5 ** 2
    t9 = (-0.5e1 / (0.2e1*1j)) * t1
    t10 = np.cos(Phi)
    t11 = 0.1e1 - t10
    t12 = np.sqrt(t11)
    t14 = 0.1e1 + t10
    t15 = np.sqrt(t14)
    t16 = t15 * t10
    t18 = np.exp(-1j * phi1)
    t21 = t10 ** 2
    t24 = np.exp(1j * phi1)
    t29 = np.exp(2j * phi1)
    t33 = np.sqrt(0.70e2)
    t35 = np.exp(-4j * phi1)
    t37 = t6 ** 2
    t40 = np.sqrt(0.35e2)
    t44 = t15 * t14
    t47 = np.exp(-3j * phi1)
    t50 = np.sqrt(0.10e2)
    t52 = 0.7e1 * t21
    t54 = t6 * (-0.1e1 + t52)
    t57 = np.sqrt(0.5e1)
    t66 = t21 ** 2
    t75 = 0.1e1 / t12
    t87 = np.exp(3j * phi1)
    t93 = np.exp(4j * phi1)
    Tsym[0] = 1
    Tsym[1] = -((0.5e1 / 0.4e1) * t1 * t3 * t6)
    Tsym[2] = -1*(t9 * t12 * t16 * t18)
    Tsym[3] = (-0.5e1 / 0.2e1 + 0.15e2 / 0.2e1 * t21)
    Tsym[4] = -1*(t9 * t24 * t16 * t12)
    Tsym[5] = -((0.5e1 / 0.4e1) * t1 * t29 * t6)
    Tsym[6] = ((0.9e1 / 0.16e2) * t33 * t35 * t37)
    Tsym[7] = -1*((0.9e1 / (0.4e1*1j)) * t40 * t12 * t11 * t44 * t10 * t47)
    Tsym[8] = -((0.9e1 / 0.8e1) * t50 * t3 * t54)
    Tsym[9] = -1*((-0.9e1 / (0.4e1*1j)) * t57 * t18 * t12 * t15 * t10 * (-0.3e1 + t52))
    Tsym[10] = (0.27e2 / 0.8e1 - 0.135e3 / 0.4e1 * t21 + 0.315e3 / 0.8e1 * t66)
    Tsym[11] = -1*((0.9e1 / (0.4e1*1j)) * t57 * t24 * t16 * (0.3e1 - t52 - 0.3e1 * t10 + 0.7e1 * t21 * t10) * t75)
    Tsym[12] = -((0.9e1 / 0.8e1) * t50 * t29 * t54)
    Tsym[13] = -1*((0.9e1 / (0.4e1*1j)) * t10 * t44 * (0.1e1 + t21 - 0.2e1 * t10) * t87 * t40 * t75)
    Tsym[14] = ((0.9e1 / 0.16e2) * t33 * t93 * t37)
    
    Tsym=np.conj(Tsym)
    
    return Tsym
    

def GSH_Cubic_Triclinic(e_angles):
    
    phi1 = e_angles[0]
    Phi = e_angles[1]  
    phi2 = e_angles[2]  
    
    Tsym = np.zeros([10], dtype = 'complex128')  
    
    t1 = np.sqrt(0.30e2)
    t2 = (phi2 + phi1)
    t4 = np.exp(-4j * t2)
    t5 = np.cos(Phi)
    t6 = t5 ** 2
    t7 = t6 ** 2
    t9 = t6 * t5
    t17 = np.exp(-4j * phi1)
    t23 = -phi2 + phi1
    t25 = np.exp(-4j * t23)
    t33 = t4 + t4 * t7 + 4 * t4 * t9 + 6 * t4 * t6 + 4 * t4 * t5 + 14 * t17 - 28 * t17 * t6 + 14 * t17 * t7 + t25 + t25 * t7 - 4 * t25 * t9 + 6 * t25 * t6 - 4 * t25 * t5
    t37 = np.sqrt(0.1e1 - t5)
    t40 = np.sqrt(0.1e1 + t5)
    t41 = (-0.3e1 / 0.16e2*1j) * t37 * t40
    t42 = np.sqrt(0.5e1)
    t43 = np.sqrt(0.3e1)
    t44 = t42 * t43
    t45 = 4 * phi2
    t46 = 3 * phi1
    t47 = t45 + t46
    t49 = np.exp(-1j * t47)
    t56 = np.exp(-3j * phi1)
    t61 = -t45 + t46
    t63 = np.exp(-1j * t61)
    t72 = np.sqrt(0.10e2)
    t73 = t72 * t43
    t74 = np.sqrt(0.7e1)
    t75 = 2 * phi2
    t76 = t75 + phi1
    t78 = np.exp(-2j * t76)
    t85 = np.exp(-2j * phi1)
    t91 = -t75 + phi1
    t93 = np.exp(-2j * t91)
    t99 = -t78 - 2 * t78 * t5 + 2 * t78 * t9 + t78 * t7 - 16 * t85 * t6 + 14 * t85 * t7 + 2 * t85 - t93 + 2 * t93 * t5 - 2 * t93 * t9 + t93 * t7
    t103 = t45 + phi1
    t105 = np.exp(-1j * t103)
    t110 = np.exp(-1j * phi1)
    t115 = -t45 + phi1
    t117 = np.exp(-1j * t115)
    t125 = t43 * t74
    t126 = np.cos(t45)
    t138 = (0.3e1 / (0.16e2*1j)) * t40 * t42
    t139 = np.exp(1j * t115)
    t145 = np.exp(1j * phi1)
    t154 = np.exp(1j * t103)
    t158 = -t139 + 2 * t139 * t5 - 2 * t139 * t9 + t139 * t7 + 6 * t145 * t5 - 14 * t145 * t9 - 6 * t145 * t6 + 14 * t145 * t7 + t154 - 2 * t154 * t6 + t154 * t7
    t159 = 0.1e1 / t37
    t164 = np.exp(2j * t91)
    t171 = np.exp(2j * phi1)
    t178 = np.exp(2j * t76)
    t184 = -t164 + 2 * t164 * t5 - 2 * t164 * t9 + t164 * t7 - 16 * t171 * t6 + 14 * t171 * t7 + 2 * t171 - t178 - 2 * t178 * t5 + 2 * t178 * t9 + t178 * t7
    t188 = np.exp(1j * t61)
    t197 = np.exp(3j * phi1)
    t206 = np.exp(1j * t47)
    t212 = t188 + t188 * t7 - 4 * t188 * t9 + 6 * t188 * t6 - 4 * t188 * t5 + 14 * t5 * t197 - 14 * t6 * t197 - 14 * t9 * t197 + 14 * t7 * t197 - t206 - 2 * t206 * t5 + 2 * t206 * t9 + t206 * t7
    t217 = np.exp(4j * t23)
    t226 = np.exp(4j * phi1)
    t233 = np.exp(4j * t2)
    t241 = t217 + t217 * t7 - 4 * t217 * t9 + 6 * t217 * t6 - 4 * t217 * t5 + 14 * t226 - 28 * t226 * t6 + 14 * t226 * t7 + t233 + t233 * t7 + 4 * t233 * t9 + 6 * t233 * t6 + 4 * t233 * t5
    Tsym[0] = 1
    Tsym[1] = ((0.3e1 / 0.64e2) * t1 * t33)
    Tsym[2] = (t41 * t44 * (t49 + 3 * t49 * t5 + 3 * t49 * t6 + t49 * t9 - 14 * t5 * t56 + 14 * t9 * t56 - t63 + 3 * t63 * t5 - 3 * t63 * t6 + t63 * t9))
    Tsym[3] = ((0.3e1 / 0.32e2) * t73 * t74 * t99)
    Tsym[4] = (t41 * t44 * t74 * (-t105 - t105 * t5 + t105 * t6 + t105 * t9 - 6 * t110 * t5 + 14 * t110 * t9 + t117 - t117 * t5 - t117 * t6 + t117 * t9))
    Tsym[5] = ((0.3e1 / 0.16e2) * t125 * (-10 * t126 * t6 + 5 * t126 * t7 + 5 * t126 + (0.35e2 * t7) - (0.30e2 * t6) + 3))
    Tsym[6] = -1*(t138 * t125 * t158 * t159)
    Tsym[7] = ((0.3e1 / 0.32e2) * t73 * t74 * t184)
    Tsym[8] = -1*(t138 * t43 * t212 * t159)
    Tsym[9] = ((0.3e1 / 0.64e2) * t1 * t241)
    
    Tsym=np.conj(Tsym)
    
    return Tsym