# -*- coding: utf-8 -*-
"""
Created on Fri Nov 14 11:28:41 2014

@author: nhpnp3
"""

import numpy as np

CsM = np.round(10*np.random.rand(15))
#CsM = np.array([1,5,5,5,8,5])

print CsM

phi1 = np.linspace(0,10,11)


orilist_old = range(CsM.size)
orilist_new = range(CsM.size)

unique_list1 = []
unique_list2 = []

for cc in xrange(CsM.size):
    
    if np.any(np.array(orilist_old) == cc) == False:
        continue

    for dd in orilist_old:

        if CsM[cc] == CsM[dd]:           
            
            orilist_new.remove(dd)
            unique_list1.append(dd)
            unique_list2.append(cc)
    
    orilist_old = list(orilist_new)

    
print unique_list1
print unique_list2