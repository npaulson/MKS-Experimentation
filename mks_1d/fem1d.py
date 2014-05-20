# -*- coding: utf-8 -*-
"""
Created on Thu Mar 20 08:40:36 2014

@author: nhpnp3

1 Dimensional FEA
Yuksel C. Yabansu
Transfered to Python by Noah Paulson

"""
import numpy as np

def fem1d(material = [1., 1., 1., 1.]):
    E4 = 1000.
    E3 = 900.
    E2 = 750.
    E1 = 500.
    A = 0.5
    L = 2.
    
    K = np.zeros((len(material)+1,len(material)+1))
    
    for ii in range(len(material)):
        
        if material[ii] == 4.:
            E = E4
        elif material[ii] == 3.:
            E = E3
        elif material[ii] == 2.:
            E = E2
        elif material[ii] == 1.:
            E = E1
            
        k = A * E / (L * np.array([[1., -1.],[-1., 1.]])) 
        
        K[ii:(ii+2), ii:(ii+2)] = K[ii:(ii+2), ii:(ii+2)] + k
        
    E = [E1, E2, E3, E4]
    
    K[0, :] = 0
    K[0, 0] = 1
    K[-1, :] = 0
    K[-1, -1] = 1

    F = np.zeros((len(material)+1,1))
    F[-1, 0] = 1

    u = np.linalg.solve(K, F)
    
    strain = np.zeros((1, len(material)))
    
    for ii in range(len(material)):
        strain[0, ii] = (1 / L) * np.dot([-1., 1.], u[ii:ii+2, 0])
        
    stress = np.zeros((1,len(material)))
    
    for ii in range(len(material)):
        stress[0, ii] = strain[0, ii] * E[material[ii] - 1]
    
    return strain
    print strain


#m= [1, 2, 3, 2, 1, 3, 1, 3, 1, 2]
#fem1d(m)