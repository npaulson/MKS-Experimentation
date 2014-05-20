# -*- coding: utf-8 -*-
"""
Created on Mon Apr 14 12:37:20 2014

@author: nhpnp3
"""
import numpy as np

a = np.array([1,2,3,4])
b1 = np.array([[5],[6],[7],[8]])
b2 = np.array([5,6,7,8])

print a[None,:]
print b2[:,None]

print np.dot(b2[:,None],a[None,:])