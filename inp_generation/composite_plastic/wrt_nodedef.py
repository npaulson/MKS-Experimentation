# -*- coding: utf-8 -*-
"""
Created on Fri Oct 03 14:52:08 2014

@author: nhpnp3
"""

import numpy as np



el = 25
nd = el + 1
el_tot = el**3
nd_tot = nd**3

sidelen = 20.0

sidevec = np.linspace(sidelen,0,nd)

nodemat = np.zeros([nd_tot,4]) 

node = 1

for ii in xrange(nd_tot):
    [u,v,w] = np.unravel_index(ii,[nd,nd,nd])
    node = ii + 1
    
    nodemat[ii,0] = node
    nodemat[ii,1:] = [sidevec[u],sidevec[w],sidevec[v]]

filename = 'mesh3D_%snode.txt' %el
np.savetxt(filename,nodemat,['%7d','%13.5f','%13.5f','%13.5f'],',')


elmat = np.zeros([el_tot,9])
elm = np.array([1,nd**2+1,nd**2+2,nd**2+nd+2,nd**2+nd+1,1,2,nd+2,nd+1])

for ii in xrange(el_tot):    
    count = ii + 1    
    elmat[ii,:] = elm
    if count % el**2 == 0:
        elm = elm + np.array([1,nd+2,nd+2,nd+2,nd+2,nd+2,nd+2,nd+2,nd+2])
    elif count % el == 0:
        elm = elm + np.array([1,2,2,2,2,2,2,2,2]) 
    else:
        elm = elm + np.ones_like(elm)
     
filename = 'mesh3D_%selement.txt' %el
np.savetxt(filename,elmat,['%4d','%6d','%6d','%6d','%6d','%6d','%6d','%6d','%6d',],',')