# -*- coding: utf-8 -*-
"""
Created on Tue Apr 15 09:41:56 2014

I wanted to test generating the local state values for a generic local
state

For example:
For a seventh order local state there are 128 permutations of 1 and 0 for 
vectors of length 7

@author: nhpnp3
"""
import itertools as it
import numpy as np

a = [0,1]

# I use itertools to find the permutations, which outputs in tuple format
# I covert this output from tuple to list to array
b = np.array(list(it.product(a,repeat=5)))

print b