# -*- coding: utf-8 -*-
"""
Created on Wed Sep 03 09:33:40 2014

@author: nhpnp3
"""

import numpy as np

el = 21
ep = el + 1

nd_max = (el + 1)**3

N_lin = np.linspace(1,nd_max,nd_max)

N = np.swapaxes(np.reshape(np.flipud(N_lin), [ep,ep,ep]),1,2)

n1plus = N[el,1:el,1:el]
n1minus = N[0,1:el,1:el]
n2plus = N[1:el,el,1:el]
n2minus = N[1:el,0,1:el]
n3plus = N[1:el,1:el,el]
n3minus = N[1:el,1:el,0]

n1plus_n2plus = N[el,el,1:el]
n1minus_n2plus = N[0,el,1:el]
n1plus_n2minus = N[el,0,1:el]
n1minus_n2minus = N[0,0,1:el]

n2plus_n3plus = N[1:el,el,el]
n2minus_n3plus = N[1:el,0,el]
n2plus_n3minus = N[1:el,el,0]
n2minus_n3minus = N[1:el,0,0]

n3plus_n1plus = N[el,1:el,el]
n3minus_n1plus = N[el,1:el,0]
n3plus_n1minus = N[0,1:el,el]
n3minus_n1minus = N[0,1:el,0]

nodesets = open('nodesets.inp', 'w+')

face_names = {0:'n1plus', 1:'n1minus', 2:'n2plus', 3:'n2minus', 4:'n3plus', 5:'n3minus'}
faces = {0:n1plus, 1:n1minus, 2:n2plus, 3:n2minus, 4:n3plus, 5:n3minus}

for ii in xrange(6):
    nodesets.write('*Nset, nset=' + face_names[ii] + '\n')
    
    face = np.sort(np.reshape(faces[ii],(el-1)**2)).astype('int16')    
    
    for jj in xrange((el-1)**2):    
        
        if (jj + 1)%12 == 0:
            nodesets.write('   ' + str(face[jj]) + ',\n')
        else:
            nodesets.write('   ' + str(face[jj]) + ',')
    
    nodesets.write('\n**\n')


edge_names = {0:'n1plus_n2plus', 1:'n1minus_n2plus', 2:'n1plus_n2minus', 3:'n1minus_n2minus',
              4:'n2plus_n3plus', 5:'n2minus_n3plus', 6:'n2plus_n3minus', 7:'n2minus_n3minus',
              8:'n3plus_n1plus', 9:'n3minus_n1plus',10:'n3plus_n1minus',11:'n3minus_n1minus'}

edges = {0:n1plus_n2plus, 1:n1minus_n2plus, 2:n1plus_n2minus, 3:n1minus_n2minus,
         4:n2plus_n3plus, 5:n2minus_n3plus, 6:n2plus_n3minus, 7:n2minus_n3minus,
         8:n3plus_n1plus, 9:n3minus_n1plus,10:n3plus_n1minus,11:n3minus_n1minus}

for ii in xrange(12):
    nodesets.write('*Nset, nset=' + edge_names[ii] + '\n')
    
    edge = np.sort(np.reshape(edges[ii],el-1)).astype('int16')    
    
    for jj in xrange(el-1):    
        
        if (jj + 1)%12 == 0:
            nodesets.write('   ' + str(edge[jj]) + ',\n')
        else:
            nodesets.write('   ' + str(edge[jj]) + ',')
    
    if ii != 11:
        nodesets.write('\n**\n')
        

nodesets.close()    