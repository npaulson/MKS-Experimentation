# -*- coding: utf-8 -*-
"""
Created on Tue Mar 25 13:06:24 2014

@author: nhpnp3
"""

import numpy as np

def independent_columns(A, tol = 1e-05):
    """
    The following code is comes from: http://stackoverflow.com/q/13312498

    Return an array composed of independent columns of A.

    Note the answer may not be unique; this function returns one of many
    possible answers.
    """
    Q, R = np.linalg.qr(A)
    independent = np.where(np.abs(R.diagonal()) > tol)[0]
    #return A[:, independent]
    return independent
    
def remzer(r_ini):  
    
    c = 0
    r = np.zeros(len(r_ini))
    for ii in range(len(r_ini)):
        if r_ini[ii] != 0:
            
            r[c] = r_ini[ii]        
            
            c = c + 1
    
    return np.trim_zeros(r)